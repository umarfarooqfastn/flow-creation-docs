#!/usr/bin/env python3
"""
Flow Validation Script for fastn Workflows

This script validates fastn flow JSON files against common mistakes 
and requirements outlined in VALIDATION_GUIDE.md.

Usage: python3 flow_validator.py <flow_file.json>
"""

import json
import sys
import os
import re
from pathlib import Path

class FlowValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
        
        # Valid status values
        self.VALID_STATUS_VALUES = {"DEPLOYED", "CONNECT", "PUBLISH"}
        self.INVALID_STATUS_VALUES = {"DRAFT", "ACTIVE", "INACTIVE", "PENDING"}
        
        # Required top-level fields
        self.REQUIRED_TOP_LEVEL_FIELDS = {
            "clientId", "id", "name", "actionType", "inputName", 
            "inputModelId", "outputModelId", "headerModelId", "resolver", "metaData"
        }
        
        # Additional fields that prevent "null" import errors
        self.ADDITIONAL_REQUIRED_FIELDS = {
            "newName": None,
            "description": None, 
            "chatWelcomeMessage": None,
            "errorModelId": "",
            "version": "1.0.1"
        }
        
        # Required model object fields
        self.REQUIRED_MODEL_FIELDS = {
            "id", "name", "jsonSchema", "clientId", "version", "type", "preview",
            "uiSchema", "isReadOnly", "imageUrl", "groupId", "resourceType", 
            "deleted", "isCommunityCreated", "dataModel"
        }
        
        # All step type fields that must be explicitly declared (even as null)
        self.REQUIRED_STEP_NULL_FIELDS = {
            "actionId", "inline", "function", "composite", "loop", "internalDatabase",
            "aiAction", "mcpClient", "logger", "downLoadFile", "endLoop", "trigger",
            "converter", "variables", "state", "conditional", "lambdaFunction",
            "outputSchema", "prevStep", "enableDebug", "description", "debugBreakAfter",
            "configuredStepSetting", "filter", "limit", "splitOut", "aggregate",
            "merge", "aiAgent", "settings"
        }
        
        # Standard model IDs from base_flow.json
        self.STANDARD_MODEL_IDS = {
            "07a1436d4df2fe3ee87d4fd70ea6a259",  # input model
            "json",  # output model  
            "9fed297b87c60d6808c16df827fc4407"   # header model
        }
        
        # Valid step types
        self.VALID_STEP_TYPES = {
            "COMPOSITE", "INLINE", "CONDITIONAL", "LOOP", "VARIABLE", 
            "INTERNAL_DB", "API", "LOGGER"
        }
        
        # Valid conditional operations (enum values)
        self.VALID_CONDITIONAL_OPERATIONS = {
            "DOES_NOT_CONTAIN", "LENGTH_EQ", "GREATER_THAN", "LESS_THAN", 
            "NOT_EXISTS", "EQ_IGNORE_CASE", "EQ", "ENDS_WITH", "GREATER_THAN_OR_EQ", 
            "LESS_THAN_OR_EQ", "STARTS_WITH", "DOES_NOT_START_WITH", "NOT_EQ", "NEQ", 
            "MATCHES_REGEX", "EXISTS", "CONTAINS", "NONE", "DOES_NOT_MATCH_REGEX", 
            "TYPE_OF", "DOES_NOT_END_WITH"
        }
        
        # Invalid operations that are commonly used by mistake
        self.INVALID_CONDITIONAL_OPERATIONS = {
            "GT": "GREATER_THAN",
            "LT": "LESS_THAN", 
            "GTE": "GREATER_THAN_OR_EQ",
            "LTE": "LESS_THAN_OR_EQ",
            "!=": "NOT_EQ",
            "==": "EQ",
            "EQUALS": "EQ",
            "NOT_EQUALS": "NOT_EQ"
        }

    def add_error(self, message, location=""):
        """Add a critical error that will cause flow failure"""
        self.errors.append(f"❌ ERROR{f' [{location}]' if location else ''}: {message}")
    
    def add_warning(self, message, location=""):
        """Add a warning for potential issues"""
        self.warnings.append(f"⚠️  WARNING{f' [{location}]' if location else ''}: {message}")
    
    def add_info(self, message, location=""):
        """Add informational message"""
        self.info.append(f"ℹ️  INFO{f' [{location}]' if location else ''}: {message}")

    def validate_json_structure(self, data):
        """Check basic JSON structure requirements"""
        # 1. Root object must be array
        if not isinstance(data, list):
            self.add_error("Root object must be an array, not an object. Wrap your flow in square brackets []")
            return False
        
        if len(data) == 0:
            self.add_error("Flow array is empty")
            return False
            
        if len(data) > 1:
            self.add_warning("Multiple flows detected in array. Only first flow will be validated.")
            
        return True

    def validate_top_level_fields(self, flow):
        """Validate required top-level fields"""
        missing_fields = []
        
        for field in self.REQUIRED_TOP_LEVEL_FIELDS:
            if field not in flow:
                missing_fields.append(field)
                
        if missing_fields:
            self.add_error(f"Missing required top-level fields: {', '.join(missing_fields)}")
            self.add_info("Copy these fields from base_flow.json template")

    def validate_status_field(self, flow):
        """Validate status field has correct enum value"""
        if "status" not in flow:
            self.add_warning("Missing 'status' field")
            return
            
        status = flow["status"]
        if status not in self.VALID_STATUS_VALUES:
            if status in self.INVALID_STATUS_VALUES:
                self.add_error(f"Invalid status value '{status}'. This will cause deserialization failure!")
                self.add_error(f"Valid status values are: {', '.join(self.VALID_STATUS_VALUES)}")
                self.add_error("NEVER use 'DRAFT' - it's not a valid enum value")
            else:
                self.add_error(f"Unknown status value '{status}'. Use one of: {', '.join(self.VALID_STATUS_VALUES)}")

    def validate_naming_patterns(self, flow):
        """Validate that names follow proper camelCase naming conventions"""
        name = flow.get("name", "")
        flow_id = flow.get("id", "")
        
        # Validate flow name pattern: camelCase (starts with lowercase, only letters and numbers)
        camel_case_pattern = r'^[a-z][a-zA-Z0-9]*$'
        
        if name and not re.match(camel_case_pattern, name):
            self.add_error(f"Invalid flow name '{name}' - must be camelCase (start with lowercase, only letters/numbers, no spaces/dashes/underscores)")
            self.add_info("Good examples: 'syncShopifyOrders', 'processPayments', 'updateInventory'")
            
        # Validate flow ID pattern (same as name)
        if flow_id and not re.match(camel_case_pattern, flow_id):
            self.add_error(f"Invalid flow id '{flow_id}' - must be camelCase (start with lowercase, only letters/numbers, no spaces/dashes/underscores)")
            self.add_info("Good examples: 'syncShopifyOrders', 'processPayments', 'updateInventory'")
            
        # Check for common naming mistakes
        if name:
            if ' ' in name:
                self.add_error(f"Flow name '{name}' contains spaces - use camelCase instead")
            if '-' in name or '_' in name:
                self.add_error(f"Flow name '{name}' contains dashes/underscores - use camelCase instead")
            if name[0].isupper():
                self.add_error(f"Flow name '{name}' starts with uppercase - use camelCase (start with lowercase)")
                
        # Validate step names
        self._validate_step_names(flow)
        
    def _validate_step_names(self, flow):
        """Validate step naming conventions"""
        if "resolver" not in flow or "steps" not in flow["resolver"]:
            return
            
        steps = flow["resolver"]["steps"]
        camel_case_pattern = r'^[a-z][a-zA-Z0-9]*$'
        
        for i, step in enumerate(steps):
            step_id = step.get("id", "")
            step_type = step.get("type", "")
            location = f"Step {i + 1}"
            
            if not step_id:
                self.add_error(f"Step missing 'id' field", location)
                continue
                
            # For COMPOSITE steps, check if name matches connector endpoint
            if step_type == "COMPOSITE":
                self._validate_composite_step_name(step, location)
            else:
                # For custom steps, validate camelCase
                if not re.match(camel_case_pattern, step_id):
                    self.add_error(f"Invalid step name '{step_id}' - must be camelCase (start with lowercase, only letters/numbers)", location)
                    self.add_info("Good step names: 'transformData', 'validateInput', 'processOrders'")
                    
                # Check for common mistakes
                if ' ' in step_id:
                    self.add_error(f"Step name '{step_id}' contains spaces - use camelCase", location)
                elif '-' in step_id:
                    self.add_error(f"Step name '{step_id}' contains dashes - use camelCase", location) 
                elif '_' in step_id:
                    self.add_error(f"Step name '{step_id}' contains underscores - use camelCase", location)
                elif step_id[0].isupper():
                    self.add_error(f"Step name '{step_id}' starts with uppercase - use camelCase (start with lowercase)", location)
                    
            # Recursively check nested steps
            self._validate_nested_step_names(step, f"{step_id}")
            
    def _validate_composite_step_name(self, step, location):
        """Validate COMPOSITE step names match connector endpoints"""
        step_id = step.get("id", "")
        
        # Check if step has function configuration (API connector)
        if "function" in step and step["function"]:
            function = step["function"]
            connector_name = function.get("name", "")
            
            if connector_name and step_id != connector_name:
                self.add_warning(f"COMPOSITE step name '{step_id}' doesn't match connector endpoint '{connector_name}'", location)
                self.add_info("COMPOSITE steps should use exact connector endpoint names from JSON files")
                self.add_info(f"Consider renaming step to '{connector_name}' to match connector")
                
        # Still validate basic naming for COMPOSITE steps without function
        camel_case_pattern = r'^[a-z][a-zA-Z0-9]*$'
        if not re.match(camel_case_pattern, step_id):
            self.add_error(f"Invalid COMPOSITE step name '{step_id}' - must be camelCase", location)
            
    def _validate_nested_step_names(self, step, parent_path):
        """Validate names in nested steps (COMPOSITE and LOOP steps)"""
        camel_case_pattern = r'^[a-z][a-zA-Z0-9]*$'
        
        # Check COMPOSITE nested steps
        if step.get("type") == "COMPOSITE" and "composite" in step:
            composite = step["composite"]
            if "steps" in composite:
                for i, nested_step in enumerate(composite["steps"]):
                    nested_id = nested_step.get("id", "")
                    nested_type = nested_step.get("type", "")
                    location = f"{parent_path}.composite.steps[{i}]"
                    
                    if nested_id and not re.match(camel_case_pattern, nested_id):
                        self.add_error(f"Invalid nested step name '{nested_id}' - must be camelCase", location)
                        
        # Check LOOP nested steps  
        elif step.get("type") == "LOOP" and "loop" in step:
            loop = step["loop"]
            if "steps" in loop:
                for i, nested_step in enumerate(loop["steps"]):
                    nested_id = nested_step.get("id", "")
                    nested_type = nested_step.get("type", "")
                    location = f"{parent_path}.loop.steps[{i}]"
                    
                    if nested_id and not re.match(camel_case_pattern, nested_id):
                        self.add_error(f"Invalid nested step name '{nested_id}' - must be camelCase", location)
                        
                    # Recursively check deeper nesting
                    self._validate_nested_step_names(nested_step, f"{parent_path}.loop.{nested_id}")
    
    def validate_conditional_operations(self, flow):
        """Validate conditional step operations use correct enum values"""
        if "resolver" not in flow or "steps" not in flow["resolver"]:
            return
            
        for i, step in enumerate(flow["resolver"]["steps"]):
            if step.get("type") == "CONDITIONAL" and "conditional" in step:
                conditional = step["conditional"]
                if "expressions" in conditional:
                    for j, expression in enumerate(conditional["expressions"]):
                        if "operation" in expression:
                            operation = expression["operation"]
                            
                            # Check for invalid operations 
                            if operation in self.INVALID_CONDITIONAL_OPERATIONS:
                                correct_op = self.INVALID_CONDITIONAL_OPERATIONS[operation]
                                self.add_error(f"Invalid conditional operation '{operation}' in step {i+1}, expression {j+1}")
                                self.add_error(f"Use '{correct_op}' instead of '{operation}'")
                                self.add_info("Valid operations: " + ", ".join(sorted(self.VALID_CONDITIONAL_OPERATIONS)))
                            
                            # Check for unknown operations
                            elif operation not in self.VALID_CONDITIONAL_OPERATIONS:
                                self.add_error(f"Unknown conditional operation '{operation}' in step {i+1}, expression {j+1}")
                                self.add_info("Valid operations: " + ", ".join(sorted(self.VALID_CONDITIONAL_OPERATIONS)))
    
    def validate_query_executor_structure(self, obj, location=""):
        """Recursively validate queryExecutor structures have required children arrays"""
        if not isinstance(obj, dict):
            return
            
        # Check if this is a queryExecutor value object
        if "returnLiteral" in obj and "symbolOrIndex" in obj and "version" in obj:
            if "children" not in obj:
                self.add_error(f"Missing 'children' array in queryExecutor structure{' at ' + location if location else ''}")
                self.add_error("All queryExecutor value objects must have a 'children' array (can be empty)")
            else:
                # Recursively check children
                children = obj.get("children", [])
                for i, child in enumerate(children):
                    if "value" in child:
                        child_location = f"{location}.children[{i}]" if location else f"children[{i}]"
                        self.validate_query_executor_structure(child["value"], child_location)
        
        # Recursively check all nested objects
        for key, value in obj.items():
            if isinstance(value, dict):
                self.validate_query_executor_structure(value, f"{location}.{key}" if location else key)
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        self.validate_query_executor_structure(item, f"{location}.{key}[{i}]" if location else f"{key}[{i}]")

    def validate_import_required_fields(self, flow):
        """Validate additional fields required for successful import"""
        for field, default_value in self.ADDITIONAL_REQUIRED_FIELDS.items():
            if field not in flow:
                self.add_warning(f"Missing '{field}' field - may cause import issues")
                self.add_info(f"Add '{field}': {default_value if default_value is not None else 'null'} to prevent 'null' import errors")

    def validate_step_null_fields(self, flow):
        """Validate that all steps have explicit null field declarations"""
        resolver = flow.get("resolver", {})
        steps = resolver.get("steps", [])
        
        for i, step in enumerate(steps):
            step_id = step.get("id", f"step_{i}")
            step_type = step.get("type", "UNKNOWN")
            
            # Check for missing null fields
            missing_fields = []
            for field in self.REQUIRED_STEP_NULL_FIELDS:
                if field not in step:
                    missing_fields.append(field)
            
            if missing_fields:
                self.add_error(f"Step '{step_id}' ({step_type}) missing required null fields: {missing_fields}")
                self.add_info(f"Steps must explicitly declare ALL step-type fields as null, even if unused")
                
            # Also check nested steps in composite/loop steps
            composite = step.get("composite")
            if composite and isinstance(composite, dict) and composite.get("steps"):
                self._validate_nested_steps_null_fields(composite["steps"], f"{step_id}.composite")
            
            loop = step.get("loop")
            if loop and isinstance(loop, dict) and loop.get("steps"):
                self._validate_nested_steps_null_fields(loop["steps"], f"{step_id}.loop")

    def _validate_nested_steps_null_fields(self, steps, parent_path):
        """Helper to validate nested step null fields"""
        for i, step in enumerate(steps):
            step_id = step.get("id", f"step_{i}")
            step_type = step.get("type", "UNKNOWN")
            
            missing_fields = []
            for field in self.REQUIRED_STEP_NULL_FIELDS:
                if field not in step:
                    missing_fields.append(field)
            
            if missing_fields:
                self.add_error(f"Nested step '{parent_path}.{step_id}' ({step_type}) missing required null fields: {missing_fields}")
                
            # Recursively check deeper nesting
            composite = step.get("composite")
            if composite and isinstance(composite, dict) and composite.get("steps"):
                self._validate_nested_steps_null_fields(composite["steps"], f"{parent_path}.{step_id}.composite")
            
            loop = step.get("loop")
            if loop and isinstance(loop, dict) and loop.get("steps"):
                self._validate_nested_steps_null_fields(loop["steps"], f"{parent_path}.{step_id}.loop")

    def validate_model_objects(self, flow):
        """Validate model objects are not null and IDs match"""
        model_checks = [
            ("inputModel", "inputModelId"),
            ("outputModel", "outputModelId"), 
            ("headerModel", "headerModelId")
        ]
        
        for model_field, id_field in model_checks:
            # Check model object exists and is not null
            if model_field not in flow:
                self.add_error(f"Missing '{model_field}' object. This will cause NPE on import!")
                self.add_info(f"Copy complete {model_field} object from base_flow.json")
                continue
                
            if flow[model_field] is None:
                self.add_error(f"'{model_field}' is null. This will cause NPE on import!")
                self.add_error("Cannot invoke DataModelInput.getId() because model is null")
                self.add_info(f"Copy complete {model_field} object from base_flow.json")
                continue
            
            # Check model ID exists
            if id_field not in flow:
                self.add_error(f"Missing '{id_field}' field")
                continue
                
            # Check model ID consistency
            model_obj = flow[model_field]
            if isinstance(model_obj, dict) and "id" in model_obj:
                if flow[id_field] != model_obj["id"]:
                    self.add_error(f"{id_field} ('{flow[id_field]}') doesn't match {model_field}.id ('{model_obj['id']}')")

    def validate_steps(self, flow):
        """Validate step structure and requirements"""
        if "resolver" not in flow or "steps" not in flow["resolver"]:
            self.add_warning("No steps found in resolver")
            return
            
        steps = flow["resolver"]["steps"]
        if not isinstance(steps, list):
            self.add_error("Steps must be an array")
            return
            
        for i, step in enumerate(steps):
            self.validate_single_step(step, f"Step {i}")

    def validate_single_step(self, step, location):
        """Validate individual step structure"""
        if not isinstance(step, dict):
            self.add_error("Step must be an object", location)
            return
            
        # Check required step fields
        if "type" not in step:
            self.add_error("Missing 'type' field", location)
            return
            
        if "id" not in step:
            self.add_error("Missing 'id' field", location)
            
        step_type = step["type"]
        if step_type not in self.VALID_STEP_TYPES:
            self.add_error(f"Invalid step type '{step_type}'", location)
            
        # Validate specific step types
        if step_type == "INLINE":
            self.validate_inline_step(step, location)
        elif step_type == "COMPOSITE":
            self.validate_composite_step(step, location)
        elif step_type == "API":
            self.validate_api_step(step, location)

    def validate_inline_step(self, step, location):
        """Validate INLINE step requirements"""
        if "inline" not in step:
            self.add_error("INLINE step missing 'inline' configuration", location)
            return
            
        inline = step["inline"]
        
        # Check for required UI metadata
        if "uiCode" not in inline:
            self.add_error("INLINE step missing 'uiCode' field (required for fastn UI)", location)
            
        if "queryExecutor" not in inline:
            self.add_error("INLINE step missing 'queryExecutor' field (required for fastn UI)", location)
            
        # Check for code field
        if "code" not in inline:
            self.add_error("INLINE step missing 'code' field", location)
        else:
            self.validate_inline_code(inline["code"], location)

    def validate_inline_code(self, code, location):
        """Check inline code for common issues"""
        if not isinstance(code, str):
            self.add_error("Inline code must be a string", location)
            return
            
        # Check for hardcoded array indices (common cause of bounds errors)
        array_index_pattern = r'\[[0-9]+\]'
        matches = re.findall(array_index_pattern, code)
        if matches:
            self.add_warning(f"Found hardcoded array indices {matches}. Consider using semantic references instead", location)
            
        # Check for problematic references
        problematic_patterns = [
            (r'flattenedRow\[1\]', "This caused 'Index 1 out of bounds' error in past flows"),
            (r'\.output\.[a-zA-Z]+\[[0-9]+\]', "Hardcoded array access may cause bounds errors")
        ]
        
        for pattern, warning in problematic_patterns:
            if re.search(pattern, code):
                self.add_warning(f"{warning}", location)

    def validate_composite_step(self, step, location):
        """Validate COMPOSITE step structure"""
        if "composite" not in step:
            self.add_error("COMPOSITE step missing 'composite' configuration", location)
            return
            
        composite = step["composite"]
        
        if "steps" not in composite:
            self.add_error("COMPOSITE step missing 'steps' array", location)
            return
            
        # Validate nested steps
        for i, nested_step in enumerate(composite["steps"]):
            self.validate_single_step(nested_step, f"{location} > Composite Step {i}")

    def validate_api_step(self, step, location):
        """Validate API step (connector) requirements"""
        function = step.get("function")
        if not function or not isinstance(function, dict):
            self.add_error("API step missing 'function' configuration", location)
            return
            
        required_function_fields = ["id", "groupId", "name", "version", "connectorId"]
        
        for field in required_function_fields:
            if field not in function:
                self.add_error(f"API step missing required function field '{field}'", location)
                
        # Check configuration
        if "configuration" not in function:
            self.add_warning("API step missing 'configuration' object", location)
        else:
            config = function["configuration"]
            if "authType" not in config:
                self.add_warning("API step missing 'authType' in configuration", location)

    def validate_data_references(self, flow):
        """Check for problematic data references throughout the flow"""
        flow_str = json.dumps(flow)
        
        # Check for the specific problematic reference that caused bounds errors
        if "flattenOrderDetails.output.flattenedRow[1]" in flow_str:
            self.add_error("Found problematic reference 'flattenOrderDetails.output.flattenedRow[1]' that causes bounds errors")
            self.add_error("This reference tries to access index [1] of an array that may only have 1 element")
            
        # Check for other hardcoded array indices in data references
        problematic_refs = re.findall(r'{{[^}]+\[[0-9]+\][^}]*}}', flow_str)
        if problematic_refs:
            self.add_warning(f"Found hardcoded array indices in data references: {problematic_refs}")
            self.add_info("Consider using semantic field names instead of array positions")

    def validate_step_connectivity(self, flow):
        """Validate that all steps are properly connected and reachable"""
        if "resolver" not in flow or "steps" not in flow["resolver"]:
            return
            
        steps = flow["resolver"]["steps"]
        start_step = flow["resolver"].get("start")
        
        if not start_step:
            self.add_error("Missing 'start' field in resolver - no entry point defined for the flow")
            return
            
        # Build step lookup dictionary
        step_dict = {}
        all_step_ids = set()
        
        for step in steps:
            if "id" in step:
                step_dict[step["id"]] = step
                all_step_ids.add(step["id"])
        
        # Find all reachable steps
        reachable_steps = set()
        self._trace_reachable_steps(start_step, step_dict, reachable_steps)
        
        # Check for unreachable steps
        unreachable_steps = all_step_ids - reachable_steps
        if unreachable_steps:
            self.add_error(f"Found orphaned/unreachable steps: {', '.join(sorted(unreachable_steps))}")
            self.add_error("All steps must be connected and reachable from the start step")
            
        # Check if start step exists
        if start_step not in step_dict:
            self.add_error(f"Start step '{start_step}' not found in steps list")
            
        # Validate next step references
        for step in steps:
            step_id = step.get("id", "unknown")
            self._validate_step_next_references(step, step_dict, step_id)

    def _trace_reachable_steps(self, step_id, step_dict, reachable_steps, visited=None):
        """Recursively trace all reachable steps from a given step"""
        if visited is None:
            visited = set()
            
        if step_id in visited or step_id not in step_dict:
            return
            
        visited.add(step_id)
        reachable_steps.add(step_id)
        
        step = step_dict[step_id]
        step_type = step.get("type", "")
        
        # Handle different step types and their navigation patterns
        if step_type == "COMPOSITE":
            # Composite steps have internal steps
            composite = step.get("composite", {})
            internal_steps = composite.get("steps", [])
            internal_start = composite.get("start")
            
            # Build internal step dict
            internal_step_dict = {}
            for internal_step in internal_steps:
                if "id" in internal_step:
                    internal_step_dict[internal_step["id"]] = internal_step
            
            # Trace internal flow
            if internal_start:
                self._trace_reachable_steps(internal_start, internal_step_dict, reachable_steps, visited)
            elif internal_steps:
                # If no explicit start, assume first step
                first_step = internal_steps[0]
                if "id" in first_step:
                    self._trace_reachable_steps(first_step["id"], internal_step_dict, reachable_steps, visited)
            
            # Follow composite step's next
            next_step = composite.get("next") or step.get("next")
            if next_step:
                self._trace_reachable_steps(next_step, step_dict, reachable_steps, visited)
                
        elif step_type == "LOOP":
            # Loop steps have internal steps and loop flow
            loop = step.get("loop", {})
            loop_steps = loop.get("steps", [])
            loop_start = loop.get("start")
            
            # Build loop step dict  
            loop_step_dict = {}
            for loop_step in loop_steps:
                if "id" in loop_step:
                    loop_step_dict[loop_step["id"]] = loop_step
            
            # Trace loop internal flow
            if loop_start:
                self._trace_reachable_steps(loop_start, loop_step_dict, reachable_steps, visited)
            
            # Follow loop's next
            next_step = loop.get("next") or step.get("next")
            if next_step:
                self._trace_reachable_steps(next_step, step_dict, reachable_steps, visited)
                
        elif step_type == "CONDITIONAL":
            # Conditional steps have expressions with different next steps
            conditional = step.get("conditional", {})
            expressions = conditional.get("expressions", [])
            
            # Follow all expression branches
            for expr in expressions:
                expr_next = expr.get("next")
                if expr_next:
                    self._trace_reachable_steps(expr_next, step_dict, reachable_steps, visited)
            
            # Follow default next
            default_next = conditional.get("next") or step.get("next")
            if default_next:
                self._trace_reachable_steps(default_next, step_dict, reachable_steps, visited)
                
        else:
            # Regular steps - follow next
            next_step = step.get("next")
            if next_step:
                self._trace_reachable_steps(next_step, step_dict, reachable_steps, visited)

    def _validate_step_next_references(self, step, step_dict, step_id):
        """Validate that next step references point to existing steps"""
        step_type = step.get("type", "")
        
        # Check main next field
        next_step = step.get("next")
        if next_step and next_step not in step_dict:
            self.add_error(f"Step '{step_id}' references non-existent next step '{next_step}'")
            
        # Check type-specific next references
        if step_type == "COMPOSITE":
            composite = step.get("composite", {})
            comp_next = composite.get("next")
            if comp_next and comp_next not in step_dict:
                self.add_error(f"Composite step '{step_id}' references non-existent next step '{comp_next}'")
                
        elif step_type == "LOOP":
            loop = step.get("loop", {})
            loop_next = loop.get("next")
            if loop_next and loop_next not in step_dict:
                self.add_error(f"Loop step '{step_id}' references non-existent next step '{loop_next}'")
                
        elif step_type == "CONDITIONAL":
            conditional = step.get("conditional", {})
            expressions = conditional.get("expressions", [])
            
            for i, expr in enumerate(expressions):
                expr_next = expr.get("next")
                if expr_next and expr_next not in step_dict:
                    self.add_error(f"Conditional step '{step_id}' expression {i} references non-existent next step '{expr_next}'")
                    
            cond_next = conditional.get("next") 
            if cond_next and cond_next not in step_dict:
                self.add_error(f"Conditional step '{step_id}' references non-existent default next step '{cond_next}'")

    def validate_flow_file(self, file_path):
        """Main validation method"""
        self.errors = []
        self.warnings = []
        self.info = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.add_error(f"Invalid JSON: {e}")
            return False
        except FileNotFoundError:
            self.add_error(f"File not found: {file_path}")
            return False
        except Exception as e:
            self.add_error(f"Error reading file: {e}")
            return False

        # Basic structure validation
        if not self.validate_json_structure(data):
            return False
            
        flow = data[0]  # First flow in array
        
        # Run all validations
        self.validate_top_level_fields(flow)
        self.validate_import_required_fields(flow)
        self.validate_naming_patterns(flow)
        self.validate_status_field(flow)
        self.validate_model_objects(flow)
        self.validate_steps(flow)
        self.validate_step_null_fields(flow)
        self.validate_conditional_operations(flow)
        self.validate_step_connectivity(flow)
        self.validate_data_references(flow)
        self.validate_query_executor_structure(flow, "flow")
        
        return len(self.errors) == 0

    def print_report(self):
        """Print validation report"""
        print("\n" + "="*60)
        print("🔍 FASTN FLOW VALIDATION REPORT")
        print("="*60)
        
        if self.errors:
            print(f"\n💥 CRITICAL ERRORS ({len(self.errors)}):")
            print("These WILL cause flow failure and must be fixed:")
            for error in self.errors:
                print(f"  {error}")
                
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            print("These may cause issues and should be reviewed:")
            for warning in self.warnings:
                print(f"  {warning}")
                
        if self.info:
            print(f"\nℹ️  INFORMATION ({len(self.info)}):")
            for info in self.info:
                print(f"  {info}")
                
        print("\n" + "="*60)
        if not self.errors and not self.warnings:
            print("✅ VALIDATION PASSED: Flow appears to be valid!")
        elif not self.errors:
            print("✅ VALIDATION PASSED: Flow is valid but has warnings to review")
        else:
            print("❌ VALIDATION FAILED: Critical errors must be fixed before deployment")
        print("="*60)

def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("  python3 flow_validator.py <flow_file.json>")
        print("\nExamples:")
        print("  python3 flow_validator.py flowExamples/shoppifyOrdersToGoogleSheet.json")
        print("  python3 flow_validator.py buildedByAI/send_email_flow.json")
        print("  python3 flow_validator.py /path/to/your/flow.json")
        sys.exit(1)

    flow_file = sys.argv[1]
    
    # Convert relative path to absolute for better error reporting
    if not os.path.isabs(flow_file):
        flow_file = os.path.abspath(flow_file)
    
    print(f"🔍 Validating flow: {flow_file}")
    
    validator = FlowValidator()
    is_valid = validator.validate_flow_file(flow_file)
    validator.print_report()
    
    # Exit with appropriate code
    sys.exit(0 if len(validator.errors) == 0 else 1)

if __name__ == "__main__":
    main()
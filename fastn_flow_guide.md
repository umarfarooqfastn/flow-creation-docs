# fastn Workflow Generation Guide

## 1. Introduction

You are an expert assistant specializing in the "fastn" automation platform. Your primary role is to generate complete and valid fastn workflow JSON based on a user's natural language request. Adhere strictly to the structures, schemas, and examples provided in this guide.

## 2. How to Build Flow Logic

Building a fastn flow involves translating a requirement into a series of connected steps. Here’s how to approach it:

### Step 1: Deconstruct the Request

First, break down the user's goal into smaller, manageable parts:

-   **What is the trigger?** What event should start the flow? (e.g., an API call, a schedule).
-   **What are the inputs?** What data is needed at the beginning? (e.g., a user ID, an order number).
-   **What are the actions?** What are the key operations that need to happen? (e.g., fetch data from an API, transform data, save to a database).
-   **What is the final output?** What should the flow produce at the end?

### Step 2: Choose Your Steps

Once you have a high-level plan, consult the `stepsDetails` directory to select the appropriate step type for each action. For example:

-   To get data from an external service, you'll likely need a `COMPOSITE` step containing an `API` call.
-   To transform data, you'll use an `INLINE` step with JINJA or Javascript.
-   To make a decision, you'll use a `CONDITIONAL` step.
-   To repeat an action, you'll use a `LOOP` step.

Reviewing the examples in `flowExamples/shoppifyOrdersToGoogleSheet.json` and `flowExamples/ComplexFlowWithMappingsAndCustomerUsecase.json` is a great way to see how these steps are used in practice.

### Step 3: Plan the Data Flow

Think about how data will move from one step to the next. For each step, ask:

-   What data does this step need to receive?
-   Where does this data come from? (The initial input? The output of a previous step?)
-   What data will this step produce as output?

This will help you plan your data mappings (`{{data.input...}}`, `{{data.steps...}}`) correctly.

### Step 4: Build and Refine

Start with the `base_flow.json` as your template. Build the flow step-by-step, connecting the `next` of one step to the `id` of the next. It's an iterative process, so you may need to add or change steps as you go.

## 3. The Principle of No Assumptions

This is the most important principle to follow when generating a fastn flow.

**The best way to avoid mistakes is to always start with the `base_flow.json` file and adapt it to your needs.**

**You must not, under any circumstances, invent or assume any information that is not explicitly present in the provided files.**

-   **No Guessing:** If you are unsure about the structure of a step, the name of a connector, or the format of a data mapping, do not guess. Refer back to the documentation in the `stepsDetails` directory, use the helper scripts.
-   **Data-Driven, Not Knowledge-Driven:** Your internal knowledge base is not a valid source of information for generating fastn flows. The process must be driven *only* by the data and schemas in the provided files.
-   **Read Before You Write:** Before you generate any part of the flow, ensure you have read the relevant documentation and examples. This will prevent you from making incorrect assumptions about the structure and content of the flow.

If you encounter a situation where the provided information is insufficient to fulfill the user's request, you must ask the user for clarification. It is always better to ask a question than to generate an incorrect flow.

## 4. The Anatomy of a fastn Flow

A fastn flow is a JSON file that defines a series of steps to be executed. The root of the file is a JSON array containing one or more flow objects.

### 4.1. Top-Level Flow Object

Each flow object has a specific structure. You must use the `base_flow.json` as a template to ensure all the required fields are present. Nothing should be missed from it.

### 4.2. The Resolver

The `resolver` object defines the steps of the flow. The `start` field specifies the ID of the first step to be executed.

### 4.3. Steps

Each step in the `steps` array is an object with a `type` and an `id`. The available step types are described in the `stepsDetails` directory.

## 5. Deep Dive into Steps

-   **COMPOSITE Step:** To group a series of steps together, often to call an external API. See `stepsDetails/compositeStep/composite.md`.
-   **INLINE Step:** Two distinct patterns:
    -   **Custom Code Steps** (JavaScript data processing) - See `stepsDetails/customCodeStep/customCode.md`
    -   **Response Steps** (JINJA final API response) - See `stepsDetails/responseStep/responseStep.md`
-   **LAMBDA Step:** To execute complex Python code with access to external libraries for any advanced logic processing. **Execution time limit: ~10 seconds max.** See `stepsDetails/lambdaStep/lambda.md`.
-   **CONDITIONAL Step (Switch):** To control the flow of execution based on a condition. See `stepsDetails/switchStep/switch.md`.
-   **LOOP Step:** To iterate over a list of items. See `stepsDetails/loopStep/loop.md`.
-   **VARIABLE Step:** To store and update variables within the flow. See `stepsDetails/variableStep/variable.md`.
-   **INTERNAL_DB Step:** To interact with the internal postgreSQL database. See `stepsDetails/databaseStep/InternalDatabase.md`.

## 6. Data Mapping

Data mapping is crucial for a flow to work correctly. You can map data from the flow's input, from a previous step, or from a parent step.

-   **From Input:** `{{data.input.my_input_field}}`
-   **From a Previous Step:** `{{data.steps.previous_step_id.output.some_output}}`
-   **From a Parent Step:** `{{data.parent.input.some_input}}`

## 7. Examples

To see complete, real-world examples of fastn flows, refer to the `flowExamples/` directory which contains:

### **Basic Examples:**
-   **`flowExamples/flow_with_connector_example.json`**: Demonstrates basic connector integration patterns
-   **`flowExamples/flow_with_looping_example.json`**: Shows how to implement loop steps for data iteration
-   **`flowExamples/flow_with_fastndb_example.json`**: Example of internal database operations

### **Advanced Examples:**
-   **`flowExamples/shoppifyOrdersToGoogleSheet.json`**: Moderately complex flow integrating Shopify, Google Sheets, and Slack. See [explanation_of_Shopify_OrdersToGoogleSheet.md](flowExamples/explanation_of_Shopify_OrdersToGoogleSheet.md) for detailed walkthrough.
-   **`flowExamples/ComplexFlowWithMappingsAndCustomerUsecase.json`**: Advanced example with complex data mappings, conditional logic, and customer-centric use cases

### **Documentation:**
-   **`flowExamples/explanation_of_Shopify_OrdersToGoogleSheet.md`**: Step-by-step explanation of flow logic, data mapping, and step connections

By studying these examples, you can gain a deeper understanding of how to construct valid and efficient fastn flows for different use cases.

## 8. Using Helper Scripts to Accelerate Development

To significantly speed up the creation of flows, especially the data mapping portions, you should use the provided helper scripts.

### `get_endpoint_details.py`

-   **Purpose:** To retrieve the full, detailed JSON contract for a specific connector endpoint. This is essential for knowing exactly what fields are available for mapping.
-   **When to use:** Before creating a `COMPOSITE` step that calls a connector, run this script to get the full request and response schema.
-   **Usage:** `python3 get_endpoint_details.py <endpoint_name>`

### `generate_uicode.py`

-   **Purpose:** To generate the complete `uiCode` for a **connector endpoint**. This is used for the mapping step inside a `COMPOSITE` step.
-   **When to use:** When you are building a `COMPOSITE` step and need to create the `INLINE` mapping step for a known connector endpoint. This script creates the necessary `uiCode` from the connector's predefined schema.
-   **Usage:** `python3 generate_uicode.py <endpoint_name>`

## 9. Step-by-Step Flow Creation Workflow

To ensure successful flow creation and avoid common pitfalls, follow this systematic workflow:

### 9.1. Pre-Creation Checklist

Before starting, ensure you have:
- Read the `base_flow.json` structure thoroughly
- Identified all required connectors using `stepsDetails/compositeStep/connectorDetails.md`
- Understood the complete requirement and broken it into discrete steps
- **Planned proper names** following the naming conventions below

### 9.2. Naming Conventions 📝

**🚨 CRITICAL: Follow These Naming Rules**

#### **Flow Naming Requirements:**
- **Format**: `camelCase` - start with lowercase, capitalize each word
- **Length**: Keep names **short and descriptive**
- **No Spaces**: Use `syncOrdersToSheet` not `sync orders to sheet`
- **No Special Characters**: Only letters and numbers, no `-`, `_`, `@`, etc.
- **Be Specific**: Describe what the flow does clearly

✅ **Good Flow Names:**
```json
"id": "syncShopifyOrders",
"name": "syncShopifyOrders"

"id": "processPayments", 
"name": "processPayments"

"id": "updateInventory",
"name": "updateInventory"
```

❌ **Bad Flow Names:**
```json
"id": "sync-orders-flow",     // Has special characters
"name": "Sync Orders Flow"    // Has spaces and capitals

"id": "shopify_to_bigcommerce_sync_flow_with_notifications",  // Too long, has underscores
"name": "process stuff"       // Has spaces, too vague
```

#### **Step Naming Requirements:**

**For Custom Steps (VARIABLE, INLINE, LOOP, CONDITIONAL):**
- **Format**: `camelCase` - start with lowercase
- **Length**: Keep **short and descriptive**
- **Purpose-Based**: Name reflects what the step does

✅ **Good Step Names:**
```json
"id": "transformData",
"id": "validateInput", 
"id": "processOrders",
"id": "formatResponse",
"id": "checkStatus"
```

**For COMPOSITE Steps (Connectors):**
- **Use Exact Connector Names**: Copy the endpoint name from connector JSON files
- **Don't Modify**: Use exactly what appears in the connector documentation

✅ **Good COMPOSITE Step Names:**
```json
"id": "getProducts",    // Exact name from shopifyConnectors.json
"id": "createProduct",  // Exact name from bigcommerceConnectors.json  
"id": "sendMessage",    // Exact name from slackConnectors.json
"id": "sendMail"        // Exact name from gmailConnectors.json
```

❌ **Bad COMPOSITE Step Names:**
```json
"id": "getShopifyProducts",     // Modified connector name
"id": "callBigCommerceAPI",     // Added extra words
"id": "send-message",           // Changed camelCase to kebab-case
```

### 9.3. Systematic Flow Creation Process

**Step 1: Start with Base Structure**
- Always begin with `base_flow.json` as your template
- Copy the complete structure, including all required top-level fields
- Update `id`, `name`, and `description` fields to match your flow

**Step 2: Plan Your Flow Logic**
- Map out the sequence of operations needed
- Identify decision points (switch/conditional steps)
- Determine loop requirements for data iteration
- Plan data transformation points (inline steps)
- **🚨 COMPULSORY: Study Complex Flow Patterns**
  - **Read:** `flowExamples/acumatica_bigComerce/ACUMATICA_BIGCOMMERCE_FLOWS_ANALYSIS.md`
  - **Purpose:** Understand how enterprise-grade data synchronization flows are architected
  - **Learn:** Multi-tenant patterns, batch processing, error handling, and complex business logic
  - **Apply:** These proven patterns to your flow design for robust, scalable solutions

**Step 3: Gather Connector Information** 
- For each external API call needed, use:
```bash
python3 get_endpoint_details.py <endpoint_name>
```
- Document the `groupId`, connector `id`, and `version` for each connector
- Note the input/output schemas for proper data mapping

**Step 4: Build Steps Incrementally**
- Start with the `resolver.start` step
- Build each step completely before moving to the next
- For composite steps, generate UI code using:
```bash
python3 generate_uicode.py <endpoint_name>
```

**Step 5: Implement Data Mapping**
- Use consistent patterns (detailed in section 6)
- Always validate data paths exist in previous step outputs

**Step 6: Validate Against Common Issues**
- Ensure all `next` fields point to valid step IDs
- Verify all required fields are present for each step type
- Check that model IDs match existing models (use base_flow.json IDs)
- Validate JSON syntax and escaping

### 9.4. Step Type Implementation Guidelines

**For COMPOSITE Steps:**
- Always include required connector fields: `groupId`, `id`, `name`, `version`, `connectorId`
- Generate UI code using the helper script - never write manually
- Include proper authentication configuration
- Validate input/output schema mapping

**For INLINE Steps:**

🚨 **CRITICAL: Choose the Correct INLINE Pattern**

**Custom Code Steps (JavaScript Data Processing):**
- Use `"language": "JAVASCRIPT"`
- Use `"hasResponse": false` (typically)
- Use `"next": "nextStepId"` (continue flow)
- Purpose: Process/transform data for subsequent steps
- Position: Middle of flow

**Response Steps (JINJA Final Response):**  
- Use `"language": "JINJA"`
- Use `"hasResponse": true`
- Use `"next": null` (end flow)
- Purpose: Return final API response to client
- Position: Terminal/last step

**General INLINE Requirements:**
- Always include both `code` and `uiCode` fields
- Ensure JavaScript code is within `handler(params)` function
- Add proper error handling in custom code
- Include `queryExecutor` for UI integration

**For CONDITIONAL Steps:**
- Define clear condition expressions with proper operations
- Ensure all branches have valid `next` step references
- Include default fallback path when needed
- Test all condition scenarios

**For LOOP Steps:**
- Define clear `loopOver` data source from previous steps
- Ensure sub-steps use `{{data.steps.loopStepId.loopOverItem}}` for current item
- Plan data extraction strategy for results outside loop scope
- Use VARIABLE steps to collect loop results if needed

**For LAMBDA Steps:**
- Always define `fastn_function(params)` as the main entry point
- Use only available Python libraries from the documented list
- Include proper error handling with try-catch blocks
- Access secrets via `params["data"]["secrets"]`, never hardcode credentials
- Return JSON-serializable data structures
- Handle timeouts for external API calls and database connections
- Design for quick execution - avoid long-running computations

### 9.5. Model ID Standards

Always use these standardized model IDs from `base_flow.json`:
- **inputModelId**: `"07a1436d4df2fe3ee87d4fd70ea6a259"`
- **outputModelId**: `"json"`
- **headerModelId**: `"9fed297b87c60d6808c16df827fc4407"`

### 9.6. Status Field Requirements

**CRITICAL**: The top-level `status` field must use ONLY these valid enum values:
- **`"DEPLOYED"`** - For production-ready flows (RECOMMENDED)
- **`"CONNECT"`** - For connection testing flows
- **`"PUBLISH"`** - For published flows

**❌ INVALID VALUES**: `"DRAFT"`, `"ACTIVE"`, `"INACTIVE"`, `"PENDING"` - These will cause deserialization errors

**✅ ALWAYS USE**: `"status": "DEPLOYED"` (copy exactly from base_flow.json)

### 9.6. Required Field Validation

Every step must include these base fields:
```json
{
  "type": "STEP_TYPE",
  "id": "uniqueStepId",
  "actionId": null,
  "next": "nextStepId",
  "prevStep": null,
  "enableDebug": false,
  "description": null,
  "debugBreakAfter": 1,
  "configuredStepSetting": null,
  "settings": {
    "failureBehavior": "FAILURE",
    "skipStatus": null,
    "errorMessage": null,
    "stepNote": null
  },
  "warnings": null,
  "tenantSettings": null
}
```

Plus step-specific configuration objects (inline, function, composite, loop, etc.)

## 10. Flow Validation & Troubleshooting

**🚀 RECOMMENDED: Use Automated Validation First**

Run the automated validation script before manual review:
```bash
python3 flow_validator.py your_flow.json
```

This script automatically validates:
- JSON structure and required fields
- Model objects (prevents NPE errors)
- Status values (prevents deserialization failures)  
- Step configurations and requirements
- Data references (prevents bounds errors)
- Composite/connector step requirements

After automated validation, use **[VALIDATION_GUIDE.md](./VALIDATION_GUIDE.md)** for comprehensive troubleshooting which provides:
- Detailed validation checklist
- Common mistakes and solutions
- Specific error troubleshooting
- Step-by-step issue resolution

## 11. Quick Reference Summary

### Essential Commands
```bash
# Get connector endpoint details
python3 stepsDetails/compositeStep/get_endpoint_details.py <endpoint_name> [connector_file.json]

# Generate UI code for connectors
python3 stepsDetails/compositeStep/generate_uicode.py <endpoint_name> [connector_file.json]

# Validate flow before deployment
python3 flow_validator.py <flow_file.json>
```

### Standard Model IDs
- **inputModelId**: `"07a1436d4df2fe3ee87d4fd70ea6a259"`
- **outputModelId**: `"json"`  
- **headerModelId**: `"9fed297b87c60d6808c16df827fc4407"`

### Data Mapping Patterns
See section 6 for complete data mapping patterns and examples.

### Complex Flow Architecture Reference
**📚 COMPULSORY READING:** `flowExamples/acumatica_bigComerce/ACUMATICA_BIGCOMMERCE_FLOWS_ANALYSIS.md`
- Enterprise-grade integration patterns for complex data synchronization
- Multi-tenant architecture, batch processing, and error handling strategies
- Real-world examples of flows ranging from 371 to 8,229 lines of complexity

### Validation Checklist
- [ ] Root structure is an array `[{...}]`
- [ ] All required top-level fields present
- [ ] **Complete model objects copied from base_flow.json (NOT null)**
- [ ] **Status field is "DEPLOYED", "CONNECT", or "PUBLISH" (NEVER "DRAFT")**
- [ ] All step IDs are unique
- [ ] All `next` fields reference valid step IDs
- [ ] All connector fields complete and accurate
- [ ] All data mappings reference existing paths
- [ ] JSON syntax is valid and properly escaped


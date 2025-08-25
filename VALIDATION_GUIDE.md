# Validate Issues

## 📋 **Automated Flow Validation**

**🚀 NEW: Use the Flow Validation Script**

Before manually checking, run the automated validation script to catch common errors:

```bash
python3 flow_validator.py your_flow.json
```

**Example Usage:**
```bash
cd /path/to/fastnFlowGeneration
python3 flow_validator.py flowExamples/shoppifyOrdersToGoogleSheet.json
```

The script automatically validates all the points below and provides detailed error reports with solutions.

## 📋 **Common Mistakes to Avoid from Flow Guidance**

After creating a flow, validate it against these common mistakes to ensure proper functioning (or use the automated script above):

### 1. **Incorrect Root Object**
- The root of the JSON file must be an **array**
- ❌ `{"clientId": "...", "id": "..."}` 
- ✅ `[{"clientId": "...", "id": "..."}]`

### 2. **Missing Top-Level Fields**
- Use the `base_flow.json` to ensure all mandatory fields are present
- Required fields: `clientId`, `id`, `name`, `actionType`, `inputName`, `inputModelId`, `outputModelId`, `headerModelId`, `resolver`, `metaData`

### 3. **Incorrect Step Structure**
- Refer to the `stepsDetails` directory and example flows for correct step structure
- Each step must have proper `type`, `id`, and corresponding configuration object

### 4. **Null or Missing Models (NPE on Import)** ❌ CRITICAL ERROR REPORTED
- **Error**: `Cannot invoke "ai.fastn.business.datahub.datamodel.DataModelInput.getId()" because "outputModel" is null`
- **Problem**: The `outputModel`, `inputModel`, or `headerModel` objects are missing/null in the flow JSON
- **Root Cause**: LLM generated flow without copying the complete model objects from `base_flow.json`

**Step-by-Step Solution:**
1. **Copy Model Objects**: Always copy the complete `inputModel`, `outputModel`, and `headerModel` objects from `base_flow.json`
2. **Verify Model IDs Match**: Ensure `outputModelId` references the actual `outputModel.id` 
3. **Never Use Null**: Never set model fields to `null` - always include complete model objects

**Required Model Structure:**
```json
{
  "inputModelId": "07a1436d4df2fe3ee87d4fd70ea6a259",
  "outputModelId": "json", 
  "headerModelId": "9fed297b87c60d6808c16df827fc4407",
  "inputModel": { /* complete model object from base_flow.json */ },
  "outputModel": { /* complete model object from base_flow.json */ },
  "headerModel": { /* complete model object from base_flow.json */ }
}
```

**Prevention**: Always start with `base_flow.json` and copy ALL fields including model objects

### 5. **Missing UI Metadata**
- The `uiCode` and `queryExecutor` fields in `INLINE` steps are required for the fastn UI
- Use the provided scripts to generate proper UI code

### 6. **Invalid Status Value** ❌ CRITICAL ERROR REPORTED
- **Error**: `Cannot deserialize value of type 'ai.fastn.business.datafetcher.models.ApiStatus' from String "DRAFT"`
- **Problem**: The top-level `status` field contains an invalid enum value
- **Valid Values ONLY**: `"DEPLOYED"`, `"CONNECT"`, `"PUBLISH"`
- **Invalid Values**: `"DRAFT"`, `"ACTIVE"`, `"INACTIVE"`, `"PENDING"` (will cause deserialization failure)
- **Solution**: Always use `"status": "DEPLOYED"` (copy exactly from base_flow.json)
- **Never use**: `"DRAFT"` - This is NOT a valid status value despite appearing in some examples

### 7. **Unescaped Inline Code**
- Inline step `code` must be properly escaped to be a valid JSON string
- Special characters and quotes must be properly escaped

### 8. **Model ID Mismatches**
- Ensure `inputModelId`, `outputModelId`, and `headerModelId` reference existing model IDs
- Use standard IDs from `base_flow.json` (see fastn_flow_guide.md section 9.4 for details)

### 9. **Step Connectivity Issues** ❌ CRITICAL ERROR REPORTED
- **Error**: `Found orphaned/unreachable steps: stepX, stepY`
- **Problem**: Steps exist in the flow but cannot be reached from the start step
- **Root Cause**: Missing or broken step connections in the flow navigation

**Step-by-Step Solution:**
1. **Check Start Step**: Ensure `resolver.start` points to an existing step ID
2. **Verify Next References**: Ensure every step's `next` field points to a valid step
3. **Handle Complex Steps**: 
   - COMPOSITE steps: Check `composite.next` and internal step connections
   - LOOP steps: Check `loop.next` and `loop.start` for internal flow
   - CONDITIONAL steps: Check all expression branches have valid `next` values
4. **Remove Unused Steps**: Delete steps that are no longer needed in the flow

**Flow Connection Pattern:**
```
Start Step → Step A → Step B → Step C → End (next: null)
             ↓
         (CONDITIONAL) → Branch 1 → Step D
                     → Branch 2 → Step E
```

**Prevention**: Always ensure every step is reachable through some execution path from the start step.

### 10. **Naming Convention Issues** ❌ CRITICAL ERROR PREVENTION

**🚨 CRITICAL: Invalid flow or step names can cause deployment failures**

#### **Flow Naming Rules:**
- **Format**: `camelCase` - start lowercase, capitalize each word
- **Length**: Keep short and descriptive (avoid overly long names)
- **Characters**: Only letters and numbers - NO spaces, dashes, underscores, special chars
- **Examples**: `syncShopifyOrders`, `processPayments`, `updateInventory`

**❌ Common Naming Mistakes:**
```json
"id": "sync-orders-flow",        // Has dashes
"name": "Sync Orders Flow"       // Has spaces and capitals
"id": "shopify_to_bigcommerce_sync_flow_with_notifications" // Too long with underscores
```

**✅ Correct Naming:**
```json
"id": "syncShopifyOrders",
"name": "syncShopifyOrders"
```

#### **Step Naming Rules:**

**For Custom Steps (VARIABLE, INLINE, LOOP, CONDITIONAL):**
- Use `camelCase`: `transformData`, `validateInput`, `processOrders`
- Keep short and descriptive
- Name should reflect step's purpose

**For COMPOSITE Steps (Connectors):**
- **CRITICAL**: Use EXACT connector endpoint names from JSON files
- Don't modify or add prefixes: use `getProducts` not `getShopifyProducts`
- Don't change casing: use `sendMessage` not `send-message`

**Step-by-Step Solution:**
1. **Check Connector Files**: Use `get_endpoint_details.py` to see exact names
   ```bash
   python3 stepsDetails/compositeStep/get_endpoint_details.py getProducts shopifyConnectors.json
   ```
2. **Copy Exact Names**: For COMPOSITE steps, use precisely what's in connector JSON
   - Use `getProducts` not `getShopifyProducts`
   - Use `sendMessage` not `send-message` or `send_message`
   - Use `createProduct` not `createBigCommerceProduct`
3. **Custom Step Names**: Use camelCase for your custom processing steps
   - Use `transformData` not `Transform_Data` or `transform-data`
   - Use `validateInput` not `ValidateInput` or `validate input`
   - Use `processOrders` not `Process-Orders` or `process_orders`
4. **Validate Length**: Keep all names reasonably short but descriptive
5. **Run Validation**: Use `flow_validator.py` to catch naming errors before deployment

**Prevention**: Always validate naming before creating flows - invalid names cause deployment errors.

### 11. **Composite/Connector Step Requirements**
- When using composite steps for API connectors, ensure all required fields are present:
  - **`id`**: Must match the connector ID from connector details (e.g., `"_knexa_2Yrk5ZdsORprOGpdpf9R4piOtmn"`)
  - **`groupId`**: Must match the platform group ID from connector details (e.g., `"_knexa_2fc3b972-2f75-49d4-8cce-3a11a5990408"`)
  - **`name`**: Endpoint name (e.g., `"getProducts"`, `"sendMail"`, `"sendMessage"`)
  - **`version`**: Connector version (e.g., `"1.1.0"`)
  - **`connectorId`**: Usually `"community"`
  - **UI Code**: Always required for composite steps - use `generate_uicode.py` script to generate
  - **Configuration**: Must include proper auth type, retry settings, and validation flags

#### Platform Group IDs Reference:
See `stepsDetails/compositeStep/composite.md` for complete platform group IDs list.

#### How to Get Connector Details:
```bash
python3 get_endpoint_details.py <endpoint_name>
```

#### Example Connector Structure:
```json
"function": {
  "id": "_knexa_2Yrk5ZdsORprOGpdpf9R4piOtmn",
  "groupId": "_knexa_2fc3b972-2f75-49d4-8cce-3a11a5990408", 
  "connectorId": "community",
  "name": "getProducts",
  "version": "1.1.0",
  "configuration": {
    "enableAuth": true,
    "authType": "APIKEY",
    // ... other config
  }
}
```

---

## 🐛 **Specific Issue Resolution: "Index 1 out of bounds for length 1"**

### **Problem**
The flow was throwing "Index 1 out of bounds for length 1" error when trying to send products via Slack.

### **Root Cause** 
The issue was in the Slack connector template in `stepsDetails/compositeStep/slackConnectors.json` line 15, which had a hardcoded reference to:

```json
"text": {
  "target": "{{data.steps.flattenOrderDetails.output.flattenedRow[1]}}"
}
```

This template was trying to access index `[1]` of an array that only had 1 element (index 0 only), causing the bounds error.

### **Solution**
1. **Identified the contaminated template**: Found the bad reference in slackConnectors.json
2. **Cleaned UI Code**: Removed all path/field/position metadata that contained the bad template  
3. **Fixed data mapping**: Ensured all references point to `{{data.steps.prepareProductsMessage.output.message}}` (a string) instead of array indices
4. **Enhanced JavaScript error handling**: Added proper bounds checking and error handling
5. **Used correct model IDs**: Updated to match `base_flow.json` structure

### **Key Changes**

#### Before (Problematic):
```json
"text": {
  "target": "{{data.steps.flattenOrderDetails.output.flattenedRow[1]}}"
}
```

#### After (Fixed):
```json  
"text": {
  "target": "{{data.steps.prepareProductsMessage.output.message}}"
}
```

### **Prevention Tips**
1. **Always validate generated UI code** from connector templates
2. **Avoid hardcoded array indices** in templates  
3. **Use semantic data references** instead of positional array access
4. **Test with actual data structures** before deployment
5. **Follow base_flow.json structure exactly** for model IDs and metadata

### **Verification Checklist**
- ✅ No `[1]` references found in the flow
- ✅ No `flattenedRow` references found in the flow  
- ✅ All data mappings point to proper string outputs
- ✅ Enhanced error handling in JavaScript steps
- ✅ Correct model IDs matching base_flow.json
- ✅ **Complete model objects copied from base_flow.json (inputModel, outputModel, headerModel)**
- ✅ **Model objects are NOT null (prevents NPE on import)**
- ✅ **Status field uses ONLY valid enum values: "DEPLOYED", "CONNECT", or "PUBLISH"**
- ✅ **NEVER uses "DRAFT" as status value (causes deserialization error)**
- ✅ **All steps are connected and reachable from start step (no orphaned steps)**
- ✅ **All next step references point to existing steps**
- ✅ **Start step exists and is properly defined in resolver**
- ✅ **Flow and step names follow camelCase conventions (no spaces, dashes, underscores)**
- ✅ **COMPOSITE step names match exact connector endpoint names from JSON files**
- ✅ **Flow name is short, descriptive, and deployment-safe**
- ✅ **LAMBDA steps have proper lambdaFunction configuration with Python code**
- ✅ **LAMBDA steps define fastn_function(params) as entry point**
- ✅ **LAMBDA steps use only available Python libraries from documented list**
- ✅ No linter errors in final JSON

The flow is now safe from array bounds errors, status deserialization failures, and properly handles the product data structure.

---

## 🛠️ **Flow Validation Script Details**

**Script Location:** `flow_validator.py` (in project root directory)

**What the Script Validates:**

✅ **JSON Structure**
- Root object must be array
- Required top-level fields present
- Valid JSON format

✅ **Critical Error Prevention**
- **NPE Prevention**: Validates inputModel, outputModel, headerModel are not null
- **Status Deserialization**: Ensures status uses valid enum values (DEPLOYED, CONNECT, PUBLISH)
- **Model ID Consistency**: Verifies model IDs match model object IDs

✅ **Step Validation**
- Valid step types (COMPOSITE, INLINE, CONDITIONAL, etc.)
- Required step fields (type, id, configuration objects)
- INLINE step requirements (uiCode, queryExecutor)
- API step requirements (function configuration)

✅ **Step Connectivity Validation**
- All steps must be reachable from the start step
- Detects orphaned/unreachable steps
- Validates next step references exist
- Handles complex flow patterns (COMPOSITE, LOOP, CONDITIONAL)
- Traces through all possible execution paths

✅ **Naming Convention Validation**
- Enforces camelCase for all flow and step names
- Detects spaces, dashes, underscores in names
- Validates flow names start with lowercase
- Checks COMPOSITE step names match connector endpoints
- Validates nested step naming in LOOP and COMPOSITE steps

✅ **LAMBDA Step Validation**
- Validates required lambdaFunction configuration
- Checks for required fields (code, language, version)
- Ensures language is set to "PYTHON"
- Validates presence of fastn_function(params) entry point
- Checks for queryExecutor configuration

✅ **Data Reference Safety**
- Detects hardcoded array indices that cause bounds errors
- Flags problematic references like `flattenedRow[1]`
- Warns about positional array access patterns

✅ **Composite/Connector Steps**
- Required function fields (id, groupId, name, version)
- Authentication configuration presence
- Connector ID validation

**Script Output:**
- **❌ CRITICAL ERRORS**: Issues that WILL cause flow failure
- **⚠️ WARNINGS**: Issues that may cause problems
- **ℹ️ INFO**: Helpful suggestions and guidance

**Exit Codes:**
- `0`: Validation passed (no critical errors)
- `1`: Validation failed (critical errors found)

**Integration with CI/CD:**
The script can be used in automated pipelines to validate flows before deployment:

```bash
# Validate and exit with appropriate code
python3 flow_validator.py myflow.json
if [ $? -eq 0 ]; then
    echo "Flow validation passed"
else 
    echo "Flow validation failed"
    exit 1
fi
```

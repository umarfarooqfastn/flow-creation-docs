# Response Step (INLINE with JINJA) 📤

Response Steps are **INLINE** steps that return the **final API response** to the client. They are the terminal steps that end the flow execution and provide the output.

## 🎯 **Purpose**
Response Steps are used to:
- Return the final API response to the client
- Format the output data for the API consumer
- Provide status information about the flow execution
- End the flow execution chain

## ⚙️ **Essential Requirements for Response Steps**

### **1. Language & Response Configuration**
```json
{
  "language": "JINJA",
  "hasResponse": true,
  "next": null
}
```

### **2. Terminal Step Pattern**
- **ALWAYS** have `"next": null` (end the flow)
- **ALWAYS** have `"hasResponse": true` 
- Are typically the **last step** in the flow execution path

### **3. JINJA Template Format**
Response Steps use **JINJA** templating language for simple data formatting:

```json
{
  "code": "{\n  \"status\": \"success\",\n  \"message\": \"{{data.steps.someStep.output.message}}\",\n  \"count\": {{data.steps.someStep.output.count}}\n}",
  "language": "JINJA"
}
```

## 🚫 **What Response Steps Should NOT Do**

❌ **Don't use JavaScript for complex logic**
❌ **Don't process or transform data** 
❌ **Don't have `"next": "nextStep"`** (they end the flow)
❌ **Don't have `"hasResponse": false"`**

## ✅ **vs Custom Code Steps**

| Aspect | Response Step | Custom Code Step |
|--------|---------------|------------------|
| **Purpose** | Return final API response | Process/transform data |
| **Language** | `JINJA` | `JAVASCRIPT` |
| **hasResponse** | `true` | `false` (typically) |
| **next** | `null` (end flow) | `"nextStepId"` (continue flow) |
| **Position** | Terminal/last step | Middle of flow |
| **Complexity** | Simple formatting | Complex logic/calculations |

## 📋 **Common Response Step Patterns**

### **1. Simple Success Response**
```json
{
  "type": "INLINE",
  "id": "Success",
  "inline": {
    "code": "{\n  \"message\": \"Success\"\n}",
    "language": "JINJA",
    "hasResponse": true,
    "next": null,
    "uiCode": "..."
  }
}
```

### **2. Status with Data Response**
```json
{
  "type": "INLINE", 
  "id": "finalResponse",
  "inline": {
    "code": "{\n  \"status\": \"success\",\n  \"message\": \"Operation completed\",\n  \"itemsProcessed\": {{data.steps.processStep.output.count}},\n  \"timestamp\": \"{{ 'now' | date('Y-m-d H:i:s') }}\"\n}",
    "language": "JINJA",
    "hasResponse": true,
    "next": null,
    "uiCode": "..."
  }
}
```

### **3. Error Response Pattern**
```json
{
  "type": "INLINE",
  "id": "errorResponse", 
  "inline": {
    "code": "{\n  \"status\": \"error\",\n  \"error\": \"{{data.steps.errorStep.output.errorMessage}}\",\n  \"timestamp\": \"{{ 'now' | date('Y-m-d H:i:s') }}\"\n}",
    "language": "JINJA",
    "hasResponse": true,
    "isError": true,
    "statusCode": 400,
    "next": null,
    "uiCode": "..."
  }
}
```

## 🔄 **Data Access Patterns in Response Steps**

Response Steps access data using **JINJA syntax**:

```json
{
  "code": "{\n  \"result\": \"{{data.steps.stepId.output.fieldName}}\",\n  \"input\": \"{{data.input.fieldName}}\",\n  \"variable\": \"{{data.var.variableName}}\"\n}"
}
```

## 🎯 **When to Use Response Steps**

✅ **Use Response Steps when:**
- You need to return the final API response
- The step is the last step in the flow
- You're formatting simple output data
- You need to end the flow execution

❌ **Don't Use Response Steps when:**  
- You need to process data for subsequent steps
- You need complex JavaScript logic
- The step is in the middle of the flow
- You need to transform or calculate data

## 📁 **Example Flows**

**Response Steps are used in:**
- `shoppifyOrdersToGoogleSheet.json` - `Success` step
- `shopify_to_bigcommerce_sync_flow.json` - `finalResponse` step
- `flow_with_connector_example.json` - Final response steps

For **Custom Code examples** (data processing), see:
- `customCodeStep/customCode.md`
- `flowExamples/` directory with JavaScript transformation steps

## 🚨 **Critical for LLMs**

**🎯 Response Steps = Final API Response (JINJA, hasResponse: true, next: null)**  
**🎯 Custom Code Steps = Data Processing (JAVASCRIPT, hasResponse: false, next: nextStep)**

**Never confuse these two patterns!** They serve completely different purposes in the flow execution.

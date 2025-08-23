# Custom Code Step (INLINE with JAVASCRIPT) 🛠️

**Custom Code Steps** are **INLINE** steps that use **JAVASCRIPT** to process, transform, and manipulate data **in the middle of the flow**. They are NOT for final API responses.

## 🎯 **Purpose**
Custom Code Steps are used to:
- **Process and transform data** from previous steps
- **Calculate, filter, or manipulate** complex data structures  
- **Prepare data** for subsequent steps (API calls, database operations)
- **Implement business logic** that can't be achieved with other step types

## ⚙️ **Essential Requirements for Custom Code Steps**

### **1. Language & Processing Configuration**
```json
{
  "language": "JAVASCRIPT",
  "hasResponse": false,
  "next": "nextStepId"
}
```

### **2. Processing Step Pattern**
- **ALWAYS** have `"next": "nextStepId"` (continue flow)
- **TYPICALLY** have `"hasResponse": false`
- Are **middle steps** in the flow execution path
- Process data for **subsequent steps** to use

### **3. JavaScript Handler Function**
All code MUST be within the `handler(params)` function:

```javascript
function handler(params) {
  // Access previous step data
  const inputData = params.data.steps.previousStep.output;
  
  // Process/transform data
  const processedData = inputData.map(item => ({
    id: item.id,
    name: item.title.toUpperCase(),
    price: parseFloat(item.price) || 0
  }));
  
  // Return data for next steps
  return {
    processedItems: processedData,
    count: processedData.length
  };
}
```

## 🚫 **What Custom Code Steps Should NOT Do**

❌ **Don't return final API responses** (use Response Steps instead)
❌ **Don't have `"next": null"`** (they continue the flow)
❌ **Don't use JINJA language** (use JAVASCRIPT)
❌ **Don't put code outside handler function**

## ✅ **vs Response Steps**

| Aspect | Custom Code Step | Response Step |
|--------|------------------|---------------|
| **Purpose** | Process/transform data | Return final API response |
| **Language** | `JAVASCRIPT` | `JINJA` |
| **hasResponse** | `false` (typically) | `true` |
| **next** | `"nextStepId"` (continue flow) | `null` (end flow) |
| **Position** | Middle of flow | Terminal/last step |
| **Complexity** | Complex logic/calculations | Simple formatting |

## 🔄 **Data Access Patterns in handler(params)**

Access previous step data using JavaScript:

```javascript
function handler(params) {
  // From previous steps
  const stepData = params.data.steps.stepId.output.fieldName;
  
  // From input
  const inputData = params.data.input.fieldName;
  
  // From variables
  const varData = params.data.var.variableName;
  
  // From loop items (in LOOP context)
  const loopItem = params.data.steps.loopStepId.loopOverItem;
  
  // From parent context (in nested steps)  
  const parentData = params.data.parent.input.fieldName;
}
```

**Essential Requirements for INLINE Steps:**
See `fastn_flow_guide.md` section 9.3 for complete implementation guidelines.

**Complete Data Mapping Patterns:**
See `fastn_flow_guide.md` section 6 for all data access patterns.

**Complete INLINE Step Structure:**
{
"type": "INLINE",
"id": "flattenOrderDetails",
"actionId": null,
"inline": {
    "code": "function handler(params) {\n  const orderDetails = params.data.steps.loopOverOrders.loopOverItem;\n\n  const flattenedRow = [\n    orderDetails.id || \"\",                                     // Order ID\n    orderDetails.name || \"\",                                   // Order Name\n    orderDetails.financial_status || \"\",                       // Payment Status\n    orderDetails.processed_at || \"\",                           // Order Date\n    orderDetails.subtotal_price || \"\",                         // Subtotal\n    orderDetails.total_price || \"\",                            // Total\n    orderDetails.currency || \"\",                               // Currency\n    orderDetails.email || \"\",                                  // Customer Email\n    orderDetails.line_items?.[0]?.name || \"\",                  // First Item Name\n    orderDetails.line_items?.[0]?.price || \"\",                 // First Item Price\n    orderDetails.line_items?.[0]?.quantity || \"\",              // First Item Quantity\n    orderDetails.shipping_address?.address1 || \"\",             // Shipping Address\n    orderDetails.shipping_address?.city || \"\",\n    orderDetails.shipping_address?.country || \"\"\n  ];\n  let flag = true;\n  if (orderDetails.financial_status === \"paid\") {\n    flag = false;\n  }\n  return {\n    flattenedRow: flattenedRow,\n    flag: flag\n  };\n}",
    "language": "JAVASCRIPT",
    "fields": [],
    "next": "Switch",
    "uiCode": "function handler(params) {\n  const orderDetails = params.data.steps.loopOverOrders.loopOverItem;\n\n  const flattenedRow = [\n    orderDetails.id || \"\",                                     // Order ID\n    orderDetails.name || \"\",                                   // Order Name\n    orderDetails.financial_status || \"\",                       // Payment Status\n    orderDetails.processed_at || \"\",                           // Order Date\n    orderDetails.subtotal_price || \"\",                         // Subtotal\n    orderDetails.total_price || \"\",                            // Total\n    orderDetails.currency || \"\",                               // Currency\n    orderDetails.email || \"\",                                  // Customer Email\n    orderDetails.line_items?.[0]?.name || \"\",                  // First Item Name\n    orderDetails.line_items?.[0]?.price || \"\",                 // First Item Price\n    orderDetails.line_items?.[0]?.quantity || \"\",              // First Item Quantity\n    orderDetails.shipping_address?.address1 || \"\",             // Shipping Address\n    orderDetails.shipping_address?.city || \"\",\n    orderDetails.shipping_address?.country || \"\"\n  ];\n  let flag = true;\n  if (orderDetails.financial_status === \"paid\") {\n    flag = false;\n  }\n  return {\n    flattenedRow: flattenedRow,\n    flag: flag\n  };\n}",
    "hasResponse": false,
    "isError": false,
    "statusCode": 200,
    "outputSchema": null,
    "queryExecutor": null
},
"function": null,
"composite": null,
"loop": null,
"internalDatabase": null,
"aiAction": null,
"mcpClient": null,
"logger": null,
"downLoadFile": null,
"endLoop": null,
"trigger": null,
"converter": null,
"variables": null,
"state": null,
"conditional": null,
"lambdaFunction": null,
"outputSchema": null,
"next": "Switch",
"prevStep": null,
"enableDebug": false,
"description": null,
"debugBreakAfter": 1,
"configuredStepSetting": null,
"filter": null,
"limit": null,
"splitOut": null,
"aggregate": null,
"merge": null,
"aiAgent": null,
"settings": {
    "failureBehavior": "FAILURE",
    "skipStatus": null,
    "errorMessage": null,
    "stepNote": null
},
"ftp": null,
"warnings": null,
"tenantSettings": null
}

## 🎯 **When to Use Custom Code Steps**

✅ **Use Custom Code Steps when:**
- You need to **transform data** from one format to another
- You need to **calculate values** or perform complex operations
- You need to **filter, map, or reduce** data arrays
- You need to **combine data** from multiple previous steps
- You need to **validate or clean** data before sending to APIs
- The step is **in the middle** of the flow (not the last step)

❌ **Don't Use Custom Code Steps when:**
- You just need to return a **final API response**
- You need **simple data formatting** (use JINJA Response Steps)
- The step is the **last step** in the flow (use Response Steps)
- You don't need to **process data** for subsequent steps

## 📋 **Common Custom Code Patterns**

### **1. Data Transformation**
```javascript
function handler(params) {
  const products = params.data.steps.getProducts.output.products;
  
  // Transform Shopify to BigCommerce format
  const transformed = products.map(product => ({
    name: product.title || 'Unknown Product',
    price: parseFloat(product.variants[0]?.price) || 0,
    type: 'physical',
    is_visible: true
  }));
  
  return { transformedProducts: transformed };
}
```

### **2. Data Flattening**
```javascript  
function handler(params) {
  const order = params.data.steps.loopOverOrders.loopOverItem;
  
  // Flatten complex order to array for spreadsheet
  const flattened = [
    order.id || "",
    order.name || "",
    order.financial_status || "",
    order.total_price || "",
    order.line_items?.[0]?.name || ""
  ];
  
  return { flattenedRow: flattened };
}
```

### **3. Business Logic Processing**
```javascript
function handler(params) {
  const orderData = params.data.steps.getOrder.output;
  
  // Apply business rules
  let status = 'pending';
  if (orderData.financial_status === 'paid' && orderData.fulfillment_status === 'fulfilled') {
    status = 'completed';
  } else if (orderData.financial_status === 'paid') {
    status = 'processing';
  }
  
  return { 
    processedStatus: status,
    requiresAction: status === 'pending'
  };
}
```

## 📁 **Example Flows**

**Custom Code Steps are used in:**
- **`shopify_to_bigcommerce_sync_flow.json`**: `transformProductData`, `prepareSuccessMessage` (data processing)
- **`shoppifyOrdersToGoogleSheet.json`**: `flattenOrderDetails` (data transformation)
- **`ComplexFlowWithMappingsAndCustomerUsecase.json`**: Multiple data processing steps

**Response Steps (NOT Custom Code) are used in:**  
- **`shoppifyOrdersToGoogleSheet.json`**: `Success` step (final response)
- **`shopify_to_bigcommerce_sync_flow.json`**: `finalResponse` step (final response)

For **Response Step examples** (final API responses), see:
- `responseStep/responseStep.md`

## 🚨 **Critical for LLMs**

**🎯 Custom Code Steps = Data Processing (JAVASCRIPT, hasResponse: false, next: nextStep)**  
**🎯 Response Steps = Final API Response (JINJA, hasResponse: true, next: null)**

**Key Decision Rule:**
- If the step **processes data for subsequent steps** → Custom Code Step  
- If the step **returns final response to client** → Response Step

**Never confuse these two patterns!** They serve completely different purposes in the flow execution.
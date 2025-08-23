### Loop Step

**What is Loop Step and Usage of It**
-Loop step is used to loop over data , do infinte loop and for loop.
-Loop step is mostly used when we need to loop over data
-Loop step configuration is we need to pass the array to it from previouse steps
-Inside the there can be multiple steps like composite step(connector step) , database step or any step available

**Essential Requirements for LOOP Steps:**
See `fastn_flow_guide.md` section 9.3 for complete implementation guidelines.

**Data Access Patterns in Loops:**
See `fastn_flow_guide.md` section 6 for complete data mapping patterns.

**Complete LOOP Step Structure Example:**

```json
{
  "type": "LOOP",
  "id": "loopOverOrders",
  "actionId": null,
  "loop": {
    "id": "loopOverOrders",
    "loopOver": "{{data.steps.getOrders.output.orders}}",
    "start": "flattenOrderDetails",
    "steps": [
      {
        "type": "INLINE",
        "id": "flattenOrderDetails",
        "inline": {
          "code": "function handler(params) {\n  const orderDetails = params.data.steps.loopOverOrders.loopOverItem;\n  // Process the current item\n  return processedData;\n}",
          "language": "JAVASCRIPT",
          "next": "conditionalStep"
        }
      }
    ]
  },
  "next": "stepAfterLoop"
}
```

**Common Mistakes to Avoid:**
See `VALIDATION_GUIDE.md` for complete list of common mistakes and solutions.

**Complete Examples:**

See these example flows in `../../flowExamples/` that demonstrate loop steps:

- **`flow_with_looping_example.json`**: Dedicated example showing various loop patterns and configurations
- **`shoppifyOrdersToGoogleSheet.json`**: Loop over Shopify orders for processing with [detailed explanation](../../flowExamples/explanation_of_Shopify_OrdersToGoogleSheet.md)
- **`ComplexFlowWithMappingsAndCustomerUsecase.json`**: Advanced loop implementations with complex data extraction

All examples demonstrate proper loop configuration, item access, and data flow patterns.
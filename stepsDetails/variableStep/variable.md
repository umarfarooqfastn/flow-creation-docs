### Variable Step

**Whats is Variable Step and Usage**
- Variable Step is being used for storing values for next usage into the flow.
- Variable is being used to get the data from loop to outside the loop for further use.
- We can insert data into the varaible from previouse step or from input or from headers.
- It can be used for logic as well i mentioned above when we need to push the data out side the loop scope we will insert the data into variable.but before we create varaibale with same name field outside the loop and before the loop step.
- Full usecase examples available in `../../flowExamples/` directory
**Essential Requirements for VARIABLE Steps:**
See `fastn_flow_guide.md` section 9.3 for complete implementation guidelines.

**Data Access Patterns for Variables:**
See `fastn_flow_guide.md` section 6 for complete data mapping patterns.

**Complete VARIABLE Step Structure Example:**

```json
{
  "type": "VARIABLE",
  "id": "initializeVariables",
  "actionId": null,
  "variables": {
    "id": "initializeVariables",
    "assignVar": [
      {
        "field": "sheetTitle",
        "mapping": "{% if data.input.sheetTitle is defined %}{{data.input.sheetTitle}}{% else %}\"OrderDetails\"{% endif %}"
      },
      {
        "field": "name", 
        "mapping": "{% if data.input.name is defined %}{{data.input.name}}{% else %}null{% endif %}"
      }
    ],
    "outputVariables": [
      {
        "name": "sheetTitle",
        "type": "string",
        "target": "{{data.variables.sheetTitle}}"
      },
      {
        "name": "name", 
        "type": "string",
        "target": "{{data.variables.name}}"
      }
    ],
    "next": null
  },
  "next": "nextStep"
}
```

**Common Use Cases:**
- Storing loop iteration results for use outside the loop
- Initializing default values from input parameters
- Collecting aggregated data across multiple steps
- Managing state between conditional branches

**Common Mistakes to Avoid:**
See `VALIDATION_GUIDE.md` for complete list of common mistakes and solutions.

**Complete Examples:**

See these example flows in `../../flowExamples/` that demonstrate variable steps:

- **`shoppifyOrdersToGoogleSheet.json`**: Variable initialization for input parameters and defaults with [detailed explanation](../../flowExamples/explanation_of_Shopify_OrdersToGoogleSheet.md)
- **`ComplexFlowWithMappingsAndCustomerUsecase.json`**: Advanced variable usage patterns for complex data management and loop data extraction
- **`flow_with_looping_example.json`**: Variable usage for collecting loop results

All examples show proper variable declaration, initialization, and scope management.
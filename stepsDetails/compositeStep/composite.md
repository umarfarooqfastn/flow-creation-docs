### Connector or Composite Step

**What is Connector or Composite Step**
- This Step is being used to call APIs for platforms in the flow like Google services (Gmail, Shopping, Calendar), MongoDB, Slack, CRMs, AWS.
- We have connectors (endpoints) for 1000+ platforms.
- Composite steps encapsulate multiple sub-steps to complete a connector operation, typically including data mapping and API calls.

**Critical Requirements for Composite Steps**
See `fastn_flow_guide.md` section 9.3 for complete implementation guidelines.

**Connector Details**
- Connectors details available in `connectorDetails.md` file.
- Using that information you need to convert the details into a composite step.
- Input schema, output schema and IDs details are available in the same file.
- After selecting the connector or endpoint of a platform inject the generated schema into workflow or flow.

**Essential Workflow for Composite Steps:**

1. **Identify Required Connector & Endpoint:**
   - Review available connectors in `connectorDetails.md`
   - Choose the appropriate endpoint for your use case
   - Note the connector file name (e.g., `shopifyConnectors.json`)

2. **Get Connector Details:**
```bash
# For unique endpoints (recommended approach)
python3 get_endpoint_details.py <endpoint_name> <connector_file.json>

# For searching all connectors (will prompt if duplicates exist)
python3 get_endpoint_details.py <endpoint_name>
```

3. **Generate UI Code:**
```bash
# For unique endpoints (recommended approach)
python3 generate_uicode.py <endpoint_name> <connector_file.json>

# For searching all connectors
python3 generate_uicode.py <endpoint_name>
```

4. **Extract Required Fields:**
- Note the `groupId` (platform identifier)
- Note the connector `id` (specific endpoint identifier)
- Note the `version` (connector version)
- Note authentication requirements

**Important:** Many endpoint names exist across multiple connectors (e.g., `getProducts` in both Shopify and Bigcommerce). Always specify the connector file to avoid ambiguity and ensure you get the correct endpoint details.

**Complete Composite Step Structure Example:**

```json
{
  "type": "COMPOSITE",
  "id": "uniqueCompositeStepId",
  "actionId": null,
  "composite": {
    "id": "compositeStepId",
    "next": null,
    "steps": [
      {
        "type": "INLINE",
        "id": "mapInputData",
        "inline": {
          "code": "{\n  \"field1\": \"{{data.input.value1}}\",\n  \"field2\": \"{{data.steps.previousStep.output.value2}}\"\n}",
          "language": "JINJA",
          "fields": [],
          "next": "callConnector",
          "uiCode": "{\"actionType\":\"map\",\"target\":{...}}",
          "hasResponse": true,
          "isError": false,
          "statusCode": 200,
          "outputSchema": null,
          "queryExecutor": {...}
        },
        "function": null,
        "composite": null,
        // ... all required null fields
        "next": "callConnector"
      },
      {
        "type": "API",
        "id": "callConnector", 
        "function": {
          "id": "_knexa_2Yrk5ZdsORprOGpdpf9R4piOtmn",
          "groupId": "_knexa_2fc3b972-2f75-49d4-8cce-3a11a5990408",
          "connectorId": "community",
          "name": "endpointName",
          "version": "1.1.0",
          "configuration": {
            "enableAuth": true,
            "authType": "APIKEY",
            "retryOnFailure": true,
            "retryCount": 3,
            "retryInterval": 1000,
            "enableValidation": true,
            "timeout": 30000
          }
        },
        "inline": null,
        "composite": null,
        // ... all required null fields
        "next": null
      }
    ]
  },
  "function": null,
  "inline": null,
  // ... all other required null fields
  "next": "nextStepInMainFlow",
  "settings": {
    "failureBehavior": "FAILURE",
    "skipStatus": null,
    "errorMessage": null,
    "stepNote": null
  }
}
```

**Platform Group IDs Reference:**
- **Shopify**: `_knexa_2fc3b972-2f75-49d4-8cce-3a11a5990408`
- **Gmail**: `5743b46c-38a0-418f-84fa-8ed18198f72e`  
- **Slack**: `_knexa_c9085d88-85d0-4436-82c6-4e42d6aba4c6`
- **Acumatica**: `_knexa_7e87c3fe-4ddf-4a79-a12e-0da07cccbfc3`

**Data Mapping in Composite Steps:**
- Input mapping step: Maps flow data to connector expected format
- Output processing step: Maps connector response to flow format
- Always use semantic field names, avoid array indices

**Common Mistakes to Avoid:**
See `VALIDATION_GUIDE.md` for complete list of common mistakes and solutions.

**Complete Examples:**

See these example flows in `../../flowExamples/` that demonstrate composite steps:

- **`flow_with_connector_example.json`**: Basic connector integration patterns
- **`shoppifyOrdersToGoogleSheet.json`**: Multi-platform integration (Shopify + Google Sheets + Slack) with [detailed explanation](../../flowExamples/explanation_of_Shopify_OrdersToGoogleSheet.md)
- **`ComplexFlowWithMappingsAndCustomerUsecase.json`**: Advanced composite step patterns with complex data mappings

All examples show proper connector configuration, UI code generation, and data mapping patterns.
### Note on UI Code Generation

For custom INLINE or VARIABLE steps, the `uiCode` structure must be manually created based on the code block structure. Unlike connector endpoints that have predefined schemas, custom code steps require manual UI code creation that matches the data structure being returned.

**UI Code Generation Guidelines:**
- For JINJA steps returning JSON objects, create UI code that matches the output structure
- For JavaScript steps, ensure UI code reflects the returned object properties
- Always include proper field mappings and data types
- Test UI code generation with actual data structures

**Manual UI Code Example for Custom Step:**
```json
{
  "actionType": "map",
  "target": {
    "fieldName": {
      "actionType": "map", 
      "target": "{{data.steps.previousStep.output.value}}",
      "targetType": "string",
      "isRequired": true
    }
  },
  "targetType": "object"
}
```
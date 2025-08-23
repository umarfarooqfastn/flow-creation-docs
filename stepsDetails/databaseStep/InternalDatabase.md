### Database Step (INTERNAL_DB)

**What is Database Step and Usage**
- Database step is connected with PostgreSQL internally with fastn. Each user has database access.
- In this step user can perform any database operation like CREATE TABLE, INSERT, UPDATE, DELETE, SELECT.
- Data can come from previous steps, be static, or come from input as well as from headers.
- Supports dynamic SQL generation using data mapping patterns.

**Essential Requirements for INTERNAL_DB Steps:**
See `fastn_flow_guide.md` section 9.3 for complete implementation guidelines.

**Data Access Patterns in SQL:**
See `fastn_flow_guide.md` section 6 for data mapping patterns. Note: Always use single quotes around string values in SQL.

**Complete INTERNAL_DB Step Structure Example:**

```json
{
  "type": "INTERNAL_DB",
  "id": "CreateTableOrders",
  "actionId": null,
  "internalDatabase": {
    "id": "CreateTableOrders",
    "sql": "CREATE TABLE IF NOT EXISTS orders (\n  id VARCHAR(255) PRIMARY KEY,\n  name VARCHAR(255),\n  financial_status VARCHAR(100),\n  processed_at TIMESTAMP,\n  subtotal_price DECIMAL(10,2),\n  total_price DECIMAL(10,2),\n  currency VARCHAR(10),\n  customer_email VARCHAR(255),\n  item_name VARCHAR(255),\n  item_price DECIMAL(10,2),\n  item_quantity INTEGER,\n  shipping_address VARCHAR(500),\n  shipping_city VARCHAR(100),\n  shipping_country VARCHAR(100)\n);",
    "params": [],
    "outputSchema": null,
    "next": null
  },
  "next": "nextStep",
  "settings": {
    "failureBehavior": "FAILURE",
    "skipStatus": null,
    "errorMessage": null,
    "stepNote": null
  }
}
```

**Example INSERT with Dynamic Data:**

```json
{
  "type": "INTERNAL_DB", 
  "id": "InsertOrderData",
  "actionId": null,
  "internalDatabase": {
    "id": "InsertOrderData",
    "sql": "INSERT INTO orders (id, name, financial_status, processed_at, subtotal_price, total_price, currency, customer_email, item_name, item_price, item_quantity, shipping_address, shipping_city, shipping_country) VALUES ('{{data.steps.flattenOrderDetails.output.flattenedRow[0]}}', '{{data.steps.flattenOrderDetails.output.flattenedRow[1]}}', '{{data.steps.flattenOrderDetails.output.flattenedRow[2]}}', '{{data.steps.flattenOrderDetails.output.flattenedRow[3]}}', {{data.steps.flattenOrderDetails.output.flattenedRow[4]}}, {{data.steps.flattenOrderDetails.output.flattenedRow[5]}}, '{{data.steps.flattenOrderDetails.output.flattenedRow[6]}}', '{{data.steps.flattenOrderDetails.output.flattenedRow[7]}}', '{{data.steps.flattenOrderDetails.output.flattenedRow[8]}}', {{data.steps.flattenOrderDetails.output.flattenedRow[9]}}, {{data.steps.flattenOrderDetails.output.flattenedRow[10]}}, '{{data.steps.flattenOrderDetails.output.flattenedRow[11]}}', '{{data.steps.flattenOrderDetails.output.flattenedRow[12]}}', '{{data.steps.flattenOrderDetails.output.flattenedRow[13]}}');",
    "params": [],
    "outputSchema": null,
    "next": null
  },
  "next": "nextStep"
}
```

**Common Database Operations:**
- **CREATE TABLE**: Define table structure
- **INSERT**: Add new records with dynamic data
- **UPDATE**: Modify existing records
- **DELETE**: Remove records based on conditions
- **SELECT**: Query data for use in subsequent steps

**Common Mistakes to Avoid:**
See `VALIDATION_GUIDE.md` for complete list of common mistakes and solutions.

**SQL Injection Prevention:**
- Always validate input data before using in SQL
- Use proper data type casting for numeric values
- Sanitize string inputs to prevent malicious SQL

**Complete Examples:**

See these example flows in `../../flowExamples/` that demonstrate database steps:

- **`flow_with_fastndb_example.json`**: Dedicated database operations example showing various SQL patterns
- **`shoppifyOrdersToGoogleSheet.json`**: Table creation and data insertion with dynamic values with [detailed explanation](../../flowExamples/explanation_of_Shopify_OrdersToGoogleSheet.md)
- **`ComplexFlowWithMappingsAndCustomerUsecase.json`**: Advanced database operations with complex data processing

All examples demonstrate proper SQL syntax, data mapping, and error handling for PostgreSQL operations.

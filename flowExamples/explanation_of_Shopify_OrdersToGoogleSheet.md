# Flow Logic and Step-by-Step Explanation

This document provides a detailed explanation of how fastn flows are structured and executed, using the `shoppifyOrdersToGoogleSheet.json` flow as a primary example.

For guidance on how to decide on the logic for a new flow, please refer to the "How to Build Flow Logic" section in the [fastn_flow_guide.md](../fastn_flow_guide.md).

## How Steps are Connected

A fastn flow is a sequence of steps that are executed in a specific order. The logic of the flow is controlled by the `resolver` object, which contains a `steps` array and a `start` field.

- **`resolver.start`**: This field specifies the `id` of the first step to be executed in the flow.
- **`step.next`**: Each step object has a `next` field that contains the `id` of the next step to be executed. This creates a chain of execution, defining the flow's logic.
- **Conditional Branching**: In the case of a `CONDITIONAL` (or `Switch`) step, the `expressions` array defines different paths. Each expression has a `next` field that determines where the flow should go if the condition is met.
- **Loops**: In a `LOOP` step, the `steps` array defines a sub-flow that is executed for each item in the loop. The `start` field within the `loop` object specifies the first step inside the loop.

By following the `start` and `next` fields, you can trace the entire execution path of a fastn flow.

## Data Mapping and the Resolver

Understanding how to control the flow of execution and pass data between steps is fundamental to building fastn flows.

### The Resolver: Orchestrating the Flow

The `resolver` object is the conductor of your workflow. It uses two key properties to manage the sequence of operations:

1.  **`start`**: This property in the `resolver` object holds the `id` of the very first step that should be executed. In our example, `resolver.start` is `"Variable5785"`, so the flow begins there.

2.  **`next`**: Each step within the `steps` array has a `next` property. This property holds the `id` of the step that should be executed immediately after the current step completes.

This creates a linked list or a chain of execution. The flow starts at the `start` step and follows the `next` references from one step to the next until it reaches a step where `next` is `null`.

**Example Trace:**
`Variable5785` -> `getOrders` -> `createSpreadsheet` -> ... -> `Success` (end)

### Data Mapping: Passing Information Between Steps

Steps in a flow are not isolated; they need to share information. This is done through data mapping, using a Jinja-like template syntax.

#### Mapping from the Initial Flow Input

Your flow can receive an initial payload of data. You can access this data anywhere in the flow using the `data.input` object.

In `shoppifyOrdersToGoogleSheet.json`, the first step `Variable5785` uses this to initialize some variables:

```json
"code": "{\n  \"sheetTitle\": {% if data.input.sheetTitle is defined %}\"{{data.input.sheetTitle}}\"{% else %}\"OrderDetails\"{% endif %},\n  \"name\": {% if data.input.name is defined %}\"{{data.input.name}}\"{% else %}null{% endif %}\n}"
```

Here, `{{data.input.sheetTitle}}` and `{{data.input.name}}` pull values from the JSON body of the initial request that triggered the flow.

#### Mapping from Previous Steps

The output of any step is available to all subsequent steps in the flow. You can access it using the `data.steps` object, followed by the `id` of the step you want to get data from.

A clear example is the `loopOverOrders` step. Its `loopOver` property is set to `{{data.steps.getOrders.output.orders}}`. This tells the loop to iterate over the `orders` array that was returned in the `output` of the `getOrders` step.

Inside the loop, the `flattenOrderDetails` step accesses the current item of the iteration via `data.steps.loopOverOrders.loopOverItem`.

This mechanism of passing outputs from one step to the inputs of another is the core of building complex, multi-step automations in fastn.

## Deep Dive: `shoppifyOrdersToGoogleSheet.json`

This flow is designed to fetch paid orders from Shopify, save them to a Google Sheet, store them in an internal database, and then send a notification to a Slack channel.

Here is a step-by-step breakdown of the flow's logic:

1.  **`Variable5785` (Start Step)**
    -   **Type:** `VARIABLE`
    -   **Purpose:** To initialize variables based on the flow's input.
    -   **Logic:** It takes `sheetTitle` and `name` from the input data (`data.input`). If `sheetTitle` is not provided, it defaults to "OrderDetails".
    -   **Next Step:** `getOrders`

2.  **`getOrders`**
    -   **Type:** `COMPOSITE`
    -   **Purpose:** To fetch orders from a Shopify store.
    -   **Logic:** This is a composite step that likely contains at least two sub-steps: an `INLINE` step to map the input data to the Shopify API request, and an `API` step to make the actual call to the Shopify `getOrders` endpoint.
    -   **Next Step:** `createSpreadsheet`

3.  **`createSpreadsheet`**
    -   **Type:** `COMPOSITE`
    -   **Purpose:** To create a new spreadsheet in Google Sheets.
    -   **Logic:** Similar to the previous step, this composite step will have an `INLINE` mapping step and an `API` step to call the Google Sheets `createSpreadsheet` endpoint. The `title` of the spreadsheet is taken from the `sheetTitle` variable defined in the first step.
    -   **Next Step:** `CreateTableOrders`

4.  **`CreateTableOrders`**
    -   **Type:** `INTERNAL_DB`
    -   **Purpose:** To create a table in the internal database to store order information.
    -   **Logic:** It executes a `CREATE TABLE IF NOT EXISTS` SQL statement to ensure the `orders` table exists.
    -   **Next Step:** `loopOverOrders`

5.  **`loopOverOrders`**
    -   **Type:** `LOOP`
    -   **Purpose:** To iterate over the list of orders fetched from Shopify.
    -   **Logic:** The `loopOver` field is set to `{{data.steps.getOrders.output.orders}}`, which is the array of orders returned by the `getOrders` step. For each order in this array, it executes a series of sub-steps, starting with `flattenOrderDetails`.
    -   **Next Step (after loop):** `sendMessage`

    ### Inside the Loop:

    a.  **`flattenOrderDetails`**
        -   **Type:** `INLINE`
        -   **Purpose:** To transform the complex, nested order object into a flat array of values suitable for a spreadsheet row.
        -   **Logic:** A Javascript `handler` function extracts the required fields from the order object (`loopOverItem`) and returns a `flattenedRow` array. It also sets a `flag` to `false` if the order's `financial_status` is "paid".
        -   **Next Step:** `Switch`

    b.  **`Switch`**
        -   **Type:** `CONDITIONAL`
        -   **Purpose:** To check if the order has been paid.
        -   **Logic:** It checks the value of the `flag` from the previous step. If the flag is `false` (meaning the order is paid), it proceeds to the `appendSheet` step. Otherwise, it goes to the `InsertTableOrders` step.

    c.  **`appendSheet`**
        -   **Type:** `COMPOSITE`
        -   **Purpose:** To append the flattened order data to the Google Sheet.
        -   **Logic:** This composite step calls the Google Sheets `appendSheet` endpoint, passing the `flattenedRow` to be inserted.
        -   **Next Step:** This is the end of the conditional branch. The loop will continue with the next item.

    d.  **`InsertTableOrders`**
        -   **Type:** `INTERNAL_DB`
        -   **Purpose:** To insert the flattened order data into the internal database.
        -   **Logic:** It executes an `INSERT` SQL statement, mapping the values from the `flattenedRow` array to the columns of the `orders` table.
        -   **Next Step:** This is the end of the conditional branch. The loop will continue with the next item.

6.  **`sendMessage`**
    -   **Type:** `COMPOSITE`
    -   **Purpose:** To send a notification message to Slack.
    -   **Logic:** This composite step calls the Slack `sendMessage` endpoint with a predefined message.
    -   **Next Step:** `Success`

7.  **`Success`**
    -   **Type:** `INLINE`
    -   **Purpose:** To return a final success message.
    -   **Logic:** It returns a simple JSON object: `{"message": "Success"}`.
    -   **Next Step:** `null` (This is the end of the flow).

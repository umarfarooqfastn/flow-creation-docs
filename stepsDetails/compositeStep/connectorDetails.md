# Connector Details

This file provides details for the available connectors.

## Bigcommerce
- **Group ID:** `_knexa_c866d6f4-9ca4-40f5-9af5-5c54a9c5b4f3`
- **Details File:** `./Bigcommerce.json`
- **Endpoints:** `getChannels`, `getChannel`, `createChannel`, `updateChannel`, `getChannelActiveTheme`, `getChannelsCurrencyAssignments`, `getCustomers`, `createCustomer`, `getCategoryTrees`, `upsertCategoryTree`, `getCategories`, `createCategories`, `updateCategories`, `deleteCatagoryTree`, `deleteCategories`, `createProduct`, `getACategoryTree`, `updateProduct`, `getBrands`, `createBrand`, `getWebhooks`, `createWebhook`, `deleteWebhook`, `getWebhook`, `getProduct`, `deleteProduct`, `getProducts`, `getProductBySku`

## Shopify

- **Group ID:** `_knexa_2fc3b972-2f75-49d4-8cce-3a11a5990408`
- **Details File:** `./shopifyConnectors.json`
- **Endpoints:** `getProducts`, `updateVariants`, `getVariant`, `createBasicProduct`, `updateBasicProduct`, `getProductsCount`, `createWebhook`, `registerWebhook`, `getWebhooks`, `deleteWebhook`, `getAccessToken`, `updateOrder`, `getLocations`, `getInventoryLevels`, `getInventoryItems`, `getBulkInventory`, `getFulfillmentOrder`, `moveFulfillmentOrder`, `createFulfillment`, `getOrders`, `getProductsGraphQL`, `createStagedUploadURL`, `bulkCreateProducts`, `createProduct`, `createVariant`, `updateProduct`, `getProductByHandle`, `deleteProduct`, `getProduct`, `setInventoryLevel`, `updateInventoryItem`

## Acumatica

- **Group ID:** `_knexa_7e87c3fe-4ddf-4a79-a12e-0da07cccbfc3`
- **Details File:** `./acumaticaConnectors.json`
- **Endpoints:** `getRecords`, `createSalesOrder`, `createStockItem`, `generateToken`, `getTables`, `getMetaDataOfTables`, `deleteSalesOrder`, `deleteStockItem`, `getSaleOrder`, `getSalesOrders`, `getStockItem`, `getStockItems`, `createContact`, `createLead`, `createOpportunity`, `deleteContact`, `deleteLead`, `deleteOpportunity`, `getContact`, `getContacts`, `getCustomers`, `getEntities`, `getLead`, `getLeads`, `getOpportunities`, `getOpportunity`, `login`, `logout`

## Gmail

- **Group ID:** `5743b46c-38a0-418f-84fa-8ed18198f72e`
- **Details File:** `./gmailConnectors.json`
- **Endpoints:** `sendMail`, `getMails`, `getMail`, `getMailAttachments`

## Slack

- **Group ID:** `_knexa_c9085d88-85d0-4436-82c6-4e42d6aba4c6`
- **Details File:** `./slackConnectors.json`
- **Endpoints:** `sendMessage`

## How to retrieve endpoint data

To retrieve the full details for a specific endpoint, an AI can use the `get_endpoint_details.py` script located in this directory.

**Usage:**

The script supports two usage patterns:

1. **Search all connectors** (will prompt if multiple matches found):
```bash
python3 get_endpoint_details.py <endpoint_name>
```

2. **Search specific connector** (recommended when endpoint names conflict):
```bash
python3 get_endpoint_details.py <endpoint_name> <connector_file.json>
```

**Examples:**

1. Search for `sendMessage` in all connectors:
```bash
python3 get_endpoint_details.py sendMessage
```

2. Get `getProducts` specifically from Shopify connector:
```bash
python3 get_endpoint_details.py getProducts shopifyConnectors.json
```

3. Get `getProducts` specifically from Bigcommerce connector:
```bash
python3 get_endpoint_details.py getProducts Bigcommerce.json
```

**Important:** Since endpoint names like `getProducts` exist in multiple connectors (Shopify, Bigcommerce), it's recommended to specify the connector file to avoid ambiguity.

The script will output the complete JSON object for that endpoint, which can then be parsed and used.

## How to generate UI Code

To generate the `uiCode` for a specific endpoint, an AI can use the `generate_uicode.py` script located in this directory.

**Usage:**

The script supports two usage patterns:

1. **Search all connectors** (will use first match found):
```bash
python3 generate_uicode.py <endpoint_name>
```

2. **Search specific connector** (recommended when endpoint names conflict):
```bash
python3 generate_uicode.py <endpoint_name> <connector_file.json>
```

**Examples:**

1. Generate UI code for `sendMessage` from any connector:
```bash
python3 generate_uicode.py sendMessage
```

2. Generate UI code for `getProducts` specifically from Shopify:
```bash
python3 generate_uicode.py getProducts shopifyConnectors.json
```

3. Generate UI code for `getProducts` specifically from Bigcommerce:
```bash
python3 generate_uicode.py getProducts Bigcommerce.json
```

**Important:** Since endpoint names like `getProducts` exist in multiple connectors, it's recommended to specify the connector file to ensure you get the UI code for the correct endpoint.

The script will output the complete `uiCode` JSON object for that endpoint, which can then be used for mapping in a flow.

## Available Connector Files

For reference, here are the available connector JSON files:
- `shopifyConnectors.json` - Shopify connector endpoints
- `Bigcommerce.json` - Bigcommerce connector endpoints  
- `acumaticaConnectors.json` - Acumatica connector endpoints
- `gmailConnectors.json` - Gmail connector endpoints
- `slackConnectors.json` - Slack connector endpoints
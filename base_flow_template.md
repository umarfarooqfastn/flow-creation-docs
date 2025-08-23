
# Base Flow Template

This template provides a high-level overview of a base flow, based on the structure of `base_flow.json`.

## Flow Details

- **ID:** `shoppifyOrdersToGoogleSheet`
- **Name:** `shoppifyOrdersToGoogleSheet`
- **Description:** `Not provided`
- **Action Type:** `READ`
- **Version:** `1.0.1`
- **Status:** `DEPLOYED`
- **Resource Type:** `EXTERNAL`
- **Created By:** `GenAIDeveloper`

## Flow Structure

A flow is composed of a series of steps that are executed in a specific order. The `resolver` property in the JSON defines the sequence of these steps.

### Trigger

The flow can be triggered in various ways, such as through an API request or a schedule. The `metaData` in the flow definition contains information about the trigger type and other invocation details.

### Steps

The `steps` array within the `resolver` contains the detailed configuration for each step in the flow. These steps can be of various types, including:

- **COMPOSITE:** A collection of other steps.
- **INLINE:** A step that executes a piece of code (e.g., JINJA, JAVASCRIPT).
- **API:** A step that makes an API call to an external service.
- **LOOP:** A step that iterates over a list of items.
- **CONDITIONAL:** A step that executes different branches based on a condition.
- **VARIABLE:** A step that defines or modifies variables.
- **INTERNAL_DB:** A step that interacts with an internal database.

For the complete and detailed configuration of each step, please refer to the `base_flow.json` file.

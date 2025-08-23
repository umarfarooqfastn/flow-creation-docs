### Switch Step

**Whats is Switch step**
- Switch step is basically condition base step of comparing , evaluating and checking kind of **IF ElseIF ELSE** we use in Code

**Available Conditions in Switch Step**
-In same Directory Read detailsSwitchCases.json.
-In This Flow All of the conditions are handled equals , not equals and much more.
-There are Below success steps i have added as well so how the next step will be not under all of the cases but some of the cases to understand how next step will be added.

**Usage of Switch Step**
- Switch Step is used to switch between the steps
- what ever the condition will be true it next step will be executed based on that condition

**Detail Information for Switch**
- Available here `./detailsSwitchCases.json`

**Formating of Switch Step**
{
"type": "CONDITIONAL",
"id": "Switch",
"actionId": null,
"inline": null,
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
"conditional": {
    "id": "Switch",
    "next": "InsertTableOrders",
    "expressions": [
    {
        "name": "ifPaid",
        "logic": "AND",
        "conditions": null,
        "variable": "{{data.steps.flattenOrderDetails.output.flag}}",
        "value": "false",
        "operation": "EQ_IGNORE_CASE",
        "next": "appendSheet"
    }
    ],
    "queryExecutor": {
    "children": [
        {
        "key": {
            "type": "java.lang.String",
            "value": "data"
        },
        "value": {
            "children": [
            {
                "key": {
                "type": "java.lang.String",
                "value": "steps"
                },
                "value": {
                "children": [
                    {
                    "key": {
                        "type": "java.lang.String",
                        "value": "flattenOrderDetails"
                    },
                    "value": {
                        "children": [
                        {
                            "key": {
                            "type": "java.lang.String",
                            "value": "output"
                            },
                            "value": {
                            "children": [
                                {
                                "key": {
                                    "type": "java.lang.String",
                                    "value": "flag"
                                },
                                "value": {
                                    "children": [],
                                    "returnLiteral": true,
                                    "symbolOrIndex": {
                                    "type": "java.lang.String",
                                    "value": "flag"
                                    },
                                    "version": 2
                                }
                                }
                            ],
                            "returnLiteral": false,
                            "symbolOrIndex": {
                                "type": "java.lang.String",
                                "value": "output"
                            },
                            "version": 2
                            }
                        }
                        ],
                        "returnLiteral": false,
                        "symbolOrIndex": {
                        "type": "java.lang.String",
                        "value": "flattenOrderDetails"
                        },
                        "version": 2
                    }
                    }
                ],
                "returnLiteral": false,
                "symbolOrIndex": {
                    "type": "java.lang.String",
                    "value": "steps"
                },
                "version": 2
                }
            }
            ],
            "returnLiteral": false,
            "symbolOrIndex": {
            "type": "java.lang.String",
            "value": "data"
            },
            "version": 2
        }
        }
    ],
    "returnLiteral": false,
    "symbolOrIndex": {
        "type": "null",
        "value": null
    },
    "version": 2
    }
},
"lambdaFunction": null,
"outputSchema": null,
"next": "InsertTableOrders",
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

**Complete Examples:**

See these example flows in `../../flowExamples/` that demonstrate conditional/switch steps:

- **`shoppifyOrdersToGoogleSheet.json`**: Payment status checking (paid vs unpaid orders) with [detailed explanation](../../flowExamples/explanation_of_Shopify_OrdersToGoogleSheet.md)  
- **`ComplexFlowWithMappingsAndCustomerUsecase.json`**: Advanced conditional logic with multiple branching scenarios
- **`flow_with_looping_example.json`**: Conditional processing within loop iterations

All examples show proper condition expressions, variable references, and branching logic.
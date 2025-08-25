# Lambda Step (LAMBDA with PYTHON) 🐍

**Lambda Steps** are **LAMBDA** steps that execute **Python code** in a serverless environment for complex processing, data transformation, and custom business logic that goes beyond simple data mapping.

## 🎯 **Purpose**
Lambda Steps are used to:
- **Execute complex Python algorithms** and business logic
- **Integrate with external Python libraries** (JWT, MongoDB, Google Cloud, OpenAI, etc.)
- **Perform advanced data processing** that requires computational power
- **Handle authentication and security operations** (token verification, encryption)
- **Connect to databases and external services** using Python clients
- **Process large datasets** with Python's data processing capabilities

## ⚙️ **Essential Requirements for Lambda Steps**

### **1. Step Type Configuration**
```json
{
  "type": "LAMBDA",
  "id": "processWithPython",
  "lambdaFunction": {
    "code": "Python code here",
    "language": "PYTHON",
    "version": 2,
    "next": "nextStepId",
    "queryExecutor": {},
    "validation": {
      "validData": true,
      "reason": null,
      "valid": false,
      "queryExecutor": null
    }
  }
}
```

### **2. Required Function Structure**
**CRITICAL**: All Lambda steps must define a `fastn_function(params)` function:
```python
def fastn_function(params):
    # Your Python logic here
    result = {"status": "success", "data": "processed"}
    return result
```

### **3. Data Access Pattern**
```python
# Access input data
input_data = params["data"]["input"]

# Access headers
auth_header = params["data"]["headers"]["authorization"]

# Access secrets/credentials
api_key = params["data"]["secrets"]["api_key"]
db_connection = params["data"]["secrets"]["mongodb_url"]

# Access data from previous steps
previous_result = params["data"]["steps"]["previousStepId"]["output"]
```

## 📚 **Available Python Libraries**

### **✅ Standard Python Libraries** (Always Available)
```python
import json          # JSON processing
import datetime      # Date/time operations
import re            # Regular expressions
import base64        # Base64 encoding/decoding
import hashlib       # Hashing functions
import uuid          # UUID generation
import urllib        # URL operations
import time          # Time operations
import os            # Operating system interface
import math          # Mathematical functions
import random        # Random number generation
```

### **✅ Data Processing Libraries**
```python
import pandas        # Data analysis and manipulation
import numpy         # Numerical computing
import csv           # CSV file operations
```

### **✅ HTTP & API Libraries**
```python
import requests      # HTTP library for API calls
import urllib3       # Advanced HTTP library
```

### **✅ Authentication & Security**
```python
import jwt           # PyJWT for JWT tokens
import cryptography  # Cryptographic recipes and primitives
import bcrypt        # Password hashing
```

### **✅ Database Clients**
```python
import pymongo       # MongoDB client
import psycopg2      # PostgreSQL client
import mysql         # MySQL client
import redis         # Redis client
```

### **✅ Cloud Platform Libraries**
```python
# Google Cloud Platform
from google.cloud import storage
from google.cloud import firestore
from google.cloud import bigquery

# AWS Libraries
import boto3         # AWS SDK

# Azure Libraries  
from azure.storage.blob import BlobServiceClient
```

### **✅ AI & Machine Learning**
```python
import openai        # OpenAI API client
import anthropic     # Anthropic API client (Claude)
import tiktoken      # OpenAI tokenizer
```

### **✅ Specialized Libraries**
```python
import xml           # XML processing
import yaml          # YAML processing
import pillow        # Image processing (PIL)
import openpyxl      # Excel file operations
```

## 🏗️ **Lambda Step Structure**

```json
{
  "type": "LAMBDA",
  "id": "pythonProcessingStep",
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
  "conditional": null,
  "lambdaFunction": {
    "code": "def fastn_function(params):\n    # Your Python code here\n    return {\"result\": \"success\"}",
    "next": "nextStepId",
    "validation": {
      "validData": true,
      "reason": null,
      "valid": false,
      "queryExecutor": null
    },
    "language": "PYTHON",
    "version": 2,
    "queryExecutor": {
      "children": [],
      "returnLiteral": false,
      "symbolOrIndex": {
        "type": "null",
        "value": null
      },
      "version": 2
    }
  },
  "outputSchema": null,
  "next": null,
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
```

## 📝 **Common Lambda Patterns**

### **1. JWT Token Verification**
```python
import jwt
from jwt import InvalidTokenError

def fastn_function(params):
    auth_header = params["data"]["headers"]["authorization"]
    if not auth_header.startswith('Bearer '):
        return {"error": "Missing or invalid Authorization header"}

    token = auth_header.replace('Bearer ', '')
    client_secret = params["data"]["secrets"]["jwt_secret"]

    try:
        payload = jwt.decode(token, client_secret, algorithms=['HS256'])
        return {
            "status": "success",
            "user_id": payload.get('user_id'),
            "email": payload.get('email')
        }
    except InvalidTokenError as e:
        return {"error": f"Token verification failed: {str(e)}"}
```

### **2. Database Operations**
```python
import pymongo
import json

def fastn_function(params):
    # Connect to MongoDB
    connection_string = params["data"]["secrets"]["mongodb_url"]
    client = pymongo.MongoClient(connection_string)
    db = client.get_database("your_database")
    collection = db.get_collection("your_collection")
    
    # Get input data
    input_data = params["data"]["input"]
    
    try:
        # Insert document
        result = collection.insert_one(input_data)
        return {
            "status": "success",
            "inserted_id": str(result.inserted_id)
        }
    except Exception as e:
        return {"error": f"Database operation failed: {str(e)}"}
    finally:
        client.close()
```

### **3. OpenAI Integration**
```python
import openai
import json

def fastn_function(params):
    # Configure OpenAI
    openai.api_key = params["data"]["secrets"]["openai_api_key"]
    
    # Get input data
    user_prompt = params["data"]["input"]["prompt"]
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1000
        )
        
        return {
            "status": "success",
            "response": response.choices[0].message.content,
            "usage": response.usage
        }
    except Exception as e:
        return {"error": f"OpenAI API call failed: {str(e)}"}
```

### **4. Data Processing & Analysis**
```python
import pandas as pd
import json

def fastn_function(params):
    # Get array data from previous step
    raw_data = params["data"]["steps"]["fetchDataStep"]["output"]["items"]
    
    try:
        # Convert to DataFrame
        df = pd.DataFrame(raw_data)
        
        # Perform data analysis
        summary = {
            "total_records": len(df),
            "average_price": df['price'].mean() if 'price' in df.columns else 0,
            "categories": df['category'].value_counts().to_dict() if 'category' in df.columns else {}
        }
        
        # Filter and transform data
        processed_data = df[df['status'] == 'active'].to_dict('records')
        
        return {
            "status": "success",
            "summary": summary,
            "processed_data": processed_data
        }
    except Exception as e:
        return {"error": f"Data processing failed: {str(e)}"}
```

### **5. External API Integration**
```python
import requests
import json

def fastn_function(params):
    # Get API credentials
    api_key = params["data"]["secrets"]["external_api_key"]
    base_url = "https://api.external-service.com"
    
    # Get input parameters
    user_id = params["data"]["input"]["user_id"]
    
    try:
        # Make API call
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            f"{base_url}/users/{user_id}",
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            return {
                "status": "success",
                "user_data": response.json()
            }
        else:
            return {
                "error": f"API call failed with status {response.status_code}",
                "details": response.text
            }
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
```

## 🔧 **Best Practices for Lambda Steps**

### **✅ DO:**
- **Always define `fastn_function(params)`** as the main entry point
- **Use proper error handling** with try-catch blocks
- **Return consistent JSON structures** with status indicators
- **Access secrets securely** via `params["data"]["secrets"]`
- **Use appropriate libraries** from the available list
- **Include timeout handling** for external API calls
- **Close database connections** in finally blocks
- **Return meaningful error messages** for debugging

### **❌ DON'T:**
- Don't hardcode credentials or API keys in the code
- Don't use undefined/unavailable Python libraries
- Don't skip error handling for external operations
- Don't return Python objects (return JSON-serializable data)
- Don't forget to handle network timeouts
- Don't leave database connections open
- Don't use blocking operations without timeouts

## 🎯 **When to Use Lambda Steps**

✅ **Use Lambda Steps for:**
- **Complex business logic** requiring Python algorithms
- **JWT token verification** and authentication processing
- **Database operations** (MongoDB, PostgreSQL, MySQL)
- **AI/ML integrations** (OpenAI, Anthropic APIs)
- **Data analysis** and statistical processing
- **External API integrations** requiring complex logic
- **File processing** and data transformation
- **Cryptographic operations** and security functions

❌ **Don't Use Lambda Steps for:**
- **Simple data mapping** (use INLINE steps instead)
- **Basic API calls** (use COMPOSITE steps instead)
- **Simple conditional logic** (use CONDITIONAL steps instead)
- **Variable assignments** (use VARIABLE steps instead)

## 📊 **Data Access Patterns**

```python
def fastn_function(params):
    # Input data from the flow
    input_data = params["data"]["input"]
    
    # Headers from HTTP request
    headers = params["data"]["headers"]
    auth_token = headers.get("authorization", "")
    
    # Secrets/credentials
    secrets = params["data"]["secrets"]
    db_url = secrets.get("database_url")
    api_key = secrets.get("api_key")
    
    # Data from previous steps
    previous_step_data = params["data"]["steps"]["previousStepId"]["output"]
    
    # Loop iteration data (if inside a LOOP step)
    loop_item = params["data"]["parent"]["loopOverItem"]
    
    return {"processed": True}
```

## 🚨 **Critical Requirements**

1. **Function Name**: Must be exactly `fastn_function(params)`
2. **Return Value**: Must be JSON-serializable (dict, list, str, int, bool, None)
3. **Error Handling**: Always include try-catch for external operations
4. **Library Usage**: Only use libraries from the available list
5. **Security**: Never hardcode secrets, always use `params["data"]["secrets"]`
6. **Performance**: Include timeouts for external calls and database operations

## 📚 **Example Flows Using Lambda Steps**

**Relevant flows in `flowExamples/`:**
- `acumatica_bigComerce/tokenVerification.json` - JWT token verification example
- Look for flows with `"type": "LAMBDA"` for more examples

## 🔍 **Validation & Testing**

Always validate your Lambda steps with:
```bash
python3 flow_validator.py your_flow.json
```

The validator will check for:
- Proper Lambda step structure
- Required `lambdaFunction` fields
- Valid `queryExecutor` configuration
- Correct step connections and references

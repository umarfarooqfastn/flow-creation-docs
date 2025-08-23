import json
import re
import sys
import os

def get_endpoint_details(endpoint_name, connector_file=None):
    """
    Retrieves the details of a specific endpoint from the connector JSON files.

    Args:
        endpoint_name (str): The name of the endpoint to retrieve.
        connector_file (str, optional): The specific connector JSON file to search in.
                                       If None, searches all connector files.

    Returns:
        str: A JSON string containing the endpoint details, or an empty string if not found.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # If connector_file is provided, search only in that file
    if connector_file:
        json_file_path = os.path.join(script_dir, connector_file)
        if not os.path.exists(json_file_path):
            print(f"Error: {json_file_path} not found.")
            return ""
        
        return _search_endpoint_in_file(json_file_path, endpoint_name)
    
    # Otherwise, search in all connector files as before
    markdown_file_path = os.path.join(script_dir, 'connectorDetails.md')

    if not os.path.exists(markdown_file_path):
        print(f"Error: {markdown_file_path} not found.")
        return ""

    with open(markdown_file_path, 'r') as f:
        content = f.read()

    # Find the connector section that contains the endpoint
    found_endpoints = []
    for section in content.split('## '):
        if f"- **Endpoints:**" in section and endpoint_name in section:
            # Extract the JSON file path
            match = re.search(r'- \*\*Details File:\*\* `\./(.*)`', section)
            connector_name_match = re.search(r'^([^\n]+)', section.strip())
            
            if match and connector_name_match:
                json_file_name = match.group(1)
                connector_name = connector_name_match.group(1)
                json_file_path = os.path.join(script_dir, json_file_name)

                if not os.path.exists(json_file_path):
                    print(f"Error: {json_file_path} not found.")
                    continue

                result = _search_endpoint_in_file(json_file_path, endpoint_name, return_data=True)
                if result:
                    found_endpoints.append({
                        'connector': connector_name,
                        'file': json_file_name,
                        'data': result
                    })

    if len(found_endpoints) == 0:
        print(f"Endpoint '{endpoint_name}' not found in any connector.")
        return ""
    elif len(found_endpoints) == 1:
        print(json.dumps(found_endpoints[0]['data'], indent=2))
        return ""
    else:
        print(f"Multiple connectors found with endpoint '{endpoint_name}':")
        for i, ep in enumerate(found_endpoints):
            print(f"{i+1}. {ep['connector']} (file: {ep['file']})")
        print(f"\nPlease specify the connector file using:")
        print(f"python3 get_endpoint_details.py {endpoint_name} <connector_file.json>")
        return ""

def _search_endpoint_in_file(json_file_path, endpoint_name, return_data=False):
    """
    Search for an endpoint in a specific JSON file.
    
    Args:
        json_file_path (str): Path to the JSON file to search
        endpoint_name (str): Name of the endpoint to find
        return_data (bool): If True, return the data instead of printing
    
    Returns:
        dict or None: Endpoint data if found and return_data=True, otherwise None
    """
    try:
        with open(json_file_path, 'r') as jf:
            data = json.load(jf)
            for item in data:
                # The slackConnectors.json has a different structure
                if 'node' in item:
                    if item['node']['name'] == endpoint_name:
                        if return_data:
                            return item
                        else:
                            print(json.dumps(item, indent=2))
                            return True
                else:
                    if 'name' in item and item['name'] == endpoint_name:
                        if return_data:
                            return item
                        else:
                            print(json.dumps(item, indent=2))
                            return True
    except Exception as e:
        print(f"Error reading {json_file_path}: {e}")
        
    return None

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage:")
        print("  python3 get_endpoint_details.py <endpoint_name>")
        print("  python3 get_endpoint_details.py <endpoint_name> <connector_file.json>")
        print("\nExamples:")
        print("  python3 get_endpoint_details.py sendMessage")
        print("  python3 get_endpoint_details.py getProducts shopifyConnectors.json")
        sys.exit(1)

    endpoint_name_to_find = sys.argv[1]
    connector_file = sys.argv[2] if len(sys.argv) == 3 else None
    get_endpoint_details(endpoint_name_to_find, connector_file)
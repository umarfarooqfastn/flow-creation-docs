import json
import sys
import subprocess
import os

def get_endpoint_details(endpoint_name, connector_file=None):
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'get_endpoint_details.py')
    cmd = ['python3', script_path, endpoint_name]
    if connector_file:
        cmd.append(connector_file)
        
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"Error getting endpoint details: {result.stderr}")
        return None
    
    if not result.stdout.strip():
        print(f"No endpoint data returned for '{endpoint_name}'")
        return None
        
    return json.loads(result.stdout)

def generate_ui_code_from_schema(schema, path_prefix=""):
    target = {}
    if "properties" in schema:
        for key, prop in schema["properties"].items():
            current_path = f"{path_prefix}.{key}" if path_prefix else key
            target[key] = {
                "actionType": "map",
                "target": "",
                "targetType": prop.get("type", "string"),
                "actions": [],
                "enum": prop.get("enum", []),
                "title": prop.get("title", ""),
                "description": prop.get("description", ""),
                "isRequred": key in schema.get("required", []),
                "default": prop.get("default", ""),
                "autoEscape": "MANUAL",
                "selected": False,
                "byUser": False,
                "path": current_path,
                "field": path_prefix,
                "position": current_path.split('.'),
                "key": key
            }
            if prop.get("type") == "object":
                target[key]["target"] = generate_ui_code_from_schema(prop, current_path)["target"]
            elif prop.get("type") == "array":
                if "items" in prop and prop["items"].get("type") == "object":
                     target[key]["items"] = generate_ui_code_from_schema(prop["items"], current_path)


    return {"actionType": "map", "target": target, "targetType": "object"}


def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage:")
        print("  python3 generate_uicode.py <endpoint_name>")
        print("  python3 generate_uicode.py <endpoint_name> <connector_file.json>")
        print("\nExamples:")
        print("  python3 generate_uicode.py sendMessage")
        print("  python3 generate_uicode.py getProducts shopifyConnectors.json")
        sys.exit(1)

    endpoint_name = sys.argv[1]
    connector_file = sys.argv[2] if len(sys.argv) == 3 else None
    endpoint_details = get_endpoint_details(endpoint_name, connector_file)

    if not endpoint_details:
        sys.exit(1)

    try:
        if 'node' in endpoint_details:
            request_schema_str = endpoint_details['node']['contract']['action']['request']['schema']
        else:
            request_schema_str = endpoint_details['contract']['action']['request']['schema']

        request_schema = json.loads(request_schema_str)
        ui_code = generate_ui_code_from_schema(request_schema)
        print(json.dumps(ui_code, indent=2))
        
    except KeyError as e:
        print(f"Error: Missing required field in endpoint details: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in schema: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

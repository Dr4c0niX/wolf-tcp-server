import json

def parse_request(data):
    try:
        return json.loads(data) if isinstance(data, str) else None
    except json.JSONDecodeError:
        return None

def format_response(status, data):
    return json.dumps({
        "status": status,
        "response": data
    }, ensure_ascii=False)
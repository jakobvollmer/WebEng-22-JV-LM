from jsonschema import validate
import json

RESERVATION = {
    "type": "object",
    "properties": {
        "id": {"type": "string", "minLength":1},
        "from": {"type": "string", "minLength":1},
        "to": {"type": "string", "minLength":1},
        "room_id": {"type": "string", "minLength":1},
    },
    "required": ["id", "from", "to", "room_id"],
}

def isValid (instance:json, schema:json) -> bool:
    try:
        validate(instance=instance, schema=schema)
        return True
    except Exception as e:
        return False
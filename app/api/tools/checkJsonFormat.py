from jsonschema import validate
import json

from api import errors

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

def check (instance:json, schema:json) -> None:
    try:
        validate(instance=instance, schema=schema)
        return
    except Exception as e:
        raise errors.MismatchingJsonObject(e)

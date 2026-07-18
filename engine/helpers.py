import json


def resolve_reference_alias(name: str) -> list[str]:
    try:
        with open("engine/config/reference_dataset.json", "r") as f:
            data = json.load(f)
            return data.get(name, [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def map_field(label: str, profile: dict[str, str]) -> str | None:
    normalized = label.lower()
    for key, value in profile.items():
        if key.replace("_", " ") in normalized:
            return value
    return None


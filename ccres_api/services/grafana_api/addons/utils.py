from typing import Dict, Any

def clean_none(d:Dict[Any,Any])-> Dict[Any,Any]:
    cleaned_d = {}
    for key, value in d.items():
        if value is None:
            continue
        cleaned_d[key] = value
    return cleaned_d

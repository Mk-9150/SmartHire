from typing import Any
import json

def parse_cors(v:Any)->list[str] | str :
    if isinstance(v, str) and not v.startswith("[") :
        return [v.strip() for v in v.split(",")]
    elif isinstance(v,list | str):
        return v
    raise ValueError(v)


def load_json_error(error_message:Any):
    details=json.loads(error_message.text)
    errorDetail=details.get("detail")
    return errorDetail
    
    
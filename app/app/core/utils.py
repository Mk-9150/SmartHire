from typing import Any 

def parse_cors(cors:str):
    
    if isinstance(cors,str) and not cors.startswith("["):
        return [origin.strip() for origin in cors.split(",") ]
    elif isinstance(cors,list | str):
        return cors
    
    raise ValueError(v)


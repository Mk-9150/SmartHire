from typing import Any


# def parse_cors(v:Any):
def parse_cors(v:str):
    ...
    if isinstance(v,str) and not v.startswith("["):
        ...
        return [cor.strip() for cor in v.split(",")]
    elif isinstance(v,list | str) :
        ...
        return v
        
    return ValueError(e)         
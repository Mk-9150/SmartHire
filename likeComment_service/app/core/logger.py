import logging
import logging.config
from typing import Any
def Logger_Config(module:Any):
    ...
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s -  %(name)s   -  [%(levelname)s] -  %(message)s",
     )
    
    return logging.getLogger(module)
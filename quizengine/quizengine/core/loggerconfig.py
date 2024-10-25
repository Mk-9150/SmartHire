import logging 

def loggerconfigu(module):
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s -  %(name)s   -  [%(levelname)s] -  %(message)s",
    )
    
    return logging.getLogger(module)
from fastapi import Depends , HTTPException , status
from app.core.db_setting import engine
from sqlmodel import Session
from typing import Annotated
from aiokafka import AIOKafkaProducer
from app.core.app_setting import setting

def SDependency():
    ...
    with Session(engine) as session:
        yield session
        
        
SessionDependency = Annotated[Session, Depends(SDependency)]



async def producerDependency():
    ...
    producer=AIOKafkaProducer(bootstrap_servers=setting.BOOTSTRAP_SERVER_KAFKA_URL)
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()
        
L_producer=Annotated[AIOKafkaProducer,Depends(producerDependency)]        

    
    
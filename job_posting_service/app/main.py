from fastapi import FastAPI 
from fastapi.responses import RedirectResponse
from sqlmodel import SQLModel
from app.models import model
from app.core.db_settings import engine
from contextlib import  asynccontextmanager

def create_Table():
   SQLModel.metadata.create_all(engine)  


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Starting Application")
    # create_Table()
    yield
    print("Shutting down")
    
app = FastAPI(lifespan=lifespan)

# alembic revision --autogenerate -m "Create a baseline migrations"
@app.get("/")
def pushToDocs()->RedirectResponse:
    return RedirectResponse(url="/docs")


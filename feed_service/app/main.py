from fastapi import FastAPI 

app:FastAPI = FastAPI()


@app.get("/")
def home():
    return "feed service"
from fastapi import FastAPI#Python class that provides all the functionality for your API
from routes.driver import router as DriverRouter

app = FastAPI() #FastAPI instance
app.include_router(DriverRouter, tags=["Driver"], prefix="/drivers")

@app.get("/")
def root() -> dict:
    return {"message": "Hello world"}
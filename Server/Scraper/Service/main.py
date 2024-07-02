from fastapi import FastAPI

from controllers import ServiceController
from routes import router

app = FastAPI()
controller = ServiceController()
app.include_router(router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Task API!"}

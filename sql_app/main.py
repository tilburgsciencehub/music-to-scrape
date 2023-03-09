# Import FastAPI
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import api

# Initialize the app
app = FastAPI()

app.include_router(api.router)
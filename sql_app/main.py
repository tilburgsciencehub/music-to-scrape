# Import FastAPI
from fastapi import FastAPI
import api

# Initialize the app
app = FastAPI(docs_url=None, redoc_url="/docs")

app.include_router(api.router)
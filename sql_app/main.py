# Import FastAPI
from fastapi import FastAPI
import api

# Initialize the app docs_url=None, redoc_url="/docs"
app = FastAPI()

app.include_router(api.router)
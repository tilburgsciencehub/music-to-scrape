# Import FastAPI
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import api
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi

# Initialize the app
app = FastAPI(docs_url=None, redoc_url="/docs")

app.include_router(api.router)

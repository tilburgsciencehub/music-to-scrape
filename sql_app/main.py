# Import FastAPI
from fastapi import FastAPI
import api
import uvicorn

# Initialize the app docs_url=None, redoc_url="/docs"
app = FastAPI()

app.include_router(api.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the API of Music-to-scrape"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
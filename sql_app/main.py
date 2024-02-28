# Import FastAPI
from fastapi import FastAPI
import api
import uvicorn


description = """
Music to Scrape API helps you to learn how to extract data from the internet. It essentially mimicks data available at music streaming services, but... be aware: we are a sandbox site without real data.
Curious what our data looks like? Then head over to our website to see our "sandbox" music streaming service in action.  🚀

## Endpoints

- You can query various endpoints for __users__ (e.g., a list of users, a user's demographic information, a user's listening history) and __artists__ (e.g., an artist's top songs).
- In addition, we serve several __feeds__ that are shown on the landing page, such as __weekly charts__ (e.g., for artists, songs), and lists of __featured artists__ and __recently active users__.

## Access to the API

Our API is freely accessible, which means you do not have to authenticate with the API but can just readily use all of the endpoints.

## Visit our website

In case you haven't done so, visit our website at [https://music-to-scrape.org]() to see our mock front end and learn more about this project.


"""

# Initialize the app docs_url=None, redoc_url="/docs"
app = FastAPI(description = description, title = "Music To Scrape API", version = '0.11', docs_url=None, redoc_url="/docs",
              contact = {"name": "Hannes Datta",
                         "url": "https://hannesdatta.com",
                         "email": "h.datta@tilburguniversity.edu"}
              )

app.include_router(api.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the API of Music-to-scrape"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
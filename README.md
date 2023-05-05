# APIs to scrape

A mock-up API of a music streaming service so you can learn how web scraping and APIs work.

## Getting started

We'll post a link to the website and API here eventually.

## Running this project on your own server

- Install required Python packages

```
pip install fastapi
pip install fastapi_utils
pip install sqlalchemy
pip install pydantic
pip install uvicorn
pip install gunicorn
pip install flask
pip install flask_sqlalchemy
```

## How to start the API
- Clone repository locally
- Open terminal
- Go to the `sql_app` folder inside the repository
- Run the following command: `uvicorn main:app --port 8080`

## How to open the documentation;
If you want to check the documentation, you can go to following address when uvicorn is started: 
- `http://127.0.0.1:8080/docs`
- Uvicorn will show you which link is used when running the application.

## How to start the flask app
- Clone repository locally
- Open terminal
- Go to the `flask_app` folder inside the repository
- Run the following command: `gunicorn main:app --bind 127.0.0.1:8000
`


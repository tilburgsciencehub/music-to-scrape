# Music to scrape

We’re a fictitious music streaming service with a real website and API. Built for educational purposes, you can use us to learn web scraping! 

## Getting started

We'll post a link to the website and API here eventually.

## Running this project on your own computer/server

### Install packages and simulate data

- Clone this repository
- Ensure you have R installed, and run `simulate.R` in `src/simulate` to generate the ficitious data.
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

### Start the API
- Open terminal
- Go to the `fastapi` folder inside the repository
- Run the following command: `uvicorn main:app --port 8080`
  - If you want to the FastAPI connection, press Ctrl + C in the terminal to quit.
  - If you want to check the documentation, you can go to following address when uvicorn is started:
    - `http://127.0.0.1:8080/docs`
    - `uvicorn` will show you which link is used when running the application.

### Start the front end 
- Open terminal
- Go to the `flask_app` folder inside the repository
- Run the following command: `gunicorn main:app --bind 127.0.0.1:8000`
- If you want to the Flask connection, press Ctrl + c in the terminal to quit.

### How to change the data
- Open the `simulate.R` file within the `src/simulate` folder
- Make your adjustments
- Run the complete file top-down, and the databases will be updated.


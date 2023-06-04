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
- Run the following command: `gunicorn app:app --bind 127.0.0.1:8000`
- If you want to the Flask connection, press Ctrl + c in the terminal to quit.

### How to change the data
- Open the `simulate.R` file within the `src/simulate` folder
- Make your adjustments
- Run the complete file top-down, and the databases will be updated.

# Acknowledgements

- Raw data with song names used in simulating the data: https://github.com/mahkaila/songnames
- Photos
  - Landing page
    - Featured artist: A trumpet player from Caracas, Venezuela. Credits to [Ana Maria Arevalo Gosen for providing the photo](https://www.instagram.com/anitasinfiltro/).
    - Recently played & featured artists
      - https://picsum.photos/id/100/100/100
      - The images are released under the Unsplash license, which allows for free and unrestricted use, including commercial use, without requiring attribution (although attribution is appreciated).
     - Top 15
       - https://picsum.photos/id/237/50/50
       - License is same as above
     - Recent users:
       - Self-made icon
   - Song Page: No Pictures
   - Artist Page:
     - https://images.unsplash.com/photo-1605722243979-fe0be8158232
     - "Unsplash photos are made to be used freely. All photos can be downloaded and used for free for commercial and non-commercial purposes.             Attribution isn’t required"
    - User Page:
      -  Self-made icon

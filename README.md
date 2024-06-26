<img src="flask_app/static/images/logo.png" height="50">

# Music-to-scrape

We’re __music-to-scrape__, a fictitious music streaming service with a real website and API. Built for __educational purposes__, you can use us to __learn web scraping__! 

## Getting started

Head over to __[https://music-to-scrape.org]()__ to view our live website, or directly check out our __[API documentation](https://api.music-to-scrape.org/docs)__.

<img src="screenshot.png" alt="drawing" width="600"/>

## Running this project

### Using Docker

#### Starting up the frontend and backend

The easiest way to run our project is using Docker.

- [Install Docker](docs/install_docker.md) and clone this repository.
- Open the terminal at the repository's root directory and run the following commands: `docker compose build` and `docker compose up`.
- Wait a bit for the website and API to be launched. If the process breaks, you likely haven't allocated enough memory (e.g., the built takes about 6 GB of memory)
- Once docker has been launched, you can access the website and API locally at these addresses:
    - API: `http://localhost:8080` (whereby localhost typically is `127.0.0.1`)
    - Front end: `http://localhost:8000`
- Press Ctrl + C in the terminal to quit.

#### Configuring server for public access and HTTPS traffic

If you're running this project publicly, it's worthwhile configuring HTTPS access on your server. Following the [notes here](docs/server.md).

TLDR:

- If you have already built the image, it's enough to start it with `docker compose up -d`.
- If you want to rebuild, use `docker compose build` first.
- Unsure whether a docker container with the site is running already? Check with `docker ps`; stop unnecessary images using `docker stop IMAGEID`.

### Manual setup (i.e., not using Docker)

#### Install packages and simulate data

- Clone this repository
- Ensure you have R installed, and run `simulate.R` in `src/simulate` to generate the fictitious data.
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

#### Start the API
- Open terminal
- Go to the `sql_app` folder inside the repository
- Run the following command: `uvicorn main:app --port 8080`
  - If you want to the FastAPI connection, press Ctrl + C in the terminal to quit.
  - If you want to check the documentation, you can go to following address when uvicorn is started:
    - `http://127.0.0.1:8080/docs`
    - `uvicorn` will show you which link is used when running the application.

#### Start the front end 
- Open terminal
- Go to the `flask_app` folder inside the repository
- Run the following command: `gunicorn app:app --bind 127.0.0.1:8000`
- If you want to the Flask connection, press Ctrl + c in the terminal to quit.

#### Changing the data
- Open the `simulate.R` file within the `src/simulate` folder
- Make your adjustments
- Run the complete file top-down, and the databases will be updated.

# Acknowledgements

- Raw data with song names used in simulating the data: https://github.com/mahkaila/songnames
- Featured artist on the landing page: A trumpet player from Caracas, Venezuela. Credits to [Ana Maria Arevalo Gosen for providing the photo](https://www.instagram.com/anitasinfiltro/).
- Album art by [dicebear.com](https://dicebear.com), [thumbs](https://www.dicebear.com/styles/thumbs/) & [shapes](https://www.dicebear.com/styles/shapes/) libraries
- Avatars by [dicebear.com](https://dicebear.com), [avataars](https://www.dicebear.com/styles/avataaars/) library
  
  
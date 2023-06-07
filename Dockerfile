FROM continuumio/miniconda3

WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install -y libcurl4-openssl-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN conda update -n base -c defaults conda && \
    conda install -c conda-forge -c r r-base=4.1.3 r-data.table r-dbi r-rsqlite && \
    R -e "install.packages('curl', repos='http://cran.rstudio.com/')" && \
    pip install fastapi fastapi-utils sqlalchemy pydantic uvicorn gunicorn flask flask_sqlalchemy
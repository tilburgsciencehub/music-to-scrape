FROM continuumio/miniconda3 AS dependencies

RUN apt-get update && \
    apt-get install -y libcurl4-openssl-dev && \
    find /var/*/apt -type f -delete

RUN conda update -n base -c defaults conda && \
    conda install -c conda-forge -c r r-base=4.1.3 r-data.table r-dbi r-rsqlite && \
    R -e "install.packages('curl', repos='http://cran.rstudio.com/')" && \
    pip install fastapi fastapi-utils sqlalchemy pydantic uvicorn gunicorn flask flask_sqlalchemy

FROM dependencies AS final

COPY . /app
WORKDIR /app
RUN Rscript src/simulate/simulate.R

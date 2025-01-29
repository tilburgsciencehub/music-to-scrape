FROM continuumio/miniconda3:24.5.0-0 AS dependencies

RUN apt-get update && \
    apt-get install -y libcurl4-openssl-dev gcc python3-dev && \
    find /var/*/apt -type f -delete

RUN conda update -n base -c defaults conda && \
    conda install -c conda-forge -c r r-base=4.1.3 r-data.table=1.14.8 r-dbi=1.1.3 r-rsqlite=2.3.1 && \
    R -e "install.packages('curl', repos='http://cran.rstudio.com/')" && \
    pip install typing-inspect==0.9.0 fastapi==0.115.7 fastapi-utils==0.8.0 SQLAlchemy==1.4.54 pydantic==2.10.6 uvicorn==0.34.0 gunicorn==23.0.0 flask==3.1.0 flask_sqlalchemy==3.0.5

FROM dependencies AS final

COPY . /app
WORKDIR /app
RUN Rscript src/simulate/simulate.R

# Python version can be changed, e.g.
# FROM python:3.8
# FROM docker.io/fnndsc/conda:python3.10.2-cuda11.6.0
FROM docker.io/python:3.10.5-slim-buster

LABEL org.opencontainers.image.authors="FNNDSC <dev@babyMRI.org>" \
      org.opencontainers.image.title="COVIDnet-meta" \
      org.opencontainers.image.description="A ChRIS plugin that analyzes an upstream COVID prediction.json file and, if COVID infection inferred, will exit with an exception. This has the effect of coloring the node red in the DAG representation."

WORKDIR /usr/local/src/pl-covidnet-meta

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
ARG extras_require=none
RUN pip install ".[${extras_require}]"

CMD ["covidnet_meta", "--help"]

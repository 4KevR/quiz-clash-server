FROM python:3.12.3-slim as base

WORKDIR /flask-app

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends python3-dev  \
    && apt-get install -y --no-install-recommends python3-setuptools  \
    && apt-get install -y --no-install-recommends build-essential libssl-dev libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

FROM base

COPY . .

ENTRYPOINT ["uwsgi", "app.ini"]

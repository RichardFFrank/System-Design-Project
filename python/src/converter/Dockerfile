# python:3:10-slim-bullseye is the base image layer. i.e. layer 1
FROM python:3.10-slim-bullseye 

# layer 2 -> install os dependencies (--no-cache-dir = don't cache to keep size small. 
# --no-install-suggests means don't install recommended packages since we can't be sure how those will change and affect us.)
RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential ffmpeg \
    && pip install --no-cache-dir --upgrade pip

# layer 3
WORKDIR /app

# layer 4
COPY ./requirements.txt /app

# layer 5
RUN pip install --no-cache-dir --requirement /app/requirements.txt

# layer 6
COPY . /app

# layer 7
CMD ["python3", "consumer.py"]
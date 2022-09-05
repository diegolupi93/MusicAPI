FROM python:3.8-alpine

WORKDIR /app
# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV CACHE_TYPE=redis
ENV CACHE_REDIS_HOST=redis
ENV CACHE_REDIS_PORT=6379
ENV CACHE_REDIS_DB=0
ENV CACHE_REDIS_URL=redis://redis:6379/0
ENV CACHE_DEFAULT_TIMEOUT=120
# Copy requirements from local to docker image
COPY requirements.txt /app
# Install the dependencies in the docker image
RUN pip3 install -r requirements.txt --no-cache-dir
# Copy everything from the current dir to the image
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
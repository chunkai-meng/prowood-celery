FROM python:3.10-slim

ENV APP_HOME /app
WORKDIR $APP_HOME

# Removes output stream buffering, allowing for more efficient logging
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY ./requirements ./requirements
RUN pip install --no-cache-dir -r ./requirements/base.txt

ENV APP_HOME /app
ENV TZ=Pacific/Auckland

WORKDIR $APP_HOME

# Removes output stream buffering, allowing for more efficient logging
ENV PYTHONUNBUFFERED 1

# Copy local code to the container image.
COPY . .
# Collect static files
RUN python -m manage collectstatic -v 3 --no-input
#CMD gunicorn --bind 0.0.0.0:8888 --workers 1 --threads 8 --timeout 0 proj.asgi:application -k uvicorn.workers.UvicornWorker
EXPOSE 8888
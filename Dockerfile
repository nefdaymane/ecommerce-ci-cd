FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt requirements.txt


RUN pip install --no-cache-dir -r requirements.txt


COPY . /app
WORKDIR /app


EXPOSE 5000


CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

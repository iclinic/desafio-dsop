FROM tiangolo/uvicorn-gunicorn-fastapi:latest

COPY requirements.txt .
COPY ./api /app

RUN pip install -r requirements.txt



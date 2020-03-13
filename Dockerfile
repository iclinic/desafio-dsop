FROM tiangolo/uvicorn-gunicorn-fastapi:latest

RUN pip install -r requirements.txt

COPY ./api /app
COPY requirements.txt .
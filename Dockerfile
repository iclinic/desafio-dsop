FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY requirements.txt .
COPY ./api /app/app

RUN pip install -r requirements.txt



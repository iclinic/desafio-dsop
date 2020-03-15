FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY requirements.txt .
COPY ./api /app/app
COPY ./static /app/static

RUN pip install -r requirements.txt



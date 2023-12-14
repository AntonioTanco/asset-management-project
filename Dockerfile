FROM python:3.11.7

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

RUN pip install fastapi uvicorn

COPY ./requirements.txt /app/requirements.txt

CMD [ "uvicorn", "--host", "0.0.0.0", "--port", "8000", "main:app" ]
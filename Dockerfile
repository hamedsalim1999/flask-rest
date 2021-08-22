FROM python:3.8.11-alpine3.14
RUN mkdir code
WORKDIR /code
COPY . /code
RUN apk update && apk add sudo libressl-dev postgresql-dev libffi-dev gcc musl-dev python3-dev py-cryptography
RUN apk add --update py3-pip
RUN pip install --no-cache-dir --upgrade pip
RUN sudo pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["python", "app.py"]
FROM python:3.8.11-alpine3.14
RUN mkdir code
WORKDIR /code
COPY . /code
RUN apk add py-cryptography
RUN pip install --no-cache-dir --upgrade pip
RUN pip install cryptography -vvv --no-binary=cryptography
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["python", "app.py"]
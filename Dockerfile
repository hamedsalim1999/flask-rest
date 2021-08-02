FROM python:3.8-alpine
RUN mkdir code
WORKDIR /code
COPY . /code
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
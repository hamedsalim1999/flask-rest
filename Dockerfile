FROM python:3.7-alpine
RUN mkdir code
WORKDIR /code
COPY . /code
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
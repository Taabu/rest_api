FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app
COPY mysql/* /docker-entrypoint-initdb.d/

CMD ["python", "app/__init__.py"]

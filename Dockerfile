FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install Flask flask-mysqldb bcrypt Werkzeug mysqlclient gunicorn

CMD ["python","app.py"]
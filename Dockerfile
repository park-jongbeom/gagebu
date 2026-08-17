FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD [ "gunicorn", "mysite.wsgi", "-d", "0.0.0.0:8000", "-w", "2" ]
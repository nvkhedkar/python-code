FROM python:3.7.5

WORKDIR /app

COPY . /app

RUN pip --no-cache-dir install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "--reload", "-b", "0.0.0.0:8000", "app:app"]

FROM python:3.8-slim-buster

RUN apt-get update -y && \
    apt-get install -y sox libsox-fmt-mp3 bpm-tools

COPY requirements.txt /app/requirements.txt
RUN mkdir /sessions

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

WORKDIR /
CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app" ]
#CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]

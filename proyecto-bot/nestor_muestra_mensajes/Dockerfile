FROM python:3.6.3

ENV MONGO_HOST localhost
ENV MONGO_PORT 27017

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

ENV PYTHONUNBUFFERED=1

WORKDIR /nestor_muestra_mensajes

COPY ./nestor_muestra_mensajes.py /nestor_muestra_mensajes.py

CMD [ "python", "/nestor_muestra_mensajes.py" ]

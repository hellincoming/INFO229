FROM python:3.6.3

ENV MONGO_HOST localhost
ENV MONGO_PORT 27017

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

ENV PYTHONUNBUFFERED=1

WORKDIR /nestor_almacenar

COPY ./nestor_almacenar.py /nestor_almacenar.py

CMD [ "python", "/nestor_almacenar.py" ]

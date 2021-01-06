FROM python:3.6.3

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

ENV PYTHONUNBUFFERED=1

WORKDIR /nestor_bot_help

COPY ./nestor_bot_help.py /nestor_bot_help.py

CMD [ "python", "/nestor_bot_help.py" ]

FROM python:3.5.3
WORKDIR /app/

ADD requirements/base.txt requirements/prod.txt /app/

RUN pip install -r prod.txt

ADD . /app

RUN chmod +x keys.sh

ENTRYPOINT ./keys.sh

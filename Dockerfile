FROM python:3.9

WORKDIR /var/www/

COPY ./requirements.txt ./
COPY ./app ./app

RUN pip3 install -r ./requirements.txt

CMD [ "python3", "app/run.py"]
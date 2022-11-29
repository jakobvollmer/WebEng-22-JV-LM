FROM python:3.9

WORKDIR /var/www/

COPY ./requirements.txt ./
RUN pip3 install -r ./requirements.txt

COPY ./app ./app

CMD [ "python3", "app/run.py"]
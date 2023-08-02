FROM python:3.10.11

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "waitress-serve", "--call" , "run_server:get_app"]
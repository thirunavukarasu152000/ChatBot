FROM python:3.10.11


ENV OPENAI_API_KEY $OPENAI_API_KEY
ENV WEAVIATE_API_URL $WEAVIATE_API_URL
ENV WEAVIATE_API_KEY $WEAVIATE_API_KEY

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "waitress-serve", "--call" , "run_server:get_app"]
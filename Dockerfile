FROM python:3.8-slim-buster
RUN mkdir /app
WORKDIR /app
ADD . /app/

# pipenv istallation
RUN pip install pipenv
COPY Pipfile* /app/
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt
RUN pip install psycopg2-binary

COPY . /app/


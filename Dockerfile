FROM python:3.8

ARG PIPENV_ARGS

ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1

# Add app user
RUN adduser --disabled-login app

RUN pip install pipenv==2018.11.26

WORKDIR /app/

COPY Pipfile Pipfile.lock /app/

# Install application requirements
RUN pipenv install --deploy --system $PIPENV_ARGS && \
    rm -rf /root/.cache

# Bundle app source
COPY . /app/

USER app

FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUBUFFERED 1

RUN mkdir -p /home/app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
WORKDIR $APP_HOME

COPY . $APP_HOME

RUN pip install --upgrade pip \
    && pip install pipenv \
    && pipenv install --system --dev

RUN useradd -ms /bin/bash newuser
RUN chown -R newuser $APP_HOME

USER newuser

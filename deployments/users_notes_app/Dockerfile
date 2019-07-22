FROM python:3.7.4
ADD users_notes_app/ /app
WORKDIR /app
RUN apt-get update
COPY common/ /app/common/
COPY ./requirements.txt /app/common/requirements.txt
RUN pip install -r common/requirements.txt

CMD python app.py


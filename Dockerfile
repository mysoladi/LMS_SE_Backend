FROM python:3.11.6-alpine

WORKDIR /home/application

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./lms_login_api lms_login_api/

COPY ./manage.py .

COPY ./utils utils/

COPY ./entrypoint.sh .

COPY ./.env .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]

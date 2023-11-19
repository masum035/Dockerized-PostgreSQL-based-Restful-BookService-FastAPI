FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN alembic upgrade head
RUN chmod +x startup.sh

EXPOSE 80

ENV MODULE_NAME="app.main"
ENV VARIABLE_NAME="app"

CMD ["./startup.sh"]

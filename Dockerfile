FROM python:3.11-rc-alpine
RUN python -m pip install --upgrade pip
RUN mkdir /app
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
CMD ["./docker-entrypoint.sh"]
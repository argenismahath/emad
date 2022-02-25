FROM python3.9

RUN pip install flask gunicorn

COPY src/ appflask/
WORKDIR /server

ENV PORT 8080

CMD exec gunicorn -bind :$PORT --workers 1 --threads 8 appflask:app
FROM python:3.8

WORKDIR /server

COPY ./server/requirements.txt /server/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /server/requirements.txt

COPY server /server

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "3003"]
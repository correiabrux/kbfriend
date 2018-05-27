FROM python:3.7-rc AS builder
WORKDIR /app

COPY kbfriend.py /app
COPY requirements.txt /app

RUN python3 -m venv . && \
bin/pip3 install -r requirements.txt

FROM python:3.7-rc-slim
WORKDIR /app
COPY --from=builder /app /app

ENTRYPOINT [ "bin/python3", "/app/kbfriend.py" ]

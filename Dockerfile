FROM python:3.10-slim as base

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt

FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y libpq5

COPY --from=base /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY ./app /code/app

WORKDIR /code

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

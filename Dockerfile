FROM python:3.12-slim

WORKDIR /app

COPY ../poetry.lock ../pyproject.toml ./
# apt-get update && apt-get install -y gcc libpq-dev && \
RUN pip install --upgrade pip && \
	pip install poetry && \
	poetry config virtualenvs.create false && \
	poetry install --no-interaction --no-ansi

COPY ./app .

CMD ["python3", "main.py"]
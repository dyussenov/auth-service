FROM python:3.10

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi
RUN apt-get update \
  && apt-get install -y netcat-traditional \
  && apt-get install -y lsof \
  && rm -rf /var/lib/apt/lists/*


COPY . /app

RUN chmod +x /app/wait-for-db.sh

EXPOSE 8000

ENTRYPOINT ["/app/wait-for-db.sh"]
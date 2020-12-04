FROM revolutiontech/zappa:1.0

COPY . .

RUN poetry install --no-dev

CMD ["poetry", "run", "zappa", "update"]

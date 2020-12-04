FROM revolutiontech/zappa:1.0

RUN yum install -y libffi-devel

COPY . .

RUN poetry install --no-dev

CMD ["poetry", "run", "zappa", "update"]

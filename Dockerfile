FROM python:3.11-slim as base

RUN apt-get update && apt-get install --yes \
    curl \
    iputils-ping \
    net-tools \
    dnsutils \
    telnet \
    netcat-traditional

FROM base AS poetry
RUN pip install poetry==1.5.1

FROM poetry AS export
COPY pyproject.toml poetry.lock ./
RUN poetry export --format requirements.txt > requirements.txt

FROM base AS runtime
COPY --from=export requirements.txt .

RUN pip install --requirement requirements.txt

COPY src/ src/
COPY static/ static/

CMD ["python", "-m", "src"]

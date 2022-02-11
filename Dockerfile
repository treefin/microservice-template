FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

ENV WEB_CONCURRENCY=1
ENV PORT=2329
ENV MODULE_NAME=xxx_service
ENV VARIABLE_NAME=xxx_service_app
# Handle gracefully on client side
ENV GRACEFUL_TIMEOUT=0

# Add your own certificates
COPY secrets/yyy.pem /usr/local/share/ca-certificates/yyy.pem
RUN update-ca-certificates

ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

# dependencies
COPY ./pyproject.toml /pyproject.toml
COPY ./poetry.lock /poetry.lock
COPY ./scripts /scripts

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-dev

# xxx_service code - changes often - keep at bottom
COPY xxx_service /app/xxx_service

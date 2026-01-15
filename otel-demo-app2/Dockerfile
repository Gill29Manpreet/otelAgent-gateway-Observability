FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    opentelemetry-distro \
    opentelemetry-exporter-otlp

COPY app_b.py .

ENV OTEL_SERVICE_NAME=service-b
ENV OTEL_TRACES_EXPORTER=otlp
ENV OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
ENV OTEL_EXPORTER_OTLP_ENDPOINT=http://10.128.0.11:4318
ENV OTEL_RESOURCE_ATTRIBUTES=environment=lab

CMD ["opentelemetry-instrument", "python", "-m", "uvicorn", "app_b:app", "--host", "0.0.0.0", "--port", "8081"]

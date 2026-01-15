FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# ---- OpenTelemetry configuration ----
ENV OTEL_SERVICE_NAME=demo-app
ENV OTEL_TRACES_EXPORTER=otlp
ENV OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
ENV OTEL_EXPORTER_OTLP_ENDPOINT=http://10.128.0.11:4318
ENV OTEL_RESOURCE_ATTRIBUTES=service.version=1.0,environment=lab

# (Optional but useful for troubleshooting; can remove later)
ENV OTEL_LOG_LEVEL=info

# ---- Start app with auto-instrumentation ----
CMD ["opentelemetry-instrument", "python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]

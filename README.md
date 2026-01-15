# OpenTelemetry Agent → Gateway → Observability (POC)

This repository demonstrates a **scalable OpenTelemetry architecture**
using a **Gateway pattern**, where lightweight agents forward telemetry
to a central gateway, which then exports data to observability backends.

This setup reflects **real-world enterprise observability designs**.

---

+-------------------+      +---------------------+      +---------------------------+
| OTEL Agent VM     | ----> | OTEL Gateway VM     | ----> | Observability Backends    |
| (Host metrics,    | OTLP  | (Aggregation,       | OTLP  | - Splunk Observability    |
| logs, traces)     | 4317  | enrichment, export) | 443  | - Jaeger (Tracing UI)     |
+-------------------+      +---------------------+      +---------------------------+

---

## Why Gateway Pattern?

- Reduces outbound connections from hosts
- Centralized control of exporters, tokens, and routing
- Easier scaling and security management
- Industry-standard pattern (used at scale)

---

## Repository Structure

otelAgent-gateway-Observability/
├── README.md
├── configs/
│   └── otel/
│       ├── agent-config.yml      # OTEL agent (no exporters)
│       └── gateway-config.yml    # OTEL gateway (exporters here)
├── docker-compose/
│   └── otel-gateway/
│       └── docker-compose.yml    # Gateway + Jaeger
├── services/
│   ├── service-a/
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   └── requirements.txt
│   └── service-b/
│       ├── app_b.py
│       ├── Dockerfile
│       └── docker-compose.yml
├── windows/
│   └── README.md                 # Windows metrics setup (Prometheus)

---

## Components

### OTEL Agent (Old VM / Host VM)

- Collects:
  - Host metrics
  - Logs
  - Traces
- **Does NOT export to backends**
- Sends data only to the gateway via OTLP

**Ports used**
- Outbound: `4317 → Gateway`

---

### OTEL Gateway (New VM)

- Receives OTLP data from agents and applications
- Enriches telemetry (resource detection, attributes)
- Exports data to:
  - Splunk Observability Cloud (primary backend)
  - Jaeger (local trace UI for POC/debugging)

**Ports exposed**

| Port  | Purpose                     |
|------|-----------------------------|
| 4317 | OTLP gRPC (from agents)     |
| 4318 | OTLP HTTP (from apps)       |
| 16686| Jaeger UI                   |

---

### Backends

- **Splunk Observability Cloud**
  - Metrics, traces, logs (primary backend)
- **Jaeger**
  - Trace visualization (POC / local debugging)

---

## Data Flow

1. Agent or application collects telemetry
2. Telemetry is sent via OTLP → Gateway
3. Gateway:
   - Applies processors
   - Handles authentication
   - Controls batching and export
4. Observability platforms receive clean, enriched telemetry

---

## Demo Application Services (Trace Validation)

In addition to host-based OTEL agents, this repository includes
**two containerized FastAPI services** used to validate **end-to-end
distributed tracing through the OpenTelemetry Gateway**.

These services demonstrate how real applications send traces to the
gateway using **OTLP over HTTP**, and how trace context propagates
across multiple services.

### Services

- **service-a**
  - Entry-point API
  - Receives external requests
  - Calls service-b
  - Exports traces to the OTEL Gateway

- **service-b**
  - Downstream API
  - Simulates processing latency
  - Participates in the same trace as service-a

### Trace Flow

Client
→ service-a
→ service-b
→ OpenTelemetry Gateway
→ Splunk Observability Cloud


### Key Characteristics

- OpenTelemetry Python auto-instrumentation
- OTLP **HTTP/protobuf** used for application → gateway communication
- Docker user-defined network for service discovery
- Verified parent-child span relationships
- Clean service topology visible in APM service maps
- Accurate latency attribution across services

These services are intended for:
- Gateway validation
- Distributed tracing experiments
- Learning and troubleshooting
- POC demonstrations

They are **not production applications**.

---

## What This Repo Is (and Is Not)

✅ This repo **IS**
- A reference OpenTelemetry Gateway architecture
- A clean separation of agent, application, and gateway responsibilities
- Suitable for scaling to many hosts and services

❌ This repo **IS NOT**
- A single-node / all-in-one setup
- A direct agent → backend configuration
- A production-ready application stack

---

## When to Use This Pattern

Use **Agent → Gateway** when:
- You have multiple hosts or services
- You want centralized token and exporter management
- You need traffic control, batching, or sampling
- You plan to grow beyond a lab setup

---

## Next Improvements (Planned)

- Ansible automation for agents
- TLS / mTLS between agents, apps, and gateway
- Gateway HA / load balancing
- Cost control via sampling & filtering
- Security hardening

---

## Related Repositories

- **observability-lab**
  - Direct agent → backend setup
  - Single-node lab / learning

This repository builds on that foundation with a **gateway-based,
enterprise-ready observability architecture**.

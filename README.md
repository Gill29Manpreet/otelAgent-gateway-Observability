# OpenTelemetry Agent → Gateway → Observability (POC)

This repository demonstrates a **scalable OpenTelemetry architecture**
using a **Gateway pattern**, where lightweight agents forward telemetry
to a central gateway, which then exports data to backends.

This setup reflects **real-world enterprise observability designs**.

---

+-------------------+ +---------------------+ +---------------------------+
| OTEL Agent VM | -----> | OTEL Gateway VM | -----> | Observability Backends |
| (Host metrics, | OTLP | (Aggregation, | OTLP | - Splunk Observability |
| logs, traces) | 4317 | enrichment, export)| 443 | - Jaeger (Tracing UI) |
+-------------------+ +---------------------+ +---------------------------+


### Why Gateway Pattern?
- Reduces outbound connections from hosts
- Centralized control of exporters, tokens, and routing
- Easier scaling and security management
- Industry-standard pattern (used at scale)

---

## Repository Structure

otelAgent-gateway-Observability/
├── README.md
├── configs/
│ └── otel/
│ ├── agent-config.yml # OTEL agent (no exporters)
│ └── gateway-config.yml # OTEL gateway (exporters here)
├── docker-compose/
│ └── otel-gateway/
│ ├── docker-compose.yml # Gateway + Jaeger
├── windows/
│ └── README.md # Windows metrics setup (Prometheus)


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
- Receives OTLP data from agents
- Enriches telemetry (resource detection, attributes)
- Exports to:
  - Splunk Observability Cloud
  - Jaeger (for trace UI)

**Ports exposed**
| Port | Purpose |
|-----|--------|
| 4317 | OTLP gRPC (from agents) |
| 4318 | OTLP HTTP (optional) |
| 16686 | Jaeger UI |

---

### Backends
- **Splunk Observability Cloud**
  - Metrics, traces, logs
- **Jaeger**
  - Trace visualization (POC / local debugging)

---

## Data Flow

1. Agent collects telemetry
2. Agent sends OTLP → Gateway
3. Gateway:
   - Applies processors
   - Handles authentication
   - Exports data
4. Observability platforms receive clean, enriched telemetry

---

## What This Repo Is (and Is Not)

✅ This repo **IS**
- A reference architecture
- A clean separation of agent vs gateway responsibilities
- Suitable for scaling to many hosts

❌ This repo **IS NOT**
- A single-node / all-in-one setup
- Direct agent → backend configuration

---

## When to Use This Pattern

Use **Agent → Gateway** when:
- You have multiple hosts / clusters
- You want centralized token management
- You need traffic control and batching
- You plan to grow beyond a lab setup

---

## Next Improvements (Planned)

- Ansible automation for agents
- TLS/mTLS between agent and gateway
- Gateway HA / load balancing
- Cost control via sampling & filtering
- Security hardening

---

## Related Repositories

- **observability-lab**
  - Direct agent → backend setup
  - Single-node lab / learning

This repo builds on that foundation with **enterprise-ready architecture**.


# Windows Observability Setup (Prometheus + Grafana)

This document explains how to monitor a Windows laptop using:

- windows_exporter
- Prometheus (Windows binary)
- Grafana

The goal is to collect CPU, memory, disk, and network metrics locally
from a Windows machine and visualize them in Grafana.

---

## Architecture Overview

This setup runs entirely on the Windows laptop.

windows_exporter (port 9182)  
↓  
Prometheus (port 9090)  
↓  
Grafana (port 3000)

No Docker, Linux server, or cloud VM is involved.

---

## Ports Used

| Component        | Port | Purpose                         |
|------------------|------|---------------------------------|
| windows_exporter | 9182 | Exposes Windows metrics         |
| Prometheus       | 9090 | Scrapes metrics                 |
| Grafana          | 3000 | Visualization UI                |

---

## windows_exporter Installation

### Download

Download the MSI from:  
https://github.com/prometheus-community/windows_exporter/releases

### Installation Options

During installation:
- Enable **Firewall Exception**
- Keep default installation path:

C:\Program Files\windows_exporter\

---

## Verify windows_exporter Service

Run **CMD as Administrator**:

```cmd
sc query windows_exporter

Expected:
STATE : RUNNING

Check port binding:
netstat -ano | findstr 9182

Expected:
TCP 0.0.0.0:9182 LISTENING


Troubleshooting: Port 9182 Not Reachable
Problem

Even though windows_exporter was running, this failed:

curl http://localhost:9182/metrics

Root Cause

The service was started without an explicit listen address, so it
did not bind correctly to port 9182.

Fix

Update the service binary path:
sc config windows_exporter binPath= "\"C:\Program Files\windows_exporter\windows_exporter.exe\" --listen-address=0.0.0.0:9182"

Restart the service:
sc stop windows_exporter
sc start windows_exporter

Verify again:
curl http://localhost:9182/metrics
Metrics output confirms the exporter is working.

Prometheus Setup on Windows
Directory
C:\observability\prometheus\
Contents

prometheus.exe

promtool.exe

prometheus.yml

prometheus.yml Configuration
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "windows-laptop"
    static_configs:
      - targets:
          - "localhost:9182"

Start Prometheus
cd C:\observability\prometheus
prometheus.exe --config.file=prometheus.yml

Open in browser:
http://localhost:9090/targets

Expected:
windows-laptop → UP

Grafana Setup

URL: http://localhost:3000

Add Prometheus datasource:

URL: http://localhost:9090

Dashboards

Use dashboards built for windows_exporter, not node_exporter.

Recommended dashboards:

Windows Exporter Full

Windows Host Overview

Note: Some dashboards show N/A because they expect Linux node_exporter metrics.

Summary

This setup enables:

Local Windows system monitoring

Permanent Grafana dashboards

No dependency on Splunk Observability or cloud services

This forms a foundation for:

Ansible automation

OpenTelemetry Collector on Windows

Multi-host monitoring

---

## ✅ What to do next (CMD)

```cmd
cd C:\observability-lab
git add windows/README.md
git commit -m "Add Windows Prometheus + Grafana observability documentation"
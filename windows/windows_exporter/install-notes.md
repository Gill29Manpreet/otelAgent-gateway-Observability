\# windows\_exporter Installation Notes



\## Common Issue: Port 9182 not reachable



Symptoms:

\- Service running

\- curl http://localhost:9182/metrics fails



Root Cause:

windows\_exporter service started without explicit listen address.



Fix:

Reconfigure service:



sc config windows\_exporter binPath= "\\"C:\\Program Files\\windows\_exporter\\windows\_exporter.exe\\" --listen-address=0.0.0.0:9182"



Restart service:

sc stop windows\_exporter

sc start windows\_exporter



Verify:

netstat -ano | findstr 9182

curl http://localhost:9182/metrics


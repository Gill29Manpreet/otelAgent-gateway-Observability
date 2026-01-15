print("🔥 THIS APP.PY IS RUNNING 🔥")

from fastapi import FastAPI
import random
import time
import requests
from opentelemetry import trace

app = FastAPI()

# Tracer provided by opentelemetry-instrument
tracer = trace.get_tracer(__name__)

@app.get("/fast")
def fast():
    with tracer.start_as_current_span("manual-fast-span"):
        return {"status": "fast ok"}

@app.get("/slow")
def slow():
    with tracer.start_as_current_span("manual-slow-span"):
        time.sleep(random.uniform(0.5, 2.0))
        return {"status": "slow ok"}

@app.get("/error")
def error():
    with tracer.start_as_current_span("manual-error-span"):
        if random.random() < 0.5:
            raise Exception("simulated error")
        return {"status": "sometimes ok"}

@app.get("/call-b")
def call_b():
    time.sleep(0.1)
    response = requests.get("http://service-b:8081/work")
    return {"from_service_b": response.json()}

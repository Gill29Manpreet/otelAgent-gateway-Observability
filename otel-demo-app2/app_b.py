from fastapi import FastAPI
import time
import random

app = FastAPI()

@app.get("/work")
def do_work():
    time.sleep(0.3)
    return {"status": "done"}

@app.get("/work-error")
def do_work_error():
    time.sleep(0.2)
    if random.random() < 0.7:
        raise Exception("downstream service-b failure")
    return {"status": "sometimes ok"}

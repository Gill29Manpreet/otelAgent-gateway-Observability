from fastapi import FastAPI
import time

app = FastAPI()

@app.get("/work")
def do_work():
    time.sleep(0.3)
    return {"status": "done"}

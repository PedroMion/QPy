from fastapi import FastAPI
from qpy import environment

app = FastAPI(
    title="qpy API",
    description="API to expose QPy funcionalities",
    version="0.1.0",
)

@app.get("/simulate")
def simulate():
    """
    Simulates a queue and retuns metrics.
    """
    return "Hello World!"
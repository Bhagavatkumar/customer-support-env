from fastapi import FastAPI
from env.core import CustomerSupportEnv

app = FastAPI()
env = CustomerSupportEnv()

@app.get("/")
def home():
    return {"message": "CSRE running"}

# ✅ FIX: GET + POST दोनों
@app.get("/reset")
@app.post("/reset")
def reset():
    return env.reset()

@app.get("/state")
def state():
    return env.state()

@app.post("/step")
def step(action: dict):
    return env.step(action)

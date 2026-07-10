from fastapi import FastAPI

app = FastAPI(
    title="AI Database Copilot",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "AI Database Copilot"
    }
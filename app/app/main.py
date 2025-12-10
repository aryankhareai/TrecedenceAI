from fastapi import FastAPI
from app.api.endpoints import router as api_router

app = FastAPI(title="Workflow Engine API", description="A simple workflow engine API")

# Include the API router
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Workflow Engine API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

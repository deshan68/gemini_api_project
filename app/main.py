from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.config import config
from app.api.endpoints import generate_sub


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(generate_sub.router, prefix="/api/v1", tags=["generateSab"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=config.get("app", "host"),
        port=config.get("app", "port"),
        reload=config.get("app", "reload")
    )

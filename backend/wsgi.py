import os
from pathlib import Path

# Create directories if they don't exist
Path("data").mkdir(exist_ok=True)
Path("logs").mkdir(exist_ok=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=True
    )

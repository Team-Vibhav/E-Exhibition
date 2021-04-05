from app import api
import uvicorn
import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    uvicorn.run(api.app, host="0.0.0.0", port=8000, log_level="info", debug=True)

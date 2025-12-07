from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
import os

# Load .env variables
load_dotenv()


class Config(BaseModel):
    API_KEY: str = Field(..., min_length=5)
    TIMEOUT: int = Field(default=10)
    CIRCUIT_FAIL_THRESHOLD: int = Field(default=3)
    CIRCUIT_RESET_TIME: int = Field(default=30)


def load_config():
    """Load and validate configuration values."""
    try:
        cfg = Config(
            API_KEY=os.getenv("API_KEY"),
            TIMEOUT=int(os.getenv("TIMEOUT", 10)),
            CIRCUIT_FAIL_THRESHOLD=int(os.getenv("CIRCUIT_FAIL_THRESHOLD", 3)),
            CIRCUIT_RESET_TIME=int(os.getenv("CIRCUIT_RESET_TIME", 30)),
        )
        return cfg
    except ValidationError as e:
        raise RuntimeError("❌ Config validation failed") from e

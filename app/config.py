import os
from dotenv import load_dotenv

# Load env variables from .env file
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Bamsae AI Backend"
    VERSION: str = "0.1.0"
    
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")

settings = Settings()

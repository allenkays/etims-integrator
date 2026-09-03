import os

from dotenv import load_dotenv


load_dotenv()


VSCU_BASE_URL = os.getenv(
    "VSCU_BASE_URL",
    "http://localhost:8088"
)
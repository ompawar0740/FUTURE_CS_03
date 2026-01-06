import os
from dotenv import load_dotenv

# Load variables from .env FIRST
load_dotenv()

# Fetch AES key
AES_KEY = os.getenv("AES_SECRET_KEY")

if not AES_KEY:
    raise Exception("AES_SECRET_KEY not set in environment")

# AES-256 requires exactly 32 bytes
AES_KEY = AES_KEY.encode()

# Upload directory
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")

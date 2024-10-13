import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
GROUP_ID = os.getenv("GROUP_ID")
ADMIN_ID = os.getenv("ADMIN_ID")
URL = os.getenv("URL")
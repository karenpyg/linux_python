"""Remote host configuration."""
from os import getenv, path
from dotenv import load_dotenv

# Load environment variables from .env
BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))
print(getenv("SECRET_KEY"))
# SSH Connection Variables
ENVIRONMENT = getenv("ENVIRONMENT")
SSH_REMOTE_HOST = getenv("SSH_REMOTE_HOST")
SSH_USERNAME = getenv("SSH_USERNAME")
SSH_PASSWORD = getenv("SSH_PASSWORD")
SSH_KEY_FILEPATH = getenv("SSH_KEY_FILEPATH")
SCP_DESTINATION_FOLDER = getenv("SCP_DESTINATION_FOLDER")

# Local file directory
LOCAL_FILE_DIRECTORY = f"{BASE_DIR}/files"

# print(BASE_DIR ,
# ENVIRONMENT ,
# SSH_REMOTE_HOST ,
# SSH_USERNAME ,
# SSH_PASSWORD ,
# SSH_KEY_FILEPATH ,
# SCP_DESTINATION_FOLDER ,
# LOCAL_FILE_DIRECTORY )
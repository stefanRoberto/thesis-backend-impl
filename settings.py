import os
from dotenv import load_dotenv

load_dotenv()

database = dict(
    USERNAME=os.getenv('DB_USERNAME'),
    PASSWORD=os.getenv('DB_PASSWORD'),
    HOST=os.getenv('DB_HOST'),
    PORT=os.getenv('DB_PORT'),
    NAME=os.getenv('DB_NAME')
)

import os
from dotenv import load_dotenv
load_dotenv()

class MyLocalDBConfig:
    db_name = os.getenv("LOCAL_DB_NAME")
    server = "localhost"
    database = os.getenv("LOCAL_DB_BASE")
    user = os.getenv("LOCAL_DB_USER")
    password = os.getenv("LOCAL_DB_PASSWORD")
    port = os.getenv("LOCAL_DB_PORT")

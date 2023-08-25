import os
import dotenv

dotenv.load_dotenv('.env')
MYSQL_HOST = os.environ['MYSQL_HOST']
MYSQL_USER = os.environ['MYSQL_USER']
MYSQL_PASSWORD = os.environ['MYSQL_PASSWORD']
MYSQL_DB = os.environ['MYSQL_DB']

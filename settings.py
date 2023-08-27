import os
import dotenv

dotenv.load_dotenv('.env')
MYSQL_HOST = os.environ['MYSQL_HOST']
MYSQL_USER = os.environ['MYSQL_USER']
MYSQL_PASSWORD = os.environ['MYSQL_PASSWORD']
MYSQL_DB = os.environ['MYSQL_DB']
TOKEN_QUERY = os.environ['TOKEN_QUERY']
GET_COMMENT_QUERY = os.environ['GET_COMMENT_QUERY']
POST_COMMENT_QUERY = os.environ['POST_COMMENT_QUERY']
DELETE_COMMENT_QUERY = os.environ['DELETE_COMMENT_QUERY']
GET_ALL_COMMENTS_QUERY= os.environ['GET_ALL_COMMENTS_QUERY']
TOKEN_URL = os.environ['TOKEN_URL']



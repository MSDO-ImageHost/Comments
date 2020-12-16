'''
USER = "root"
PASSWORD = "toor"
HOST = "database"
PORT = 5432
DATABASE = "commentdb"
DATABASE_CONNECTION_URI = f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

'''
import os

USER = os.environ['MYSQL_USER']
PASSWORD = os.environ['MYSQL_PASSWORD']
HOST = "mySQL"
DATABASE = os.environ['MYSQL_DATABASE']
DATABASE_CONNECTION_URI = f'mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:3306/{DATABASE}'
'''
USER = os.environ['POSTGRES_USER']
PASSWORD = os.environ['POSTGRES_PASSWORD']
HOST = os.environ['POSTGRES_HOST']
PORT = os.environ['POSTGRES_PORT']
DATABASE = os.environ['POSTGRES_DB']
DATABASE_CONNECTION_URI = f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
'''
AMQP_USER = PORT = os.environ['RABBITMQ_DEFAULT_USER']
AMQP_PASSWORD = os.environ['RABBITMQ_DEFAULT_PASS']
AMQP_URI = f"amqp://{AMQP_USER}:{AMQP_PASSWORD}@rabbitmq:5432/"

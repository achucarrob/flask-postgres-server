# Conexion a la base de datos

# libreria que permite la conexion a pgadmin4
import psycopg2
from psycopg2 import DatabaseError
# libreria que resguarda sensible data y funcion que carga en esta pagina esos datos
from dotenv import load_dotenv
import os

# call the function que contiene variables de entorno (sensible data)
load_dotenv()

# funcion que conecta a la db
def get_connection():
    try:
        return psycopg2.connect(
            host=os.getenv('HOST'),
            user=os.getenv('USER_NAME'),
            password=os.getenv('PASSWORD'),
            database=os.getenv('DATABASE_NAME')
        )
    except DatabaseError as ex:
        raise ex

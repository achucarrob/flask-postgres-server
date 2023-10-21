from flask import Flask, request
# importar la conexion a la db 
from database.db import get_connection

app = Flask(__name__)

conn = get_connection()

cur = conn.cursor()

@app.route('/')
def index():
    return 'Hello, world!'

# post a new contact to the db
@app.route('/new_contact', methods=['POST'])
def new_contact():
    # recibir desde el front los values en formato json
    new_contact = request.get_json()
    name = new_contact['name']
    phone_number = new_contact['number']

    cur.execute('INSERT INTO public.contacts( name, "number") VALUES (%s, %s)', (name, phone_number))
    conn.commit()

    cur.close()
    conn.close()
    '''
    result = cur.fetchone()
    print(result)'''
    return "nuevo contacto"
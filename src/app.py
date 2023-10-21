from flask import Flask, request, jsonify
# importar la conexion a la db 
from database.db import get_connection

app = Flask(__name__)

# Instancia de la conexion a la db
conn = get_connection()
# cursos (iterador) de db
cur = conn.cursor()

# home endpoint
@app.get('/')
def index():
    return 'Hello, world!'

# post a new contact to the db
@app.post('/new_contact')
def new_contact():
    # recibir desde el front los values en formato json
    new_contact = request.get_json()
    name = new_contact['name']
    phone_number = new_contact['number']

    # Query
    # Los valores de name y number seran remplazados (%s, %s) por los valores de la tupla name y phone_number
    cur.execute('INSERT INTO public.contacts( name, "number") VALUES (%s, %s)', (name, phone_number))
    # commit to the db
    conn.commit()

    return "nuevo contacto"

# get all contacts listed
@app.get('/contacts')
def contacts():
    cur.execute('SELECT * FROM public.contacts')
    result = cur.fetchall()
    return jsonify(result)

# get contact by id
@app.get('/contact/<id>')
def contact_by_id(id):
    cur.execute('SELECT * FROM public.contacts WHERE id = (%s)',(id))
    result = cur.fetchall()
    return jsonify(result)

# update contact
@app.put('/edit/<id>')
def edit(id):
    selected_contact = request.get_json()
    name = selected_contact['name']
    phone_number = selected_contact['number']

    cur.execute(''' UPDATE public.contacts
	SET name= %s, "number"= %s
	WHERE id = %s RETURNING *
    ''', (name, phone_number, id))
    result = cur.fetchone()
    conn.commit()

    return jsonify(result)

# delete contact
@app.delete('/delete/<id>')
def delete(id):
    cur.execute('''DELETE FROM public.contacts
	WHERE id = %s RETURNING *''', (id))
    result = cur.fetchone()
    conn.commit()

    return jsonify(result)
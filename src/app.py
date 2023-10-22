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
# create a new user
@app.post('/new_user')
def new_user():
    # recibir desde el front los values en formato json
    new_user = request.get_json()
    name = new_user['name']
    email = new_user['email']

    # Query
    # Los valores de name y email seran remplazados (%s, %s) por los valores de la tupla name y email
    cur.execute('''INSERT INTO public."user"(name, email)
	VALUES (%s , %s) RETURNING *''', (name, email))
    # commit to the db
    result = cur.fetchone()
    conn.commit()


    return jsonify(result)

# post a new contact to the db
@app.post('/new_contact')
def new_contact():
    # recibir desde el front los values en formato json
    new_contact = request.get_json()
    name = new_contact['name']
    phone_number = new_contact['number']
    user_id = new_contact['user_id']

    # Query
    # Los valores de name y number seran remplazados (%s, %s) por los valores de la tupla name y phone_number
    cur.execute('INSERT INTO public.contacts( name, "number", user_id) VALUES (%s, %s, %s) RETURNING *', (name, phone_number, user_id))
    # commit to the db
    result = cur.fetchone()
    conn.commit()

    return jsonify(result)

# get all contacts listed
@app.get('/users')
def users():
    cur.execute('SELECT * FROM public.user')
    result = cur.fetchall()
    return jsonify(result)

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

# delete user
@app.delete('/delete_user/<id>')
def delete_user(id):
    cur.execute('''DELETE FROM public.user
	WHERE id = %s RETURNING *''', (id))
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
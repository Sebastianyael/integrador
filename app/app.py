from flask import Flask , render_template , request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = 'mongodb+srv://sebastianyael963:ViHNAGbZRL9@integradora.onlvtmq.mongodb.net/integradora?retryWrites=true&w=majority&appName=Integradora'
mongo = PyMongo(app)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/main-feed', methods=['POST'])
def feed():
    
    matricula = int(request.form['mat'].strip())
    contraseña = request.form['contraseña'].strip()

    print(f'Matrícula recibida: {matricula}')
    print(f'Contraseña recibida: {contraseña}')


    usuario = mongo.db.usuarios.find_one({'matricula': matricula, 'contraseña': contraseña})
    print(usuario)
    if usuario:
        return render_template('main-feed.html')
    else:
        return "Usuario no encontrado"


if(__name__ == '__main__'):
    app.run(debug = True)
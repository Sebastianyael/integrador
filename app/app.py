from flask import Flask , render_template , request , redirect , url_for , session , flash
from flask_pymongo import PyMongo
import os

app = Flask(__name__)

app.config["MONGO_URI"] = 'mongodb+srv://sebastianyael963:ViHNAGbZRL9@integradora.onlvtmq.mongodb.net/integradora?retryWrites=true&w=majority&appName=Integradora'
mongo = PyMongo(app)
app.secret_key = 'sebas'

@app.route('/' , methods = ['GET'])
def login():
    return render_template('login.html')


@app.route('/main-feed', methods=[ 'POST'])
def feed():
    
    matricula = int(request.form['mat'].strip())
    contraseña = request.form['contraseña'].strip()

    print(f'Matrícula recibida: {matricula}')
    print(f'Contraseña recibida: {contraseña}')


    usuario = mongo.db.usuarios.find_one({'matricula': matricula, 'contraseña': contraseña})
    print(usuario)
    if usuario:
        return  redirect(url_for('main_feed_view'))
    else:
        flash('Usuario no encontrado')
        return redirect(url_for('login'))
        
    
@app.route('/feed', methods=['GET'])
def main_feed_view():
    return render_template('main-feed.html')


if(__name__ == '__main__'):
    app.run(debug = True , host='0.0.0.0' , port=int(os.environ.get('PORT' , 5000)))
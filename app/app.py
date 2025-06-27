from flask import Flask , render_template , request
from flask_mysqldb import MySQL 

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'prueba'

conexion = MySQL(app)

@app.route('/main-feed' , methods = ['POST'])
def feed():
    try:
        matricula = request.form['matricula']
        contraseña = request.form['contraseña']

        cursor = conexion.connection.cursor()
        query = "SELECT * FROM login WHERE matricula = %s AND contraseña = %s"
        cursor.execute(query , (matricula , contraseña))
        result = cursor.fetchone()
        if result:
            return render_template('main-feed.html')
        else:
            return render_template('login.html')
        
    except Exception as e:
        return f"Error de conexión: {str(e)}"
    
@app.route('/')
def index():
    return render_template('login.html')

if(__name__ == '__main__'):
    app.run(debug = True)



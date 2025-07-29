from flask import Flask , render_template , flash , redirect , url_for , jsonify ,abort
from flask import Flask , render_template , request
from flask_mysqldb import MySQL 
import mysql.connector

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'prueba'

conexion = MySQL(app)
app.secret_key = '123'


@app.route('/')
def index():
    return render_template('login.html')


# @app.route('/main-feed' , methods = ['POST'])
# def feed():
#     try:
#         matricula = request.form['matricula']
#         contraseña = request.form['contraseña']
#         cursor = conexion.connection.cursor()
#         print(matricula)

#         if matricula.startswith('P'):
#             query = "SELECT * FROM profesores WHERE MatriculaProf = %s AND contraseña = %s"
#             cursor.execute(query , (matricula , contraseña))
#             result = cursor.fetchone()
#             if result:
#                 return render_template('teacher-feed.html')
#             else:
#                 flash('Usuario no encontrado')
#                 return render_template('login.html')

            
#         else:  
#             query = "SELECT * FROM login WHERE matricula = %s AND contraseña = %s"
#             cursor.execute(query , (matricula , contraseña))
#             result = cursor.fetchone()
#             if result:
#                 return render_template('main-feed.html')
#             else:
#                 flash('Usuario no encontrado')
#                 return render_template('login.html')   
        
        
#     except Exception as e:
#         return f"❌ Error de conexión: {str(e)}"
    

@app.route('/buscar', methods=['POST'])
def alumno():
    mat = None
    nombre = None  # definir siempre la variable
    apellidoPaterno = None
    apellidoMaterno = None
    onFlex = 'on-flex'
    if request.method == 'POST':
        matricula = request.form['matricula']
        print(f"Matrícula recibida: {matricula}")
        
        cursor = conexion.connection.cursor()
        query = "SELECT * FROM DatosGeneralesEstudiante WHERE Matricula = %s"
        cursor.execute(query, (matricula,))
        resultado = cursor.fetchone()
        print(resultado)
        if resultado:
            mat = resultado[0]
            nombre = resultado[1]
            apellidoPaterno = resultado[2]
            apellidoMaterno = resultado[3]
        else:
            nombre = "No encontrado"

    return render_template('teacher-feed.html', nombre=nombre , mat=mat , apellidoPaterno = apellidoPaterno , apellidoMaterno = apellidoMaterno , estado = onFlex)


@app.route('/grupo/crear', methods=['POST'])
def crear_grupo():
    try:
        if request.method == 'POST':
            nombre = request.form.get('nombre_grupo')
            cuatrimestre = request.form.get('cuatrimestre')
            salon = request.form.get('salon')
            anio = request.form.get('año_escolar')  
            materia = request.form.get('materia')

            print(f"Grupo creado: {nombre}, {cuatrimestre}, {salon}, {anio}, {materia}")

            cursor = conexion.connection.cursor()
            query = """
                INSERT INTO grupos (nombre, cuatrimestre, salon, anio_escolar, materia)
                VALUES (%s, %s, %s, %s, %s)
            """
            valores = (nombre, cuatrimestre, salon, anio, materia)
            cursor.execute(query, valores)
            conexion.connection.commit()
            cursor.close()

            return redirect(url_for('teacher_feed'))
    except Exception as e:
        return print({str(e)})
    

from flask import jsonify

@app.route('/grupo', methods=['GET'])
def mostrar_datos():
    cursor = conexion.connection.cursor()
    cursor.execute("SELECT id, nombre, cuatrimestre, salon, anio_escolar, materia FROM grupos")
    grupos = cursor.fetchall()

    # Definir los nombres de las columnas
    columnas = ['id', 'nombre', 'cuatrimestre', 'salon', 'anio_escolar', 'materia']

    # Convertir cada fila en un diccionario
    resultados = []
    for fila in grupos:
        resultados.append(dict(zip(columnas, fila)))

    return jsonify(resultados)

@app.route('/grupo/editar' , methods = ['PUT'])
def actualizar_grupo():
    try:
        datos_actualizados = request.json
        cursor = conexion.connection.cursor()
        query = """
                UPDATE grupos
                SET nombre = %s,
                cuatrimestre = %s,
                salon = %s,
                anio_escolar = %s,
                materia = %s
                WHERE id = %s
                """
        cursor.execute(query , (datos_actualizados.get('nombre'), datos_actualizados.get('cuatrimestre'), datos_actualizados.get('salon'), datos_actualizados.get('anio_escolar'), datos_actualizados.get('materia'), datos_actualizados.get('id')))
        conexion.connection.commit()
        return jsonify({'mensaje': 'Grupo actualizado correctamente'}), 200
    except Exception as e:
        print(f"Error {str(e)}")
        return jsonify({'mensaje': str(e)}),500
    

@app.route('/alumnos' , methods = ['POST'])
def mostrar_calificaciones_alumnos():
    datos_recibidos = request.get_json()
    id_grupo = datos_recibidos.get('id')

    cursor =     



@app.route('/teacher-feed')
def teacher_feed():
    return render_template('teacher-feed.html')


    
@app.route('/exit' , methods = ['POST'])
def exit():
    return render_template('login.html')


if(__name__ == '__main__'):
    app.run(debug = True)
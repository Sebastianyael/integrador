from flask import Flask , render_template , flash , redirect , url_for , jsonify ,request #importa el framework de flask y varias funcionalidades de este framework
from flask_mysqldb import MySQL #importa la biblioteca de mysql para trabajar con flask
from flask.globals import session #importa las sessiones de flask

app = Flask(__name__) #inicia la aplicacion de flask

#configuracion de la base de datos
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'prueba'
app.secret_key = '123'
mysql = MySQL(app)

#ruta que renderiza la palntilla login.html 
@app.route('/')
def feed():
    return render_template('login.html')

#clase base de datos con dos metodos insercion y seleccion
#insercion recibe la consulta que realizara en la base de datos
#seleccion recibe la consulta que realizara la base de datos y devuelve los resultados 
class BaseDatos:
    def __init__(self, query='', values=()):
        self.query = query
        self.values = values

    def insercion(self,query,values):
        try:
            self.query = query
            self.values = values
            cursor = mysql.connection.cursor()
            cursor.execute(self.query, self.values)
            mysql.connection.commit()
            cursor.close()
            return f"Inserción exitosa"
        except Exception as e:
            return f"Error en inserción: {str(e)}"

    def seleccion(self,query,matricula,contraseña):
        try:
            self.query = query
            self.values = (matricula , contraseña)
            cursor = mysql.connection.cursor()
            cursor.execute(self.query, self.values)
            resultado = cursor.fetchall()
            cursor.close()
            return resultado
        except Exception as e:
            print(f"Error en selección: {str(e)}")
            return None


class Usuario(BaseDatos):
    def __init__(self, id=None, nombre=None, correo=None, especialidad=None,
                 matricula=None, cuatrimestre=None, carrera=None, contraseña=None):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.especialidad = especialidad
        self.matricula = matricula
        self.cuatrimestre = cuatrimestre
        self.carrera = carrera
        self.contraseña = contraseña
        super().__init__()  # Para inicializar BaseDatos

    
    def buscar(self,query,matricula):
        try:
            self.query = query
            self.values = (matricula,)
            cursor = mysql.connection.cursor()
            cursor.execute(self.query, self.values)
            resultado = cursor.fetchall()
            cursor.close()
            return resultado
        except Exception as e:
            print(f"Error en selección: {str(e)}")
            return None
        
    def eliminar(self,query,parametro):
        try:
            self.query = query
            self.values = (parametro,)
            cursor = mysql.connection.cursor()
            cursor.execute(self.query,self.values)
            cursor.close()
            return True
        except Exception as e:
            return None


#ruta que que elimina un grupo de la base de datos cuando se le hace una peticcion desde JavaScript
@app.route('/grupo/eliminar' , methods = ['DELETE'])
def eliminar_grupo():
    try:
        datos = request.get_json()
        id_grupo = datos.get('id')#recibe el id del grupo que se eliminara 
        print(f"este es el id del grupo que se eliminara {id_grupo}")

        #consulta que eliminara el grupo en la base de datos
        query = """
            DELETE FROM grupos WHERE id = %s
        """
        grupo_eliminado = Usuario() #manda a llamar la clase usuario para usar el metodo eliminar
        grupo_eliminado.eliminar(query,id_grupo) #utiliza el metodo eliminar que recive la consulta y el id del grupo que eliminara 
        
        alumnos_inscritos = Usuario() #manda a llamar la clase usuario para usar el metodo eliminar
        
        #consulta que eliminara todos los alumnos que esten inscritos al grupo que se eliminara
        alumnos_inscritos_query_eliminar = """
            DELETE FROM datosacademicosestudiante2 WHERE id_grupo = %s
        """
        #utiliza el metodo eliminar que recibe la consulta alumnos_inscritos_query_eliminar
        alumnos_inscritos.eliminar(alumnos_inscritos_query_eliminar,id_grupo)

        #hace commit en la base de datos para actualizarla
        mysql.connection.commit()

        return jsonify({'mensaje': 'Grupo actualizado correctamente'}), 200
    except Exception as e:
        return jsonify({'mensaje' : str(e)})

#ruta que que busca todos los grupos que esten en la base de datos
@app.route('/grupo', methods=['GET'])
def mostrar_datos():
    #consulta que busca todos los datos de cada grupo
    query = """
        SELECT id, nombre, cuatrimestre, salon, anio_escolar, materia FROM grupos WHERE MatriculaProf = %s
    """
    #guarda la matricula del profe en la sesion para mostrar todos los grupos que esten relacionados por el profesor que ha iniciado sesion
    usuario_sesion = session['usuario']
    mostrar_grupos = Usuario() #manda a llamar la clase usuario para usar el metodo buscar que busca los datos de los grupos en la base de datos
    grupos = mostrar_grupos.buscar(query,usuario_sesion)
    print(f"estos son los grupos encontrados{grupos}") 
    
    resultados = []

    # Paso 2: Por cada grupo, buscar el nombre de la materia
    for grupo in grupos:
        id_grupo, nombre, cuatrimestre, salon, anio_escolar, id_materia = grupo

        query_materia = "SELECT Nombre_Materia FROM materia WHERE Clave_Materia = %s"
        materia_resultado = mostrar_grupos.buscar(query_materia, (id_materia,))
        nombre_materia = materia_resultado[0][0] if materia_resultado else "Sin materia"

        resultados.append({
            'id': id_grupo,
            'nombre': nombre,
            'cuatrimestre': cuatrimestre,
            'salon': salon,
            'anio_escolar': anio_escolar,
            'materia': nombre_materia
        })

    return jsonify(resultados)



#ruta de inicio de sesion 
@app.route('/', methods=['POST'])
def login_usuario():
    #recibe la matricula y la contraseña ingresada por el usuario y lo guarda en la sesion
    matricula_logueada = request.form.get('matricula')
    contraseña = request.form.get('contraseña')
    
    session['contraseña'] = contraseña
    
    #condicional que evalua la primera letra de la matricula que el usuario ingreso
    if matricula_logueada.startswith('A'):
        session['alumno'] = matricula_logueada
        #si la matricula empieza con la letra A crea una consulta para buscar esa matricula y la contraseña en la tabla iniciarsesion
        query = """
            SELECT * FROM iniciarsesion WHERE Matricula = %s AND Contrasena = %s
        """
        usuario_logueado = Usuario()#manda a llamar la clase Usuario para usar el metodo seleccion que recibe la consulta y retorna el resultado
        resultado = usuario_logueado.seleccion(query,matricula_logueada,contraseña)
 
        #si encuentra al usuario redireccionara al usuario para mostrar el feed del alumno
        if resultado:
            return redirect(url_for('mostrar_alumno_feed'))
        else:
            #si no, muestra el mensaje usuario no encontrado y retorna al login
            flash('Usuario no encontrado')
            return redirect(url_for('mostrar_login_feed'))
        
    elif matricula_logueada.startswith('P'):
        session['usuario'] = matricula_logueada
        #si la matricula empieza con P crea un query que busca la matricula y la contraseña en la tabla profesor y repite le mismo metodo que el usuario
        query =  """
            SELECT * FROM profesor WHERE MatriculaProf = %s AND Contraseña = %s
        """
        usuario_logueado = Usuario()
        resultado = usuario_logueado.seleccion(query,matricula_logueada,contraseña)

        if resultado:
            return redirect(url_for('mostrar_teacher_feed'))
        else:
            flash('Usuario no encontrado')
            return redirect(url_for('mostrar_login_feed'))
    
        

#ruta que busca a un alumno por matricula cuando el profesor la ingresa y da click en el boton buscar utiliza la clase usuario y el metodo seleccion
@app.route('/buscar', methods=['POST'])
def alumno():
    matricula_buscar = request.form.get('matricula')
    alumno_buscar = Usuario()
    query = """
        SELECT * FROM datosgeneralesestudiante WHERE Matricula = %s
    """
    resultado = alumno_buscar.buscar(query,matricula_buscar)
    print(f"Resultado: {resultado}")
    
    #si encuantra al usuario renderizara el feed del profesor con el la matricula del alumno y su nombre complet0
    if resultado:
        alumno = resultado[0]  
        nombre = alumno[1]
        apellidoPaterno = alumno[2]
        apellidoMaterno = alumno[3]
        mat = alumno[0]
        
    else:
        nombre = apellidoPaterno = apellidoMaterno = mat = ''
        
        
    #renderiza el feed del porfesor con la informacion del alumno que busco
    return render_template(
        'teacher-feed.html',
        nombre=nombre,
        mat=mat,
        apellidoPaterno=apellidoPaterno,
        apellidoMaterno=apellidoMaterno,
        
    )


#ruta que edita un grupo cuando se da click en el lapiz color morado
@app.route('/grupo/editar' , methods = ['PUT'])
def actualizar_grupo():
    try:
        datos_actualizados = request.json #recibe los datos actualizados desde JavaScript en formato Json
        cursor = mysql.connection.cursor() 
        datos_actualizados.get('nombre')
        #consulta que actualiza el grupo con el id que recibio de JavaScript
        query = """ 
                UPDATE grupos
                SET nombre = %s,
                cuatrimestre = %s,
                salon = %s,
                anio_escolar = %s,
                materia = %s
                WHERE id = %s
                """
        
        #ejecuta la consulta con los datos actualizados
        cursor.execute(query , (datos_actualizados.get('nombre'), datos_actualizados.get('cuatrimestre'), datos_actualizados.get('salon'), datos_actualizados.get('anio_escolar'), datos_actualizados.get('materia'), datos_actualizados.get('id')))
        mysql.connection.commit()#hace commit en la bd para actualizar la tabla
        return jsonify({'mensaje': 'Grupo actualizado correctamente'}), 200
    except Exception as e:
        print(f"Error {str(e)}")
        return jsonify({'mensaje': str(e)}),500

#ruta que crea un grupo, recibe los datos del grupo desde JavaScript en formato Json
@app.route('/grupo/crear', methods=['POST'])
def crear_grupo():
    try:
        if request.method == 'POST':
            nombre = request.form.get('nombre_grupo')  #recibe el nombre
            cuatrimestre = request.form.get('cuatrimestre') #recibe el cuatrimestre
            salon = request.form.get('salon') #recibe el salon
            anio = request.form.get('año_escolar')   #recibe el año 
            materia = request.form.get('materia') #recibe la materia


            #crea una consulta para insertar los datos recibidos para meterlos a la base de datos con la matricula del profesor
            cursor = mysql.connection.cursor()
            query = """
                INSERT INTO grupos (nombre, cuatrimestre, salon, anio_escolar, materia , MatriculaProf)
                VALUES (%s, %s, %s, %s, %s , %s)
            """
            #guarda los datos en una coleccion y saca la matricula del profesor de la sesion que previamente guardamos
            valores = (nombre,cuatrimestre,salon,anio,materia,session['usuario'])
            #ejecuta la consulta con los valores
            cursor.execute(query, valores)

            
            mysql.connection.commit()
            cursor.close()
            print(f"Grupo creado: {nombre}, {cuatrimestre}, {salon}, {anio}, {materia}")

            return  redirect(url_for('mostrar_teacher_feed'))
    except Exception as e:
        return jsonify({'mensaje': str(e)})
    


#ruta alumnos que muestra todos  los alumnos que esten inscritos a los grupos creados por el profesor que inicio sesion
@app.route('/alumnos', methods=['POST'])
def mostrar_calificaciones_alumnos():
    datos_recibidos = request.get_json()
    id_grupo = datos_recibidos.get('id')#saca el id del grupo
    cursor = mysql.connection.cursor()
    
    #consulta que busca a los alumnos que su clave foranea sea el id del grupo que previamente recibimos
    query = """
        SELECT * FROM datosacademicosestudiante2
        WHERE id_grupo = %s
    """   
    cursor.execute(query, (id_grupo,)) #ejecuta la consulta
    resultados = cursor.fetchall() #recibe todos los resultaods
    print(resultados) #imprime los resultados

    # convierte los resultaodos a json y lo envia al frontend para mostrarlos
    columnas = [col[0] for col in cursor.description]
    datos_json = [dict(zip(columnas, fila)) for fila in resultados]
    return jsonify(datos_json)



#ruta que inscribe a los alumnos a un grupo
@app.route('/alumno/inscribir', methods=['POST'])
def inscribir_alumno():
    try:
        datos = request.get_json() #recibe la matricula del alumno que sera inscrito a un grupo y el id del grupo al que sera pertenecera el alumno
        matricula = datos.get('matriculaAlumno')
        id_grupo = datos.get('nombreGrupo')

        cursor = mysql.connection.cursor()

        # Obtener nombre completo del alumno de la tabla datosgeneralesestudiante 
        query = """
            SELECT Nombre, A_Paterno, A_Materno 
            FROM datosgeneralesestudiante 
            WHERE Matricula = %s
        """
        cursor.execute(query, (matricula,))
        nombre_completo = cursor.fetchone()  

        # Obtener cuatrimestre del grupo de la tabla grupos
        cuatrimestre_grupo_query = """
            SELECT cuatrimestre 
            FROM grupos 
            WHERE id = %s
        """
        cursor.execute(cuatrimestre_grupo_query, (id_grupo,))#ejecuta la consulta
        cuatrimestre_grupo = cursor.fetchone()#recibe el el cuatrimestre de la tabla grupos

        # Insertar en datosacademicosestudiante de esta tabla se extraeran los alumnos para mostralos en el feed del profesor
        datos_academicos_table_query = """
            INSERT INTO datosacademicosestudiante2 
            (Matricula, id_grupo, cuatrimestre, Nombre, A_Paterno, A_Materno)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        datos_academicos_table_values = (
            matricula,
            id_grupo,
            cuatrimestre_grupo[0],
            nombre_completo[0],
            nombre_completo[1],
            nombre_completo[2]
        )

        cursor.execute(datos_academicos_table_query, datos_academicos_table_values)
        mysql.connection.commit()

        return jsonify({
            'mensaje': 'Datos insertados correctamente',
            'matricula': matricula,
            'grupo': id_grupo,
            'nombre': nombre_completo[0],
            'apellidoP':nombre_completo[1],
            'apellidoM':nombre_completo[2]
        })

    except Exception as e:
        return jsonify({'error': str(e)})
    

    
@app.route("/subirCalificaciones", methods=['POST'])
def subir_calificaciones_function():
    try:
        calificaciones = request.get_json()
        print(calificaciones) 
        matricula = calificaciones.get('matricula')
        calificacion_primer_parcial = calificaciones.get('primerParcial')
        calificacion_segundo_parcial = calificaciones.get('segundoParcial')
        calificacion_tercer_parcial = calificaciones.get('tercerParcial')
        examen_extraordinario = calificaciones.get('examenExtraordinario') 
        calificacion_final = calificaciones.get('calificacionFinal')
        nombre_de_lamateria = calificaciones.get('materia')
        cuatrimestre = calificaciones.get('cuatrimestre')
        matricula_profesor = session['usuario']

        usuario = Usuario()
        query = """
            SELECT Clave_Materia FROM materia WHERE Nombre_Materia = %s
        """
        materia_id = usuario.buscar(query,nombre_de_lamateria) 
        values = (
            matricula,
            materia_id,
            matricula_profesor,
            calificacion_primer_parcial,
            calificacion_segundo_parcial,
            calificacion_tercer_parcial,
            calificacion_final,
            examen_extraordinario,
            cuatrimestre
        )

        subir_calificaciones = Usuario()

        query = """
            SELECT * FROM calificaciones_cuatri WHERE cuatrimestre = %s
        """
        resultado = subir_calificaciones.buscar(query, (cuatrimestre,))
        
        if not resultado:
            query = """
                INSERT INTO calificaciones_cuatri (Matricula, materia, MatriculaProf, P1, P2, P3, CF, EE, cuatrimestre)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            print(subir_calificaciones.insercion(query,values))
            return redirect(url_for('mostrar_teacher_feed')) 
        else:
            query = """
                UPDATE calificaciones_cuatri
                SET P1 = %s,
                    P2 = %s,
                    P3 = %s,
                    EE = %s
                WHERE Matricula = %s
            """
            valores = (
                calificacion_primer_parcial,
                calificacion_segundo_parcial,
                calificacion_tercer_parcial,
                examen_extraordinario,
                matricula
            )
            print(subir_calificaciones.insercion(query, valores))
            return redirect(url_for('mostrar_teacher_feed'))  

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)})
    

@app.route('/materias', methods=['GET'])
def obtener_materias():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT Clave_Materia, Nombre_Materia FROM materia")
        materias = cursor.fetchall()

        lista_materias = []
        for materia in materias:
            lista_materias.append({
                'clave': materia[0],
                'nombre': materia[1]
            })

        return jsonify(lista_materias)
    except Exception as e:
        return jsonify({'error': str(e)})
    






    

@app.route('/teacher-feed') #ruta para renderizar el feed del profesor
def mostrar_teacher_feed():
    return render_template('teacher-feed.html')

@app.route('/main-feed')#ruta para renderizar el feed del alumno
def mostrar_alumno_feed():
    return render_template('main-feed.html')

@app.route('/login')#ruta para renderizar el feed del login
def mostrar_login_feed():
    return render_template('login.html')

@app.route('/exit' , methods = ['POST']) #ruta para renderizar el login cuando se cierre sesion
def exit():
    return render_template('login.html')





if __name__ == '__main__':
    app.run(debug=True)
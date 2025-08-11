from flask import Flask , render_template , flash , redirect , url_for , jsonify ,request,current_app,send_file #importa el framework de flask y varias funcionalidades de este framework
from flask_mysqldb import MySQL #importa la biblioteca de mysql para trabajar con flask
from flask.globals import session #importa las sessiones de flask
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
from flask_cors import CORS
from reportlab.lib.utils import ImageReader
import io
import matplotlib
matplotlib.use('Agg')
from reportlab.lib.pagesizes import letter
import os
 

app = Flask(__name__) #inicia la aplicacion de flask
CORS(app, origins=["http://127.0.0.1:5000", "http://localhost:5000"])
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


#ruta que que elimina un grupo de la base de datos cuando se le hace una peticion desde el Frontend
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
        grupo_eliminado = Usuario() 
        grupo_eliminado.eliminar(query,id_grupo) 
        
        alumnos_inscritos = Usuario() 
        
        #consulta que eliminara todos los alumnos que esten inscritos al grupo que se eliminara
        alumnos_inscritos_query_eliminar = """
            DELETE FROM inscripciones WHERE id_grupo = %s
        """
        #utiliza el metodo eliminar que recibe la consulta alumnos_inscritos_query_eliminar
        alumnos_inscritos.eliminar(alumnos_inscritos_query_eliminar,id_grupo)

        #hace commit en la base de datos para actualizarla
        mysql.connection.commit()

        return jsonify({'mensaje': 'Grupo actualizado correctamente'}), 200
    except Exception as e:
        return jsonify({'mensaje' : str(e)})
    
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
        


@app.route('/grupo', methods=['GET'])
def mostrar_datos():
    query = "SELECT * FROM profesores_info WHERE matricula = %s"
    usuario_sesion = session.get('usuario')
    mostrar_grupos = Usuario()
    grupos = mostrar_grupos.buscar(query, (usuario_sesion,))

    
    columnas = ['matricula', 'nombre', 'apellidoPaterno', 'apellidoMaterno', 'especialidad',
                'idGrupo', 'nombreGrupo', 'cuatrimestre', 'salon', 'anioEscolar', 'materia']

    resultados = []
    for fila in grupos:
        resultado = dict(zip(columnas, fila))
        resultados.append(resultado)

    return jsonify(resultados)
    
        

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

#ruta que crea un grupo, recibe los datos del grupo desde el frontend en formato Json
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
        SELECT * FROM inscripciones
        WHERE id_grupo = %s
    """   
    cursor.execute(query, (id_grupo,)) #ejecuta la consulta
    resultados = cursor.fetchall() #recibe todos los resultaods
     #imprime los resultados

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
            INSERT INTO inscripciones 
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

        user = Usuario()
        carrera = user.buscar("""SELECT nombre FROM grupos WHERE id = %s""",(id_grupo,))
        user.insercion("""UPDATE datosacademicosestudiante SET cuatrimestre = %s,carrera = %s WHERE Matricula = %s""",(cuatrimestre_grupo[0],carrera[0][0],matricula))

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

        # Extraer datos del JSON
        matricula = calificaciones.get('matricula')
        p1 = calificaciones.get('primerParcial')
        p2 = calificaciones.get('segundoParcial')
        p3 = calificaciones.get('tercerParcial')
        ee = calificaciones.get('examenExtraordinario')
        cf = calificaciones.get('calificacionFinal')
        materia_nombre = calificaciones.get('materia')
        cuatrimestre = calificaciones.get('cuatrimestre')
        id_grupo = calificaciones.get('id')
        estado = calificaciones.get('estado')

        # Verificar sesión activa
        matricula_profesor = session.get('usuario')
        if not matricula_profesor:
            return jsonify({'error': 'Sesión no activa'})

        # Obtener ID de la materia
        usuario = Usuario()
        materia_resultado = usuario.buscar(
            "SELECT Clave_Materia FROM materia WHERE Nombre_Materia = %s",
            (materia_nombre,)
        )
        if not materia_resultado:
            return jsonify({'error': 'Materia no encontrada'})
        materia_id = materia_resultado[0][0]

        subir_calificaciones = Usuario()

        # Verificar si ya existen calificaciones para ese alumno, cuatrimestre y materia
        resultado = subir_calificaciones.buscar("""
            SELECT * FROM calificaciones_cuatri 
            WHERE cuatrimestre = %s AND Matricula = %s AND materia = %s
        """, (cuatrimestre, matricula, materia_id))

        if not resultado:
            query = """
                INSERT INTO calificaciones_cuatri 
                (Matricula, materia, MatriculaProf, P1, P2, P3, CF, EE, cuatrimestre, id_grupo,estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s)
            """
            values = (matricula, materia_id, matricula_profesor, p1, p2, p3, cf, ee, cuatrimestre, id_grupo ,estado)
        else:
            query = """
                UPDATE calificaciones_cuatri
                SET P1 = %s, P2 = %s, P3 = %s, CF = %s, EE = %s
                WHERE Matricula = %s AND materia = %s AND cuatrimestre = %s
            """
            values = (p1, p2, p3, cf, ee, matricula, materia_id, cuatrimestre)

        print(subir_calificaciones.insercion(query, values))
        return redirect(url_for('mostrar_teacher_feed'))

    except Exception as e:
        print("Error al subir calificaciones:", e)
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
    

@app.route('/generar_pdf', methods=['POST'])
def generar_pdf():
    try:
        datos = request.get_json()
        id = datos.get('id')
        
        query = "SELECT Matricula, CF FROM calificaciones_cuatri WHERE id_grupo = %s"
        clase = Usuario()
        resultados = clase.buscar(query, (id,))

        grupo_query = """
            SELECT * FROM grupos WHERE id = %s 
        """

        resultados_grupos = clase.buscar(grupo_query,(id,))
        materia = clase.buscar("""SELECT Nombre_Materia FROM materia WHERE Clave_Materia = %s""",(resultados_grupos[0][5]))
        profesor = clase.buscar("""SELECT Nombre,A_Paterno,A_Materno FROM profesor WHERE MatriculaProf = %s""",(resultados_grupos[0][6]))
        print(profesor)
        
        

        cursor  = mysql.connection.cursor()
        nombres = []
        for matricula_cf in resultados:
            matricula = matricula_cf[0]
            nombre_completo_query = """
                SELECT Nombre,A_Paterno,A_Materno FROM datosgeneralesestudiante WHERE Matricula = %s
            """
            cursor.execute(nombre_completo_query,(matricula,))
            resultado = cursor.fetchone()
            nombre_completo = " ".join(resultado)
            nombres.append(nombre_completo)


        pdf = canvas.Canvas("reporte.pdf", pagesize=letter)
        ruta_pdf = os.path.join(current_app.root_path, 'reporte.pdf')
        pdf = canvas.Canvas(ruta_pdf, pagesize=letter)
        pdf.setFont("Helvetica-Bold", 10)
        ruta_imagen = os.path.join(current_app.root_path, "static", "images", "logo_estado_mexico.jpeg")
        pdf.drawImage(ruta_imagen, 40, 700, width=200, height=100)

        pdf.drawString(210, 710, "ACTA DE CALIFICACIONES FINALES")

        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(120, 700, "Programa Educativo: ")
        pdf.drawString(120, 680, f"Asignatura: {materia[0][0]} ")
        pdf.drawString(120, 660, f"Profesor: {profesor[0][0]} {profesor[0][1]} {profesor[0][2]}")
        pdf.drawString(380, 680, f"Cuatrimestre: {resultados_grupos[0][2]} {resultados_grupos[0][4]} ")
        pdf.drawString(380, 660, f"Grupo: {resultados_grupos[0][1]} ")

        y = 620
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(100 ,y , "No.")
        pdf.drawString(160, y, "Matrícula")
        pdf.drawString(250,y,"Nombre del Estudiante")
        pdf.drawString(400, y, "Calificación Total")
        pdf.line(80, y-2, 500, y-2)
        contador = 0
        pdf.setFont("Helvetica", 9)
        y -= 20
        no = 0
        for matricula, calificacion in resultados:
            no +=1
            pdf.drawString(100, y, str(no))
            pdf.drawString(160, y, str(matricula))
            pdf.drawString(250,y,str(nombres[contador]))
            pdf.drawString(430, y, str(calificacion))
            contador += 1
            y -= 25

        y_linea = 100
        longitud_linea = 130 

        pdf.setFont("Helvetica",8)
        pdf.drawString(170,130,f"{profesor[0][0]} {profesor[0][1]} {profesor[0][2]}")

        x1_profesor = 150
        x2_profesor = x1_profesor + longitud_linea
        pdf.line(x1_profesor, y_linea, x2_profesor, y_linea)
        
        texto_profesor = "Firma del Profesor"
        ancho_texto = pdf.stringWidth(texto_profesor, "Helvetica", 9)
        x_texto_profesor = x1_profesor + (longitud_linea - ancho_texto) / 2
        pdf.setFont("Helvetica", 9)
        pdf.drawString(x_texto_profesor, y_linea - 20, texto_profesor)

        x1_tutor = 370
        x2_tutor = x1_tutor + longitud_linea
        pdf.line(x1_tutor, y_linea, x2_tutor, y_linea)

        texto_tutor = "Firma del Tutor"
        ancho_texto_tutor = pdf.stringWidth(texto_tutor, "Helvetica", 9)
        x_texto_tutor = x1_tutor + (longitud_linea - ancho_texto_tutor) / 2
        pdf.drawString(x_texto_tutor, y_linea - 20, texto_tutor)
 
        pdf.save()
        ruta = "reporte.pdf"
        return send_file(
            ruta_pdf,
            as_attachment=True,
            download_name="acta.pdf",
            mimetype="application/pdf"
        )
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)})
    
#calificaciones_cuatri
#datosgeneralesdelestudiante
#profesor opcional
#datosacademicosestudiante

from flask import jsonify, session

@app.route("/datos/alumno", methods=['GET'])
def mostrar_datos_alumno():
    try:
        matricula_alumno = 'A00000001'
        user = Usuario()

        datos_generales_estudiante = user.buscar("""
            SELECT * FROM datosgeneralesestudiante WHERE Matricula = %s
        """, (matricula_alumno,))
        
        datos_academicos_estudiante = user.buscar("""
            SELECT * FROM datosacademicosestudiante WHERE Matricula = %s
        """, (matricula_alumno,))
        

        # Construir el JSON de respuesta
        respuesta = {
            "datos_generales": datos_generales_estudiante[0] if datos_generales_estudiante else {},
            "datos_academicos": datos_academicos_estudiante[0] if datos_academicos_estudiante else {},
            
        }

        return jsonify(respuesta)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/calificacionesCuatrimestre', methods=['POST'])
def calificaciones_por_cuatrimestre():
    try:
        matricula = session.get('alumno')
        datos = request.get_json()
        cuatrimestre = datos.get('cuatrimestre')
        user = Usuario()

        # Usar la vista calificaciones
        calificaciones = user.seleccion("""
            SELECT clave_materia, nombre_materia, profesor, primerParcial, segundoParcial, tercerParcial, calificacionFinal, extraordinario, estado
            FROM calificaciones
            WHERE matricula = %s AND cuatrimestre = %s
        """, matricula, cuatrimestre)

        resultados = []
        for cal in calificaciones:
            resultados.append({
                "clave_materia": cal[0],
                "nombre_materia": cal[1],
                "profesor": cal[2],
                "calificacion": {
                    "primer_parcial": cal[3],
                    "segundo_parcial": cal[4],
                    "tercer_parcial": cal[5],
                    "CF": cal[6],
                    "extraordinario": cal[7],
                    "estado": cal[8]
                }
            })

        return jsonify(resultados)
    
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/grafica-pdf', methods=['POST'])
def grafica_pdf():
    try:
        #  Obtener los datos enviados en formato JSON 
        datos = request.get_json()
        id = datos.get('id')

        #  Crear instancia para consultar la base de datos 
        user = Usuario()

        #  Consultar las calificaciones del grupo con el id recibido
        calificaciones = user.buscar("""
            SELECT P1, P2, P3, CF, EE FROM calificaciones_cuatri WHERE id_grupo = %s
        """, (id,))


        #  Si no hay calificaciones para ese grupo, devolver mensaje y código 404
        if not calificaciones:
            return jsonify({"mensaje": "No hay datos para este grupo"}), 404

        # 6. Separar cada tipo de calificación en listas individuales y convertir a float
        P1 = [float(row[0]) for row in calificaciones]
        P2 = [float(row[1]) for row in calificaciones]
        P3 = [float(row[2]) for row in calificaciones]
        CF = [float(row[3]) for row in calificaciones]
        EE = [float(row[4]) for row in calificaciones]

        # 7. Calcular promedio de cada tipo de calificación
        promedios = {
            'P1': sum(P1) / len(P1),
            'P2': sum(P2) / len(P2),
            'P3': sum(P3) / len(P3),
            'CF': sum(CF) / len(CF),
            'EE': sum(EE) / len(EE),
        }

        # 8. Preparar las etiquetas y valores para graficar
        etiquetas = list(promedios.keys())
        valores = list(promedios.values())

        # 9. Crear figura con matplotlib y graficar barras
        plt.figure(figsize=(6, 4))  # Tamaño figura (6x4 pulgadas)
        plt.bar(etiquetas, valores, color='skyblue')  # Barras color azul claro
        plt.title('Promedio de calificaciones')  # Título de la gráfica
        plt.ylim(0, 10)  # Limitar eje Y de 0 a 10


        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='PNG')  # Guardar en formato PNG
        plt.close()  
        img_buffer.seek(0)  

        # 11. Crear buffer para el PDF y canvas con tamaño carta
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)

        # 12. Leer la imagen desde el buffer para insertarla en el PDF
        img = ImageReader(img_buffer)
        # 13. Dibujar la imagen en el PDF (posición X=50, Y=500, tamaño 500x300)
        c.drawImage(img, 50, 500, width=500, height=300)

        # 14. Finalizar página y guardar el PDF en el buffer
        c.showPage()
        c.save()

        pdf_buffer.seek(0)  # Volver al inicio del buffer para enviar

        # 15. Enviar el PDF generado como archivo para descargar
        return send_file(pdf_buffer, mimetype='application/pdf', download_name='grafica.pdf')

    except Exception as e:
        # 16. Si hay un error, imprimirlo en consola y devolverlo en JSON con código 500
        print('Error:', e)
        return jsonify({"error": str(e)}), 500
    


@app.route('/profesores', methods=['GET'])
def mostrar_profesores():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT MatriculaProf, Nombre, A_Paterno, A_Materno, especialidad 
            FROM profesor
        """)
        resultados = cursor.fetchall()

        # Convertir a lista de diccionarios para que JS reciba claves y valores
        profesores = [
            {
                "MatriculaProf": row[0],
                "Nombre": row[1],
                "A_Paterno": row[2],
                "A_Materno": row[3],
                "Especialidad": row[4]
            }
            for row in resultados
        ]

        return jsonify(profesores)
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
    session.clear()
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)


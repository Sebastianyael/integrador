const crearButton = document.getElementById('crear') //boton de crear un grupo
const modal = document.getElementById('modal') //pantalla gris que aparece detras de la carta 
const modalCard = document.getElementById('modal-card') //carta que aparece al pulsar el boton de enviar/lapiz de estidar/inscribir

const cancelar = document.getElementById('cancelar')
const enviar = document.getElementById('enviar')  //boton que envia los datos del formulario para crear un grupo

const gruposContainer = document.getElementById('grupos-resultados') //contenedor done estan los grupos

let expanded = false

const formParaInscribir = document.getElementById('div-del-form-para-inscribir')
const divSubirCalificaciones = document.getElementById('div-del-form-para-subir-calificaciones')
const divDeLaGrafica = document.getElementById('grafica-div')

const formularios = [modalCard,formParaInscribir,divSubirCalificaciones,divDeLaGrafica]
function cleanMain(form,display){
    let position = formularios.findIndex(a => a.classList.contains('on') || a.classList.contains('on-flex') )
    formularios[position].classList.replace('on' , 'off')
    formularios[position].classList.replace('on-flex' , 'off')
    form.classList.replace('off' , display)  
}


//cuando se da click en el boton de crear aparece la carta con el formulario de crear grupo y limpia las cajas de texto del formulario
crearButton.addEventListener('click' , (event) =>{
    abrirModal()
    const on = 'on'
    cleanMain(modalCard,on)
    document.getElementById('p-tittle').innerText = 'Crear Grupo';
    const iTittle = document.getElementById('i-tittle');
    iTittle.classList.replace('fa-regular', 'fa-solid');
    iTittle.classList.replace('fa-pencil', 'fa-user');

    const actualizarButton = document.getElementById('actualizar');
    const enviarButton = document.getElementById('enviar')
    if(actualizarButton.classList.contains('on-flex') == true){
        actualizarButton.classList.replace('on-flex' , 'off')
        enviarButton.classList.replace('off' , 'on-flex')
    }
    
    const nombreInput = document.getElementById('nombre-input')
    nombreInput.value = ''

    const cuatrimestreSelect = document.getElementById('cuatrimestre-select')
    cuatrimestreSelect.value = ''

    const añoInput = document.getElementById('año-input')
    añoInput.value = ''

    const salonSelect = document.getElementById('salon-select')
    salonSelect.value =  ''

    const materiaInput = document.getElementById('materia-input')
    materiaInput.value =  ''
    const form = document.getElementById('form')
    form.action = '/grupo/crear' 

    fetch('/materias')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('materia-input');
            select.innerHTML = ''
            
            data.forEach(materia => {
                const option = document.createElement('option');
                option.value = materia.clave;
                option.textContent = materia.nombre;
                select.appendChild(option);
            });
        })
        .catch(error => console.error('Error cargando materias:', error));
    
})

//funcion para abrir la carta
function abrirModal(){
    modalCard.classList.replace('close-card' , 'open-card')
    modal.classList.replace('close-modal' , 'open-modal')

}

//funcion para cerrar la carta
function cerrarModal(){
    modalCard.classList.replace('open-card' , 'close-card')
    modal.classList.replace('open-modal' , 'close-modal')
    
}

function cerrarDiv(div){
    div.classList.replace('open-card' , 'close-div')
}

function abrirDiv(div){
    div.classList.replace('close-div' , 'open-card')
}


//cuando se pulsa el boton de cancelar del formulario de crear o editar grupo se cerrara la carta
cancelar.addEventListener('click' , () =>{
    cerrarModal()
})

//funcion para editar un grupo
//hace una peticion http con fecth hacia la ruta /grupo/editar de flask para sacar la informacion de la base de datos
//del grupo que se quiera editar y rrellena los inputs con la informacion del grupo
//recibe los datos en formato json y envia el id del grupo en formato json
function editGroup(grupo) {
    abrirModal(); // abre el modal
    
    const select = document.getElementById('materia-input');
    select.innerHTML = ''
    fetch('/materias')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('materia-input');
            data.forEach(materia => {
                const option = document.createElement('option');
                option.value = materia.clave;
                option.textContent = materia.nombre;
                select.appendChild(option);
            });
        })
        .catch(error => console.error('Error cargando materias:', error));
    
    // Rellenar inputs
    document.getElementById('p-tittle').innerText = 'Editar Grupo';
    const iTittle = document.getElementById('i-tittle');
    iTittle.classList.replace('fa-regular', 'fa-solid');
    iTittle.classList.replace('fa-user', 'fa-pencil');

    const nombreInput = document.getElementById('nombre-input');
    const cuatrimestreSelect = document.getElementById('cuatrimestre-select');
    const añoInput = document.getElementById('año-input');
    const salonSelect = document.getElementById('salon-select');
    const materiaInput = document.getElementById('materia-input');
    

    // Cargar datos del grupo
    nombreInput.value = grupo.nombreGrupo;
    cuatrimestreSelect.value = grupo.cuatrimestre;
    añoInput.value = grupo.anioEscolar;
    salonSelect.value = grupo.salon;
    materiaInput.value = grupo.materia;
    console.log(grupo.materia)

    const actualizarButton = document.getElementById('actualizar');
    const enviarButton = document.getElementById('enviar')
    if(enviarButton.classList.contains('on-flex') == true){
        enviarButton.classList.replace('on-flex' , 'off')
        actualizarButton.classList.replace('off' , 'on-flex')
    }

    // Eliminar cualquier listener previo
    const nuevoBoton = actualizarButton.cloneNode(true);
    actualizarButton.parentNode.replaceChild(nuevoBoton, actualizarButton);

    nuevoBoton.addEventListener('click', (e) => {
        e.preventDefault();
        fetch('/grupo/editar', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id: grupo.idGrupo,
                nombre: nombreInput.value,
                cuatrimestre: cuatrimestreSelect.value,
                salon: salonSelect.value,
                anio_escolar: añoInput.value,
                materia: materiaInput.value
            })
        })
        .then(res => res.json())  
        .then(data => {
            console.log("Grupo actualizado:", data); 
            location.reload()
        
        })
        .catch(error => console.error('Error:', error));
    });
}


/*Funcion que elimina un grupo cuando se da click en el boton rojo 
cuando se da click a ese boton se envia a una ruta flask /grupo/eliminar con el id del grupo a eliminar
*/
function deleteGroup(grupoId){
        fetch('/grupo/eliminar', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id: grupoId
            })
        })
        .then(res => res.json())
        .then(data => {
            console.log('Grupo eliminado', data);
            location.reload(    )
        })
        .catch(error => console.error('Error', error));
}

/*
Cuando se carga la pagina del profesor hace una peticion a una ruta flask /grupo para traer
todos los grupos que el profesor ha creado 
y crea contenedor div para mostrar cada grupo en pantalla y etiquetas p de texto para mostrar la info del grupo
recibe todo en formato json 
*/

const alumnos = document.getElementById('alumnos')
addEventListener('DOMContentLoaded' , () =>{
    const pGruposDe = document.getElementById('grupos-de')
    

    fetch('/grupo' , {
        method: 'get'
    })
        .then(res => res.json())
        .then(grupos => {
            console.log(grupos)
            
            const gruposContainer = document.getElementById('grupos-resultados')
            grupos.forEach(grupo => {
                const nombreCompleto = `Grupos de ${grupo.nombre} ${grupo.apellidoPaterno} ${grupo.apellidoMaterno}`
                pGruposDe.innerText = nombreCompleto
                const groupDiv = document.createElement('button')
                groupDiv.className = 'grupos-container'
                groupDiv.id = 'grupo-div'

                const div = document.createElement('div')
                div.className = 'grupos-container2'

                const nombre = document.createElement('p')
                const grafica = document.createElement('button')
                const iconGrafica = document.createElement('i')
                iconGrafica.classList.add('fa-solid')
                iconGrafica.classList.add('fa-chart-simple')
                grafica.appendChild(iconGrafica)
                grafica.className = 'grafica-button'
                grafica.addEventListener('click' , () =>{
                    generarGrafica(grupo.idGrupo)
                })
                const cuatrimestre = document.createElement('p')
                const profesorAsignado = document.createElement('p')
                const añoEscolar = document.createElement('p')
                const materia = document.createElement('p')
                const updateButton = document.createElement('button')
                const pencil = document.createElement('i')
                const eliminarButton = document.createElement('button')
                const xIcon = document.createElement('i')
                const arrow = document.createElement('button')
                const arrowIcon = document.createElement('i')
                arrowIcon.classList.add('fa-solid')
                arrowIcon.classList.add('fa-file')
                arrow.className = 'pdf-button'
                arrow.appendChild(arrowIcon)
                arrow.id = 'arrow-button'
                arrow.addEventListener('click' , () =>{
                    descargarPDF(grupo.idGrupo)
                })
                const idGrupo = document.createElement('p')
                idGrupo.textContent = grupo.idGrupo

                div.addEventListener('click' , () =>{
                    alumnos.innerHTML = ''
                    alumnosEnGrupo(grupo.idGrupo , grupo.materia , grupo.cuatrimestre)
            
                })
                
                xIcon.classList.add('fa-solid')
                xIcon.classList.add('fa-x')
                eliminarButton.className = 'eliminar'
                eliminarButton.addEventListener('click', () =>{
                    deleteGroup(grupo.idGrupo)
                })

                updateButton.addEventListener("click", () => {
                    editGroup(grupo)
                })
                pencil.className = 'updateButton'
                pencil.classList.add('fa-solid')
                pencil.classList.add('fa-pencil')

                nombre.textContent = grupo.nombreGrupo
                cuatrimestre.textContent = grupo.cuatrimestre
                profesorAsignado.textContent = grupo.salon
                añoEscolar.textContent = grupo.anioEscolar
                materia.textContent = grupo.materia

                updateButton.appendChild(pencil)
                
                eliminarButton.appendChild(xIcon)
                div.appendChild(idGrupo)
                div.appendChild(nombre)
                div.appendChild(cuatrimestre)
                div.appendChild(profesorAsignado)
                div.appendChild(añoEscolar)
                div.appendChild(materia)
                div.appendChild(updateButton)
                div.appendChild(grafica)
                div.appendChild(arrow)
                div.appendChild(eliminarButton)  
                groupDiv.appendChild(div)
                gruposContainer.appendChild(groupDiv)
                
            });

            
        })
        .catch(error => console.error(error))
})

function generarGrafica(id){
    console.log(id)
    fetch('http://localhost:5000/grafica-pdf', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: id })
        })
        .then(response => {
            if (!response.ok) throw new Error('Error al obtener PDF');
            return response.blob();
            
        })
        .then(blob => {
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'grafica.pdf';
            document.body.appendChild(a);
            a.click();
            a.remove();
            URL.revokeObjectURL(url);
        })
        .catch(console.error);
}



function descargarPDF(id , grupo){
    fetch('/generar_pdf', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        id: id,
        grupoFetch: grupo
    })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al generar el PDF');
        }
        return response.blob();  
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'acta.pdf'; // nombre del archivo descargado
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url); // liberar memoria
    })
    .catch(error => {
        console.error('Error:', error);
    });

}


function subirCalificaciones(alumnoMatricula,grupoMateria,cuatrimestre,grupoId){

    abrirModal()
    abrirDiv(formParaInscribir)
    const onFlex = 'on-flex'
    cleanMain(divSubirCalificaciones,onFlex)

    const cancelarDivCalificaciones = document.getElementById('cancelar-div-calificaciones')
    cancelarDivCalificaciones.addEventListener('click' , () =>{
        cerrarDiv(divSubirCalificaciones)
        cerrarModal()
        
    })

    
    const subirButton = document.getElementById('subir')

    subirButton.addEventListener('click' ,() =>{
        const primerParcial = document.getElementById('primer-parcial').value
        const segundoParcial = document.getElementById('segundo-parcial').value
        const tercerParcial = document.getElementById('tercer-parcial').value
        const examenExtraordinario = document.getElementById('examen-extraordinario').value
        const calificacionFinal = document.getElementById('calificacion-final').value
        let arrayDeCalificacionesSting = [primerParcial,segundoParcial,tercerParcial,examenExtraordinario,calificacionFinal]
        let arrayDeCalificacionesFloat =  arrayDeCalificacionesSting.map(value => parseFloat(value))
        const estado = document.getElementById('estado')
        

             fetch("/subirCalificaciones" , {
             method: 'POST' , 
             headers : {
                 'Content-Type' : 'application/json'
             },
             body: JSON.stringify({
                 matricula: alumnoMatricula,
                 materia:grupoMateria,
                 cuatrimestre:cuatrimestre,
                 id:grupoId,
                 primerParcial : arrayDeCalificacionesFloat[0],
                 segundoParcial: arrayDeCalificacionesFloat[1],
                 tercerParcial: arrayDeCalificacionesFloat[2],
                 examenExtraordinario: arrayDeCalificacionesFloat[3],
                 calificacionFinal: arrayDeCalificacionesFloat[4],
                 estado:estado.value
                
             })
         })
         .then(response => alert('Calificaciones asignadas'))
         .then(data => {
            location.reload();
         })
         .catch(error => console.error('Error', error) )

        
         cerrarDiv(divSubirCalificaciones)
         cerrarModal()
        
         })
    }







/*
    funcion para mostrar los alumnos que estan inscritos por cada grupo que el profesor a creado
    hace una peticion http a la ruta flask /alumnos y crea un contenedor div para cada alumno en el grupo

*/ 
function alumnosEnGrupo(grupoId , grupoMateria,grupoCuatrimestre){
    fetch('/alumnos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id: grupoId
        })
    })
    .then(response => response.json())
    .then(alumnos => {
        console.log(alumnos);
        const Alumnos = document.getElementById('alumnos')
        
        
        
        alumnos.forEach(alumno =>{
            const divAlumno = document.createElement('button')
            divAlumno.className = 'alumno-en-el-grupo'
            divAlumno.id = 'div-del-alumno'

            divAlumno.addEventListener('click' , () =>{
                subirCalificaciones(alumno.Matricula,grupoMateria,grupoCuatrimestre,grupoId)
            })

            const matricula = document.createElement('p')
            const nombre = document.createElement('p')
            const apellidoPaterno = document.createElement('p')
            const apellidoMaterno = document.createElement('p')
            const cuatrimestre = document.createElement('p')
            

            matricula.textContent = alumno.Matricula
            nombre.textContent = alumno.Nombre
            apellidoPaterno.textContent = alumno.A_Paterno
            apellidoMaterno.textContent = alumno.A_Materno
            cuatrimestre.textContent = alumno.cuatrimestre

            divAlumno.appendChild(matricula)
            divAlumno.appendChild(nombre)
            divAlumno.appendChild(apellidoPaterno)
            divAlumno.appendChild(apellidoMaterno)
            divAlumno.appendChild(cuatrimestre)

            Alumnos.appendChild(divAlumno)


        })
    })
    .catch(error => console.error('Error:', error));
}

const inscribirAlumnoButton = document.getElementById('inscribir-alumno')

let modalAbierto = false 
/*
    cada que se da click en el boton del alumno aparece la carta con un campo de texto para que el profesor inscriba el alumno
*/
inscribirAlumnoButton.addEventListener('click', () => {
    modalAbierto = !modalAbierto
    abrirModal()
    abrirDiv(formParaInscribir)
    const onFlex = 'on-flex'
    cleanMain(formParaInscribir,onFlex)

    const cancelarDiv = document.getElementById('cancelar-div')
    cancelarDiv.addEventListener('click' , () =>{
        cerrarDiv(formParaInscribir)
        cerrarModal()
        
    })

    if (modalAbierto === true) {
        

        const formParaInscribir = document.getElementById('div-del-form-para-inscribir')
        formParaInscribir.classList.replace('off', 'on-flex')

        
        const pMatriculaAlumno = document.getElementById('p-matricula-alumno').innerText
        const inscribir = document.getElementById('inscribir')

        // Prevenir múltiples listeners
        inscribir.replaceWith(inscribir.cloneNode(true))
        const nuevoInscribir = document.getElementById('inscribir')


        nuevoInscribir.addEventListener('click', (e) => {
            const inputNombreGrupo = document.getElementById('input-nombre-del-grupo').value;

            if (inputNombreGrupo.trim() === '') {
                const labelError = document.getElementById('label-error');
                labelError.innerText = 'Campo vacío';
                labelError.style.color = 'red';
                e.preventDefault();
                return; 
            }

            inscribirAlumno(pMatriculaAlumno, inputNombreGrupo);
            cerrarModal();
        });
    }
});

/*
    funcion que enviar datos a un ruta flask con la matricula que el profesor busca y el id del grupo donde estara este alumno
*/
function inscribirAlumno(matriculaAlumno,nombreGrupo){
        fetch('/alumno/inscribir', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                matriculaAlumno: matriculaAlumno,
                nombreGrupo: nombreGrupo
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Respuesta del servidor:", data);
            
        })
        .catch(error => {
            console.error("Error en el fetch:", error);
        });
    }
















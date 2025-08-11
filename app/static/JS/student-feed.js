const feedMain = document.getElementById('feed-container')  //contenedor principal 
const feedNotes = document.getElementById('calificaciones-panel')   //contenedor de calificaciones
const feedHorario = document.getElementById('feed-horario') //contenedor de horario 
const feedCalendario = document.getElementById('feed-calendar') //contenedor del calendario
const feedTeacher = document.getElementById('feed-teacher') //contenedor de los profesores

const aside = document.getElementById('aside') //variable del Aside
const buttonAside = document.getElementById('bars') //boton del header 

const iconBars = document.getElementById('icon-bars')

const informaciónPersonalButton = document.getElementById('Información-personal-button')

//Botones del aside 
const home = document.getElementById('home') 
const calificaciones = document.getElementById('calificaciones') 
const horario = document.getElementById('horario')  //
const calendario = document.getElementById('calendario') 
const profesores = document.getElementById('profesores') 

let feeds = [feedMain ,  feedNotes , feedHorario , feedCalendario , feedTeacher] //array de los contenedores
const asideButtons  = [home , calificaciones , horario , calendario , profesores] //array de los botones del aside

let varBackground = document.documentElement; 
let colorClassEstado = document.documentElement;
let feedContainerWidth = document.documentElement;

//botones de las cards
const cardCalificaciones = document.getElementById('card-calificaciones')
const cardh =  document.getElementById('cardh')
const cardProfesores = document.getElementById('card-profesores')
const cardCalendario = document.getElementById('card-calendario')


//Funcion que limpia el body y pone el feed que  corresponda
function cleanMain(feed){
    let position = feeds.findIndex(a => a.classList.contains('on'))
    feeds[position].classList.replace('on' , 'off')
    feed.classList.replace('off' , 'on')
    
}


//Boton que muestra y esconde el aside
buttonAside.addEventListener('click' , () =>{
    if(aside.classList.contains('off') === true){
        aside.classList.replace('off' , 'on-flex')
        feedContainerWidth.style.setProperty('--feedContainerWidth' , '3/11')
        iconBars.classList.replace('fa-bars' , 'fa-bars-staggered')
            
    }else{
        aside.classList.replace('on-flex' , 'off')
        feedContainerWidth.style.setProperty('--feedContainerWidth' , '1/12')
        iconBars.classList.replace('fa-bars-staggered' , 'fa-bars')
    }

})


//Funcion que pone el color al boton del aside 
function classEstado(button){
     let position = asideButtons.findIndex(a => a.classList.contains('estado') === true)
     asideButtons[position].classList.remove('estado')
     button.classList.add('estado')
}


//Boton Home
home.addEventListener('click' , () => {
    cleanMain(feedMain)
    classEstado(home)
    varBackground.style.setProperty('--bg-color' , 'rgb(242, 239, 239)')
    colorClassEstado.style.setProperty('--font-color-estado' , 'rgb(36, 163, 74)')
    aside.classList.replace('on-flex' , 'off')
    feedContainerWidth.style.setProperty('--feedContainerWidth' , '1/11')
    buttonAside.classList.replace('off' , 'on')
   
})


//Boton de calificaciones
calificaciones.addEventListener('click' , () =>{
    cleanMain(feedNotes)
    classEstado(calificaciones)
    
    buttonAside.classList.add('off')
})

cardCalificaciones.addEventListener('click' , () => {
    cleanMain(feedNotes)
    classEstado(calificaciones)
    
    if(window.innerWidth  > 767){
        aside.classList.replace('off' , 'on-flex')
        
        buttonAside.classList.add('off')
    }   
    else{
        buttonAside.classList.add('on')
    }
})


//boton de horario
horario.addEventListener('click' , () =>{
    cleanMain(feedHorario)
    classEstado(horario)
  
    buttonAside.classList.add('off')
    

})

cardh.addEventListener('click' , () =>{
    cleanMain(feedHorario)
    classEstado(horario)
    if(window.innerWidth > 757){
        
        
        buttonAside.classList.add('off')
        aside.classList.replace('off' , 'on-flex')
    }
    else{
        buttonAside.classList.add('on')
    }

    
})

//boton de calendario
calendario.addEventListener('click' , () =>{
    cleanMain(feedCalendario)
    classEstado(calendario)
    
    buttonAside.classList.add('off')
})

cardCalendario.addEventListener('click' , () =>{
    cleanMain(feedCalendario)
    classEstado(calendario)
    if(window.innerWidth > 767){
        
        buttonAside.classList.add('off')
        aside.classList.replace('off' , 'on-flex')
    }
    else{
        buttonAside.classList.add('on')
    }
    
})

//Boton de profesores
profesores.addEventListener('click' , () =>{
    cleanMain(feedTeacher)
    classEstado(profesores)
   
    buttonAside.classList.add('off')
})

cardProfesores.addEventListener('click' , () =>{
    
    cleanMain(feedTeacher)
    classEstado(profesores)
    if(window.innerWidth > 767){
        
        buttonAside.classList.add('off')
        aside.classList.replace('off' , 'on-flex')
    }else{
        buttonAside.classList.add('on')
    }
    
})

document.addEventListener("DOMContentLoaded", function () {
    let fondos = document.querySelectorAll('.fondo1');

    let observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                let fondo = entry.target;
                fondo.style.backgroundImage = `url('/static/images/cal.webp')`;
                observer.unobserve(fondo); // Deja de observar después de cargar
            }
        });
    });

    fondos.forEach(fondo => {
        observer.observe(fondo);
    });
});


document.addEventListener("DOMContentLoaded", function () {
    let fondos = document.querySelectorAll('.fondo2');

    let observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                let fondo = entry.target;
                fondo.style.backgroundImage = `url('/static/images/hor.webp')`;
                observer.unobserve(fondo); // Deja de observar después de cargar
            }
        });
    });

    fondos.forEach(fondo => {
        observer.observe(fondo);
    });
});


document.addEventListener("DOMContentLoaded", function () {
    let fondos = document.querySelectorAll('.fondo3');

    let observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                let fondo = entry.target;
                fondo.style.backgroundImage = `url('/static/images/calen.webp')`;
                observer.unobserve(fondo); // Deja de observar después de cargar
            }
        });
    });

    fondos.forEach(fondo => {
        observer.observe(fondo);
    });
});


document.addEventListener("DOMContentLoaded", function () {
    let fondos = document.querySelectorAll('.fondo4');

    let observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                let fondo = entry.target;
                fondo.style.backgroundImage = `url('/static/images/prof.webp')`;
                observer.unobserve(fondo); // Deja de observar después de cargar
            }
        });
    });

    fondos.forEach(fondo => {
        observer.observe(fondo);
    });
});


document.addEventListener("DOMContentLoaded", function () {
    let fondos = document.querySelectorAll('.fondo5');

    let observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                let fondo = entry.target;
                fondo.style.backgroundImage = `url('/static/images/estudent.webp')`;
                observer.unobserve(fondo); // Deja de observar después de cargar
            }
        });
    });

    fondos.forEach(fondo => {
        observer.observe(fondo);
    });
});

addEventListener('DOMContentLoaded' , () =>{
    const nombreCompleto = document.getElementById('nombre-completo')
    const matricula = document.getElementById('matricula')
    const carrera = document.getElementById('carrera')
    const correo = document.getElementById('correo')
    
    fetch('/datos/alumno' , {
        method: 'get'
    }).then(res => res.json())
    .then(datos => {
        nombreCompleto.innerText = `${datos.datos_generales[1]} ${datos.datos_generales[2]} ${datos.datos_generales[3]}`
        matricula.innerText = `Matricula: ${datos.datos_generales[0]}`
        //carrera.innerText = `Carrera: ${datos.calificaciones[9]}`
        correo.innerText = `Correo: ${datos.datos_generales[9]}`
        
        

    })
    .catch(error => console.error(error))
})



const cuatrimestreEnviar = document.getElementById('cuatrimetre-boton')
const cuerpoTabla = document.getElementById('cuerpo-tabla')
const noMateria = document.getElementById('numer_materia')
const promedioP = document.getElementById('promedio')
cuatrimestreEnviar.addEventListener('click' , () =>{
    cuerpoTabla.innerHTML = ''
    promedioP.innerHTML = ''
    noMateria.innerHTML = ''
    const cuatrimestre = document.getElementById('cuatrimestre-select').value
    fetch('/calificacionesCuatrimestre',{
        method: 'post',
        headers:{
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            cuatrimestre: cuatrimestre
        })
    })
    .then(res => res.json())
    .then(data => {

    data.forEach(item => {
         
    const fila = document.createElement('tr');

    const materia = document.createElement('th');
    const profesor = document.createElement('th');
    const evaluacionUno = document.createElement('th');
    const evaluacionDos = document.createElement('th');
    const evaluacionTres = document.createElement('th');
    const extraordinario = document.createElement('th');
    const promedioGeneral = document.createElement('th');
    const estado = document.createElement('th');

    const cal = item.calificacion;
        promedioP.textContent = item.promedio

    materia.textContent = item.nombre_materia;
    profesor.textContent = item.profesor;
    evaluacionUno.textContent = cal.primer_parcial;
    evaluacionDos.textContent = cal.segundo_parcial;
    evaluacionTres.textContent = cal.tercer_parcial;
    extraordinario.textContent = cal.extraordinario;
    promedioGeneral.textContent = cal.CF;
    
    estado.textContent = cal.estado

    noMateria.textContent = cal.noMaterias
   
    if(estado.textContent == 'reprobado'){
        estado.style.color = 'red'
    }
    

    fila.appendChild(materia);
    fila.appendChild(profesor);
    fila.appendChild(evaluacionUno);
    fila.appendChild(evaluacionDos);
    fila.appendChild(evaluacionTres);
    fila.appendChild(promedioGeneral);
    fila.appendChild(extraordinario);
    fila.appendChild(estado);

    cuerpoTabla.appendChild(fila);

        })
    })
    .catch(error => console.error('error' , error))


})
    

informaciónPersonalButton.addEventListener('click' , () =>{
    fetch('/datos/alumno' , {
        method: 'get'
    }).then(res => res.json())
    .then(datos => {
        const matricula = document.getElementById('mat')
        const nombre =document.getElementById('nom')
        const fecha = document.getElementById('fecha')
        const estado = document.getElementById('estado')
        const rfc = document.getElementById('rfc')
        const curp = document.getElementById('curp')
        const domiciolio = document.getElementById('domicilio')

        matricula.textContent = datos.datos_generales[0]
        nombre.textContent = `Nombre ${datos.datos_generales[1]} ${datos.datos_generales[2]} ${datos.datos_generales[2]}`
        fecha.textContent = `Fecha de Nacimineto ${datos.datos_generales[4]}`
        estado.textContent = `Estado Civil ${datos.datos_generales[5]}`
        rfc.textContent = `RFC ${datos.datos_generales[6]}`
        curp.textContent = `CURP ${datos.datos_generales[7]}`
        domiciolio.textContent = `Domicilio ${datos.datos_generales[8]}`


    })
    .catch(error => console.error(error))
})

const feedTeacher__card = document.getElementById('feed-teacher__card') 

cardProfesores.addEventListener('click', () => {
    fetch('/profesores')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            data.forEach(profesor => {
                const section = document.createElement('section')
                const cortina = document.createElement('div')
                const img = document.createElement('img')
                const h1 = document.createElement('h1')
                const Pespecialidad = document.createElement('p')
                const Pcorreo = document.createElement('p')
                    
                section.classList.add('feed-teacher__card')
                cortina.classList.add('cortina')
                img.classList.add('feed-teacher__img')
                h1.textContent = `${profesor.Nombre} ${profesor.A_Paterno} ${profesor.A_Materno}`
                Pespecialidad.textContent = profesor.Especialidad

                section.appendChild(cortina)
                section.appendChild(img)
                section.appendChild(h1)
                section.appendChild(Pespecialidad)
                feedTeacher.appendChild(section)
                

            })
        })
        .catch(error => {
            console.error('Hubo un problema con la solicitud:', error);
        });
})
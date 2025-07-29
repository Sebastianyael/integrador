const feedMain = document.getElementById('feed-container')  //contenedor principal 
const feedNotes = document.getElementById('calificaciones-panel')   //contenedor de calificaciones
const feedHorario = document.getElementById('feed-horario') //contenedor de horario 
const feedCalendario = document.getElementById('feed-calendar') //contenedor del calendario
const feedTeacher = document.getElementById('feed-teacher') //contenedor de los profesores

const aside = document.getElementById('aside') //variable del Aside
const buttonAside = document.getElementById('bars') //boton del header 

const iconBars = document.getElementById('icon-bars')

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

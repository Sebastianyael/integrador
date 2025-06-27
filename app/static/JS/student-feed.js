const feedMain = document.getElementById('feed-container')
const feedNotes = document.getElementById('calificaciones-panel')
const feedHorario = document.getElementById('feed-horario')
const feedCalendario = document.getElementById('feed-calendar')
const feedTeacher = document.getElementById('feed-teacher')

let varBackground = document.documentElement;
let colorClassEstado = document.documentElement

let body = document.getElementById('body')
function cleanMain(feed){
    let feeds = [feedMain ,  feedNotes , feedHorario , feedCalendario , feedTeacher]
    let position = feeds.findIndex(a => a.classList.contains('on'))
    feeds[position].classList.replace('on' , 'off')
    feed.classList.replace('off' , 'on')
    
}


const home = document.getElementById('home')
const calificaciones = document.getElementById('calificaciones')
const horario = document.getElementById('horario')
const calendario = document.getElementById('calendario')
const profesores = document.getElementById('profesores')
function classEstado(button){
     const asideButtons  = [home , calificaciones , horario , calendario , profesores]
     position = asideButtons.findIndex(a => a.classList.contains('estado') === true)
     asideButtons[position].classList.remove('estado')
     button.classList.add('estado')
}



home.addEventListener('click' , () => {
    cleanMain(feedMain)
    classEstado(home)
    varBackground.style.setProperty('--bg-color' , 'rgb(214, 245, 224)')
    colorClassEstado.style.setProperty('--font-color-estado' , 'rgb(36, 163, 74)')
   
})




calificaciones.addEventListener('click' , () =>{
    cleanMain(feedNotes)
    classEstado(calificaciones)
    varBackground.style.setProperty('--bg-color' , 'rgb(212, 232, 247)')
    colorClassEstado.style.setProperty('--font-color-estado' , 'rgb(67, 101, 127)')
})



horario.addEventListener('click' , () =>{
    cleanMain(feedHorario)
    classEstado(horario)
    varBackground.style.setProperty('--bg-color' , 'rgb(247, 228, 212)')
    colorClassEstado.style.setProperty('--font-color-estado' , 'rgb(210, 121, 47)')
    
    

})


calendario.addEventListener('click' , () =>{
    cleanMain(feedCalendario)
    classEstado(calendario)
    varBackground.style.setProperty('--bg-color' , 'rgb(228, 212, 247)')
    colorClassEstado.style.setProperty('--font-color-estado' , 'rgb(108, 80, 143)')

})

profesores.addEventListener('click' , () =>{
    cleanMain(feedTeacher)
    classEstado(profesores)
    varBackground.style.setProperty('--bg-color' , 'rgb(247, 244, 212)')
    colorClassEstado.style.setProperty('--font-color-estado' , 'rgb(83, 80, 38)')

})
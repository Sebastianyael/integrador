const textCard = document.getElementById('text-card')
const text = "Hola y Bienvenido al sistema de ReNova UTVT"
const speed = 34
let i = 0

function type(){
    if(i < text.length){
        textCard.textContent += text.charAt(i)
        i++
        setTimeout(type , speed)
    }
}

type()


const closeButton = document.getElementById('close-button') 

closeButton.addEventListener('click' , () =>{
    let modal = document.getElementById('modal')
    let modalCard = document.getElementById('modal-card')
    modalCard.classList.add('close-card')
    modal.classList.add('close-modal')
})


const enviar = document.getElementById('enviar')
const matricula = document.getElementById('matricula')
const contraseña = document.getElementById('contraseña')
const labelTwo = document.getElementById('label-two')
const labelOne = document.getElementById('label-one')

enviar.addEventListener('click' , (event) =>{

    labelOne.innerText = ''
    labelTwo.innerText = ''

    if(matricula.value.trim() === ''){
        labelOne.textContent = 'Campo Vacio'
        matricula.style.borderColor = 'red'
        event.preventDefault()
    }
        
    if(contraseña.value.trim() === ''){
        labelTwo.textContent = 'Campo Vacio'
        contraseña.style.borderColor = 'red'  
        event.preventDefault()
    }else{
        matricula.style.borderColor = ''
        contraseña.style.borderColor = ''
    }
})



const userNotFound = document.getElementById('userNotFound')

matricula.addEventListener('focus' , () =>{
    labelOne.innerHTML = ''
    matricula.style.borderColor = 'green'
})

contraseña.addEventListener('focus' , () =>{
    labelTwo.innerHTML = ''
    contraseña.style.borderColor = 'green'
})


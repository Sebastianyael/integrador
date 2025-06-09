
let closeButton = document.getElementById('close-button')

closeButton.addEventListener('click' , () =>{
    let modal = document.getElementById('modal')
    let modalCard = document.getElementById('modal-card')
    modalCard.classList.add('close-card')
    modal.classList.add('close-modal')
})


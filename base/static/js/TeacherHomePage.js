const testJs = ()=>{
    const sidebar = document.querySelector(".sidebar")
    
    const button = document.querySelector(".fa-bars")

    button.addEventListener('click', ()=>{
        sidebar.classList.toggle("shownav")
    })

}
testJs()
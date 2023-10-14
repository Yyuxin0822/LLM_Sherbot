// //////////// 

addGlobalEventListener('keydown','#modal-note',e=>{
    if (e.shiftKey && e.key === "Enter") {
        let content = e.target.value;
        console.log("The content is");
        console.log(content);
        let modalbody=document.getElementById("modal-body")
        let modalnote=document.createElement("p");
        modalnote.className = 'note';
        modalnote.style.color = "red";
        modalnote.innerHTML = content;
        modalbody.appendChild(modalnote);
        e.target.value = "";
        e.preventDefault();
    }
})



// //////////// // //////////// // ////////////
// //////////// // //////////// // ////////////




const openModalButtons=document.querySelectorAll('[data-modal-target]')
const closeModalButtons=document.querySelectorAll('[data-close-button]')

const overlay=document.getElementById('overlay')    
// openModal(modal)
openModalButtons.forEach(button=>{
    console.log(button.innerHTML)
    button.addEventListener('click',()=>{
        var modal=document.querySelector('#' +button.dataset.modalTarget)
        console.log(modal)
        openModal(modal)
    })
})

closeModalButtons.forEach(button=>{
    button.addEventListener('click',()=>{
        var modal=button.closest('.modal')
        closeModal(modal)
    })
})

function openModal(modal){
    console.log(modal)
    if(modal==null) return
    modal.classList.add('active')
    overlay.classList.add('active')
}


function closeModal(modal){
    if(modal==null) return
    modal.classList.remove('active')
    overlay.classList.remove('active')
}





//////////////////////////////////////////////////////
let isResizing = false;
let startHeight;
let startY;

const resizable = document.getElementById('modal');
const handle = document.getElementById('handle');
resizable.scrollTop = resizable.scrollHeight;
handle.addEventListener('mousedown', function(e) {
    isResizing = true;
    startY = e.clientY;
    startHeight = resizable.offsetHeight;
    document.addEventListener('mousemove', doResize);
    document.addEventListener('mouseup', stopResize);

});

function doResize(e) {
    if (!isResizing) return;

    const diffY = e.clientY - startY;
    resizable.style.height = (startHeight - diffY) + 'px'; // Adjusted for downward dragging
}

function stopResize() {
    isResizing = false;
    document.removeEventListener('mousemove', doResize);
    document.removeEventListener('mouseup', stopResize);
}
//////////////////////////////////////////////////////








let seenMessages = new Set();  // A set to keep track of messages we've already added

function fetchRepeatedly() {
    const message = getData(message_url);
    message.then(result => {
        let modal = document.getElementById("modal-body");
        modal.style.overflowY = "scroll";
        modal.style.scrollBehavior = "smooth";
        modal.style.scrollbarWidth = "thin";

        result.forEach(m => {

          let parts = m.split("\n");
          parts.forEach(part => {
            let para = part.trim();

            if (!seenMessages.has(para)) { 
              let p = document.createElement("p");
              p.className = 'message';
              seenMessages.add(para);
              p.innerHTML =  para
              modal.appendChild(p);

            }
          });

        });

        setTimeout(fetchRepeatedly, 40000);//20 seconds
    }).catch(error => {
        // Handle error
        setTimeout(fetchRepeatedly, 40000);
    });
}

fetchRepeatedly();  // Start the cycle

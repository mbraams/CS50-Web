document.addEventListener('DOMContentLoaded', function(){    
    newpost();  
})


function newpost(){
    document.querySelector("#submitmessage").onclick = function() {
        let newmessage = document.querySelector("#newmessage");
        let message = newmessage.value;
        newmessage.value = "";
        fetch('/newpost', {
            method: 'POST',
            body: JSON.stringify({
                body: message
            })
          })
          .then(response => response.json())
          .then(result => {
              // Print result
              console.log(result);
          });        
        return false;
    }
}



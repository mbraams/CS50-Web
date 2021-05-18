document.addEventListener('DOMContentLoaded', function(){
    console.log("dom loaded")

    document.querySelector("#submitmessage").onclick = function() {
        console.log("i was clicked");
        let message = document.querySelector("#newmessage").value;
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
        console.log("before returning false");
        return false;
    }
})


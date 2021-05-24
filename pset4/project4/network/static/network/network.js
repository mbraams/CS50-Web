document.addEventListener('DOMContentLoaded', function(){    
    newpost();  
    getPosts();
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

function getPosts(){
    fetch('/allposts') 
        .then(response => response.json())
        .then(posts => {
            console.log(posts);
            posts.array.forEach(post => {               
                
                const container = document.createElement('div');
                const user = document.createElement('div');
                const time = document.createElement('div');
                const body = document.createElement('div');
                container.className = 'post'
                user.innerHTML = post.user;
                user.className = 'user';
                time.innerHTML = post.timestamp;
                time.className = 'time';
                body.innerHTML = post.body;
                body.className = 'content';

                container.append(user, time, body);
                document.querySelector('#allPosts').append(container)
            });
        })
    
}



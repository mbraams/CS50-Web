document.addEventListener('DOMContentLoaded', function () {
    newpost();
    like();
    editPost();
})


function newpost() {
    document.querySelector("#submitmessage").onclick = function () {
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

    }
}

function like() {
    const likeButtons = document.querySelectorAll('.like')
    likeButtons.forEach(function (likeButton) {
        likeButton.onclick = function () {
            const postID = likeButton.value;
            fetch(`/like/${postID}`)
                .then(response => response.json())
                .then(likes => {
                    if (likes['liked'] === false) {
                        fetch(`/like/${postID}`, {
                            method: 'POST',
                            body: JSON.stringify({
                                like: true
                            })
                        })
                        const likecounter = document.querySelector(`#likes${postID}`)
                        let currentcount = parseInt(likecounter.dataset.value);
                        currentcount += 1;
                        likecounter.innerHTML = `&#x2764; ${currentcount}`;
                        likecounter.dataset.value = currentcount;
                        likeButton.innerHTML = "Unlike";
                    }


                    //else unlike
                    else {
                        fetch(`/like/${postID}`, {
                            method: 'POST',
                            body: JSON.stringify({
                                like: false
                            })
                        })
                        const likecounter = document.querySelector(`#likes${postID}`)
                        let currentcount = parseInt(likecounter.dataset.value);
                        currentcount -= 1;
                        likecounter.innerHTML = `&#x2764; ${currentcount}`;
                        likecounter.dataset.value = currentcount;
                        likeButton.innerHTML = "Like";
                    }

                })
        }
    })
}

function editPost() {
    const editbuttons = document.querySelectorAll('.edit');
    editbuttons.forEach(edit => {
        edit.onclick = function () {
            const postid = edit.value;
            const postContent = document.querySelector(`#content${postid}`);
            const edittextbox = document.querySelector(`#edit-box${postid}`);
            const submitbutton = document.querySelector(`#edit-submit${postid}`);

            edittextbox.innerHTML = postContent.innerHTML;
            //show editting blocks, hide regular
            edit.style.display = 'none';
            postContent.style.display = 'none';
            edittextbox.style.display = 'block';
            submitbutton.style.display = 'block';

            submitbutton.onclick = function () {
                fetch(`/edit/${postid}`, {
                    method: "PUT",
                    body: JSON.stringify({
                        "content": edittextbox.value
                    })

                })
                    .then(response => response.json())
                    .then(result => {
                        // Print result
                        console.log(result);
                    });

                    //show regular blocks\
                    postContent.style.display = 'block';
                    edit.style.display = 'block';                    
                    edittextbox.style.display = 'none';
                    submitbutton.style.display = 'none';

                    postContent.innerHTML = edittextbox.value;

            }

        }
    })
}


//used to load posts through JS and json instead of reloading the page which exercise calls for
function getPosts() {
    fetch('/allposts')
        .then(response => response.json())
        .then(posts => {
            console.log(posts);
            const allposts = document.querySelector('#allPosts');
            allposts.innerHTML = '';
            posts.forEach((post) => {


                const container = document.createElement('div');
                const user = document.createElement('div');
                const time = document.createElement('div');
                const body = document.createElement('div');
                container.className = 'post';
                user.innerHTML = post.user;
                user.className = 'user';
                time.innerHTML = post.timestamp;
                time.className = 'time';
                body.innerHTML = post.content;
                body.className = 'content';

                container.append(user, time, body);
                console.log(container);
                allposts.append(container)
            });
        })
        .catch(error => {
            console.log(`error: ${error}`);
        })


}



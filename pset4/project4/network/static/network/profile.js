document.addEventListener('DOMContentLoaded', function () {
    like();
    editPost();
    follow();
})


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
                        likeButton.style.color = "red";
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
                        likeButton.style.color = "lightskyblue";
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


function follow() {
    const followbttn = document.querySelector('#follow');
    followbttn.onclick = function () {
        const profile_id = followbttn.dataset.profileid;
        console.log(profile_id);

        fetch(`getfollow/${profile_id}`)
            .then(response => response.json())
            .then(follows => {
                //if the user doesnt follow yet, follow
                if (follows["followed"] === false) {
                    fetch(`getfollow/${profile_id}`, {
                        method: "POST",
                        body: JSON.stringify({
                            follows: true
                        })
                    })
                    //update count
                    followercount = document.querySelector("#followercount");
                    newcount = parseInt(followercount.dataset.followers) + 1;
                    followercount.innerHTML = `Followers: ${newcount}`;
                    followercount.dataset.followers = newcount;
                    console.log("user followed");
                    followbttn.style.color = 'red';
                    followbttn.innerHTML = 'Unfollow'
                }
                //else unfollow
                else {
                    fetch(`getfollow/${profile_id}`, {
                        method: "POST",
                        body: JSON.stringify({
                            follows: false
                        })                        
                    })
                    //update count
                    followercount = document.querySelector("#followercount");
                    newcount = parseInt(followercount.dataset.followers) - 1;
                    followercount.innerHTML = `Followers: ${newcount}`;                    
                    followercount.dataset.followers = newcount;
                    followbttn.style.color = 'lightskyblue';
                    followbttn.innerHTML = 'Follow';

                    console.log("user unfollowed");
                }
            })
    }
    return false
}
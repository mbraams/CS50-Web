document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Define variables
  const recipient = document.querySelector('#compose-recipients')
  const subject = document.querySelector('#compose-subject')
  const body = document.querySelector('#compose-body')

  // Clear out composition fields
  recipient.value = '';
  subject.value = '';
  body.value = '';
  

  // Send emails from the form
  document.querySelector('form').onsubmit = function(){
    const receiver = recipient.value;
    const subject_value = subject.value;
    const message = body.value;

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: receiver,
        subject: subject_value,
        body: message
      })
    })
    .then(response => response.json())
    .then(result => {
      console.log(result);
    })
    .catch(error => {
      console.log(`Error, ${error}`);
    });
    return false;
  } 
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  const emailView = document.querySelector('#emails-view');
  emailView.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  
  console.log("check before fetch")
  // load data from user
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      console.log("fetch succeeded")
      // Print emails
      const div = document.createElement('div');
      emails.forEach((element) => {
        div.innerHTML = `Sender: ${element.sender}, subject: ${element.subject}, time: ${element.timestamp}`;
        emailView.append(div);
        console.log(`${div} was sent succesfully`);
      });
    })
    .catch(error => {
      console.log(`Error, ${error}`)
    })
  

  
}


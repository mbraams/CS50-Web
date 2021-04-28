document.addEventListener('DOMContentLoaded', function () {

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
  document.querySelector('#email-view').style.display = 'none';

  // Define variables
  const recipient = document.querySelector('#compose-recipients')
  const subject = document.querySelector('#compose-subject')
  const body = document.querySelector('#compose-body')

  // Clear out composition fields
  recipient.value = '';
  subject.value = '';
  body.value = '';


  // Send emails from the form
  document.querySelector('form').onsubmit = function () {
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
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  const emailView = document.querySelector('#emails-view');
  emailView.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;


  // load data from user
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      // Print emails


      emails.forEach((element) => {
        const mail = document.createElement('div');
        mail.className = "emailheader";
        mail.innerHTML = `Sender: ${element.sender}, subject: ${element.subject}, time: ${element.timestamp}`;
        if (element.read) {
          mail.style.backgroundColor = 'gray';
        }
        //open mail
        mail.onclick = function () {
          open_mail(element);
        }

        emailView.append(mail);
      });
    })
    .catch(error => {
      console.log(`Error, ${error}`)
    })

}

function open_mail(element) {
  //empty previous opened emails
  document.querySelector('#email-view').innerHTML = '';

  //open email and close rest  
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  //set email to 'read'
  fetch(`/emails/${element.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })

  //create divs
  const from = document.createElement('div');
  const to = document.createElement('div');
  const subject = document.createElement('div');
  const time = document.createElement('div');
  const message = document.createElement('div');
  message.className = "body";
  const archive = document.createElement('button');
  const reply = document.createElement('button');

  //give divs text
  from.innerHTML = `From: ${element.sender}`;
  to.innerHTML = `To: ${element.recipients}`;
  subject.innerHTML = `Subject: ${element.subject}`;
  time.innerHTML = `Sent on: ${element.timestamp}`;
  message.innerHTML = element.body;
  reply.innerHTML = 'Reply';

  //button and method for archiving
  if (element.archived) {
    archive.innerHTML = 'Unarchive';
  } else {
    archive.innerHTML = 'Archive';
  }
  archive.onclick = function () {
    //fetch put request
    archive_email(element);
  }

  //button for replying
  reply.onclick = function() {
    compose_email();

    //prefill form
    document.querySelector('#compose-recipients').value = element.sender;  
    // make sure the Re: doesn't repeat on longer conversations  
    if(element.subject.startsWith("Re:")){
      document.querySelector('#compose-subject').value = element.subject;
    } else {
      document.querySelector('#compose-subject').value = `Re: ${element.subject}`;
    }
    document.querySelector('#compose-body').value = `"On ${element.timestamp}, ${element.sender} wrote:" ${element.body}`
  }
  
  //build the actual email
  document.querySelector('#email-view').append(from, to, time, subject, message, archive, reply);
}

function archive_email(email) {
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !email.archived
    })
  })
    //return to inbox
    .then(response => load_mailbox('inbox'))
}

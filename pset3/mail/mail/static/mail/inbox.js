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
        if (element.read === true){
          mail.style.backgroundColor = 'gray';
        }
        //open mail
        mail.onclick = function(){
          //mark email as read
          element.read = true;
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
  

  //open email and close rest
  document.querySelector('#email-views').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  //create divs
  const from = document.createElement('div');
  const to = document.createElement('div');
  const subject = document.createElement('div');
  const time = document.createElement('div');
  const message = document.createElement('div');
  message.className = "body";

  from.innerHTML = element.sender;
  to.innerHTML = element.recipients;
  subject.innerHTML = element.subject;
  time = element.timestamp;
  const body = element.body;

  document.querySelector('#email-view').append(from, to, subject, time, message);

}


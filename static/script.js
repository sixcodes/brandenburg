var url = 'http://127.0.0.1:8000';
var xhr = new XMLHttpRequest();
xhr.open('GET', url+'/v1/leads/token/' );
xhr.setRequestHeader('Content-Type', 'application/json');
xhr.send();
xhr.onreadystatechange = function(){
    if (xhr.readyState === 4){
        var result = JSON.parse(xhr.responseText);
        document.getElementById('token').value = result.token;
    }
};

var send = function(name, email, phone_number, is_term_accepted, origin){
    var beacon = new XMLHttpRequest();
    var token = document.getElementById("token").value;
    beacon.open('POST', url+ '/v1/leads/' + token);
    beacon.setRequestHeader('Content-Type', 'application/json');
    beacon.onload = function() {
        if (beacon.status === 200) {
            console.log("ok");
        }else{
          console.log("err"+beacon.status);
        }
    };
    beacon.send(JSON.stringify({
        name: name.value,
        email: email.value,
        phone_number: phone_number.value,
        is_term_accepted: is_term_accepted.checked,
        origin: origin.value,
    }));

  beacon.onreadystatechange = function(){
      if (beacon.readyState === 4){
      callback();
      document.getElementById("leadForm").reset();
      }
  };
}
var nameField = document.getElementById("name"),
email = document.getElementById("email"),
phone_number = document.getElementById("phone_number"),
is_term_accepted = document.getElementById("is_term_accepted"),
origin = document.getElementById("origin"),
submit = document.getElementById('leadSubmit');

submit.addEventListener("click", function(){
  send(nameField, email, phone_number, is_term_accepted, origin);
}, false);

nameField.addEventListener("focusout", function(){
  if(nameField.value.length < 3){
    nameField.classList.add("lead-invalid-field");
  }else{
    nameField.classList.remove("lead-invalid-field");
  }
});

email.addEventListener("keyup", function(){
  var re = /(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)/;
  if(re.test(email.value) == true){
    email.classList.remove("lead-invalid-field");
    submit.disabled = false;
  }else{
    email.classList.add("lead-invalid-field");
    submit.disabled = true;
  }
});

phone_number.addEventListener("keyup", function(){
  if(this.value.length < 11){
    phone_number.classList.add("lead-invalid-field");
    submit.disabled = true;
  }else{
    phone_number.classList.remove("lead-invalid-field");
    submit.disabled = false;
  }
});

is_term_accepted.addEventListener("click", function(){
  if(is_term_accepted.checked == true){
    submit.disabled = false;
  }else{
    submit.disabled = true;
  }
});


const form = `
<form action="/rav-data" method="POST">
  <label for="username">Ravelry Username:</label>
  <input type="text" name="username" id="username" placeholder="Username">
  <input type="submit">
</form>`

function usernameForm(evt) {
  $('#homepage').html(form);
}

function ravelrySignUp(evt){
  alert('woooooo');
  $('#no-rav-account').toggle();
}

$('#yes-button').on('click', usernameForm);
$('#no-button').on('click', ravelrySignUp);

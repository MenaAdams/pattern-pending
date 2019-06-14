const form = `
<form action="/rav-data" method="POST">
  <label for="username">Ravelry Username:</label>
  <input type="text" name="username" class="text" id="username" placeholder="Username" required>
  <input type="submit" class="submit-button">
</form>`

function usernameForm(evt) {
  $('#homepage').html(form);
}

function ravelrySignUp(evt){
  $('#no-rav-account').toggle();
}

$('#yes-button').on('click', usernameForm);
$('#no-button').on('click', ravelrySignUp);

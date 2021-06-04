var password = document.getElementById("password"), confirm_pass = document.getElementById("confirm_pass");

function confirmPasswordMatch(){
	if(password.value != null && confirm_pass.value !=null){	
		if(password.value != confirm_pass.value) {
			confirm_pass.setCustomValidity("Passwords do not match!");
		} else {
			confirm_pass.setCustomValidity("");
		}
	}
}

password.onchange = confirmPasswordMatch;
confirm_pass.onkeyup = confirmPasswordMatch;
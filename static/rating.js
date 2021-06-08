var url = document.getElementById('update_rating_url').value;
var pet_id = document.getElementById('pet_id').value;
var user = document.getElementById('user').value;
var radio_buttons = document.getElementsByName('rate');

for(var i = 0, max = radio_buttons.length; i < max; i++) {
	radio_buttons[i].onclick = function() {
		
		var id = pet_id + user;
		var rating = this.value;
		
		var dict = {
			'id': id,
			'username': user,
			'rating': rating,
			'pet_id': pet_id
		};
					
		fetch(url, {
            method: "POST",
            credentials: "include",
            body: JSON.stringify(dict),
            cache: "no-cache",
            headers: new Headers({
                "content-type": "application/json"
            })
        });
	}
}
	

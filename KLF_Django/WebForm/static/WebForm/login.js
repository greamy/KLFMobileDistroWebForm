
function Submit() {
	const username = document.getElementById("username")
	const password = document.getElementById("password")
	$.ajax({
		type: "POST",
		url: "/form/admin/login/",
		headers: {'X-CSRFToken': getCookie("csrftoken")},
		mode: 'same-origin',
		// Do not send CSRF token to another domain.
		data: {"username": username.value, "password": password.value},
		success: function (data) {
			console.log(data);
			if (data.redirect) {
				window.location.href = data.redirect;
				return;
			}
		},
		error: function(response, textStatus, errorThrown) {
			username.value = "";
			password.value = "";
			errorMsg = document.getElementById("errorMsg")
			errorMsg.style.display = "block";
			errorMsg.innerHTML = response.responseText;
		}
	});
}
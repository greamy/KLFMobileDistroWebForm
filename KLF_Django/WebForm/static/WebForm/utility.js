// Functionality:
//		Returns value of cookie based on name. We use this mainly for CSRF cookie values for AJAX post requests.
// Parameters:
//		name: string name of the cookie you wan the value of
// Returns:
//		value of cookie, or null if cookie name doesn't exist
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
		if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
$(document).ready(function () {
	// Make an AJAX request to get the locations and sites json file
	$.ajax({
		type: "GET",
		url: "/form/get-form-settings",
		dataType: "json",
		success: function (data) {
			if (data.redirect) {
				window.location.href = data.redirect;
				return;
			}

			// Process the json data
			console.log(data);
			let inputSettings = data;

			document.getElementById("error").style.display="none";
			for (var i = 0; i < inputSettings.length;i++){
  				createForm(inputSettings[i]);
			}
		}
	});
});

//2d Array for form
//format: id, placeholder, name, type, required?, min, max
//const inputSettings = [
                       //["First Name","First Name","Fname","text", 1,0,0,0,1],
                       //["Last Name","Last Name","Lname","text", 1,0,0,0,1],
                       //["Email Address","Email Address","Email","email",0,0,0,0,1],
                       //["Number in Household","Number in Household","HHold","number",1,1,50,0,1],
                       //["Street Address","Street Address","Address","other",1,0,0,0,1],
                       //["Zip Code","Zip Code","Zip","number",1,10000,99999,0,1]];

function createForm( settings){
  const important = document.createElement("span");
  important.appendChild(document.createTextNode("*"));
  important.setAttribute("style","color:red");
  
  const label = document.createElement("label");
  label.appendChild(document.createTextNode(settings[0]));
  if (settings[4] == 1){
    label.appendChild(important);
  }
  
  const inputs = document.createElement("input");
  inputs.setAttribute("id",settings[0]);
  inputs.setAttribute("placeholder",settings[1]);
  inputs.setAttribute("name",settings[2]);
  inputs.setAttribute("type",settings[3]);
  if (settings[4] == 1){
    inputs.setAttribute("required",settings[4]);
  }
  if(settings[3] == "text"){
    inputs.setAttribute("oninvalid","setCustomValidity('Please enter letters.')");
    inputs.setAttribute("pattern","[A-Za-z]{1,}");
  }else if(settings[3] == "number"){
    inputs.setAttribute("min", settings[5]);
    if (settings[6] != 0){
      inputs.setAttribute("max", settings[6]);
    }
  }
  
  const form = document.getElementById("form");
  form.appendChild(label);
  form.appendChild(inputs);
}


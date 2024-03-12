
//2d Array for form
//format: id, placeholder, name, type, required?, min, max
const inputSettings = [
                       ["First Name","First Name","First Name","text", 1,0,0,0,1],
                       ["Last Name","Last Name","Last Name","text", 1,0,0,0,1],
                       ["Email Address","Email Address","Email Address","email",0,0,0,0,1],
                       ["Number in Household","Number in Household","Number in Household","number",1,1,50,0,1],
                       ["Street Address","Street Address","Street Address","other",1,0,0,0,1],
                       ["Zip Code","Zip Code","Zip Code","number",1,10000,99999,0,1]];

function createForm( settings){
  const important = document.createElement("span");
  important.appendChild(document.createTextNode("*"));
  important.setAttribute("style","color:red");
  
  const label = document.createElement("label");
  label.appendChild(document.createTextNode(settings[2]));
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
for (var i = 0; i < inputSettings.length;i++){
  createForm(inputSettings[i]);
}

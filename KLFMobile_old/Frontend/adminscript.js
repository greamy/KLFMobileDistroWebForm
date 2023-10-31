import * as d3 from "https://cdn.skypack.dev/d3@7.3.0";
const page = "home";

//2D array of Sites
const Sites = [["Comstock Middle School"],["Galesburg United Methodist Church"],["Saint Andrew Community Church","Heritage Christian Reformed Church","Haven Church","Douglass Community Association","Sunnyside United Methodist Church","The Salvation Army"],["Chapel Hill United Methodist Church"],["Vicksburg United Methodist Church"]];

//Array of Locations
const Locations = ["Comstock","Galesburg","Kalamazoo","Portage","Vicksburg"];

//creates Location Button and Divider for Drop Down Menu for Side Nav Bar
function CreateLoc(string){
  const da = document.createElement('i');
  da.setAttribute("class","fa fa-caret-down");
  da.setAttribute("id",string);
  
  const Loc = document.createElement('button');
  Loc.setAttribute("id", string);
  Loc.setAttribute("class","dropdown-btn");
  const text = document.createTextNode(string);
  Loc.appendChild(text);
  Loc.appendChild(da);
  
  const Sit = document.createElement('div');
  Sit.setAttribute("id","d"+string);
  Sit.setAttribute("class","drop");
  
  const element = document.getElementById("loc");
  element.appendChild(Loc);
  element.appendChild(Sit);
}

//creates all Site within Divider in Side Nav Bar
function createSites(array, string){
  const text = document.createTextNode(array);
  const Site = document.createElement('a');
  Site.setAttribute("id", string);
  Site.setAttribute("href","#"+string);
  Site.appendChild(text);
  const element = document.getElementById("d"+string);
  element.appendChild(Site);
}

//Creates All appropiate Locations with its listed sites as drop down menus
for (var i = 0; i < Locations.length; i++){
  CreateLoc(Locations[i]);
  for (var x = 0; x < Sites[i].length; x++){
    createSites(Sites[i][x],Locations[i]);
  }
}


//Creates functional Drop Down Menus
var dropdown = document.getElementsByClassName("dropdown-btn");
for (var i = 0; i < dropdown.length; i++) {
  dropdown[i].addEventListener("click", function() {
    var dropdownContent = this.nextElementSibling;
    if (dropdownContent.style.display === "block") {
      dropdownContent.style.display = "none";
    } else {
      dropdownContent.style.display = "block";
    }
  });
}

import * as d3 from "https://cdn.skypack.dev/d3@7.3.0";
//2D array of Sites
const Sites = [
  ["Comstock Middle School"],
  ["Galesburg United Methodist Church"],
  [
    "Saint Andrew Community Church",
    "Heritage Christian Reformed Church",
    "Haven Church",
    "Douglass Community Association",
    "Sunnyside United Methodist Church",
    "The Salvation Army"
  ],
  ["Chapel Hill United Methodist Church"],
  ["Vicksburg United Methodist Church"]
];



//Array of Locations
const Locations = [
  "Comstock",
  "Galesburg",
  "Kalamazoo",
  "Portage",
  "Vicksburg"
];
//creates page for each location and site
function CreatePage(array, string) {
  const textH2 = document.createTextNode(string + ": " + array);

  const h2 = document.createElement("h2");
  h2.appendChild(textH2);
  
  const div1 = document.createElement("div");
  div1.setAttribute("class", "Top-Color");
  div1.appendChild(h2);

  const filename = document.createElement("a");
  filename.appendChild(document.createTextNode("File Name"));
  
  const Update = document.createElement("a");
  Update.setAttribute("id", "Update");
  Update.appendChild(document.createTextNode("Last Modified"));
  
  const filelist = document.createElement("div");
  filelist.setAttribute("class","FileList");
  filelist.appendChild(filename);
  filelist.appendChild(Update);
  
  
  const div = document.createElement("div");
  div.setAttribute("id", array +"P");
  div.setAttribute("class", "page");
  div.appendChild(div1);
  div.appendChild(filelist);

  const loc = document.getElementById("main");
  loc.appendChild(div);
  div.style.display = "none";
}
//creates Location Button and Divider for Drop Down Menu for Side Nav Bar
function CreateLoc(string) {
  const da = document.createElement("i");
  da.setAttribute("class", "fa fa-caret-down");
  da.setAttribute("id", string);

  const Loc = document.createElement("button");
  Loc.setAttribute("id", string);
  Loc.setAttribute("class", "dropdown-btn");
  const text = document.createTextNode(string);
  Loc.appendChild(text);
  Loc.appendChild(da);

  const Sit = document.createElement("div");
  Sit.setAttribute("id", "d" + string);
  Sit.setAttribute("class", "drop");

  const element = document.getElementById("loc");
  element.appendChild(Loc);
  element.appendChild(Sit);
}

//creates all Site within Divider in Side Nav Bar
function createSites(array, string) {
  const text = document.createTextNode(array);
  const Site = document.createElement("button");
  Site.setAttribute("id", array);
  Site.setAttribute("class","PageB");
  Site.appendChild(text);
  const element = document.getElementById("d" + string);
  element.appendChild(Site);
  CreatePage(array, string);
}



console.log("CONSOLE TESTING LOG")
//Creates All appropiate Locations with its listed sites as drop down menus
for (var i = 0; i < Locations.length; i++) {
  CreateLoc(Locations[i]);
  for (var x = 0; x < Sites[i].length; x++) {
	createSites(Sites[i][x], Locations[i]);
  }
}
//Creates functional Drop Down Menus
var dropdown = document.getElementsByClassName("dropdown-btn");
for (var i = 0; i < dropdown.length; i++) {
  dropdown[i].addEventListener("click", function () {
	var dropdownContent = this.nextElementSibling;
	if (dropdownContent.style.display === "block") {
	  dropdownContent.style.display = "none";
	} else {
	  dropdownContent.style.display = "block";
	}
  });
}
//Adds listen event on site buttons to change main page
var Cpage = document.getElementById("homeP");
var pages = document.getElementsByClassName("PageB");
for (var i = 0; i < pages.length; i++){
  pages[i].addEventListener("click", function (e){
	var Npage = document.getElementById(e.target.id + "P");
	Cpage.style.display = "none";
	Npage.style.display = "block";
	Cpage = Npage;
  });
}


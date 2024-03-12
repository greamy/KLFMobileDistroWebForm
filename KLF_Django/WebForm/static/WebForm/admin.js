$(document).ready(function () {
	// Make an AJAX request to get the locations and sites json file
	$.ajax({
		type: "GET",
		url: "/form/get-location-data",
		dataType: "json",
		success: function (data) {
			// Process the json data
			let locations = processData(data);
			populateLocations(locations[0], locations[1]);
		}
	});
});

//2d Array for form
//format: id, placeholder, name, type, required?, min, max, hide?, TEFAP
// TODO: Replace this definition with server call on 'Edit form' button click.
const inputSettings = [
                       ["First Name","First Name","First Name","text", 1,0,0,0,1],
                       ["Last Name","Last Name","Last Name","text", 1,0,0,0,1],
                       ["Email Address","Email Address","Email Address","email",0,0,0,0,1],
                       ["Number in Household","Number in Household","Number in Household","number",1,1,50,0,1],
                       ["Street Address","Street Address","Street Address","other",1,0,0,0,1],
                       ["Zip Code","Zip Code","Zip Code","number",1,10000,99999,0,1]];
let Universal = "";

//form editor
function FormSetting(settings, x){
  const info = document.createElement("b");
  info.appendChild(document.createTextNode("\u24d8"));

  const TEFAP = document.createElement("i");
  TEFAP.setAttribute("title", "TEFAP");
  TEFAP.setAttribute("class","fa fa-book");

  const name = document.createElement("p");
  if(settings[8] == 1){
    name.appendChild(TEFAP);
    name.appendChild(document.createTextNode(" "));
  }
  name.appendChild(document.createTextNode(settings[2]));

  const Plabel = document.createElement("label");
  Plabel.setAttribute("for",settings[0]);
  Plabel.appendChild(document.createTextNode("Placeholder: "));
  Plabel.setAttribute("style","font-size: 16px; margin-left: 10px");

  const rename = document.createElement("input");
  rename.setAttribute("placeholder",settings[1]);
  rename.setAttribute("name",settings[2]);
  rename.setAttribute("id",settings[0]);
  rename.setAttribute("class","rename");

  const rlabel = document.createElement("label");
  rlabel.setAttribute("for", "require");
  rlabel.appendChild(document.createTextNode("Required?"));
  rlabel.setAttribute("style","font-size: 16px; margin-left: 10px");

  const require = document.createElement("input");
  require.setAttribute("type","checkbox");
  require.setAttribute("id","require");
  if (settings[4] == 1){
    require.setAttribute("checked", 1);
  }
  const tlabel = document.createElement("label");
  tlabel.appendChild(document.createTextNode("Type:"));
  tlabel.setAttribute("for", "type");
  tlabel.setAttribute("style","font-size: 16px; margin-left: 10px");

  const text = document.createElement("option");
  text.appendChild(document.createTextNode("Text"));
  text.setAttribute("title","Accepts only Letters");
  text.setAttribute("value","text");
  if (settings[3] == "text"){
    text.setAttribute("selected",1);
  }

  const Email = document.createElement("option");
  Email.appendChild(document.createTextNode("Email"));
  Email.setAttribute("title","Accepts only an Email Address");
  Email.setAttribute("value","email");
  if (settings[3] == "email"){
    Email.setAttribute("selected",1);
  }

  const number = document.createElement("option");
  number.appendChild(document.createTextNode("Number"));
  number.setAttribute("title","Accepts only Numbers");
  number.setAttribute("value","number");
  if (settings[3] == "number"){
    number.setAttribute("selected",1);
  }

  const other = document.createElement("option");
  other.appendChild(document.createTextNode("Other"));
  other.setAttribute("title","Accepts all Characters");
  other.setAttribute("value","other");
  if (settings[3] == "other"){
    other.setAttribute("selected",1);
  }

  const type = document.createElement("select");
  type.setAttribute("id","type");
  type.appendChild(text);
  type.appendChild(Email);
  type.appendChild(number);
  type.appendChild(other);

  const mlabel = document.createElement("label");
  mlabel.setAttribute("for", "min");
  mlabel.appendChild(document.createTextNode("Min:"));
  mlabel.setAttribute("style","font-size: 16px; margin-left: 10px");

  const min = document.createElement("input");
  min.setAttribute("id","min");
  min.setAttribute("type","number");
  min.setAttribute("min","0");
  min.setAttribute("style","width:50px");
  min.setAttribute("placeholder", settings[5]);

  const xlabel = document.createElement("label");
  xlabel.setAttribute("for", "max");
  xlabel.appendChild(document.createTextNode("Max:"));
  xlabel.appendChild(info);
  xlabel.setAttribute("title","Set to 0 if you don't want a limit");
  xlabel.setAttribute("style","font-size: 16px; margin-left: 10px");

  const max = document.createElement("input");
  max.setAttribute("id","max");
  max.setAttribute("type","number");
  max.setAttribute("min","0");
  max.setAttribute("style","width:50px");
  max.setAttribute("placeholder", settings[6]);

    const upA = document.createElement("i");
  upA.setAttribute("class","arrow up");

  const up = document.createElement("button");
  up.setAttribute("class","arrows");
  up.setAttribute("id","up");
  up.appendChild(upA);

  const downA = document.createElement("i");
  downA.setAttribute("class","arrow down");

  const down = document.createElement("button");
  down.setAttribute("class","arrows");
  down.setAttribute("id","down");
  down.appendChild(downA);

  const nOrder = document.createElement("div");
  nOrder.setAttribute("class","nOrder");
  nOrder.appendChild(document.createTextNode(x+1));


  const order = document.createElement("div");
  order.setAttribute("id","orderStyle");
  order.appendChild(up);
  order.appendChild(nOrder);
  order.appendChild(down);

  const LRemove = document.createElement("i");
  LRemove.appendChild(document.createTextNode("X"));

  const Remove = document.createElement("button");
  Remove.setAttribute("id","Remove");
  if (settings[8]==1){
    Remove.setAttribute("Disabled",1);
  }
  Remove.appendChild(LRemove);

  const visible = document.createElement("i");
  visible.setAttribute("class","fa fa-eye");
  visible.setAttribute("title","Visibility");

  const Vcheck = document.createElement("input");
  Vcheck.setAttribute("type","checkbox");
  if (settings[7]==0){
    Vcheck.setAttribute("checked", 1);
  }

  const Visdiv = document.createElement("div");
  Visdiv.appendChild(visible);
  Visdiv.appendChild(Vcheck);
  Visdiv.setAttribute("class","Visdiv");

  const option = document.createElement("div");
  option.setAttribute("id","option");
  option.appendChild(name);
  option.appendChild(Plabel);
  option.appendChild(rename);
  option.appendChild(rlabel);
  option.appendChild(require);
  option.appendChild(tlabel);
  option.appendChild(type);
  if (settings[3] == "number"){
    option.appendChild(mlabel);
    option.appendChild(min);
    option.appendChild(xlabel);
    option.appendChild(max);
  }
  option.appendChild(order);
  option.appendChild(Remove);
  option.appendChild(Visdiv);

  const optionView = document.createElement("div");
  optionView.appendChild(option);

  const Save = document.createElement("button");
  Save.setAttribute("id","SaveForm");
  Save.appendChild(document.createTextNode("Save Form"));

  const add = document.createElement("button");
  add.setAttribute("id","AddField");
  add.appendChild(document.createTextNode("Add Field"));

  const FormButtons = document.createElement("div");
  FormButtons.setAttribute("class","FormButton");
  FormButtons.appendChild(Save);
  FormButtons.appendChild(add);

  const formSetting = document.getElementById("form-setting");
  formSetting.appendChild(optionView);
  if(x+1 == inputSettings.length){
    formSetting.appendChild(FormButtons);
  }
}

function processData(data) {
	var rows = data;
	var locations = [];
	var sites = [];
	
	for (var location in rows) {
		if (rows.hasOwnProperty(location)) {
			locations.push(location);
			sites.push(rows[location]); // Assuming rows[location] is an array
		}
	}
	return [locations, sites];
}

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

function createSite() {
	const loc = document.getElementById("InputLocation");
	const site = document.getElementById("InputSite");
	document.getElementById("loader").style.display="inline-block"; // for loading animation on page

	$.ajax({
		type: "POST",
		url: "/form/post-location-data/", 
		dataType: "json",
		headers: {'X-CSRFToken': getCookie("csrftoken")},        
		mode: 'same-origin',
		// Do not send CSRF token to another domain.
		data: {"newLocation": loc.value, "newSite": site.value}, 
		success: function (data) {
			loc.value = "";
			site.value = "";
			let locations = processData(data);
			ResetLocations();
			populateLocations(locations[0], locations[1]);
			document.getElementById("loader").style.display = "none";
		},
		error: function (request, textStatus, errorThrown) {
			// TODO: Update error label field on HTML with the response text, set label field to display.

			loc.value = "";
			site.value = "";
			console.log(request.responseText)
			document.getElementById("loader").style.display = "none";
			document.getElementById("error-overlay").style.display = "block";
		}
	});
}

function No(){
  document.getElementById("overlay").style.display="none";
  document.getElementById(Universal).style.display="none";
}
function off() {
  document.getElementById("error-overlay").style.display = "none";
}

function DeleteOverlay() {
	document.getElementById("overlay").style.display="block";
}

function DeleteSite(){
//	Universal = string+array;
//	document.getElementById(Universal).style.display="inline-block";
	document.getElementById("overlay").style.display="none";
	var pages = document.getElementsByClassName("PageB");

	var page_data = getCurrentPage();
	var location = page_data[0];
	var site = page_data[1];
	let Npage = page_data[2];
	Npage.remove();

	$.ajax({
		type: "POST",
		url: "/form/delete-location-data/",
		dataType: "json",
		headers: {'X-CSRFToken': getCookie("csrftoken")},
		mode: 'same-origin',
		// Do not send CSRF token to another domain.
		data: {"location": location, "site": site},
		success: function (data) {
			let locations = processData(data);
			ResetLocations();
			populateLocations(locations[0], locations[1]);
			let homeP = document.getElementById("homeP");
			homeP.style.display="block";
		}
	});
}

function getCurrentPage() {
	var pages = document.getElementsByClassName("PageB");
	var location = "";
	var site = "";
	var Npage = null;

	for (let page of pages) {
		Npage = document.getElementById(page.id + "P");
		if (Npage.style.display != "none"){
			let siteName = Npage.childNodes[0].innerText;
			let temp = siteName.split(": ");
			location = temp[0];
			site = temp[1];
		}
	}
	return [location, site, Npage]
}

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

	const QR = document.createElement("button");
	QR.setAttribute("onClick","GenerateQR()");
	QR.setAttribute("class","QR");
	QR.appendChild(document.createTextNode("Generate QR Code"));
	
	const Delete = document.createElement("button");
  	Delete.setAttribute("onClick","DeleteOverlay('"+string+"','"+array+"')");
  	Delete.setAttribute("class","delete");
  	Delete.appendChild(document.createTextNode("Delete Site"));

  	const loader = document.createElement("div");
 	loader.setAttribute("class", "dloader");
	loader.setAttribute("id", string + array);
	Delete.appendChild(loader);
  
  	const bgroup = document.createElement("div");
  	bgroup.setAttribute("class","btn-group");
  	bgroup.appendChild(QR);
  	bgroup.appendChild(Delete);
	
	const div = document.createElement("div");
	div.setAttribute("id", array +"P");
	div.setAttribute("class", "page");
	div.appendChild(div1);
	div.appendChild(bgroup);
	div.appendChild(filelist);

	const loc = document.getElementById("main");
	loc.appendChild(div);
	div.style.display = "none";
}

//creates Location Button and Divider for Drop Down Menu for Side Nav Bar
function CreateLoc(string) {
	const da = document.createElement("i");
	da.setAttribute("class", "fa fa-caret-right");
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

//generate qr
function GenerateQR() {
	page_data = getCurrentPage();
	var location = page_data[0];
	var site = page_data[1];

	$.ajax({
		type: "GET",
		url: "/form/QR",
		data: {"location": location, "site": site},
		xhrFields: {
            responseType: 'blob' // Set the response type to blob
        },
		success: function (data) {
			var blob = new Blob([data], { type: 'image/png' }); // Create a blob from the response data
            var url = window.URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = 'QR.png'; // Specify the filename
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
		}
	});
}

function ResetLocations() {
	const sideBar = document.getElementById("loc");
  	while (sideBar.firstChild) {
    		sideBar.removeChild(sideBar.lastChild);
  	}
}

function populateLocations(locations, sites) {
	//Creates All appropriate Locations with its listed sites as drop down menus
	for (var i = 0; i < locations.length; i++) {
    	CreateLoc(locations[i]);
		for (var x = 0; x < sites[i].length; x++) {
			createSites(sites[i][x], locations[i]);
		}
	}
	//Creates functional Drop Down Menus
	var dropdown = document.getElementsByClassName("dropdown-btn");
	var last = 0;
	for (var i = 0; i < dropdown.length; i++) {
		dropdown[i].addEventListener("click", function () {
			var dropdownContent = this.nextElementSibling;
			if (last != 0) {
				last.style.display = "none";
			}
			if (last != dropdownContent) {
				dropdownContent.style.display = "block";
			}
			if (last == dropdownContent) {
				last = 0;
			}
			else {
				last = dropdownContent;
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
}
for (var i = 0; i < inputSettings.length;i++){
  		FormSetting(inputSettings[i], i);
}

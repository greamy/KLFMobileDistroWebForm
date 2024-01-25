$(document).ready(function () {
	// Make an AJAX request to get the locations and sites json file
	$.ajax({
		type: "GET",
		url: "/form/get-location-data",
		dataType: "text",
		success: function (data) {
			// Process the json data
			let locations = processData(data);
			populateLocations(locations[0], locations[1]);
		}
	});

	function processData(data) {
		var locations = [];
		var sites = [];
   		var rows = JSON.parse(data);

		for (var location in rows) {
			if (rows.hasOwnProperty(location)) {
				locations.push(location);
				sites.push(rows[location]); // Assuming rows[location] is an array
			}
    	}
		return [locations, sites];
	}
});

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
	console.log(loc.value);
	console.log(site.value);

	// Make an AJAX request to get the JSON file
	$.ajax({
		type: "POST",
		url: "/form/post-location-data/", // Replace with the actual path to your JSON file on the server
		headers: {'X-CSRFToken': getCookie("csrftoken")},        
		mode: 'same-origin',
		// Do not send CSRF token to another domain.
		data: {"newLocation": loc.value, "newSite": site.value}, 
		success: function (data) {
		// Process the CSV data
		}
	});
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
	QR.appendChild(document.createTextNode("Generate QR Code"));


	const Delete = document.createElement("button");
  	Delete.setAttribute("onClick","Delete('"+string+"','"+array+"')");
  	Delete.setAttribute("class","delete");
  	Delete.appendChild(document.createTextNode("Delete Site"));
  
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
	console.log("hello whats up");
	var httpreq = new XMLHttpRequest();
	httpreq.open("GET", "/form/QR", true);
	httpreq.send();
}

function Delete(string,array){
  console.log(string);
  console.log(array);
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

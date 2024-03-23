$(document).ready(function () {
	// Make an AJAX request to get the locations and sites json file
	$.ajax({
		type: "GET",
		url: "/form/get-location-data",
		dataType: "json",
		success: function (data) {
			if (data.redirect) {
				window.location.href = data.redirect;
				return;
			}

			// Process the json data
			let locations = processLocationData(data);
			populateLocations(locations[0], locations[1]);

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
			populateFormSettings(inputSettings);
		}
	});
});

let Universal = "";

// Functionality:
//		Creates editable field row in 'Edit Form' page
// Parameters:
// 		settings: array of settings for form field being added, like shown above
//		x: integer representing order in the list of form fields.
// Returns: Nothing
function FormSetting(settings, x, isLast) {
	const info = document.createElement("b");
	info.appendChild(document.createTextNode("\u24d8"));

	const TEFAP = document.createElement("i");
	TEFAP.setAttribute("title", "TEFAP Required Field");
	TEFAP.setAttribute("class","fa fa-book");

	const name = document.createElement("p");
	if(settings[8] == 1) {
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
	if (settings[4] == 1) {
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
	if (settings[3] == "text") {
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
	if (settings[3] == "number") {
		number.setAttribute("selected",1);
	}

	const other = document.createElement("option");
	other.appendChild(document.createTextNode("Other"));
	other.setAttribute("title","Accepts all Characters");
	other.setAttribute("value","other");
	if (settings[3] == "other") {
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
	if (settings[8]==1) {
		Remove.setAttribute("Disabled",1);
	}
	Remove.appendChild(LRemove);

	const visible = document.createElement("i");
	visible.setAttribute("class","fa fa-eye");
	visible.setAttribute("title","Visibility");

	const Vcheck = document.createElement("input");
	Vcheck.setAttribute("type","checkbox");
	if (settings[7]==0) {
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
	if (isLast) {
		formSetting.appendChild(FormButtons);
	}
}

// Functionality:
//		Transforms javascript object into multi-dimensional array for use in other functions in this file.
// Parameters:
//		data: javascript object containing list of locations and sites, usually returned from AJAX call to server.
// Returns:
//		2d Array, [0] is array of locations, [1] is another 2d array of sites, each element in this array is a location
// TODO: Sort location list alphabetically and then sort site array to match
function processLocationData(data) {
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



// Functionality:
//		Runs when 'Create' button is clicked on home page. Sends AJAX request to server to create new site,
//			then updates UI.
// Parameters: None
// Returns: None
function createSite() {
	const loc = document.getElementById("InputLocation");
	const site = document.getElementById("InputSite");
	document.getElementById("error-create-site").style.display="none";
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
			if (data.redirect) {
				window.location.href = data.redirect;
				return;
			}
			loc.value = "";
			site.value = "";
			let locations = processLocationData(data);
			ResetLocations();
			populateLocations(locations[0], locations[1]);
			document.getElementById("loader").style.display = "none";
		},
		error: function (response, textStatus, errorThrown) {
			loc.value = "";
			site.value = "";
			document.getElementById("loader").style.display = "none";
			errorOverlay = document.getElementById("error-create-site");
			errorOverlay.innerHTML = response.responseText;
			errorOverlay.style.display = "block";
		}
	});
}

// Functionality:
//		Runs after user clicks 'yes' to the delete site pop-up. Sends request to server to delete the site,
//			then updates UI accordingly.
// Parameters: None
// Returns: None
function DeleteSite(){
	document.getElementById("overlay").style.display="none";

	var page_data = getCurrentPage();
	var location = page_data[0];
	var site = page_data[1];
	let Npage = page_data[2];

	$.ajax({
		type: "POST",
		url: "/form/delete-location-data/",
		dataType: "json",
		headers: {'X-CSRFToken': getCookie("csrftoken")},
		mode: 'same-origin',
		// Do not send CSRF token to another domain.
		data: {"location": location, "site": site},
		success: function (data) {
			if (data.redirect) {
				window.location.href = data.redirect;
				return;
			}
			let locations = processLocationData(data);
			ResetLocations();
			populateLocations(locations[0], locations[1]);
			let homeP = document.getElementById("homeP");
			homeP.style.display="block";
			Npage.remove();
		}
	});
}

function Logout(){
	$.ajax({
		type: "GET",
		url: "/form/admin/logout/",
		dataType: "json",
		headers: {'X-CSRFToken': getCookie("csrftoken")},
		mode: 'same-origin',
		// Do not send CSRF token to another domain.
		success: function (data) {
			if (data.redirect) {
				window.location.href = data.redirect;
				return;
			}
		}
	});
}

// Functionality:
//		Runs when 'Are you sure?' overlay 'No' button is clicked. Just disables the overlay and performs no action.
// Parameters: None
// Returns: None
function No(){
  document.getElementById("overlay").style.display="none";
  document.getElementById(Universal).style.display="none";
}

// Functionality:
//		Runs when user is done with the error overlay. Disables the overlay so user can continue to use the site.
// Parameters: None
// Returns: None
function off() {
  document.getElementById("error-overlay").style.display = "none";
}

// Functionality:
//		Runs when user clicks 'Delete Site' button in a site's page. Enables 'Are you sure?' pop-up.
// Parameters: None
// Returns: None
function DeleteOverlay() {
	document.getElementById("overlay").style.display="block";
}

// Functionality:
//		Returns the page object of the currently selected site page.
// Parameters: None
// Returns:
//		Array of current location, site, and page object of current page.
function getCurrentPage() {
	var pages = document.getElementsByClassName("PageB");
	var location = "";
	var site = "";
	var Npage = null;
	var CurPage = null;

	for (let page of pages) {
		Npage = document.getElementById(page.id + "P");
		if (page.id != "form" && page.id != "profile" && Npage.style.display != "none"){
			CurPage = Npage;
			let siteName = Npage.childNodes[0].innerText;
			let temp = siteName.split(": ");
			location = temp[0];
			site = temp[1];
		}
	}
	return [location, site, CurPage]
}

// Functionality:
//		creates HTML page elements for each location and site
// Parameters:
//		array: TODO: consult with joey about these parameters
//		string:
// Returns: None
function CreatePage(array, string) {
	const textH2 = document.createTextNode(string + ": " + array);

	const h2 = document.createElement("h2");
	h2.appendChild(textH2);

	const div1 = document.createElement("div");
	div1.setAttribute("class", "Top-Color");
	div1.appendChild(h2);

	const filename = document.createElement("a");
	filename.appendChild(document.createTextNode("Distribution Date"));

	const Update = document.createElement("a");
	Update.setAttribute("id", "Update");
	Update.appendChild(document.createTextNode("Download"));

	const filelist = document.createElement("div");
	filelist.setAttribute("class","FileList");
	filelist.setAttribute("id", "fileList")
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

// Functionality:
//		Creates Location Button and Divider for Drop Down Menu for Side Nav Bar
// Parameters:
//		string: id to be used for element creation
// Returns: None
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

// Functionality:
//		Creates all Site within Divider in Side Nav Bar
// Parameters:
//		array:
//		string:
// Returns: None
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

// Functionality:
//		Sends request to server to generate QR code for currently selected site.
// Parameters: None
// Returns: None
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
			if (data.redirect) {
				window.location.href = data.redirect;
				return;
			}

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

// Functionality:
//		Clears side-nav of all locations, usually so we can repopulate the list with new data from server response.
// Parameters: None
// Returns: None
function ResetLocations() {
	const sideBar = document.getElementById("loc");
  	while (sideBar.firstChild) {
    		sideBar.removeChild(sideBar.lastChild);
  	}
}

// Functionality:
//		Send request to server to retrieve list of dates where there was >= 1 submission at newly selected site.
//		Also, update UI with newly acquired list of dates.
// Parameters:
//		Npage: document object of newly selected page element
// Returns: None
function GetSubmissionDates(new_page) {
	var page_data = getCurrentPage();
	var location = page_data[0]
	var site = page_data[1]

	table_head = document.getElementById("fileList");
	if (table_head.lastChild.id == "submissionTable") {
		table_head.removeChild(table_head.lastChild)
	}

	$.ajax({
		type: "GET",
		url: "/form/get-submission-table/",
		data: {"location": location, "site": site},
		success: function (data) {
			if (data.redirect) {
				window.location.href = data.redirect;
				return;
			}

			filelist = document.getElementById("fileList");

			table = document.createElement("table");
			table.setAttribute("id", "submissionTable")
			filelist.appendChild(table);

			table_body = document.createElement("tbody");
			table.appendChild(table_body);

			data.forEach(function(date) {
				table_row = document.createElement("tr");
				table_body.appendChild(table_row);

				entry = document.createElement("td");
				entry.innerHTML = date;
				table_row.appendChild(entry);

				b = document.createElement("td");
				download = document.createElement("button");
				di = document.createElement("i");
				di.setAttribute("class","fa fa-download");

				download.appendChild(di);
				download.setAttribute("id","download");
				download.setAttribute("onClick", "DownloadSubmissions('" + site + "','" + date + "')");

				b.appendChild(download);
				table_row.appendChild(b);
			});
		}
	});
}

function DownloadSubmissions(site, date) {
	$.ajax({
		type: "GET",
		url: "/form/get-excel-file/",
		data: {"site": site, "date": date},
		xhrFields: {
            responseType: 'blob' // Set the response type to blob
        },
		success: function (data) {
			if (data.redirect) {
				window.location.href = data.redirect;
				return;
			}

			var blob = new Blob([data], {
				type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
			}); // Create a blob from the response data
            var url = window.URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = site + ' ' + date + '.xlsx'; // Specify the filename
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
		}
	});
}

// Functionality:
//		Creates list of locations and sites in side-nav, as drop down menus. Ran on page load.
// Parameters:
//		locations: array of string location names
//		sites: 2d array of sites, each element of array is a list of sites
//			under the same indexed location from locations array
// Returns: None
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
			// TODO: Run function to send AJAX request to generate list of submission dates and update table
			if (e.target.id + "P" != "homeP" && e.target.id + "P" != "formP"){
				GetSubmissionDates(Npage);
			}
		});
	}
}

function populateFormSettings(inputSettings) {
	for (var i = 0; i < inputSettings.length; i++) {
		FormSetting(inputSettings[i], i, i + 1 == inputSettings.length);
	}
}

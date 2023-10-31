import * as d3 from "https://cdn.skypack.dev/d3@7.3.0";
const page = "home";

const Sites = [["Comstock Middle School"],["Galesburg United Methodist Church"],["Saint Andrew Community Church","Heritage Christian Reformed Church","Haven Church","Douglass Community Association","Sunnyside United Methodist Church","The Salvation Army"],["Chapel Hill United Methodist Church"],["Vicksburg United Methodist Church"]];


d3.select("cs").selectAll("a")
  .data(Sites[0])
  .enter()
  .append("a")
  .text((d) => d);

d3.select("gb").selectAll("a")
  .data(Sites[1])
  .enter()
  .append("a")
  .text((d) => d);

d3.select("kz").selectAll("a")
  .data(Sites[2])
  .enter()
  .append("a")
  .text((d) => d);

d3.select("pt").selectAll("a")
  .data(Sites[3])
  .enter()
  .append("a")
  .text((d) => d);

d3.select("vb").selectAll("a")
  .data(Sites[4])
  .enter()
  .append("a")
  .text((d) => d);



var dropdown = document.getElementsByClassName("dropdown-btn");
var i;

for (i = 0; i < dropdown.length; i++) {
  dropdown[i].addEventListener("click", function() {
    var dropdownContent = this.nextElementSibling;
    if (dropdownContent.style.display === "block") {
      dropdownContent.style.display = "none";
    } else {
      dropdownContent.style.display = "block";
    }
  });
}
$(document).ready(function () {
  var error = document.getElementById("error");
  if (error.innerText === "") {
    error.style.display = "none";
  }
  var redirect = document.getElementById("redirect");
  if (redirect != null && redirect.innerText == 1) {
    setTimeout(function() {
      window.location.href = "/form/login";
    }, 3000); // 3000 milliseconds = 5 seconds
  }
});

function Check(){
  console.log("checking equality!");
  const Ps = document.getElementById("NPassword").value;
  const CPs = document.getElementById("CPassword").value;
  if (Ps != CPs){
    console.log("Not equal!");
    var error = document.getElementById("error");
    error.innerText = "New passwords do not match!"
    error.style.display = "block";
    return false;
  }
}

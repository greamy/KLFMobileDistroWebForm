$(document).ready(function () {
  var error = document.getElementById("error");
  if (error.innerText === "") {
    error.style.display = "none";
  }
});

function Check(){
  const Ps = document.getElementById("NPassword").value;
  const CPs = document.getElementById("CPassword").value;
  if (Ps != CPs){
    document.getElementById("warning").style.display = "block";
    return false;
  }
}

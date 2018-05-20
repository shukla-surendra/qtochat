//getting token
element = document.getElementById("qtochat_start_script")
token = element.getAttribute("token")
console.log(token)
notify_visit_to_server(token)

function notify_visit_to_server(token) {
  var xhttp;
  if (window.XMLHttpRequest) {
    // code for modern browsers
    xhttp = new XMLHttpRequest();
    } else {
    // code for IE6, IE5
    xhttp = new ActiveXObject("Microsoft.XMLHTTP");
  }

  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
     console.log(this.responseText);
    }
  };
  xhttp.open("POST", "http://127.0.0.1:8000/notify", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  //xhttp.setRequestHeader('Accept', 'application/json');
  data = "token="+token+"&test=testdata";
  xhttp.send(data);
}
SITE="http://127.0.0.1:8000/"
//getting token
element = document.getElementById("qtochat_start_script")
token = element.getAttribute("token")
console.log(token)
notify_visit_to_server(token)


//setting cookie

function getCookie(c_name, remote) {


    // get normal cookies
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}

function setCookie(c_name, value, expiredays, remote) {


    var cookiebody;
    var exdate = new Date();
    exdate.setSeconds(exdate.getSeconds() + expiredays);
    //exdate.setDate(exdate.getDate() + expiredays);

    cookiebody = c_name + "=" + escape(value) +
((expiredays == null) ? "" : ";expires=" + exdate.toUTCString());

    if (remote != null) {
        // remote cookie// send cookies to LogonServ
    }
    else // normal cookie
        document.cookie = cookiebody;
}

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
   // Check for UUID of this user (if not exist create one)
  var uuid = getCookie("site_uuid");
  if (uuid == "") {
    var d = new Date();
    var rnd = Math.floor((Math.random() * 100000) + 1);
    uuid = d.getDay() + '_' + d.getMonth() + '_' + d.getYear() + '_' + rnd + '_' + d.getSeconds() + '_' + d.getMilliseconds() + '_' + d.getMinutes() + '_' + d.getHours();
    setCookie("site_uuid", uuid);
  }
  xhttp.open("POST", SITE+"notify?type=ping&quuid="+uuid, true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  //xhttp.setRequestHeader('Accept', 'application/json');

  data = "token="+token;
  xhttp.send(data);
}

chatFrame='<div class="chatframe" style="height:350px;width:250px;position:fixed;bottom:40px;right:40px;border-radius:15px">'
+'<div class="chatbox_header" style="width:100%;height:10%;border-radius:15px 15px 0 0; background-color:#428bca"></div>'
+'<div class="chatbox_content" id="chatbox_content" style="width:100%;height:80%;overflow-y: auto; padding:10px;box-sizing:border-box"><p>first</p><p>p</p><p>p</p><p>p</p><p>p</p><p>p</p><p>p</p><p>p</p><p>p</p><p>p</p><p>p</p><p>p</p><p>p</p><p>p</p><p>p</p><p>p</p><p>p</p><p>p</p><p>p</p><p>p</p><p>p</p><p>p</p><p>p</p><p>p</p><p>p</p><p>p</p><p>p</p><p>p</p><p>p</p><p>p</p><p>last</p></div>'
+'<div class="chatbox_footer" style="width:100%;height:10%;border-radius:0 0 15px 15px; background-color:#f0f3f5"><input type="text" placeholder="Write A reply..." id="qto_text_field" onkeypress="runScript(event)" style="background-color:#f0f3f5; border:0 solid #f0f3f5; width:100%;"></div>'
+'</div>';
var wrapper= document.createElement('div');
wrapper.innerHTML= chatFrame;
var div = wrapper.firstChild;
document.body.appendChild(div);

function runScript(e) {
    if (e.keyCode == 13) {
       value = document.getElementById("qto_text_field").value;
       var nwrapper= document.createElement('div');
       nwrapper.innerHTML= "<p>"+value+"</p>";
       document.getElementById("chatbox_content").appendChild(nwrapper);
       document.getElementById("qto_text_field").value = "";
       scrollToBottom();
       replyFromBot();
    }
}


function replyFromBot()
    {
        var nwrapper= document.createElement('div');
        nwrapper.innerHTML= "<p> Hello This is reply from Bot</p>";
        document.getElementById("chatbox_content").appendChild(nwrapper);
        scrollToBottom();
    }

function scrollToBottom()
{
    var objDiv = document.getElementById("chatbox_content");
    objDiv.scrollTop = objDiv.scrollHeight;	
}
scrollToBottom();
//Start variable declaration
qtochat_server_url = "http://127.0.0.1:3000/";
qtochat_content = document.getElementById("qtochat_content");
qtochat_foot = document.getElementById("qtochat_input");
(function() {
  $("#live-chat header").on("click", function() {
    $(".chat").slideToggle(300, "swing");
    $(".chat-message-counter").fadeToggle(300, "swing");
  });

  $(".chat-close").on("click", function(e) {
    e.preventDefault();
    $("#live-chat").fadeOut(300);
    //$(window.parent.document).find("qtochat-chat").fadeOut(300);
    window.parent.document.getElementById("qtochat-chat").style.display =
      "none";
  });
})();

//getting cookie
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

//setting cookie
function setCookie(c_name, value, expiredays, remote) {
  var cookiebody;
  var exdate = new Date();
  exdate.setSeconds(exdate.getSeconds() + expiredays);
  //exdate.setDate(exdate.getDate() + expiredays);
  cookiebody =
    c_name +
    "=" +
    escape(value) +
    (expiredays == null ? "" : ";expires=" + exdate.toUTCString());
  if (remote != null) {
    // remote cookie// send cookies to LogonServ
  } // normal cookie
  else document.cookie = cookiebody;
}

//return uuid
function getUUID() {
  var uuid = getCookie("qtochat_uuid");
  if (uuid == "") {
    var d = new Date();
    var rnd = Math.floor(Math.random() * 100000 + 1);
    uuid =
      d.getDay() +
      "_" +
      d.getMonth() +
      "_" +
      d.getYear() +
      "_" +
      rnd +
      "_" +
      d.getSeconds() +
      "_" +
      d.getMilliseconds() +
      "_" +
      d.getMinutes() +
      "_" +
      d.getHours();
    setCookie("qtochat_uuid", uuid);
  }
  return uuid;
}

//return token
function getToken() {
  element = window.parent.document.getElementById("qtochat_start_script");
  token = element.getAttribute("token");
  return token;
}

//getting Socket Connection Object
function getSocket() {
  var socket = io(
    qtochat_server_url+"?token=" + getToken() + "&uuid=" + getUUID()
  );
  return socket;
}

socket = getSocket();

function appendResponse(respMessage) {
  window.sessionStorage.setItem("question", JSON.stringify(respMessage));

  if (respMessage.expectedControl == "yes/no") {
    responseBox = document.createElement("div");
    responseBox.setAttribute("class", "chat-message clearfix");
    responseBox.setAttribute("id", "chat-message");
    responseBox.innerHTML =
      '<img src="http://gravatar.com/avatar/2c0ad52fc5943b78d6abe069cc08f320?s=32" alt="Avatar" height="32" width="32">' +
      '<div class="chat-message-content clearfix">' +
      respMessage.message +
      '</div><a href="#" class="react" data-ans="yes" onclick="respondYes(this)">Yes</a>&nbsp;<a href="#" class="react" onclick="respondNo(this)" data-ans="no">No</a>';
    qtochat_content.appendChild(responseBox);
    //disable input area
    disableChatInput();
  } else if (respMessage.expectedControl == "text") {
    responseBox = document.createElement("div");
    responseBox.setAttribute("class", "chat-message clearfix");
    responseBox.innerHTML =
      '<img src="http://gravatar.com/avatar/2c0ad52fc5943b78d6abe069cc08f320?s=32" alt="Avatar" height="32" width="32">' +
      '<div class="chat-message-content clearfix">' +
      respMessage.message +
      "</div>";
    qtochat_content.appendChild(responseBox);
    //disable input area
    enableChatInput();
  } else if (respMessage.expectedControl == "") {
    responseBox = document.createElement("div");
    responseBox.setAttribute("class", "chat-message clearfix");
    responseBox.innerHTML =
      '<img src="http://gravatar.com/avatar/2c0ad52fc5943b78d6abe069cc08f320?s=32" alt="Avatar" height="32" width="32">' +
      '<div class="chat-message-content clearfix">' +
      respMessage.message +
      "</div>";
    qtochat_content.appendChild(responseBox);
    disableChatInput();
  }

  scrollToBottom();
}
//get response from event
socket.on("message", function(respMessage) {
  appendResponse(respMessage);
});
//disable chat Input
function disableChatInput() {
  qtochat_foot.style.display = "none";
}
//fire submit from user
qtochat_foot.addEventListener("keypress", function(event) {
  if (event.keyCode === 13) {
    question_object = JSON.parse(window.sessionStorage.getItem("question"));
    response = qtochat_foot.value;
    response = response.replace(/<(?:.|\n)*?>/gm, "");
    if (response == "") {
      qtochat_foot.value = "";
      return;
    }
    response_object = JSON.parse(window.sessionStorage.getItem("question"));
    response_object.message = response;
    message = response_object;
    socket.emit("message", message);
    responseBox = document.createElement("div");
    responseBox.setAttribute("class", "message-left");
    responseBox.innerHTML =
      '<div class ="chat-message clearfix">' + response + "</div>";
    qtochat_content.appendChild(responseBox);
    qtochat_foot.value = "";
    scrollToBottom();
    //disabling chat input
    disableChatInput();
  }
});

//disable chat Input
function enableChatInput() {
  qtochat_foot.style.display = "block";
}

function respondYes(self) {
  //there is "&nbsp;" after self treated as next sibling so to remove anchor self.nextSibling.nextSibling is used
  self.parentNode.removeChild(self.nextSibling.nextSibling);
  self.parentNode.removeChild(self);
  response_object = JSON.parse(window.sessionStorage.getItem("question"));
  response_object.message = "yes";
  socket.emit("message", response_object);
  //append replies to chatbox as yes from user side
}

function respondNo(self) {
  //there is "&nbsp;" after self treated as next sibling so to remove anchor self.nextSibling.nextSibling is used
  self.parentNode.removeChild(self.previousSibling.previousSibling);
  self.parentNode.removeChild(self);
  response_object = JSON.parse(window.sessionStorage.getItem("question"));
  response_object.message = "no";
  socket.emit("message", response_object);
  console.log(response_object);
  //apend replies to chatbox as yes from user side
}

function loadChatProfile() {
  var xhttp = new XMLHttpRequest();
  xhttp.open(
    "GET",
    qtochat_server_url + "load_chat_profile/" + getToken(),
    false
  );
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      json_object = JSON.parse(this.responseText);
      window.sessionStorage.setItem(
        "question",
        JSON.stringify(json_object.default_q)
      );
      appendResponse(json_object.default_q);
    }
  };

  xhttp.send();
}

//scroll chat to bottom
function scrollToBottom() {
  qtochat_content.scrollTop = qtochat_content.scrollHeight;
}

//inititalise chat
loadChatProfile();

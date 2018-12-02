SITE = 'http://qtochat.com'
const myvar =
  "<html>" +
  "<head>" +
  '<link rel="stylesheet" href="'+SITE+'/static/app/style.css"/>' +
  '<script src="'+SITE+'/static/app/socket.io.js"></script>' +
  "</head>" +
  "<body>" +
  '	<div id="live-chat">		' +
  '		<header class="clearfix">' +
  '			<a href="#" class="chat-close">x</a>' +
  "			<h4>John Doe</h4>" +
  '			<span class="chat-message-counter">3</span>' +
  "		</header>" +
  '		<div class="chat">' +
  `
  ` +
  '			<div class="chat-history" id="qtochat_content">' +
  ' <div class="welcome"><img src="'+SITE+'/static/app/giphy.gif"></div>' +
  "			</div> <!-- end chat-history -->" +
  '			<div style="height:30px">			' +
  '         <pre class="qtochat-chat-send-button"></pre>' +
  '					<input type="text" id="qtochat_input" placeholder="Type your message?" autofocus></div>' +
  "		</div> <!-- end chat -->" +
  ` <div class='footer_note'>Chat by Qtochat` +
  "	</div>" +
  "<!-- end live-chat -->" +
  '<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.0.2/jquery.min.js"></script>' +
  '<script src="'+SITE+'/static/app/internal.js"></script>' +
  "</body>" +
  "</html>";

const scriptTag = document.getElementById("qtochat_start_script");
const qtochatInput = document.getElementById("qtochat_input");
const chatmessage = document.getElementById("chat-message");
const wrapperDiv = document.createElement("div");
wrapperDiv.setAttribute("id", "qtochat-chat");
ifrm = document.createElement("iframe");
ifrm.setAttribute("id", "qtochat-iframe");
ifrm.setAttribute("frameborder", 0);
ifrm.setAttribute("allowfullscreen", "");
ifrm.setAttribute("onload", "iframeLoaded()");
wrapperDiv.appendChild(ifrm);

ifrm.onload = function() {
  doc = document.getElementById("qtochat-iframe").contentWindow.document;
  doc.open();
  doc.write(myvar);
  doc.close();
};

document.body.appendChild(wrapperDiv);
//Need more Robust Solution
setTimeout(function() {
  document
    .getElementById("qtochat-chat")
    .setAttribute(
      "style",
      "bottom: 100px; font-size: 12px; right: 24px;position: fixed; width:300px;"
    );

  document.getElementById("qtochat-chat").style.boxShadow =
    "0 0 10px rgba(0, 0, 0, 0.6)";

  document.getElementById("qtochat-iframe").height = document.getElementById(
    "qtochat-iframe"
  ).contentWindow.document.body.scrollHeight;
}, 500);

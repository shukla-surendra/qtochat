
if (window.addEventListener) {window.addEventListener('DOMMouseScroll', wheel, false);
window.onmousewheel = document.onmousewheel = wheel;}

function wheel(event) {
  var delta = 0;
  if (event.wheelDelta) delta = (event.wheelDelta)/120 ;
  else if (event.detail) delta = -(event.detail)/3;

  handle(delta);
  if (event.preventDefault) event.preventDefault();
  event.returnValue = false;
}

function handle(sentido) {
  var inicial = document.body.scrollTop;
  var time = 1000;
  var distance = 200;

animate({
  delay: 0,
  duration: time,
  delta: function(p) {return p;},
  step: function(delta) {
window.scrollTo(0, inicial-distance*delta*sentido);   
  }
})}

function setCookie(name,value,date) {
  if (date) {

    var expires = "; expires="+date.toGMTString();
  }
  else var expires = "";
  document.cookie = name+"="+value+expires+"; path=/";
}

function getCookie(name) {
  var nameEQ = name + "=";
  var ca = document.cookie.split(';');
  for(var i=0;i < ca.length;i++) {
    var c = ca[i];
    while (c.charAt(0)==' ') c = c.substring(1,c.length);
    if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
  }
  return null;
}

function removeCookie(name) {
  setCookie(name,"",ExpireDayCookie(-1));
}

function ExpireMinCookie(minutes) {
    var date = new Date();
    date.setTime(date.getTime() + (minutes * 60 * 1000));
    return date;
}

function ExpireDayCookie(days) {
    var date = new Date();
    date.setTime(date.getTime()+(days*24*60*60*1000));
    return date;
}

function ExpireSecCookie(secs) {
    var date = new Date();
    date.setTime(date.getTime()+(secs*1000));
    return date;
}
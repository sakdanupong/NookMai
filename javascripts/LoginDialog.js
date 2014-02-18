var gLoginDialog;
var width = 900;
var height = 400;

function LoginDialog() {
	var $ = document;
	var head  = $.getElementsByTagName('head')[0];
    var link  = $.createElement('link');
    link.rel  = 'stylesheet';
    link.type = 'text/css';
    link.href = '/stylesheets/login_dialog.css';
    link.media = 'all';
    head.appendChild(link);

	var dialog = "<div id='dialog-overlay'></div> \
	       		  <div id='dialog-box'> \
				  	<div class='dialog-content'> \
				  		<div><a class='hyper_link_no_underline' id='close_this_window' href='#'>close this window</a></div> \
				  		<div id='login_dialog_caption'>you'll need to login or register to do that</div> \
				  		<div>\
				  			<div id='login_div'>\
				  				<div id='login_right_div'>\
				  					<div id='create_account_caption'><b>LOGIN</b></div>\
				  					<div id='create_account_sub_caption'>already have an account and just want to login?</div>\
				  					<div class='login_input_wrapper'><p class='login_dialog_title'>username: </p><input class='login_dialog_input' id='login_username' type='text'></input></div>\
				  					<div class='login_input_wrapper'><p class='login_dialog_title'>password: </p><input class='login_dialog_input' id='login_password' type='text'></input></div>\
				  					<div class='login_input_wrapper'><input type='checkbox' id='login_rememberme' onClick='loginRememberme();'></input><label class='login_dialog_title'> remember me</label></div>\
				  					<div class='login_input_wrapper'><a class='hyper_link_no_underline' href='#'>recovery password</a></div>\
				  					<div class='login_input_wrapper'><input type='submit' value='login' onClick='clickLogin();'></input></div>\
				  				</div>\
				  				<div id='login_left_div'><div id='vertical_line'></div></div>\
				  			</div>\
				  			<div id='register_div'>\
				  				<div id='register_right_div'> \
				  					<div class='register_privacy_caption'><b>privacy philosophy</b></div>\
				  					<div class='login_input_wrapper'>\
				  						<ul id='privacy_choice'>\
											<li>we limit data collected about you and your use of the platform,</li>\
											<li>your personal information is never for sale,</li>\
											<li>we use and disclose information to prevent people from abusing the platform, but</li>\
											<li>we never disclose it for any other reason unless required by law.</li>\
										</ul>\
				  					</div>\
				  					<div class='login_input_wrapper'><label class='login_dialog_title'>for more information, see our </label><a class='hyper_link_no_underline' href='#' class='login_dialog_title'>privacy policy.</a></div>\
				  				</div> \
				  				<div id='register_left_div'> \
				  					<div id='create_account_caption'><b>CREATE A NEW ACCOUNT</b></div>\
				  					<div id='create_account_sub_caption'>all it takes is a username and password</div>\
				  					<div id='register_content_div'>\
				  						<div class='login_input_wrapper'><p class='login_dialog_title'>username: </p><input class='login_dialog_input' id='register_username' type='text'></input></div>\
				  						<div class='login_input_wrapper'><p class='login_dialog_title'>account recovery email: </p><input class='login_dialog_input' id='register_email' type='text'></input></div>\
				  						<div class='login_input_wrapper'><p class='login_dialog_title'>password: </p><input class='login_dialog_input' id='register_password' type='text'></input></div>\
				  						<div class='login_input_wrapper'><p class='login_dialog_title'>verify password: </p><input class='login_dialog_input' id='register_confirm_password' type='text'></input></div>\
				  						<div class='login_input_wrapper'><input type='checkbox' id='register_rememberme' onClick='registerRememberme();'></input><label class='login_dialog_title'> remember me</label></div>\
				  						<div class='login_input_wrapper'><input type='submit' value='create account' onClick='clickRegister();'></input></div>\
				  					</div>\
				  				</div> \
				  			</div>\
				  		</div> \
	       			</div>\
	       		  </div>"

	this.gLoginDialog = $.createElement('div');
    this.gLoginDialog.innerHTML = dialog;
  	
}

LoginDialog.prototype.show = function() {
	var _body = document.getElementsByTagName('body') [0];
	// <body scroll="no"> 
    _body.appendChild(this.gLoginDialog);

    getRemember();

  	var maskHeight = $(document).height();  
	var maskWidth = $(window).width();
	var windowHeight = $(window).height();

	// calculate the values for center alignment
	var dialogTop =  (windowHeight - height) / 2; 
	var dialogLeft = (maskWidth - width) / 2;//(maskWidth/2) - ($('#dialog-box').width()/2); /

	// // assign values to the overlay and dialog box
	$('#dialog-overlay').css({height:maskHeight, width:maskWidth});
	$('#dialog-box').css({height:height, width:width});
	$('#dialog-box').css({top:dialogTop, left:dialogLeft});

	// display the message
	$('#dialog-message').html("message");

	$('#dialog-overlay, #close_this_window').click(function () {		
		gLoginDialog.dismissLoginDialog();
		return false;
	});

};

LoginDialog.prototype.dismissLoginDialog = function() {
	// alert('sdfsdfsfd');
	if (this.gLoginDialog) {
		this.gLoginDialog.remove();	
	}
};

function getRemember() {
	var login_username = getCookie('login_username');
	if (login_username)
     	$("#login_username").val(login_username);
	var login_password = getCookie('login_password');
	if (login_password)
		$("#login_password").val(login_password);
	var login_check = getCookie('logincheckbox');
	if (login_check)
		$("#login_rememberme").prop("checked", true);

	var register_username = getCookie('register_username');
	if (register_username)
		$("#register_username").val(register_username);
	var register_password = getCookie('register_password');
	if (register_password)
		$("#register_password").val(register_password);
	var register_confirm_password = getCookie('register_confirm_password');
	if (register_confirm_password)
		$("#register_confirm_password").val(register_confirm_password);
	var register_email = getCookie('register_email');
	if (register_email)
		$("#register_email").val(register_email);
	var registercheckbox = getCookie('registercheckbox');
	if (registercheckbox)
		$("#register_rememberme").prop("checked", true);

};

function clickRegister() {
	alert('register click !!!!');
};

function clickLogin() {
	alert('login click!!');
};

function registerRememberme() {
	var c = $("#register_rememberme");
   if(c.is(":checked")){
     var u = $("#register_username").val();
     var p = $("#register_password").val();
     var cp = $("#register_confirm_password").val();
     var e = $("#register_email").val();

     setCookie("register_username", u, ExpireMinCookie(5));
     setCookie("register_password", p, ExpireMinCookie(5));
     setCookie("register_confirm_password", cp, ExpireMinCookie(5));
     setCookie("register_email", e, ExpireMinCookie(5));
     setCookie("registercheckbox", 1, ExpireMinCookie(5))
   } else {
	 removeCookie('register_username');
	 removeCookie('register_password');
     removeCookie('register_confirm_password');
     removeCookie('register_email');
     removeCookie('registercheckbox');
   }
};

 function loginRememberme() {
	var c = $("#login_rememberme");
   if(c.is(":checked")){
   	 var u = $("#login_username").val();
     var p = $("#login_password").val();
     setCookie("login_username", u, ExpireDayCookie(2));
     setCookie("login_password", p, ExpireDayCookie(2));
     setCookie("logincheckbox", 1, ExpireDayCookie(2))
   } else {
		removeCookie('login_username');
		removeCookie('login_password');
		removeCookie('logincheckbox');
   } 
};




// LoginDialog.prototype.reloadScrollBars = function() {
//     document.documentElement.style.overflow = 'auto';  // firefox, chrome
//     document.body.scroll = "yes"; // ie only
// }

// LoginDialog.prototype.unloadScrollBars = function() {
//     document.documentElement.style.overflow = 'hidden';  // firefox, chrome
//     document.body.scroll = "no"; // ie only
// }

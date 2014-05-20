var gLoginDialog;
var width = 900;
var height = 400;
var registerCallBack;
var loginCallBack;
var registerRequest;
var loginRequest;
var obj;

function LoginDialog(p_registerCallback, p_loginCallback) {
	var $ = document;
	var head  = $.getElementsByTagName('head')[0];
    var link  = $.createElement('link');
    link.rel  = 'stylesheet';
    link.type = 'text/css';
    link.href = '/stylesheets/login_dialog.css';
    link.media = 'all';
    head.appendChild(link);

    var link  = $.createElement('link');
    link.rel  = 'stylesheet';
    link.type = 'text/css';
    link.href = '/stylesheets/login_loading.css';
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
				  					<div class='login_input_wrapper'><p class='login_dialog_title'>password: </p><input class='login_dialog_input' id='login_password' type='password'></input></div>\
				  					<div class='login_input_wrapper'><input type='checkbox' id='login_rememberme' onClick='loginRememberme();'></input><label class='login_dialog_title'> remember me</label></div>\
				  					<div class='login_input_wrapper'><a class='hyper_link_no_underline' href='#'>recovery password</a></div>\
				  					<div class='login_input_wrapper'>\
				  						<input id='login_btn' type='submit' value='login' onClick='clickLogin();'></input>\
				  						<div id='login_loading'>\
				  							<div id='noTrespassingOuterBarG'>\
												<div id='noTrespassingFrontBarG' class='noTrespassingAnimationG'>\
													<div class='noTrespassingBarLineG'></div>\
													<div class='noTrespassingBarLineG'></div>\
													<div class='noTrespassingBarLineG'></div>\
													<div class='noTrespassingBarLineG'></div>\
													<div class='noTrespassingBarLineG'></div>\
													<div class='noTrespassingBarLineG'></div>\
												</div>\
											</div>\
										</div>\
				  					</div>\
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
				  						<div class='login_input_wrapper'><p class='login_dialog_title'>password: </p><input class='login_dialog_input' id='register_password' type='password'></input></div>\
				  						<div class='login_input_wrapper'><p class='login_dialog_title'>verify password: </p><input class='login_dialog_input' id='register_confirm_password' type='password'></input></div>\
				  						<div class='login_input_wrapper'><input type='checkbox' id='register_rememberme' onClick='registerRememberme();'></input><label class='login_dialog_title'> remember me</label></div>\
				  						<div class='login_input_wrapper'>\
				  							<input id='create_account_btn' type='submit' value='create account' onClick='clickRegister();'></input>\
				  							<div id='register_loading'>\
					  							<div id='noTrespassingOuterBarG'>\
													<div id='noTrespassingFrontBarG' class='noTrespassingAnimationG'>\
														<div class='noTrespassingBarLineG'></div>\
														<div class='noTrespassingBarLineG'></div>\
														<div class='noTrespassingBarLineG'></div>\
														<div class='noTrespassingBarLineG'></div>\
														<div class='noTrespassingBarLineG'></div>\
														<div class='noTrespassingBarLineG'></div>\
													</div>\
												</div>\
											</div>\
				  						</div>\
				  					</div>\
				  				</div> \
				  			</div>\
				  		</div> \
	       			</div>\
	       		  </div>"

	this.gLoginDialog = $.createElement('div');
    this.gLoginDialog.innerHTML = dialog;
    this.loginCallBack = p_loginCallback;
    registerCallBack = p_registerCallback;
  	show();
  	obj = this;
}

function show() {
	//var _body = document.getElementsByTagName('body') [0];
	// <body scroll="no"> 
    //_body.appendChild(this.gLoginDialog);
    document.body.appendChild(gLoginDialog);

    getRemember();

  	var maskHeight = $(document).height();  
	var maskWidth = $(window).width();
	var windowHeight = $(window).height();

	// calculate the values for center alignment
	var dialogTop =  (windowHeight - height) / 2; 
	var dialogLeft = (maskWidth - width) / 2;//(maskWidth/2) - ($('#dialog-box').width()/2); /

	var beginDialogPost = -height;
	// // assign values to the overlay and dialog box
	$('#dialog-overlay').css({height:maskHeight, width:maskWidth});
	$('#dialog-box').css({height:height, width:width});
	$('#dialog-box').css({top:beginDialogPost, left:dialogLeft});

	var animateTop = dialogTop + height;
	$('#dialog-box').animate({top: '+='+animateTop}, 600, function () {
	});


	$('#dialog-overlay, #close_this_window').click(function () {		
		dismissLoginDialog();
		return false;
	});

};

function dismissLoginDialog(p_callBack) {

	cancelAllRequest();

	var windowHeight = $(window).height();

	// calculate the values for center alignment
	var dialogTop =  (windowHeight - height) / 2; 

	var animateTop = dialogTop + height;
	$('#dialog-box').animate({top: '-='+animateTop}, 600, function () {
		setTimeout(function() {
			if (gLoginDialog) {
				gLoginDialog.remove();	
			}
			if (p_callBack)
				p_callBack();
		} ,100);
	});


};

function getRemember() {
	var login_username = getCookie('login_username');
	if (login_username)
     	$("#login_username").val(login_username);
	var login_password = getCookie('login_password');
	// if (login_password)
	// 	$("#login_password").val(login_password);
	var login_check = getCookie('logincheckbox');
	if (login_check)
		$("#login_rememberme").prop("checked", true);

	var register_username = getCookie('register_username');
	if (register_username)
		$("#register_username").val(register_username);
	// var register_password = getCookie('register_password');
	// if (register_password)
	// 	$("#register_password").val(register_password);
	// var register_confirm_password = getCookie('register_confirm_password');
	// if (register_confirm_password)
	// 	$("#register_confirm_password").val(register_confirm_password);
	var register_email = getCookie('register_email');
	if (register_email)
		$("#register_email").val(register_email);
	var registercheckbox = getCookie('registercheckbox');
	if (registercheckbox)
		$("#register_rememberme").prop("checked", true);

};

function cancelAllRequest() {
	if(registerRequest && registerRequest.readystate != 4){
        registerRequest.abort();
        registered();
    }

    if(loginRequest && loginRequest.readystate != 4){
        loginRequest.abort();
        logedin();
    }
}

function registering() {
	var loading = $("#register_loading");
	var button = $("#create_account_btn");
	loading.show();
	button.hide();
}

function registered() {
	var loading = $("#register_loading");
	var button = $("#create_account_btn");
	loading.hide();
	button.show();
}

function clickRegister() {
	cancelAllRequest();
	var u = $("#register_username").val();
	var p = $("#register_password").val();
	var cp = $("#register_confirm_password").val();
	var e = $("#register_email").val();

	if (u.length == 0 || p.length == 0 || cp.length == 0) {
		if (u.length == 0) 
			alert("Please fill username.");
		else if (p.length == 0)
			alert("Please fill password.");
		else if (cp.length == 0)
			alert("Please fill verify password.");

		return;
	}

	if (u.length < 4) {
		alert("username must have least 4 letters.");
		return;
	}

	if (p.length < 8 || cp.length < 8) {
		alert("password must have least 8 letters");
		return;
	}

	if (p != cp) {
		alert('Password and verify password mismatch.');
		return;
	}

	var pHash = md5(p);

	var formData = new FormData();
    formData.append('username', u);
    formData.append('password', pHash);
    formData.append('email', e)

	registering();

	registerRequest = $.ajax({
	            url: '/api_register',  //Server script to process data
	            type: 'POST',
	            mimeType:"multipart/form-data",
	            dataType: 'json',
	            success: function(json) {
	              var success = json['success'];
	              var data = json['data'];
	              var reason = json['reason'];
	              registerCallBack(success, data, reason, obj);
	              registered();
	            },
	            data: formData,
	            cache: false,
	            contentType: false,
	            processData: false
	          });


};

function logingin() {
	var loading = $("#login_loading");
	var button = $("#login_btn");
	loading.show();
	button.hide();
}

function logedin() {
	var loading = $("#login_loading");
	var button = $("#login_btn");
	loading.hide();
	button.show();
}

function clickLogin() {
	cancelAllRequest();
	var u = $("#login_username").val();
	var p = $("#login_password").val();

	if (u.length == 0 || p.length == 0)
		return;

	var pHash = md5(p);
	var formData = new FormData();
    formData.append('username', u);
    formData.append('password', pHash);

	logingin();

	loginRequest = $.ajax({
	            url: '/api_login',  //Server script to process data
	            type: 'POST',
	            mimeType:"multipart/form-data",
	            dataType: 'json',
	            success: function(json) {
	              var success = json['success'];
	              var data = json['data'];
	              var reason = json['reason'];
	              loginCallBack(success, data, reason, obj);
	              logedin();
	            },
	            data: formData,
	            cache: false,
	            contentType: false,
	            processData: false
	          });
};

function registerRememberme() {
	var c = $("#register_rememberme");
   if(c.is(":checked")){
     var u = $("#register_username").val();
     // var p = $("#register_password").val();
     var cp = $("#register_confirm_password").val();
     var e = $("#register_email").val();

     // password to md5
     // var pHash = md5(p);

     setCookie("register_username", u, ExpireMinCookie(5));
     // setCookie("register_password", pHash, ExpireMinCookie(5));
     setCookie("register_confirm_password", cp, ExpireMinCookie(5));
     setCookie("register_email", e, ExpireMinCookie(5));
     setCookie("registercheckbox", 1, ExpireMinCookie(5))
   } else {
	 removeCookie('register_username');
	 // removeCookie('register_password');
     removeCookie('register_confirm_password');
     removeCookie('register_email');
     removeCookie('registercheckbox');
   }
};

 function loginRememberme() {
	var c = $("#login_rememberme");
   if(c.is(":checked")){
   	 var u = $("#login_username").val();
     // var p = $("#login_password").val();

     // password to md5
     // var pHash = md5(p);

     setCookie("login_username", u, ExpireDayCookie(2));
     // setCookie("login_password", pHash, ExpireDayCookie(2));
     setCookie("logincheckbox", 1, ExpireDayCookie(2))
   } else {
		removeCookie('login_username');
		// removeCookie('login_password');
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

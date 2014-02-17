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

	// var dialog = "<div id='dialog-overlay'></div> \
	//        		  <div id='dialog-box'> \
	// 			  	<div class='dialog-content'> \
	// 					<div id='dialog-message'></div>\
	// 					<a id='btn-login' href='#' class='button'>Close</a>\
	//        			</div>\
	//        		  </div>"

	var dialog = "<div id='dialog-overlay'></div> \
	       		  <div id='dialog-box'> \
				  	<div class='dialog-content'> \
				  		<div id='login_dialog_caption'>you'll need to login or register to do that</div> \
				  		<div>\
				  			<div id='register_div'>\
				  				<div id='register_left_div'> \
				  					<div id='create_account_caption'><b>CREATE A NEW ACCOUNT</b></div>\
				  					<div id='create_account_sub_caption'>all it takes is a username and password</div>\
				  					<div id='register_content_div'>\
				  						<div class='login_input_wrapper'><p class='login_dialog_title'>username: </p><input class='login_dialog_input' id='username' type='text'></input></div>\
				  						<div class='login_input_wrapper'><p class='login_dialog_title'>account recovery email: </p><input class='login_dialog_input' id='email' type='text'></input></div>\
				  						<div class='login_input_wrapper'><p class='login_dialog_title'>password: </p><input class='login_dialog_input' id='password' type='text'></input></div>\
				  						<div class='login_input_wrapper'><p class='login_dialog_title'>verify password: </p><input class='login_dialog_input' id='confirm_password' type='text'></input></div>\
				  						<div class='login_input_wrapper'><input type='checkbox' id='rememberme'></input><label class='login_dialog_title'> remember me</label></div>\
				  						<div class='login_input_wrapper'><input type='submit' value='create account' onClick='gLoginDialog.clickRegister()'></input></div>\
				  					</div>\
				  				</div> \
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
				  					<div class='login_input_wrapper'><label class='login_dialog_title'>for more information, see our </label><a href='#' class='login_dialog_title'>privacy policy.</a></div>\
				  				</div> \
				  			</div>\
				  			<div id='login_div'>\
				  			</div>\
				  		</div> \
						<a id='btn-login' href='#' class='button'>Close</a>\
	       			</div>\
	       		  </div>"

				  		// <div><i class='dialog_input_title'>Username: </i><input type='text' id='username' class='login_input'/></div>\ 
				  		// <div><i class='dialog_input_title'>Password: </i><input type='text' id='password' class='login_input/></div>\


	this.gLoginDialog = $.createElement('div');
    this.gLoginDialog.innerHTML = dialog;
  	
}

LoginDialog.prototype.show = function() {
	var _body = document.getElementsByTagName('body') [0];
	// <body scroll="no"> 
    _body.appendChild(this.gLoginDialog);

  	var maskHeight = $(document).height();  
	var maskWidth = $(window).width();
	var windowHeight = $(window).height();

	// calculate the values for center alignment
	var dialogTop =  (windowHeight - height) / 2; 
	var dialogLeft = (maskWidth - width) / 2;//(maskWidth/2) - ($('#dialog-box').width()/2); 

	// // assign values to the overlay and dialog box
	$('#dialog-overlay').css({height:maskHeight, width:maskWidth});
	$('#dialog-box').css({height:height, width:width});
	$('#dialog-box').css({top:dialogTop, left:dialogLeft});

	// display the message
	$('#dialog-message').html("message");

	$('#btn-login').click(function () {		
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

LoginDialog.prototype.clickRegister = function() {
	alert('register click!!');
};

// LoginDialog.prototype.reloadScrollBars = function() {
//     document.documentElement.style.overflow = 'auto';  // firefox, chrome
//     document.body.scroll = "yes"; // ie only
// }

// LoginDialog.prototype.unloadScrollBars = function() {
//     document.documentElement.style.overflow = 'hidden';  // firefox, chrome
//     document.body.scroll = "no"; // ie only
// }

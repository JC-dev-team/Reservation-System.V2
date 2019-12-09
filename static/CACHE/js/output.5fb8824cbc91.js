;function send(){Notiflix.Loading.Hourglass('讀取中....')
document.getElementById("checklogin_form").action="/softwayliving/StaffAuth/";document.getElementById("checklogin_form").submit();}
function initializeApp(data){liff.getProfile().then(profile=>{})}
$(function(){document.getElementById("top_block").style.display='none'
liff.init(function(data){initializeApp(data);});});$(function(){$('#checklogin_form_submit').click(function(e){var status=true;var email=$('#email').val();var password=$('#password').val();if(email==''){alert('請輸入信箱！')
status=false;}else if(password==''){alert('請輸入密碼！')
status=false;}
if(status){send()}});});var user=$.cookie('uu');var pwd=$.cookie('pp');$(document).ready(function(){if(user){$("#email").val(user);$("#password").val(pwd);$("#che").html("<input type=\"checkbox\" onclick=\"uncheck()\" id=\"check1\" checked/>");}});function check(){$("#che").html("<input type=\"checkbox\" onclick=\"uncheck()\" id=\"check1\"/>");document.getElementById("check1").checked=true;$.cookie('uu',$("#email").val(),{expires:7});$.cookie('pp',$("#password").val(),{expires:7});}
function uncheck(){$("#che").html("<input type=\"checkbox\" onclick=\"check()\" id=\"check1\"/>");document.getElementById("check1").checked=false;$.cookie('uu','');$.cookie('pp','');}
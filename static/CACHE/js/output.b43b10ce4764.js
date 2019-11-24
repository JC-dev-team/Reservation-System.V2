;function send(){Notiflix.Loading.Hourglass('讀取中....')
document.getElementById("checklogin_form").action="/softwayliving/StaffAuth/";document.getElementById("checklogin_form").submit();}
function initializeApp(data){liff.getProfile().then(profile=>{})}
$(function(){document.getElementById("top_block").style.display='none'
liff.init(function(data){initializeApp(data);});});$(function(){$('#checklogin_form_submit').click(function(e){var status=true;var email=$('#email').val();var password=$('#password').val();if(email==''){alert('請輸入信箱！')
status=false;}else if(password==''){alert('請輸入密碼！')
status=false;}
if(status){send()}});});
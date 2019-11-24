;function send(){document.getElementById("checklogin_form").action="/booking/member/";document.getElementById("checklogin_form").submit();}
function initializeApp(data){liff.getProfile().then(profile=>{var disname={'name':profile.displayName};disname_json=JSON.parse(JSON.stringify(disname.name))})}
$(function(){Notiflix.Loading.Hourglass('111讀取中....');liff.init(function(data){initializeApp(data);});$('#social_id').val('9644ff56-e78b-11e9-a2b8-0ec425232523');$('#social_app').val('Line');$('#social_name').val('James')
send()});
;function send(){if(true){document.getElementById("checklogin_form").action="/userdashboard/auth/";document.getElementById("checklogin_form").submit();}}
function initializeApp(data){liff.getProfile().then(profile=>{var disname={'name':profile.displayName};disname_json=JSON.parse(JSON.stringify(disname.name))})}
$(function(){Notiflix.Loading.Hourglass('讀取中....');liff.init(function(data){initializeApp(data);});$('#social_id').val('9636ff56-e78b-11e9-a2b8-0ec425232520');$('#social_app').val('Line');$('#social_name').val('James')
if($('#social_id').val()!=''&&$('#social_app').val()!=''){send()}
else{window.location.replace('/userdashboard/error/');}});
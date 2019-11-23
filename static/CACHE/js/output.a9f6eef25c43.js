;function dosave(){if(true){Notiflix.Loading.Hourglass('處理中...');document.getElementById("member_form").action="/booking/booking/";document.getElementById("member_form").submit();}}
$(document).ready(function(){$("#member_submit").attr("disabled",false);$('#privacy_policy').click(function(){if($('#privacy_policy').is(':checked')){$("#member_submit").attr("disabled",false);}
if($('#privacy_policy').is(':checked')==false){$("#member_submit").attr("disabled",true);}});})
function initializeApp(data){liff.getProfile().then(profile=>{var disname={'name':profile.displayName};disname_json=JSON.parse(JSON.stringify(disname.name))
$('#img').attr('src',profile.pictureUrl);})}
$(function(){liff.init(function(data){initializeApp(data);});document.getElementById("member_birth").valueAsDate=new Date();});$(function(){$('#member_submit').click(function(e){var status=true;var member_name=$('#member_name').val();var member_phone=$('#member_phone').val();var reg_phone=new RegExp(/^09\d{8}$/);if(member_name==''){alert('請輸入姓名！')
status=false;}else if(member_phone==''){alert('請輸入電話！')
status=false;}else if(reg_phone.test(member_phone)==false){alert('手機號碼格式不正確');status=false;}
if(status){dosave()}});});
;function dosave(){if(true){Notiflix.Loading.Hourglass('處理中...');document.getElementById("member_form").action="/booking/booking/";document.getElementById("member_form").submit();}}
$(document).ready(function(){$("#member_submit").attr("disabled",false);$('#privacy_policy').click(function(){if($('#privacy_policy').is(':checked')){$("#member_submit").attr("disabled",false);}
if($('#privacy_policy').is(':checked')==false){$("#member_submit").attr("disabled",true);}});})
function initializeLiff(MyLiffId){liff.init({liffId:MyLiffId}).then(()=>{initializeApp();}).catch((err)=>{});}
function displayLiffData(){liff.getProfile().then(profile=>{$('#img').attr('src',profile.pictureUrl);})}
$(function(){initializeLiff('1654026454-2jpQJ4Py')
displayLiffData()
document.getElementById("member_birth").valueAsDate=new Date();});$(function(){$('#member_submit').click(function(e){var status=true;var member_name=$('#member_name').val();var member_phone=$('#member_phone').val();var reg_phone=new RegExp(/^09\d{8}$/);if(member_name==''){alert('請輸入姓名！')
status=false;}else if(member_phone==''){alert('請輸入電話！')
status=false;}else if(reg_phone.test(member_phone)==false){alert('手機號碼格式不正確');status=false;}
if(status){dosave()}});});
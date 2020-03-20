;function send(){document.getElementById("checklogin_form").action="/booking/member/";document.getElementById("checklogin_form").submit();}
function initializeLiff(MyLiffId){liff.init({liffId:MyLiffId},data=>{var id=data.context.userId
$('#social_id').val(id)}).then(()=>{displayLiffData()}).catch((err)=>{});}
function displayLiffData(){liff.getProfile().then(profile=>{const name=profile.displayName
$('#img').attr('src',profile.pictureUrl);$('#social_app').val('Line');$('#social_name').val(name)
var context=liff.getContext()
send()})}
$(function(){Notiflix.Loading.Hourglass('讀取中....');initializeLiff('1653788675-gE0L04We')});
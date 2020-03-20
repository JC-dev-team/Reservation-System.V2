;function send(){document.getElementById("checklogin_form").action="/booking/member/";document.getElementById("checklogin_form").submit();}
function initializeLiff(MyLiffId){liff.init({liffId:MyLiffId}).then(()=>{displayLiffData()}).catch((err)=>{});}
function displayLiffData(){liff.getProfile().then(profile=>{const name=profile.displayName
$('#img').attr('src',profile.pictureUrl);$('#social_app').val('Line');$('#social_name').val(name)
var context=liff.getContext()
$('#social_id').val(context.type)
send()})}
$(function(){Notiflix.Loading.Hourglass('讀取中....');initializeLiff('1653788675-gE0L04We')});
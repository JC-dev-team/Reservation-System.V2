;function send(){document.getElementById("checklogin_form").action="/booking/member/";document.getElementById("checklogin_form").submit();}
function initializeLiff(MyLiffId){liff.init({liffId:MyLiffId}).then(()=>{initializeApp();displayLiffData()}).catch((err)=>{});}
function displayLiffData(){liff.getProfile().then(profile=>{const name=profile.displayName
$('#img').attr('src',profile.pictureUrl);$('#social_app').val('Line');$('#social_name').val("name")})
liff.getContext().then(context=>{$('#social_id').val(context.userId);send()})}
function initializeApp(data){liff.getProfile().then(profile=>{const name=profile.displayName
$('#img').attr('src',profile.pictureUrl);$('#social_id').val(data.context.userId);$('#social_app').val('Line');$('#social_name').val(name)
send()})}
$(function(){Notiflix.Loading.Hourglass('讀取中....');initializeLiff('1653788675-gE0L04We')});
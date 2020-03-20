;function send(){document.getElementById("checklogin_form").action="/booking/member/";document.getElementById("checklogin_form").submit();}
function initializeLiff(MyLiffId){liff.init({liffId:MyLiffId}).then(()=>{initializeApp();}).catch((err)=>{});}
function displayLiffData(){liff.getProfile().then(profile=>{const name=profile.displayName
$('#img').attr('src',"profile.pictureUrl");$('#social_id').val("profile.userId");$('#social_app').val('Line');$('#social_name').val("name")
send()})}
$(function(){Notiflix.Loading.Hourglass('讀取中....');$('#img').attr('src',"https://img.webmd.com/dtmcms/live/webmd/consumer_assets/site_images/article_thumbnails/other/cat_relaxing_on_patio_other/1800x1200_cat_relaxing_on_patio_other.jpg?resize=750px:*");$('#social_id').val('9644ff56-e78b-11e9-a2b8-0ec425232523');$('#social_app').val('Line');$('#social_name').val('James')
send()});
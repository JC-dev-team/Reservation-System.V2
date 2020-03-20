;function initializeLiff(MyLiffId){liff.init({liffId:MyLiffId}).then(()=>{}).catch((err)=>{});}
function closewindow(){if(''=='admin'){window.location.href='/softwayliving/login/'}else{liff.closeWindow()
alert("close")}}
$(function(){initializeLiff('1653788675-gE0L04We')
if(''=='admin'){document.getElementById('close_button').innerText='返回管理者介面'}
if('0'!='0'){document.getElementById('information').innerText="訂位資訊 (候補 "+'0'+")"}})
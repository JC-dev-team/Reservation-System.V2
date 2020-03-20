;function initializeLiff(MyLiffId){liff.init({liffId:MyLiffId}).catch((err)=>{alert(err)});}
function closewindow(){if(''=='admin'){window.location.href='/softwayliving/login/'}else{send_flexMessage()
liff.closeWindow()}}
function send_flexMessage(){liff.sendMessages([{type:'text',text:'Hello, World!'}]).then(()=>{alert("send")}).catch((err)=>{alert(err)});}
$(function(){initializeLiff('1653788675-gE0L04We')
send_flexMessage()
if(''=='admin'){document.getElementById('close_button').innerText='返回管理者介面'}
if('0'!='0'){document.getElementById('information').innerText="訂位資訊 (候補 "+'0'+")"}})
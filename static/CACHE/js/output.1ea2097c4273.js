;function initializeLiff(MyLiffId){liff.init({liffId:MyLiffId}).catch((err)=>{alert(err)});}
function closewindow(){if(''=='admin'){window.location.href='/softwayliving/login/'}else{send_flexMessage()}}
function send_flexMessage(){liff.sendMessages({"type":"flex","altText":"this is a flex message","contents":{"type":"bubble","body":{"type":"box","layout":"vertical","contents":[{"type":"text","text":"hello"},{"type":"text","text":"world"}]}}}).then(()=>{alert("send")}).catch((err)=>{alert(err)});}
$(function(){initializeLiff('1653788675-gE0L04We')
if(''=='admin'){document.getElementById('close_button').innerText='返回管理者介面'}
if('0'!='0'){document.getElementById('information').innerText="訂位資訊 (候補 "+'0'+")"}})
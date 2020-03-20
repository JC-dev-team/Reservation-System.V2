;function initializeLiff(MyLiffId){liff.init({liffId:MyLiffId}).catch((err)=>{alert(err)});}
function closewindow(){if(''=='admin'){window.location.href='/softwayliving/login/'}else{send_flexMessage()}}
function send_flexMessage(){liff.sendMessages({"type":"bubble","header":{"type":"box","layout":"vertical","contents":[{"type":"text","text":"Header text"}]},"hero":{"type":"image","url":"https://example.com/flex/images/image.jpg"},"body":{"type":"box","layout":"vertical","contents":[{"type":"text","text":"Body text"}]},"footer":{"type":"box","layout":"vertical","contents":[{"type":"text","text":"Footer text"}]},"styles":{"comment":"See the example of a bubble style object"}}).then(()=>{alert("send")}).catch((err)=>{alert(err)});}
$(function(){initializeLiff('1653788675-gE0L04We')
if(''=='admin'){document.getElementById('close_button').innerText='返回管理者介面'}
if('0'!='0'){document.getElementById('information').innerText="訂位資訊 (候補 "+'0'+")"}})
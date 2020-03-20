;function initializeLiff(MyLiffId){liff.init({liffId:MyLiffId}).catch((err)=>{alert(err)});}
function closewindow(){if(''=='admin'){window.location.href='/softwayliving/login/'}else{send_flexMessage()
liff.closeWindow()}}
function send_flexMessage(){var flex_admin={"type":"bubble","body":{"type":"box","layout":"vertical","contents":[{"type":"text","text":'訂位通知',"size":"xl","weight":"bold","color":'#E7881D'},{"type":"box","layout":"vertical","spacing":"sm","margin":"lg","contents":[{"type":"box","layout":"baseline","spacing":"sm","contents":[{"type":"text","text":"預約","flex":1,"size":"sm","color":"#AAAAAA"},{"type":"text","text":"username_info","flex":5,"size":"sm","color":"#666666","wrap":True}]},{"type":"box","layout":"baseline","spacing":"sm","contents":[{"type":"text","text":"日期","flex":1,"size":"sm","color":"#AAAAAA"},{"type":"text","text":"date_info","flex":5,"size":"sm","color":"#666666","wrap":True}]}]}]}}
liff.sendMessages([flex_admin]).then(()=>{alert("send")}).catch((err)=>{alert(err)});}
$(function(){initializeLiff('1653788675-gE0L04We')
if(''=='admin'){document.getElementById('close_button').innerText='返回管理者介面'}
if('0'!='0'){document.getElementById('information').innerText="訂位資訊 (候補 "+'0'+")"}})
;function initializeLiff(MyLiffId){liff.init({liffId:MyLiffId}).catch((err)=>{});}
function closewindow(){if(''=='admin'){window.location.href='/softwayliving/login/'}else{send_flexMessage()
liff.closeWindow()}}
function send_flexMessage(){var username='揚昇大師'
var adult='1'+'大'
var children='0'+'小'
var phone='0900111444'
var date='2020-03-24'
var session='午餐'+' '+'11:30'
var price='NT$ '+'600'
var habit='不吃牛'
var user_flexMessage={"type":"flex","altText":"Flex Message","contents":{"type":"bubble","body":{"type":"box","layout":"vertical","contents":[{"type":"text","text":"SoftWay 訂位處理中","size":"xl","weight":"bold","color":"#E7881D"},{"type":"box","layout":"vertical","spacing":"sm","margin":"lg","contents":[{"type":"box","layout":"baseline","spacing":"sm","contents":[{"type":"text","text":"預約","flex":1,"size":"sm","color":"#AAAAAA"},{"type":"text","text":username+' '+adult+children,"flex":5,"size":"sm","color":"#666666","wrap":true}]},{"type":"box","layout":"baseline","spacing":"sm","contents":[{"type":"text","text":"電話","flex":1,"size":"sm","color":"#AAAAAA"},{"type":"text","text":phone,"flex":5,"size":"sm","color":"#666666","wrap":true}]},{"type":"box","layout":"baseline","spacing":"sm","contents":[{"type":"text","text":"日期","flex":1,"size":"sm","color":"#AAAAAA"},{"type":"text","text":date+' '+session,"flex":5,"size":"sm","color":"#666666","wrap":true}]},{"type":"box","layout":"baseline","spacing":"sm","contents":[{"type":"text","text":"價位","flex":1,"size":"sm","color":"#AAAAAA"},{"type":"text","text":price,"flex":5,"size":"sm","color":"#666666","wrap":true}]},{"type":"box","layout":"baseline","spacing":"sm","contents":[{"type":"text","text":"習慣","flex":1,"size":"sm","color":"#AAAAAA"},{"type":"text","text":habit,"flex":5,"size":"sm","color":"#666666","wrap":true}]},{"type":"box","layout":"baseline","spacing":"sm","contents":[{"type":"text","text":"備註","flex":1,"size":"sm","color":"#AAAAAA"},{"type":"text","text":habit,"flex":5,"size":"sm","color":"#666666","wrap":true}]}]}]}}}
liff.sendMessages([user_flexMessage]).catch((err)=>{});}
$(function(){initializeLiff('1653788675-gE0L04We')
if(''=='admin'){document.getElementById('close_button').innerText='返回管理者介面'}
if('0'!='0'){document.getElementById('information').innerText="訂位資訊 (候補 "+'0'+")"}})
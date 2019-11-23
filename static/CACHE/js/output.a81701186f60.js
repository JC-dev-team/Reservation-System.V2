;function getCookie(name){var cookieValue=null;if(document.cookie&&document.cookie!=''){var cookies=document.cookie.split(';');for(var i=0;i<cookies.length;i++){var cookie=jQuery.trim(cookies[i]);if(cookie.substring(0,name.length+1)==(name+'=')){cookieValue=decodeURIComponent(cookie.substring(name.length+1));break;}}}
return cookieValue;}
var csrftoken=getCookie('csrftoken');function csrfSafeMethod(method){return(/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));}
$.ajaxSetup({beforeSend:function(xhr,settings){if(!csrfSafeMethod(settings.type)&&!this.crossDomain){xhr.setRequestHeader("X-CSRFToken",csrftoken);}}});function ajax_add_store(data){$.ajax({type:'POST',url:'/softwayliving/AddStore/',data:data,success:function(response){if(response.error!=null){Notiflix.Notify.Failure('發生錯誤！！');Notiflix.Loading.Remove();}else if(response.alert!=null){Notiflix.Report.Warning('警告',response.alert,'ok');Notiflix.Loading.Remove();}else{Notiflix.Notify.Success('已新增！！');document.getElementById('add_Modal').style.display='none'
window.location.reload();}},error:function(XMLHttpRequest,textStatus,errorThrown){Notiflix.Notify.Failure('發生未知錯誤！！');Notiflix.Loading.Remove();}})}
function ajax_edit_store(data){$.ajax({type:'POST',url:'/softwayliving/ModifyStore/',data:data,success:function(response){if(response.error!=null){Notiflix.Notify.Failure('發生錯誤！！');Notiflix.Loading.Remove();}else if(response.alert!=null){Notiflix.Report.Warning('警告',response.alert,'ok');Notiflix.Loading.Remove();}else{Notiflix.Notify.Success('已儲存！！');document.getElementById('edit_Modal').style.display='none'
window.location.reload();}},error:function(XMLHttpRequest,textStatus,errorThrown){Notiflix.Notify.Failure('發生未知錯誤！！');Notiflix.Loading.Remove();}})}
function ajax_delete_store(t,data){$.ajax({type:'POST',url:'/softwayliving/DeleteStore/',data:data,success:function(response){if(response.error!=null){Notiflix.Notify.Failure('發生錯誤！！');}else if(response.alert!=null){Notiflix.Report.Warning('警告',response.alert,'ok');}else if(response.outdated!=null){Notiflix.Report.Warning('警告',response.outdated,'ok');window.location.replace(response.action)}else{Notiflix.Notify.Success('已刪除！！');t.parentElement.style.display='none'}
Notiflix.Loading.Remove();},error:function(XMLHttpRequest,textStatus,errorThrown){Notiflix.Notify.Failure('發生未知錯誤！！');Notiflix.Loading.Remove();}})}
function save_add(){Notiflix.Confirm.Show('管理者權限','確定要新增嗎?','是-新增','否',function(){var status=true
var store_name=$('#add_store_name').val();var store_address=$('#add_store_address').val();var store_phone=$('#add_store_phone').val();var store_fax=$('#add_store_fax').val();var tk_service=$('#add_tk_service').val();var seat=$('#add_seat').val();if(store_name==''||store_name==null){Notiflix.Notify.Failure('請輸入店家名稱！！')
status=false;}else if(store_address==''||store_address==null){Notiflix.Notify.Failure('請輸入店家地址！！')
status=false;}else if(store_phone==''||store_phone==null){Notiflix.Notify.Failure('請輸入店家電話！！')
status=false;}else if(store_fax==''||store_fax==null){Notiflix.Notify.Failure('請輸入店家傳真！！')
status=false;}else if(tk_service==''||tk_service==null){Notiflix.Notify.Failure('請輸入是否提供外帶！！')
status=false;}else if(seat==''||seat==null){Notiflix.Notify.Failure('請輸入店內座位數！！')
status=false;}
if(status){var data={'store_name':store_name,'store_address':store_address,'store_phone':store_phone,'store_fax':store_fax,'tk_service':tk_service,'seat':seat}
Notiflix.Loading.Hourglass('新增中....');ajax_add_store(data)}},function(){});}
function save_edit(){Notiflix.Confirm.Show('管理者權限','確定要更動嗎?','是-儲存','否',function(){var status=true;var store_name=$('#edit_store_name').val();var store_address=$('#edit_store_address').val();var store_phone=$('#edit_store_phone').val();var store_fax=$('#edit_store_fax').val();var tk_service=$('#edit_tk_service').val();var seat=$('#edit_seat').val();if(store_name==''||store_name==null){Notiflix.Notify.Failure('請輸入店家名稱！！')
status=false;}else if(store_address==''||store_address==null){Notiflix.Notify.Failure('請輸入店家地址！！')
status=false;}else if(store_phone==''||store_phone==null){Notiflix.Notify.Failure('請輸入店家電話！！')
status=false;}else if(store_fax==''||store_fax==null){Notiflix.Notify.Failure('請輸入店家傳真！！')
status=false;}else if(tk_service==''||tk_service==null){Notiflix.Notify.Failure('請輸入是否提供外帶！！')
status=false;}else if(seat==''||seat==null){Notiflix.Notify.Failure('請輸入店內座位數！！')
status=false;}
if(status){var data={'store_name':store_name,'store_address':store_address,'store_phone':store_phone,'store_fax':store_fax,'tk_service':tk_service,'seat':seat}
Notiflix.Loading.Hourglass('更新中....');ajax_edit_store(data)}},function(){});}
function add_store(){document.getElementById('add_Modal').style.display='inline'}
function edit_store(t,store_id,store_name,store_address,store_phone,store_fax,tk_service,seat){document.getElementById('edit_Modal').style.display='inline'
document.getElementById('edit_store_id').value=store_id
document.getElementById('edit_store_name').value=store_name
document.getElementById('edit_store_address').value=store_address
document.getElementById('edit_store_phone').value=store_phone
document.getElementById('edit_store_fax').value=store_fax
document.getElementById('edit_tk_service').value=tk_service
document.getElementById('edit_seat').value=seat}
function delete_store(t,store_id){Notiflix.Confirm.Show('管理者權限','確定要刪除此價位嗎?','是-刪除','否',function(){var data={'store_id':store_id}
Notiflix.Loading.Hourglass('正在刪除....');ajax_delete_store(t,data)},function(){});}
function setting(action,store_id){if(action=='admin'){Notiflix.Loading.Hourglass('請稍候...');window.location.href='/softwayliving/admins/?store_id='+store_id}}
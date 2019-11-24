;function getCookie(name){var cookieValue=null;if(document.cookie&&document.cookie!=''){var cookies=document.cookie.split(';');for(var i=0;i<cookies.length;i++){var cookie=jQuery.trim(cookies[i]);if(cookie.substring(0,name.length+1)==(name+'=')){cookieValue=decodeURIComponent(cookie.substring(name.length+1));break;}}}
return cookieValue;}
var csrftoken=getCookie('csrftoken');function csrfSafeMethod(method){return(/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));}
$.ajaxSetup({beforeSend:function(xhr,settings){if(!csrfSafeMethod(settings.type)&&!this.crossDomain){xhr.setRequestHeader("X-CSRFToken",csrftoken);}}});$.ajax({type:"GET",url:'/booking/getStoreInfo/',success:function(response){if(response.error!=null){Notiflix.Report.Failure('發生錯誤',response.error,'ok');Notiflix.Loading.Remove();}else if(response.alert!=null){Notiflix.Report.Warning('警告',response.alert,'ok');Notiflix.Loading.Remove();}else if(response.outdated!=null){Notiflix.Report.Warning('警告',response.outdated,'ok');window.location.replace(response.action)}else{$('#store_name_select').empty();for(var i=0;i<response.result.length;i++){$("#store_name_select").append($("<option></option>").attr("value",response.result[i].store_id).text(response.result[i].store_name));}}},error:function(XMLHttpRequest,textStatus,errorThrown){Notiflix.Report.Failure('錯誤','很抱歉，發生無法預期之異常','ok');Notiflix.Loading.Remove();}});function ajax_save_password(data){$.ajax({type:'POST',url:'/softwayliving/ModifyPwd/',data:data,success:function(response){if(response.error!=null){Notiflix.Notify.Failure('發生錯誤！！');Notiflix.Loading.Remove();}else if(response.alert!=null){Notiflix.Report.Warning('警告',response.alert,'ok');Notiflix.Loading.Remove();}else{Notiflix.Notify.Success('已更新密碼！！');$('#edit_Modal').toggle()
$('#password_Modal').toggle()
Notiflix.Loading.Remove();}},error:function(XMLHttpRequest,textStatus,errorThrown){Notiflix.Notify.Failure('發生未知錯誤！！');Notiflix.Loading.Remove();}})}
function ajax_add_staff(data){$.ajax({type:'POST',url:'/softwayliving/AddAdmin/',data:data,success:function(response){if(response.error!=null){Notiflix.Notify.Failure('發生錯誤！！');Notiflix.Loading.Remove();}else if(response.alert!=null){Notiflix.Report.Warning('警告',response.alert,'ok');Notiflix.Loading.Remove();}else{Notiflix.Notify.Success('已新增！！');document.getElementById('add_Modal').style.display='none'
window.location.reload();}},error:function(XMLHttpRequest,textStatus,errorThrown){Notiflix.Notify.Failure('發生未知錯誤！！');Notiflix.Loading.Remove();}})}
function ajax_save_edit(data){$.ajax({type:'POST',url:'/softwayliving/ModifyAdmin/',data:data,success:function(response){if(response.error!=null){Notiflix.Report.Failure('錯誤',response.error,'ok');Notiflix.Loading.Remove();}else if(response.alert!=null){Notiflix.Report.Warning('警告',response.alert,'ok');Notiflix.Loading.Remove();}else if(response.outdated!=null){Notiflix.Report.Warning('警告',response.outdated,'ok');window.location.replace(response.action)}else{Notiflix.Notify.Success('已儲存！！');document.getElementById('edit_Modal').style.display='none'
window.location.reload();}},error:function(XMLHttpRequest,textStatus,errorThrown){Notiflix.Notify.Failure('很抱歉，發生未知錯誤！！');Notiflix.Loading.Remove();}})}
function ajax_delete_admin(t,data){$.ajax({type:'POST',url:'/softwayliving/DeleteAdmin/',data:data,success:function(response){if(response.error!=null){Notiflix.Report.Failure('錯誤',response.error,'ok');}else if(response.alert!=null){Notiflix.Report.Warning('警告',response.alert,'ok');}else if(response.outdated!=null){Notiflix.Report.Warning('警告',response.outdated,'ok');window.location.replace(response.action)}else{Notiflix.Notify.Success('已刪除管理者！！');t.parentElement.style.display='none'
window.location.reload();}
Notiflix.Loading.Remove();},error:function(XMLHttpRequest,textStatus,errorThrown){Notiflix.Notify.Failure('很抱歉，發生未知錯誤！！');Notiflix.Loading.Remove();}})}
function save_add(){Notiflix.Confirm.Show('管理者權限','確定要新增嗎?','是-新增','否',function(){var status=true
var store_id=$('#store_name_select').val()
var staff_name=$('#add_staff_name').val();var staff_phone=$('#add_staff_phone').val();var staff_email=$('#add_email').val();var auth=$('#add_auth').val();if(staff_name==''||staff_name==null){Notiflix.Notify.Failure('請輸入管理者姓名！！')
status=false;}else if(staff_phone==''||staff_phone==null){Notiflix.Notify.Failure('請輸入管理者電話！！')
status=false;}else if(staff_email==''||staff_email==null){Notiflix.Notify.Failure('請輸入管理者信箱！！')
status=false;}else if(auth==''||auth==null){Notiflix.Notify.Failure('請輸入管理者權限！！')
status=false;}
if(status){var data={'store_id':store_id,'staff_name':staff_name,'staff_phone':staff_phone,'email':staff_email,'auth':auth,}
Notiflix.Loading.Hourglass('新增中....');ajax_add_staff(data)}},function(){});}
function save_edit(){Notiflix.Confirm.Show('管理者權限','確定要更動嗎?','是-儲存','否',function(){var staff_id=$('#edit_staff_id').val();var staff_name=$('#edit_staff_name').val();var staff_phone=$('#edit_staff_phone').val();var email=$('#edit_email').val();var auth=$('#edit_is_superuser').val();var data={'staff_id':staff_id,'staff_name':staff_name,'staff_phone':staff_phone,'email':email,'auth':auth}
Notiflix.Loading.Hourglass('更新中....');ajax_save_edit(data)},function(){});}
function add_admin(){document.getElementById('add_Modal').style.display='inline'}
function edit_admin(t,staff_id,staff_name,staff_phone,email,password,is_superuser){document.getElementById('edit_Modal').style.display='inline'
document.getElementById('edit_staff_id').value=staff_id
document.getElementById('edit_staff_name').value=staff_name
document.getElementById('edit_staff_phone').value=staff_phone
document.getElementById('edit_email').value=email
document.getElementById('edit_password').value=password
document.getElementById('edit_is_superuser').value=is_superuser
console.log(is_superuser)}
function delete_admin(t){var delete_staff_id=$('#edit_staff_id').val()
var delete_email=$('#edit_email').val()
Notiflix.Confirm.Show('管理者權限','確定要永久刪除嗎?','是-刪除','否',function(){var data={'staff_id':delete_staff_id,'email':delete_email}
Notiflix.Loading.Hourglass('正在刪除....');ajax_delete_admin(t,data)},function(){});}
function setting(action){if(action=='admin'){Notiflix.Loading.Hourglass('請稍候...');window.location.href='/softwayliving/stores/'}}
function change_password(){Notiflix.Confirm.Show('管理者權限','確定要變更密碼?','是-更改','否',function(){var status=true
var old_password=$('#old_password').val();var new_password=$('#new_password').val();var new_again_password=$('#new_again_password').val();if(new_password!=new_again_password){Notiflix.Report.Warning('錯誤','密碼與確認密碼不同','ok');status=false}else if(old_password==''){Notiflix.Report.Warning('錯誤','請輸入舊密碼','ok');status=false}else if(new_password==''){Notiflix.Report.Warning('錯誤','請輸入新密碼','ok');status=false}else if(new_again_password==''){Notiflix.Report.Warning('錯誤','請輸入確認新密碼','ok');status=false}
if(status){var data={'old_password':old_password,'new_password':new_password,'new_again_password':new_again_password,}
Notiflix.Loading.Hourglass('更新密碼中....');ajax_save_password(data)}},function(){});}
if($('#edit_is_superuser').val()==1){$("option[name='auth_super']").attr('selected',true)
$("option[name='auth_not_super']").attr('selected',true)}
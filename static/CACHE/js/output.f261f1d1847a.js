;function getCookie(name){var cookieValue=null;if(document.cookie&&document.cookie!=''){var cookies=document.cookie.split(';');for(var i=0;i<cookies.length;i++){var cookie=jQuery.trim(cookies[i]);if(cookie.substring(0,name.length+1)==(name+'=')){cookieValue=decodeURIComponent(cookie.substring(name.length+1));break;}}}
return cookieValue;}
var csrftoken=getCookie('csrftoken');function csrfSafeMethod(method){return(/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));}
$.ajaxSetup({beforeSend:function(xhr,settings){if(!csrfSafeMethod(settings.type)&&!this.crossDomain){xhr.setRequestHeader("X-CSRFToken",csrftoken);}}});function ajax_save_edit(data){$.ajax({type:'POST',url:'/softwayliving/modify_member/',data:data,success:function(response){if(response.error!=null){Notiflix.Report.Failure('錯誤',response.error,'ok');Notiflix.Loading.Remove();}else if(response.alert!=null){Notiflix.Report.Warning('警告',response.alert,'ok');Notiflix.Loading.Remove();}else if(response.outdated!=null){Notiflix.Report.Warning('警告',response.outdated,'ok');window.location.replace(response.action)}else{Notiflix.Notify.Success('已儲存！！');document.getElementById('edit_Modal').style.display='none'
window.location.reload();}},error:function(XMLHttpRequest,textStatus,errorThrown){Notiflix.Notify.Failure('很抱歉，發生未知錯誤！！');Notiflix.Loading.Remove();}})}
function ajax_lock_member(t,data){$.ajax({type:'POST',url:'/softwayliving/lock_member/',data:data,success:function(response){if(response.error!=null){Notiflix.Report.Failure('錯誤',response.error,'ok');}else if(response.alert!=null){Notiflix.Report.Warning('警告',response.alert,'ok');}else if(response.outdated!=null){Notiflix.Report.Warning('警告',response.outdated,'ok');window.location.replace(response.action)}else{Notiflix.Notify.Success('已凍結會員！！');t.parentElement.style.display='none'
window.location.reload();}
Notiflix.Loading.Remove();},error:function(XMLHttpRequest,textStatus,errorThrown){Notiflix.Notify.Failure('很抱歉，發生未知錯誤！！');Notiflix.Loading.Remove();}})}
function ajax_unlock_member(t,data){$.ajax({type:'POST',url:'/softwayliving/unlock_member/',data:data,success:function(response){if(response.error!=null){Notiflix.Report.Failure('錯誤',response.error,'ok');}else if(response.alert!=null){Notiflix.Report.Warning('警告',response.alert,'ok');}else if(response.outdated!=null){Notiflix.Report.Warning('警告',response.outdated,'ok');window.location.replace(response.action)}else{Notiflix.Notify.Success('已解除！！');t.parentElement.style.display='none'
window.location.reload();}
Notiflix.Loading.Remove();},error:function(XMLHttpRequest,textStatus,errorThrown){Notiflix.Notify.Failure('很抱歉，發生未知錯誤！！');Notiflix.Loading.Remove();}})}
function save_edit(){Notiflix.Confirm.Show('管理者權限','確定要更動嗎?','是-儲存','否',function(){var user_id=$('#edit_user_id').val();var username=$('#edit_username').val();var phone=$('#edit_phone').val();var birth=$('#edit_birth').val();var data={'user_id':user_id,'username':username,'phone':phone,'birth':birth}
Notiflix.Loading.Hourglass('更新中....');ajax_save_edit(data)},function(){});}
function edit_member(t,user_id,username,phone,birth){document.getElementById('edit_Modal').style.display='inline'
document.getElementById('edit_user_id').value=user_id
document.getElementById('edit_username').value=username
document.getElementById('edit_phone').value=phone
document.getElementById('edit_birth').value=birth}
function lock_member(t,user_id){Notiflix.Confirm.Show('管理者權限','確定要凍結此會員嗎?','是-凍結會員','否',function(){var data={'user_id':user_id}
Notiflix.Loading.Hourglass('正在凍結....');ajax_lock_member(t,data)},function(){});}
function unlock_member(t,user_id){Notiflix.Confirm.Show('管理者權限','確定要解除凍結嗎?','是-解除','否',function(){var data={'user_id':user_id}
Notiflix.Loading.Hourglass('正在解除凍結....');ajax_unlock_member(t,data)},function(){});}
function switch_list(action){if(action=='ban'){document.getElementById('ban_list').style.display='inline'
document.getElementById('normal_list').style.display='none'}else if(action=='normal'){document.getElementById('ban_list').style.display='none'
document.getElementById('normal_list').style.display='inline'}}
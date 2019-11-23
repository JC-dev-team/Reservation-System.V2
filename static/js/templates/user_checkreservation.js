
    // using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    function cancelreservation(data) {
        $.ajax({
            type: 'POST',
            url: '/userdashboard/cancel/',
            data: data,
            success: function (response) {
                if (response.error != null) {
                    Notiflix.Report.Failure('錯誤', response.error, 'ok');
                } else if (response.alert != null) {
                    Notiflix.Report.Warning('警告', response.alert, 'ok ');
                    Notiflix.Loading.Remove();
                }else if (response.outdated != null) {
                    Notiflix.Report.Warning('警告', response.outdated, 'ok');
                    window.location.replace(response.action)
                }  else {
                    result = response.result
                    Notiflix.Report.Success('提醒', '已取消此訂位！！', 'ok ');
                    window.location.reload()
                }
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                Notiflix.Report.Failure('錯誤', '無法取消訂位，請聯絡店家', 'ok ');
                Notiflix.Loading.Remove();
            }

        })
    }


    function closewindow() {
        //if open on line base
        liff.closeWindow()
    }

    function cancel_click(date, uuid) {
        Notiflix.Confirm.Show('取消訂位', '確定取消訂位', '是', '否',
            function () {
                //alert('YES');
                var data = {
                    'bk_uuid': uuid,
                    'bk_date': date
                }
                Notiflix.Loading.Hourglass('刪除訂位中....');
                cancelreservation(data)

            },
            function () {
                //alert('NO');
            });
    }
    // ready
    // $('#displayName').html('{{user_info.username}}' + '(' + '{{user_info.social_name}}' + ')')

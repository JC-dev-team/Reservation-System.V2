
    //Notiflix Loading
    Notiflix.Loading.Init({
        className: 'notiflix-loading',
        zindex: 4000,
        backgroundColor: 'rgba(0,0,0,0.8)',
        rtl: false,
        useGoogleFont: true,
        fontFamily: 'Quicksand',
        cssAnimation: true,
        cssAnimationDuration: 400,
        clickToClose: false,
        customSvgUrl: null,
        svgSize: '80px',
        svgColor: '#00b462',
        messageID: 'NotiflixLoadingMessage',
        messageFontSize: '15px',
        messageMaxLength: 34,
        messageColor: '#dcdcdc',
    });

    //Notiflix Confirm
    Notiflix.Confirm.Init({
        className: 'notiflix-confirm',
        width: '280px',
        zindex: 4003,
        position: 'center',
        distance: '10px',
        backgroundColor: '#f8f8f8',
        borderRadius: '25px',
        backOverlay: true,
        backOverlayColor: 'rgba(0,0,0,0.5)',
        rtl: false,
        useGoogleFont: true,
        fontFamily: 'Quicksand',
        cssAnimation: true,
        cssAnimationStyle: 'fade',
        cssAnimationDuration: 300,
        titleColor: '#00b462',
        titleFontSize: '16px',
        titleMaxLength: 34,
        messageColor: '#1e1e1e',
        messageFontSize: '14px',
        messageMaxLength: 110,
        buttonsFontSize: '15px',
        buttonsMaxLength: 34,
        okButtonColor: '#f8f8f8',
        okButtonBackground: '#00b462',
        cancelButtonColor: '#f8f8f8',
        cancelButtonBackground: '#FF0000',
        plainText: true,
    });

    //Notiflix Notify
    Notiflix.Notify.Init({
        width: '280px',
        position: 'right-top',
        distance: '10px',
        opacity: 1,
        borderRadius: '5px',
        rtl: false,
        timeout: 3000,
        messageMaxLength: 110,
        backOverlay: false,
        backOverlayColor: 'rgba(0,0,0,0.5)',
        ID: 'NotiflixNotify',
        className: 'notiflix-notify',
        zindex: 4001,
        useGoogleFont: true,
        fontFamily: 'Quicksand',
        fontSize: '13px',
        cssAnimation: true,
        cssAnimationDuration: 400,
        cssAnimationStyle: 'fade',
        closeButton: false,
        useIcon: true,
        useFontAwesome: false,
        fontAwesomeIconStyle: 'basic',
        fontAwesomeIconSize: '34px',
        plainText: true,
        showOnlyTheLastOne: false,
        ssuccess: {
            background: '#00b462',
            textColor: '#fff',
            childClassName: 'success',
            notiflixIconColor: 'rgba(0,0,0,0.2)',
            fontAwesomeClassName: 'fas fa-check-circle',
            fontAwesomeIconColor: 'rgba(0,0,0,0.2)',
        },
        failure: {
            background: '#f44336',
            textColor: '#fff',
            childClassName: 'failure',
            notiflixIconColor: 'rgba(0,0,0,0.2)',
            fontAwesomeClassName: 'fas fa-times-circle',
            fontAwesomeIconColor: 'rgba(0,0,0,0.2)',
        },
        warning: {
            background: '#f2bd1d',
            textColor: '#fff',
            childClassName: 'warning',
            notiflixIconColor: 'rgba(0,0,0,0.2)',
            fontAwesomeClassName: 'fas fa-exclamation-circle',
            fontAwesomeIconColor: 'rgba(0,0,0,0.2)',
        },
        info: {
            background: '#00bcd4',
            textColor: '#fff',
            childClassName: 'info',
            notiflixIconColor: 'rgba(0,0,0,0.2)',
            fontAwesomeClassName: 'fas fa-info-circle',
            fontAwesomeIconColor: 'rgba(0,0,0,0.2)',
        },
    });
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

    //設定店休日期/時段
    function admin_dayoff(data) {
        $.ajax({
            type: 'POST',
            url: '/softwayliving/add_event/',
            data: data,
            success: function (response) {
                if (response.error != null) {
                    Notiflix.Report.Failure('錯誤', response.error, 'ok');
                } else if (response.alert != null) {
                    Notiflix.Report.Warning('警告', response.alert, 'ok');
                } else if (response.outdated != null) {
                    Notiflix.Report.Warning('警告', response.outdated, 'ok');
                    window.location.replace(response.action)
                } else {
                    result = response.result
                    Notiflix.Notify.Success('已設為店休！！');
                    //Reload
                    window.location.reload();
                }
                Notiflix.Loading.Remove();
                document.getElementById('dayoff_Modal').style.display = 'none';


            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                Notiflix.Notify.Failure('很抱歉，發生未知錯誤');
                Notiflix.Loading.Remove();
                document.getElementById('dayoff_Modal').style.display = 'none';
            }

        });
    }

    //取消店休日期/時段
    function admin_cancel_dayoff(data) {
        $.ajax({
            type: 'POST',
            url: '/softwayliving/cancel_event/',
            data: data,
            success: function (response) {
                if (response.error != null) {
                    Notiflix.Report.Failure('錯誤', response.error, 'ok');
                } else if (response.alert != null) {
                    Notiflix.Report.Warning('警告', response.alert, 'ok');
                } else if (response.outdated != null) {
                    Notiflix.Report.Warning('警告', response.outdated, 'ok');
                    window.location.replace(response.action)
                } else {
                    result = response.result
                    Notiflix.Notify.Success('已取消店休！！');
                    //Reload
                    window.location.reload();
                }
                Notiflix.Loading.Remove();
                document.getElementById('dayoff_Modal').style.display = 'none';


            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                Notiflix.Notify.Failure('很抱歉，發生未知錯誤');
                Notiflix.Loading.Remove();
                document.getElementById('dayoff_Modal').style.display = 'none';
            }

        });
    }

    function admin_cancel(data, event) {
        $.ajax({
            type: 'POST',
            url: '/softwayliving/cancel/',
            data: data,
            success: function (response) {
                if (response.error != null) {
                    Notiflix.Report.Failure('錯誤', response.error, 'ok');
                } else if (response.alert != null) {
                    Notiflix.Report.Warning('警告', response.alert, 'ok');
                } else if (response.outdated != null) {
                    Notiflix.Report.Warning('警告', response.outdated, 'ok');
                    window.location.replace(response.action)
                } else {
                    result = response.result
                    event.setProp('backgroundColor', 'grey')
                    Notiflix.Notify.Success('訂單已刪除！！');

                }
                document.getElementById('information_Modal').style.display = 'none';
                Notiflix.Loading.Remove();
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                Notiflix.Notify.Failure('很抱歉，發生未知錯誤');
                Notiflix.Loading.Remove();
                document.getElementById('dayoff_Modal').style.display = 'none';
            }

        });
    }

    function admin_pass(data, event) {
        $.ajax({
            type: 'POST',
            url: '/softwayliving/pass/',
            data: data,
            success: function (response) {
                if (response.error != null) {
                    Notiflix.Report.Failure('錯誤', response.error, 'ok');
                } else if (response.alert != null) {
                    Notiflix.Report.Warning('警告', response.alert, 'ok');
                } else if (response.outdated != null) {
                    Notiflix.Report.Warning('警告', response.outdated, 'ok');
                    window.location.replace(response.action)
                } else {
                    result = response.result
                    event.setProp('backgroundColor', 'green')
                    Notiflix.Notify.Success('訂單已確認(候補)！！');
                }
                document.getElementById('information_Modal').style.display = 'none';
                Notiflix.Loading.Remove();

            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                Notiflix.Notify.Failure('很抱歉，發生未知錯誤');
                Notiflix.Loading.Remove();
                document.getElementById('information_Modal').style.display = 'none';
            }

        });
    }


    function admin_confirm(data, event) {
        $.ajax({
            type: 'POST',
            url: '/softwayliving/confirm/',
            data: data,
            success: function (response) {
                if (response.error != null) {
                    Notiflix.Report.Failure('錯誤', response.error, 'ok');
                } else if (response.alert != null) {
                    Notiflix.Report.Warning('警告', response.alert, 'ok');
                } else if (response.outdated != null) {
                    Notiflix.Report.Warning('警告', response.outdated, 'ok');
                    window.location.replace(response.action)
                } else {
                    result = response.result
                    event.setProp('backgroundColor', 'green')
                    Notiflix.Notify.Success('訂單已確認！！');

                }
                document.getElementById('information_Modal').style.display = 'none';
                Notiflix.Loading.Remove();

            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                Notiflix.Notify.Failure('很抱歉，發生未知錯誤');
                Notiflix.Loading.Remove();
                document.getElementById('information_Modal').style.display = 'none';
            }

        });
    }

    //List ajax function 
    //待確認
    function ajax_not_confirm(num) {
        $.ajax({
            type: 'GET',
            url: '/softwayliving/not_confirm/',
            success: function (response) {
                if (response.error != null) {
                    Notiflix.Report.Failure('錯誤', response.error, 'ok');
                } else if (response.alert != null) {
                    Notiflix.Report.Warning('警告', response.alert, 'ok');
                } else if (response.outdated != null) {
                    Notiflix.Report.Warning('警告', response.outdated, 'ok');
                    window.location.replace(response.action)
                } else {

                    result = response.result
                    account = response.account
                    event = 'none'
                    //Function of calendar
                    calendar_fun(event, account, result, num)

                }
                Notiflix.Loading.Remove();
                document.getElementById('dayoff_Modal').style.display = 'none';
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                Notiflix.Notify.Failure('很抱歉，發生未知錯誤');
                Notiflix.Loading.Remove();
                document.getElementById('dayoff_Modal').style.display = 'none';
            }

        })
    }
    //已確認
    function ajax_is_confirm(num) {
        $.ajax({
            type: 'GET',
            url: '/softwayliving/is_confirm/',
            success: function (response) {
                if (response.error != null) {
                    Notiflix.Report.Failure('錯誤', response.error, 'ok');
                } else if (response.alert != null) {
                    Notiflix.Report.Warning('警告', response.alert, 'ok');
                } else if (response.outdated != null) {
                    Notiflix.Report.Warning('警告', response.outdated, 'ok');
                    window.location.replace(response.action)
                } else {

                    result = response.result
                    account = response.account
                    event = 'none'
                    //Function of calendar (return calendar.render())
                    calendar_fun(event, account, result, num)

                }
                Notiflix.Loading.Remove();
                document.getElementById('dayoff_Modal').style.display = 'none';
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                Notiflix.Notify.Failure('很抱歉，發生未知錯誤');
                Notiflix.Loading.Remove();
                document.getElementById('dayoff_Modal').style.display = 'none';
            }
        })
    }
    //候補
    function ajax_waiting(num) {
        $.ajax({
            type: 'GET',
            url: '/softwayliving/waiting/',
            success: function (response) {
                if (response.error != null) {
                    Notiflix.Report.Failure('錯誤', response.error, 'ok');
                } else if (response.alert != null) {
                    Notiflix.Report.Warning('警告', response.alert, 'ok');
                } else if (response.outdated != null) {
                    Notiflix.Report.Warning('警告', response.outdated, 'ok');
                    window.location.replace(response.action)
                } else {

                    result = response.result
                    account = response.account
                    event = 'none'
                    //Function of calendar (return calendar.render())
                    calendar_fun(event, account, result, num)

                }
                Notiflix.Loading.Remove();
                document.getElementById('dayoff_Modal').style.display = 'none';
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                Notiflix.Notify.Failure('很抱歉，發生未知錯誤');
                Notiflix.Loading.Remove();
                document.getElementById('dayoff_Modal').style.display = 'none';
            }
        })
    }
    //已刪除
    function ajax_canceled(num) {
        $.ajax({
            type: 'GET',
            url: '/softwayliving/delete/',
            success: function (response) {
                if (response.error != null) {
                    Notiflix.Report.Failure('錯誤', response.error, 'ok');
                } else if (response.alert != null) {
                    Notiflix.Report.Warning('警告', response.alert, 'ok');
                } else if (response.outdated != null) {
                    Notiflix.Report.Warning('警告', response.outdated, 'ok');
                    window.location.replace(response.action)
                } else {

                    result = response.result
                    account = response.account
                    event = 'none'
                    //Function of calendar (return calendar.render())
                    calendar_fun(event, account, result, num)

                }
                Notiflix.Loading.Remove();
                document.getElementById('dayoff_Modal').style.display = 'none';
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                Notiflix.Notify.Failure('很抱歉，發生未知錯誤');
                Notiflix.Loading.Remove();
                document.getElementById('dayoff_Modal').style.display = 'none';
            }
        })
    }



    function admin_ajax_time(num, calendar) {
        $.ajax({
            type: 'POST',
            url: '/softwayliving/staff_check/',
            success: function (response) {
                if (response.error != null) {
                    Notiflix.Report.Failure('錯誤', response.error, 'ok');
                } else if (response.alert != null) {
                    Notiflix.Report.Warning('警告', response.alert, 'ok');
                } else if (response.outdated != null) {
                    Notiflix.Report.Warning('警告', response.outdated, 'ok');
                    window.location.replace(response.action)
                } else {
                    result = response.result
                    account = response.account
                    event = response.event
                    //Function of calendar (return calendar.render())
                    calendar_fun(event, account, result, num)

                }
                Notiflix.Loading.Remove();
                document.getElementById('dayoff_Modal').style.display = 'none';
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                Notiflix.Notify.Failure('很抱歉，發生未知錯誤！！');
                Notiflix.Loading.Remove();
                document.getElementById('dayoff_Modal').style.display = 'none';
            }

        });
    }

    //ajax function
    function ajax_post(num = 0) {
        //ajax data

        //Clean the calendar
        document.getElementById('calendar').innerHTML = ''

        // do ajax fuction
        admin_ajax_time(num)

        //spinner show
        Notiflix.Loading.Hourglass('讀取中....');


    }


    //calendar function
    function calendar_fun(event = 'none', account, result, num = 0, action = 'render') {
        //spinner hide
        Notiflix.Loading.Remove();
        var calendarEl = document.getElementById('calendar');
        window.calendar = new FullCalendar.Calendar(calendarEl, {
            //ColumnHeaderText
            columnHeaderText: function (date) {
                if (date.getDay() === 0) {
                    return '日';
                }
                if (date.getDay() === 1) {
                    return '一';
                }
                if (date.getDay() === 2) {
                    return '二';
                }
                if (date.getDay() === 3) {
                    return '三';
                }
                if (date.getDay() === 4) {
                    return '四';
                }
                if (date.getDay() === 5) {
                    return '五';
                }
                if (date.getDay() === 6) {
                    return '六';
                }

            },
            //Plugins - 'interaction','dayGrid'
            plugins: ['interaction', 'dayGrid', 'moment', 'list'],
            editable: true,
            //Default View
            defaultView: 'dayGridMonth',
            //defaultDate
            defaultDate: (new Date().addMonths(num)).toISOString().slice(0, 10),
            //Height
            height: 'auto',
            contentHeight: 500,
            //Header
            header: {
                left: 'prev',
                center: 'title,',
                right: 'dayGridMonth,listMonth,next'
            },
            //Header -  Title Text
            buttonText: {
                month: '月',
                list: '列表'
            },
            //Header - Title format
            titleFormat: 'YYYY  MM月',
            //List - Title format
            listDayFormat: 'MM 月 DD',
            listDayAltFormat: 'dddd',
            //Show none current date (False)
            showNonCurrentDates: false,
            //Event Limit
            eventLimit: true,
            views: {
                dayGrid: {
                    eventLimit: 3
                }
            },
            eventTimeFormat: {
                hour: '2-digit',
                minute: '2-digit',
                hour12: false
            },
            //Date selectable (true)
            selectable: true,

            events: function (info, successCallback) {

                var Event = [];
                //successCallback(Event)


                //reservation event
                for (var i = 0; i < result.length; i++) {

                    var uuid = result[i].bk_uuid
                    var date = result[i].bk_date;
                    var time = 'T' + result[i].bk_st;
                    var session = result[i].time_session;
                    var people = result[i].adult + '大' + result[i].children + '小';
                    var price = '$' + result[i].bk_price;
                    var habit = '#' + result[i].bk_habit + ' ';
                    var waiting_num = result[i].waiting_num
                    var confirm = result[i].is_confirm
                    var is_cancel = result[i].is_cancel
                    var bk_ps = result[i].bk_ps

                    var user_phone = account[i].phone
                    var user_name = account[i].username
                    var social_name = account[i].social_name

                    if (session == 'Lunch') {
                        session = '午餐'
                    } else {
                        session = '晚餐'
                    }

                    if (habit == '#無 ') {
                        habit = ''
                    }

                    if (is_cancel == true) {
                        color = 'black' //已刪除
                    } else if (confirm == true) {
                        color = 'green' //已確認
                    } else if (waiting_num == 0 && confirm == false) {
                        color = 'orange' //待確認
                    } else {
                        color = 'red' //候補
                    }

                    Event.push({
                        id: uuid,
                        title: session + ' ' + people + ' ' + price + ' ' + habit + '\n' +
                            user_name +
                            '(' + social_name + ')' + ' ' + user_phone,
                        start: date + time,
                        backgroundColor: color,
                        textColor: 'white',
                        extendedProps: {
                            bk_ps: bk_ps
                        }
                    });

                    successCallback(Event)
                }

                if (event != 'none') {
                    //dayoff event
                    for (var i = 0; i < event.length; i++) {
                        var date = event[i].event_date
                        var time_session = event[i].time_session
                        var event_type = event[i].event_type

                        if (time_session == 'Lunch') {
                            var session = '午餐'
                        } else {
                            var session = '晚餐'
                        }
                        if (event_type == 'Day off') {
                            var type = '店休'
                        }

                        Event.push({
                            title: session + type,
                            start: date,
                            backgroundColor: 'grey',
                            textColor: 'white',
                        });
                        successCallback(Event)


                    }
                }
            },

            eventRender: function (info) {
                var month_text = info.el.text

                if (month_text != undefined) {
                    var text = month_text.split(' ')[1]

                    info.el.text = text

                }


                //list of dot
                var dotEl = info.el.getElementsByClassName('fc-event-dot')[0];
                var f = info.el.getElementsByClassName('fc-list-item-title fc-widget-content')[0]

                //"<a href='tel:" + phone +" '> " + phone + "</a>"
                // if (dotEl) {
                //     dotEl.style.backgroundColor = 'white';
                // }
            },

            //Function
            dateClick: function (info) {
                var date = info.dateStr
                $("#dayoff_date").val(date)

                //document modal
                document.getElementById('dayoff_Modal').style.display = 'inline';
                document.getElementById('modal_date_dayoff').innerHTML =
                    '<p id="modal_date_dayoff">' + '<label><i class="fa fa-calendar"></i></label>' +
                    ' 日期： ' + date + '</p>'



            },
            eventClick: function (info) {
                //clean ps data
                var date = info.event.start.addDays(1).toISOString().slice(0, 10)
                $("#dayoff_date").val(date)
                $('#bk_ps').val('')
                var list_backgroundcolor = info.event.backgroundColor
                if (list_backgroundcolor == 'orange') {
                    status = "<font color='orange'>待確認</font>"
                    //hide
                    $("option[name='pass']").hide()
                    //show
                    $("option[name='confirm']").show()
                    $("option[name='cancel']").show()
                    //selected
                    $("option[name='confirm']").attr("selected", true)
                } else if (list_backgroundcolor == 'green') {
                    status = "<font color='green'>已確認</font>"
                    //hide
                    $("option[name='confirm']").hide()
                    $("option[name='pass']").hide()
                    //show
                    $("option[name='cancel']").show()
                    //selected
                    $("option[name='cancel']").attr("selected", true)
                } else if (list_backgroundcolor == 'red') {
                    status = "<font color='red'>候補</font>"
                    //hide
                    $("option[name='confirm']").hide()
                    //show
                    $("option[name='pass']").show()
                    $("option[name='cancel']").show()
                    //selected
                    $("option[name='pass']").attr("selected", true)
                } else if (list_backgroundcolor == 'grey') {
                    //open dayoff modal
                    document.getElementById('dayoff_Modal').style.display = 'inline';
                    document.getElementById('modal_date_dayoff').innerHTML =
                        '<p id="modal_date_dayoff">' + '<label><i class="fa fa-calendar"></i></label>' +
                        ' 日期： ' + date + '</p>'


                }
                
                var id = info.event.id
                var date = info.event.start.toISOString().slice(0, 10)
                var time = info.event.start.toTimeString().slice(0, 5)
                var bk_ps = info.event.extendedProps.bk_ps
                
                var time_session = info.event.title.slice(0, 2)
                var information = info.event.title.split('\n')[0]
                var user_name = info.event.title.split('\n')[1].split(' ')[0]
                var user_phone = info.event.title.split('\n')[1].split(' ')[1]

                if (time_session == '午餐') {
                    time_session = 'Lunch'
                } else {
                    time_session = 'Dinner'
                }

                $('#info_event_id').val(id)
                $('#info_event_start').val(date)
                $('#info_event_timesession').val(time_session)

                //document modal
                if (list_backgroundcolor != 'green' && list_backgroundcolor != 'orange' &&
                    list_backgroundcolor != 'red') {
                    document.getElementById('information_Modal').style.display = 'none';
                } else {
                    document.getElementById('information_Modal').style.display = 'inline';
                }

                document.getElementById('modal_date').innerHTML =
                    '<p id="modal_date">' + '<label><i class="fa fa-calendar"></i></label>' +
                    ' 日期： ' + date + '(' + time + ')' + '</p>'

                document.getElementById('modal_info').innerHTML =
                    '<p id="modal_info">' + '<label><i class="fa fa-bell"></i></label>' + ' 訂位資訊： ' +
                    '<br>' + information + '</p>'

                document.getElementById('modal_user').innerHTML =
                    '<p id="modal_user">' + '<label><i class="fa fa-user-circle"></i></label>' + ' 訂位人： ' +
                    user_name + "<a href='tel:" + user_phone + " ' style='color:blue'> " + user_phone +
                    "</a>" + '</p>'

                document.getElementById('modal_status').innerHTML =
                    '<p id="modal_status">' + '<label><i class="fa fa-info-circle"></i></label>' +
                    ' 訂單狀態： ' + status + '</p>'


                document.getElementById('bk_ps').value = bk_ps
            }
        });
        if (action == 'render') {
            return calendar.render();
        } else if (action == 'refetch') {
            return calendar.refetchEvents()
        }



    }

    //ready
    $(function () {

        //do the current month to ajax 
        var num = parseInt($('#date_num').val())
        //do the fuction of ajax_post()
        ajax_post(num)

        //Date addDays() & addMonths()
        Date.prototype.addDays = function (days) {
            var date = new Date(this.valueOf());
            date.setDate(date.getDate() + days);
            return date;
        }
        Date.prototype.addMonths = function (months) {
            var date = new Date(this.valueOf());
            date.setMonth(date.getMonth() + months);
            return date;
        }


    })


    //eventClick -> information Modal -> modal button
    $('#modal_button').click(function (e) {
        var id = $('#info_event_id').val()
        var date = $('#info_event_start').val()
        var time_session = $('#info_event_timesession').val()
        //確認訂單
        if ($("#action_select").val() == 'confirm') {

            Notiflix.Confirm.Show('管理者權限', '確定要確認此訂單嗎?', '是-確認訂單', '再看看',
                function () {

                    var data = {
                        'bk_uuid': id,
                        'bk_date': date,
                        'bk_ps': $('#bk_ps').val()
                    }

                    var event = calendar.getEventById(id)
                    //spinner show
                    Notiflix.Loading.Hourglass('確認中....');
                    admin_confirm(data, event)

                },
                function () {});

        }
        //刪除訂單
        else if ($("#action_select").val() == 'cancel') {
            Notiflix.Confirm.Show('管理者權限', '確定要刪除此訂單嗎?', '刪除訂單', '不要刪除',
                function () {
                    var data = {
                        'bk_uuid': id,
                        'bk_date': date,
                        'bk_ps':$('#bk_ps').val()
                    }
                    var event = calendar.getEventById(id)
                    admin_cancel(data, event)
                    //spinner show
                    Notiflix.Loading.Hourglass('刪除中....');
                },
                function () {});
        }
        //遞補候位
        else if ($("#action_select").val() == 'pass') {
            Notiflix.Confirm.Show('管理者權限', '確定要遞補此訂單嗎?', '遞補候位', '取消遞補',
                function () {
                    var data = {
                        'bk_uuid': id,
                        'bk_date': date,
                        'bk_ps': $('#bk_ps').val(),
                        'time_session': time_session,
                        'store_id': '6f48f753-e4f0-11e9-bfcb-0e9f22d909c0'
                    }
                    var event = calendar.getEventById(id)
                    admin_pass(data, event)
                    //spinner show
                    Notiflix.Loading.Hourglass('遞補中....');
                },
                function () {});
        }
    })


    //dateClick -> Modal -> buttonClick
    $('#modal_button_dayoff').click(function (e) {
        var date = $("#dayoff_date").val()
        var action = $("#dayoff_action_select_1").val()
        var time_session = $('#dayoff_action_select_2').val()
        if (action == 'cancel_dayoff') {
            var data = {
                'event_date': date,
                'time_session': time_session,
                'event_type': 'Day off'
            }

            admin_cancel_dayoff(data)

        } else { //creat_dayoff
            var data = {
                'event_date': date,
                'time_session': time_session,
                'event_type': 'Day off'
            }

            admin_dayoff(data)

        }

        //spinner show
        Notiflix.Loading.Hourglass('處理中....');
    })

    $("#dayoff_action_select_1").change(function (e) {
        if ($(this).val() == 'cancel_dayoff') {
            $("option[value='Allday']").hide()
        } else {
            $("option[value='Allday']").show()
        }

    })
    //next month of button
    $('body').on('click', 'button.fc-next-button', function () {
        var num_str = $('#date_num').val()
        var num = parseInt(num_str) + 1
        $('#date_num').val(num)
        //do the fuction of ajax_post()
        //ajax_post(num)
    })

    //previous month of button
    $('body').on('click', 'button.fc-prev-button', function () {
        var num_str = $('#date_num').val()
        var num = parseInt(num_str) - 1
        $('#date_num').val(num)
        //do the fuction of ajax_post()
        //ajax_post(num)
    })

    //Click 待確認
    $('#sidebar_not_confirm').click(function (e) {
        var num = parseInt($('#date_num').val())
        //hidden sidebar
        document.getElementById('mySidebar').style.display = 'none'
        //Clean the calendar
        document.getElementById('calendar').innerHTML = ''
        Notiflix.Loading.Hourglass('讀取中....');
        ajax_not_confirm(num)
    })
    //Click 已確認
    $('#sidebar_confirm').click(function (e) {
        var num = parseInt($('#date_num').val())
        //hidden sidebar
        document.getElementById('mySidebar').style.display = 'none'
        //Clean the calendar
        document.getElementById('calendar').innerHTML = ''
        Notiflix.Loading.Hourglass('讀取中....');
        ajax_is_confirm(num)
    })
    //Click 候補名單
    $('#sidebar_waiting').click(function (e) {
        var num = parseInt($('#date_num').val())
        //hidden sidebar
        document.getElementById('mySidebar').style.display = 'none'
        //Clean the calendar
        document.getElementById('calendar').innerHTML = ''
        Notiflix.Loading.Hourglass('讀取中....');
        ajax_waiting(num)
    })
    //Click 已刪除
    $('#sidebar_cancel').click(function (e) {
        var num = parseInt($('#date_num').val())
        //hidden sidebar
        document.getElementById('mySidebar').style.display = 'none'
        //Clean the calendar
        document.getElementById('calendar').innerHTML = ''
        Notiflix.Loading.Hourglass('讀取中....');
        ajax_canceled(num)
    })

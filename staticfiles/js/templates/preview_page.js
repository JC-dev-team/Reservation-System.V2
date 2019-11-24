
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
    // store selector
    $.ajax({
        type: "GET",
        url: '/booking/getStoreInfo/',
        success: function (response) {
            if (response.error != null) {
                Notiflix.Report.Failure('錯誤', response.error, 'ok');

            } else if (response.alert != null) {
                Notiflix.Report.Warning('警告', response.alert, 'ok');
            } else {
                // Clean drop-down menu
                $('#store_name_select').empty()
                
                for (var i = 0; i < response.result.length; i++) {
                    $("#store_name_select").append($("<option></option>").attr("value", response.result[
                        i].store_id).text(response.result[i].store_name));
                }
                    getStoreSeat()
                
            }
            Notiflix.Loading.Remove();
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            Notiflix.Report.Failure('錯誤', '很抱歉，發生無法預期之異常', 'ok');
            Notiflix.Loading.Remove();
        }
    });

    function getStoreSeat() {
        $.ajax({
            type: "GET",
            url: '/booking/getStoreSeat/',
            data: {
                'store_id': $('#store_name_select').val()
            },
            success: function (response) {
                
                if (response.error != null) {
                    Notiflix.Report.Failure('錯誤', response.error, 'ok');
                } else if (response.alert != null) {
                    Notiflix.Report.Warning('警告', response.alert, 'ok');
                } else {
                    // Clean drop-down menu
                    $('#adult_select').empty()
                    $('#children_select').empty()
                    for (var i = 1; i <= response.result.seat; i++) {
                        $("#adult_select").append($("<option></option>").attr("value", i).text(i.toString() + ' 大人'));
                        $("#children_select").append($("<option></option>").attr("value", i - 1).text((i - 1).toString() + ' 小孩'));
                    }
                }
                Notiflix.Loading.Remove();
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                Notiflix.Report.Failure('錯誤', '很抱歉，發生無法預期之異常', 'ok');
                Notiflix.Loading.Remove();
            }
        });

    }
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

    function people_number(data, num, calendar) {
        $.ajax({
            type: 'GET',
            url: '/booking/getCalendar/',
            data: data,
            success: function (response) {
                if (response.error != null) {
                    Notiflix.Report.Failure('錯誤', response.error, 'ok');
                } else if (response.alert != null) {
                    Notiflix.Report.Warning('警告', response.alert, 'ok');
                } else {
                    result = response.result
                    //Function of calendar 
                    calendar_fun(result, num)
                }
                Notiflix.Loading.Remove();

            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                Notiflix.Report.Failure('錯誤', '很抱歉，發生無法預期之異常', 'ok');
                Notiflix.Loading.Remove();
            }

        })
    }

    function eventClick_sendDate(data) {
        $.ajax({
            type: 'GET',
            url: '/booking/getWaitingList/',
            data: data,
            success: function (response) {
                if (response.error != null) {
                    Notiflix.Report.Failure('錯誤', response.error, 'ok');
                } else if (response.alert != null) {
                    Notiflix.Report.Warning('警告', response.alert, 'ok');
                } else {
                    var lunch_status = response.lunch_status
                    var dinner_status = response.dinner_status
                    //insert Modal of state
                    document.getElementById('modal_status').innerHTML =
                        '<label><i class="fa fa-info-circle"></i></label>' + ' 訂位狀態： ' + '<br>' +
                        lunch_status +
                        ' / ' + dinner_status

                    //select disable
                    if (lunch_status == '午餐：店休' && dinner_status == '晚餐：店休') {
                        $('#button_submit').attr('disabled', true)
                        $("option[name='noon']").attr('disabled', true)
                        $("option[name='night']").attr('disabled', true)
                        $("option[name='none']").attr('selected', true)
                    } else if (lunch_status == '午餐：店休') {
                        $('#button_submit').attr('disabled', false)
                        $("option[name='noon']").attr('disabled', true)
                        $("option[name='night']").attr('disabled', false);
                        $("option[name='night']").attr('selected', 'selected');
                    } else if (dinner_status == '晚餐：店休') {
                        $('#button_submit').attr('disabled', false)
                        $("option[name='night']").attr('disabled', true)
                        $("option[name='noon']").attr('disabled', false);
                        $("option[name='noon']").attr('selected', 'selected');
                    } else {
                        $('#button_submit').attr('disabled', false)
                        $("option[name='noon']").attr('disabled', false)
                        $("option[name='night']").attr('disabled', false)
                        $("option[name='noon']").attr('selected', true)
                    }

                    //Show the Modal
                    document.getElementById('information_Modal').style.display = 'inline';
                    //Hidden spinner
                    Notiflix.Loading.Remove();
                    // $('#cover-spin').hide();
                }
            },
            error: function (response) {
                Notiflix.Report.Failure('警告', '發生錯誤！！請重新開啟', 'ok');
                Notiflix.Loading.Remove();
            }

        })
    }

    function initializeApp(data) {
        liff.getProfile().then(profile => {
            //Line user's profile picture
            $('#img').attr('src', profile.pictureUrl);
        })
    }

    function calendar_fun(result, num = 0) {
        //spinner hide
        Notiflix.Loading.Remove();
        document.getElementById('calendar_container').style.display = 'inline'
        var calendarEl = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarEl, {
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
            plugins: ['interaction', 'dayGrid', 'moment'],
            editable: true,
            //Default View
            defaultView: 'dayGridMonth',
            //defaultDate
            defaultDate: (new Date().addDays(3).addMonths(num)).toISOString().slice(0, 10),

            //Height
            height: 'auto',
            contentHeight: 500,
            //Header
            header: {
                left: 'prev',
                center: 'title',
                right: 'next'
            },
            //Header - Title format
            titleFormat: 'YYYY  MM月',
            //Show none current date (False)
            showNonCurrentDates: false,

            //Date selectable (true)
            selectable: true,

            events: [{
                id: '1',
                title: '午餐',
                start: new Date(),
                startRecur: new Date().addDays(3),
                backgroundColor: 'green',
                textColor: 'white',
                daysOfWeek: [1,2, 3, 4, 5, 6, 0]
            },
            {
                id: '2',
                title: '晚餐',
                start: new Date(),
                startRecur: new Date().addDays(3),
                backgroundColor: 'green',
                textColor: 'white',
                daysOfWeek: [1,2, 3, 4, 5, 6, 0]
            },
            // {
            //     id: '3',
            //     title: '店休',
            //     start: new Date(),
            //     startRecur: new Date().addDays(3),
            //     backgroundColor: 'red',
            //     textColor: 'white',
            //     daysOfWeek: [1],

            // },

            ],

            eventRender: function (info) {
                var st = info.event.start
                var start = (new Date(st).addDays(1)).toISOString().slice(0, 10)
                var title = info.event.title
                var color = info.event.backgroundColor

                for (var i = 0; i < result.length; i++) {

                    //red : 人數額滿
                    if (result[i].start == start && result[i].title == title && result[i]
                        .backgroundColor ==
                        'red') {
                        info.el.style.backgroundColor = 'red'
                    }
                    //yellow : 店休
                    if (result[i].start == start && result[i].title == title && result[i]
                        .backgroundColor ==
                        'yellow') {
                        var event = calendar.getEventById(info.event.id)
                        event.setProp('title', '店休')
                        info.el.style.backgroundColor = 'red';
                        info.el.innerText = '店休'

                    }

                }
            },

            //Function
            dateClick: function (info) {

            },
            eventClick: function (info) {
                var adult = $('#adult_select').val();
                var child = $('#children_select').val();
                var store_info = $('#store_name_select').val();
                var evMousEnter_st = info.event.start
                var start = (new Date(evMousEnter_st).addDays(1)).toISOString().slice(0, 10)
                var title = info.event.title
                var color = info.el.style.backgroundColor

                if (title == '午餐') {
                    var time_session = 'Lunch'
                } else {
                    var time_session = 'Dinner'
                }
                //Monday disable
                if (title == '店休') {
                    //Notiflix  Report
                    Notiflix.Report.Warning('店休 ', '＃每週一為公休日 ', 'ok ');
                    return false
                }

                //insert Modal of date
                document.getElementById('modal_date').innerHTML =
                    '<label><i class="fa fa-calendar"></i></label>' + ' 日期： ' +
                    '<p id="bk_date_select">' +
                    start + '</p>'

                //ajax eventClick_sendDate(data)
                var data = {
                    'adult': adult,
                    'children': child,
                    'event_date': start,
                    'store_id': store_info,
                    'action': 'main'
                }
                eventClick_sendDate(data)
                //spinner show
                Notiflix.Loading.Hourglass();
            }
        });
        return calendar.render();
    }

    function ajax_post(num = 0) {
        //ajax data
        var status = true;
        var adult = $('#adult_select').val();
        var child = $('#children_select').val();
        var store_info = $('#store_name_select').val();
        // var Date = moment().add(1,'M')
        var start_month = moment().add(num, 'M').startOf('month').format('YYYY-MM-DD')
        var end_month = moment().add(num, 'M').endOf('month').format('YYYY-MM-DD');

        if (status) {
            var data = {
                'adult': adult,
                'children': child,
                'store_id': store_info,
                'start_month': start_month,
                'end_month': end_month,
                'action': 'main'
            }
            //Clean the calendar
            document.getElementById('calendar').innerHTML = ''

            // do ajax fuction

            
            if (data.adult != null && data.children != null && data.adult != '' && data.children != '' && data.store_id != '' && data.store_id != null) {
                people_number(data, num)

                //spinner show
                document.getElementById('calendar_container').style.display = 'inline'
                Notiflix.Loading.Hourglass();
            }
            else {
                Notiflix.Report.Failure('發生錯誤', '請選擇欲訂位之店家或是人數', 'ok');
            }

        }


    }

    //ready
    $(function () {
        document.getElementById('sidebar_button').style.display = 'none'
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

        //Initial User of displayName & displayPhone
        $('#displayName').html('快速查詢訂位');


        $('#adult_select, #children_select').change(function (e) {
            document.getElementById('calendar').innerHTML = ''
        })


    });




    //next month of button
    $('body').on('click', 'button.fc-next-button', function () {
        var num_str = $('#date_num').val()
        var num = parseInt(num_str) + 1
        $('#date_num').val(num)
        //do the fuction of ajax_post()
        ajax_post(num)
    })

    //previous month of button
    $('body').on('click', 'button.fc-prev-button', function () {
        var num_str = $('#date_num').val()
        var num = parseInt(num_str) - 1
        $('#date_num').val(num)
        //do the fuction of ajax_post()
        ajax_post(num)
    })

    $('#people_number_submit').click(function (e) {
        var num = parseInt($('#date_num').val())
        //do the fuction of ajax_post()
        ajax_post(num)


    })

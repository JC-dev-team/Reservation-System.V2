
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

    function ajax_add_product(data) {
        $.ajax({
            type: 'POST',
            url: '/softwayliving/AddProduct/',
            data: data,
            success: function (response) {
                if (response.error != null) {
                    Notiflix.Report.Failure('錯誤', response.error, 'ok');
                    Notiflix.Loading.Remove();
                } else if (response.alert != null) {
                    Notiflix.Report.Warning('警告', response.alert, 'ok');
                    Notiflix.Loading.Remove();
                } else {
                    Notiflix.Notify.Success('已新增！！');
                    document.getElementById('add_Modal').style.display = 'none'
                    window.location.reload();
                }

            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                Notiflix.Notify.Failure('很抱歉，發生未知錯誤！！');
                Notiflix.Loading.Remove();

            }

        })
    }

    function ajax_edit_product(data) {
        $.ajax({
            type: 'POST',
            url: '/softwayliving/ModifyProduct/',
            data: data,
            success: function (response) {
                if (response.error != null) {
                    Notiflix.Report.Failure('錯誤', response.error, 'ok');
                    Notiflix.Loading.Remove();
                } else if (response.alert != null) {
                    Notiflix.Report.Warning('警告', response.alert, 'ok');
                    Notiflix.Loading.Remove();
                } else {
                    Notiflix.Notify.Success('已儲存！！');
                    document.getElementById('edit_Modal').style.display = 'none'
                    window.location.reload();
                }

            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                Notiflix.Notify.Failure('很抱歉，發生未知錯誤！！');
                Notiflix.Loading.Remove();

            }

        })
    }

    function ajax_delete_product(t, data) {
        $.ajax({
            type: 'POST',
            url: '/softwayliving/DeleteProduct/',
            data: data,
            success: function (response) {
                if (response.error != null) {
                    Notiflix.Report.Failure('錯誤', response.error, 'ok');
                } else if (response.alert != null) {
                    Notiflix.Report.Warning('警告', response.alert, 'ok');
                } else if(response.outdated != null){
                    Notiflix.Report.Warning('警告', response.outdated, 'ok');
                    window.location.replace(response.action)
                } else {
                    Notiflix.Notify.Success('已刪除！！');
                    t.parentElement.style.display = 'none'
                }

                Notiflix.Loading.Remove();
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                Notiflix.Notify.Failure('很抱歉，發生未知錯誤！！');
                Notiflix.Loading.Remove();

            }

        })
    }


    function save_add() {
        Notiflix.Confirm.Show('管理者權限', '確定要新增嗎?', '是-新增', '否',
            function () {
                var status = true
                var prod_name = $('#add_prod_name').val();
                var prod_price = $('#add_prod_price').val();

                if (prod_name == '') {
                    Notiflix.Notify.Failure('請輸入名稱！！')
                    status = false;
                } else if (prod_price == '') {
                    Notiflix.Notify.Failure('請輸入價位！！')
                    status = false;
                }

                if (status) {
                    var data = {
                        'prod_name': prod_name,
                        'prod_price': prod_price
                    }

                    //spinner show
                    Notiflix.Loading.Hourglass('新增中....');
                    ajax_add_product(data)
                }


            },
            function () {

            });
    }

    function save_edit() {
        Notiflix.Confirm.Show('管理者權限', '確定要更動嗎?', '是-儲存', '否',
            function () {
                var prod_id = $('#edit_prod_id').val();
                var prod_name = $('#edit_prod_name').val();
                var prod_price = $('#edit_prod_price').val();


                var data = {
                    'prod_id': prod_id,
                    'prod_name': prod_name,
                    'prod_price': prod_price
                }

                //spinner show
                Notiflix.Loading.Hourglass('更新中....');
                ajax_edit_product(data)

            },
            function () {

            });

    }
    function add_product() {
        document.getElementById('add_Modal').style.display = 'inline'
    }

    function edit_product(t, prod_id, prod_name, prod_price) {
        document.getElementById('edit_Modal').style.display = 'inline'
        document.getElementById('edit_prod_id').value = prod_id
        document.getElementById('edit_prod_name').value = prod_name
        document.getElementById('edit_prod_price').value = prod_price


    }


    function delete_product(t, prod_id) {
        Notiflix.Confirm.Show('管理者權限', '確定要刪除此價位嗎?', '是-刪除', '否',
            function () {

                var data = {
                    'prod_id': prod_id
                }

                //spinner show
                Notiflix.Loading.Hourglass('正在刪除....');
                ajax_delete_product(t, data)

            },
            function () {


            });



    }

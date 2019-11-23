
    function closewindow() {
        if ('{{action}}' == 'admin') {
            window.location.href = '/softwayliving/login/'
        } else {
            liff.closeWindow()
        }


    }

    $(function () {
        if ('{{action}}' == 'admin') {
            document.getElementById('close_button').innerText = '返回管理者介面'
        }

        
        if ('{{data.waiting_num}}' != '0') { //this is not correct
            document.getElementById('information').innerText = "訂位資訊 (候補 " + '{{data.waiting_num}}' + ")"
        }
    })

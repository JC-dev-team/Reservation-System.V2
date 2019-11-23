
    function send() {
        Notiflix.Loading.Hourglass('讀取中....')
        document.getElementById("checklogin_form").action = "/softwayliving/StaffAuth/";
        document.getElementById("checklogin_form").submit();
    }

    function initializeApp(data) {
        liff.getProfile().then(profile => {
            // var disname = {
            //   'name': profile.displayName
            // };
            // disname_json = JSON.parse(JSON.stringify(disname.name))
            // $('#img').attr('src', profile.pictureUrl);
            // $('#social_id').val(data.context.userId); //data.context.userId
            // $('#social_app').val('Line');

        })
    }



    //ready
    $(function () {
        document.getElementById("top_block").style.display = 'none'

        //Notiflix.Loading.Hourglass('讀取中....');
        //init LIFF
        liff.init(function (data) {
            initializeApp(data);
        });
        //$('#email').val('123@123.com'); //data.context.userId
        //$('#password').val('Line');


        // if ($('#email').val() != '' && $('#password').val() != '') {
        //     send()
        // } else {
        //     window.location.replace('/softwayliving/error/');
        // }

    });

    $(function () {
        $('#checklogin_form_submit').click(function (e) {
            var status = true;
            var email = $('#email').val();
            var password = $('#password').val();

            if (email == '') {
                alert('請輸入信箱！')
                status = false;
            } else if (password == '') {
                alert('請輸入密碼！')
                status = false;
            }

            if (status) {
                send()
            }

        });
    });


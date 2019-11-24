
    function send() {
        if (true) {
            document.getElementById("checklogin_form").action = "/userdashboard/auth/";
            document.getElementById("checklogin_form").submit();
        }
    }

    function initializeApp(data) {
        liff.getProfile().then(profile => {
            var disname = {
              'name': profile.displayName
            };
            disname_json = JSON.parse(JSON.stringify(disname.name))
            $('#img').attr('src', profile.pictureUrl);
            $('#social_id').val(data.context.userId); //data.context.userId
            $('#social_app').val('Line');
            $('#social_name').val(disname_json)

            send()
        })
    }
    //ready
    $(function () {
        Notiflix.Loading.Hourglass('讀取中....');
        //init LIFF
        liff.init(function (data) {
            initializeApp(data);
        });
        //remember to edit it to Line Liff
        // $('#social_id').val('9636ff56-e78b-11e9-a2b8-0ec425232520'); //data.context.userId//
        // $('#social_app').val('Line');//Line
        //send data 
        // send()
        // if($('#social_id').val() != '' && $('#social_app').val() != ''){
        //     send()
        // }
        // else{
        //     window.location.replace('/userdashboard/error/');
        // }
    });



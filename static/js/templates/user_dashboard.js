
    function user_reservation() {
        Notiflix.Loading.Hourglass('讀取中....');
        window.location.href = '/booking/member/'
    }

    function user_check() {
        Notiflix.Loading.Hourglass('讀取中....');
        document.getElementById("userdashboard_form").action = "/userdashboard/checkreservation/";
        document.getElementById("userdashboard_form").submit();
    }

    


  function send(action) {
    if (action == 'reservation') {
      //訂位（使用者
      window.location.href = '/booking/login/'
    } else if (action == 'check_reservation') {
      //查詢（使用者
      Notiflix.Loading.Hourglass('讀取中....');
      window.location.href = '/userdashboard/checkreservation/'

    }


  }

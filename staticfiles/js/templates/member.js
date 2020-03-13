
  function dosave() {
    if (true) {
      Notiflix.Loading.Hourglass('處理中...');
      document.getElementById("member_form").action = "/booking/booking/";
      document.getElementById("member_form").submit();
    }
  }

  $(document).ready(function () {
    $("#member_submit").attr("disabled", false);
    //check privacy_policy
    $('#privacy_policy').click(function () {
      if ($('#privacy_policy').is(':checked')) {
        $("#member_submit").attr("disabled", false);
      }
      if ($('#privacy_policy').is(':checked') == false) {
        $("#member_submit").attr("disabled", true);
      }
    });

  })

  // function initializeApp(data) {
  //   liff.getProfile().then(profile => {
  //     var disname = {
  //       'name': profile.displayName
  //     };
  //     disname_json = JSON.parse(JSON.stringify(disname.name))
  //     $('#img').attr('src', profile.pictureUrl);
      
  //   })
  // }

  function initializeLiff(MyLiffId) {
    liff
        .init({
            liffId: MyLiffId
        })
        .then(() => {
            // start to use LIFF's api
            initializeApp();
        })
        .catch((err) => {
            // document.getElementById("liffAppContent").classList.add('hidden');
            // document.getElementById("liffInitErrorMessage").classList.remove('hidden');
        });
}

function displayLiffData(){
  liff.getProfile()
      .then(profile => {
        $('#img').attr('src', profile.pictureUrl);

      })
}

  //ready
  $(function () {
    //init LIFF
    // liff.init(function (data) {
    //   initializeApp(data);
    // });

    initializeLiff('1653788675-gE0L04We')
    displayLiffData()

    document.getElementById("member_birth").valueAsDate = new Date();

  });


  $(function () {
    $('#member_submit').click(function (e) {
      var status = true;
      // 姓名
      var member_name = $('#member_name').val();
      // 電話
      var member_phone = $('#member_phone').val();
      var reg_phone = new RegExp(/^09\d{8}$/);

      if (member_name == '') {
        alert('請輸入姓名！')
        status = false;
      } else if (member_phone == '') {
        alert('請輸入電話！')
        status = false;
      } else if (reg_phone.test(member_phone) == false) {
        alert('手機號碼格式不正確');
        status = false;
      }
      if (status) {
        dosave()
      }

    });
  });


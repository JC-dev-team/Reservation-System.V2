function send() {
    document.getElementById("checklogin_form").action = "/booking/member/";
    document.getElementById("checklogin_form").submit();

}

function initializeLiff(MyLiffId) {
    liff
        .init({
            liffId: MyLiffId
        })
        .then(() => {
            displayLiffData()
        })
        .catch((err) => {
            //alert(err)
        });
}

function displayLiffData() {
    liff.getProfile()
        .then(profile => {
            const name = profile.displayName
            $('#img').attr('src', profile.pictureUrl);
            $('#social_id').val(profile.userId)
            $('#social_app').val('Line');
            $('#social_name').val(name)

            send()
        })
}

//LineLIFF V1
// function initializeApp(data) {
//     liff.getProfile().then(profile => {
//         const name = profile.displayName
//         $('#img').attr('src', profile.pictureUrl);
//         $('#social_id').val(data.context.userId); //data.context.userId
//         $('#social_app').val('Line');
//         $('#social_name').val(name)

//         send()
//     })
// }


//ready
$(function () {
    Notiflix.Loading.Hourglass('讀取中....');
    //Line LIFF V2
    initializeLiff('1654026454-2jpQJ4Py')

    //init LIFF
    // liff.init(function (data) {
    //     initializeApp(data);
    // });



    //xxxxxx remember to edit it to Line Liff  xxxxxxxx
    // $('#img').attr('src', "https://img.webmd.com/dtmcms/live/webmd/consumer_assets/site_images/article_thumbnails/other/cat_relaxing_on_patio_other/1800x1200_cat_relaxing_on_patio_other.jpg?resize=750px:*");
    // $('#social_id').val('9644ff56-e78b-11e9-a2b8-0ec425232523'); //data.context.userId//9636ff56-e78b-11e9-a2b8-0ec425232520
    // $('#social_app').val('Line');//Line
    // $('#social_name').val('James')//James
    // xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    //send data
    //send()
    // if($('#social_id').val() == '' || $('#social_app').val() == ''){
    //     window.location.replace('/booking/error/');
    // }else{
    //     send()
    // }


    

});
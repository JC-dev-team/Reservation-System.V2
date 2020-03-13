function send() {
    Notiflix.Loading.Hourglass('讀取中....')
    document.getElementById("checklogin_form").action = "/softwayliving/StaffAuth/";
    document.getElementById("checklogin_form").submit();
}

// function initializeApp(data) {
//     liff.getProfile().then(profile => {
//         // var disname = {
//         //   'name': profile.displayName
//         // };
//         // disname_json = JSON.parse(JSON.stringify(disname.name))
//         // $('#img').attr('src', profile.pictureUrl);
//         // $('#social_id').val(data.context.userId); //data.context.userId
//         // $('#social_app').val('Line');

//     })
// }



//ready
$(function () {
    document.getElementById("top_block").style.display = 'none'
    //init LIFF
    // liff.init(function (data) {
    //     initializeApp(data);
    // });
    

});

$(function () {
    $('#checklogin_form_submit').click(function (e) {
        var status = true;
        var email = $('#email').val();
        var password = $('#password').val();

        if (email == '') {
            status = false;
        } else if (password == '') {
            status = false;
        }

        if (status) {
            send()
        }

    });
});

//cookie 
$(function () {
    if (getCookie('name')) {
        $('#email').val(getCookie('name'));
        $('#memory').prop('checked', 'checked');
    } else {
        $('#email').val('');
    }
});
$('#checklogin_form_submit').click(function () {
    if ($('#memory').prop('checked')) {
        var email = $('#email').val();
        setCookie("name", email);
    } else {
        delCookie('name');
    }
});
//        主要函数
function setCookie(name, value) //设置cookie
{
    var Days = 30;
    var exp = new Date();
    exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
    document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString();
}

function getCookie(name) //拿到cookie
{
    var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
    if (arr = document.cookie.match(reg))
        return unescape(arr[2]);
    else
        return null;
}

function delCookie(name) //删除cookie
{
    var exp = new Date();
    exp.setTime(exp.getTime() - 1);
    var cval = getCookie(name);
    if (cval != null)
        document.cookie = name + "=" + cval + ";expires=" + exp.toGMTString();
}

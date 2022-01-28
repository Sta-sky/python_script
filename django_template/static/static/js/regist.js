//注册提交js
$(function () {
    $('#subs').click(function () {

        var username = $('#username').val();
        var password = $('#passwd').val();
        var passwords = $('#passwds').val();
        var email = $('#email').val();
        var phone = $('#phone').val();
        var code = $('#code').val();
        console.log(typeof (code));
         if (Isemail(email) !== true){
             alert('邮箱格式有误，！请重新输入')
         }

        result_data = {
            'username': username, 'password': password, 'passwords': passwords, 'email': email
            , 'phone': phone, 'code': code
        };

        if (username !== '' && password !== '' && passwords !== '') {
            $.ajax({
                type: "POST",
                dataType: 'json',
                url: SER_URL + 'user/regist',
                contentType: 'application/json;charset=UTF-8',
                data: JSON.stringify(result_data),
                success: function (result) {
                    //服务器传回的是一个json对象  可以用点语法直接获取到 key对应的值
                    if (result.code === 200) {
                        alert('用户创建成功!');
                        window.localStorage.clear();
                        window.localStorage.setItem('user_name', result.username);
                        window.localStorage.setItem('user_id', result.id);
                        window.localStorage.setItem('user_token', result.token);
                        window.location.href = 'login.html'
                    } else {
                        alert(result.message)
                    }
                }
            })
        } else {
            alert('注册信息不能为空');
        }
    });

//微博授权js
    $('#icon').click(function () {
        $.ajax({
            type: 'GET',
            url: SER_URL + 'user/weibo',
            dataType: 'json',
            async: false,
            success: function (result) {
                if (result.code === 200) {
                    alert('成功跳转微博');
                    window.open(result.auth_url)
                }
            },
            error: function () {
                alert(error.message)
            }
        });
    });
});

//登录注册切换js
$('#login2').click(function () {
    window.location.href = STIC_URL + 'login.html'
});
$('#regist1').click(function () {
    window.location.href = STIC_URL + 'regist.html'
});


//获取验证码js
$('#but_code').on('click', function () {
    var username = $('#username').val();
    var phone = $('#phone').val();
    var phone_number = {'phone_number': phone, 'username': username};

    //验证手机格式
    if (phone.length === 0 || !(/^1[34578]{1}\d{9}/.test(phone))) {
        alert('手机格式有误,请核对后重新输入')
    } else if (username.length === 0) {
        alert('请输入用户名')
    } else {
        //调用时间倒计时
        time($('#but_code'));
        $.ajax({
            type: 'POST',

            url: SER_URL + 'user/send_sms',
            dataType: 'json',
            data: JSON.stringify(phone_number),
            success: function (result) {
                if (result.code === 200) {
                    alert('短信已发送')
                } else {
                    alert(result.message)
                }
            }

        })
    }
});

// 检测地址是否在服务区
function myFun(result) {
    var cityName = result.name;
    if (cityName !== '成都市') {
//        alert('系统检测到您当前地址不在服务区内,部分功能将会有所限制')
    }
//     alert('欢迎使用')
}

var myCity = new BMap.LocalCity();
myCity.get(myFun);



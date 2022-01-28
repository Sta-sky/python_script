//主页导航栏显示账户信息
$(function () {
    $('#head').load('header.html', () => {
        var res='';
        var reg='';
        res = '<a id="login" href="login.html">登录</a><span><b>|</b></span>';
        reg = res + '<a id="reg" href="regist.html">注册</a>';
        $('.top_act').html(reg);

        var loginName = window.localStorage.getItem('user_name');
        var userId = window.localStorage.getItem('user_id');
        if (loginName) {
            res = '<a id="login" href= "user_info.html?id=' + userId + '">' + loginName + '</a><span><b>|</b></span>';
            res += '<a id="logout" href="">注销</a><span><b>|</b></span>';
            reg = res + '<a id="reg" href="regist.html">注册</a>';
            $('.top_act').html(reg);
            $('#logout').on('click', (e) => {
                e.preventDefault();
                window.localStorage.clear();
                alert('退出登录');
                window.location.reload();
                window.location.href = 'index.html';
                res = '<a id="login" href="login.html">' + 登录 + '</a><span><b>|</b></span>';
                reg = res + '<a id="reg" href="regist.html">注册</a>';
                $('.top_act').html(reg);

            })
        }
    })
});


//导航栏鼠标滑入滑出显示自导航栏
$('#l2').hover(function () {
    $('#sub_nav').stop(true, true).show(400)
}, function () {
    $('#sub_nav'.stop(true, true).hide(400))
});

//导航栏主页、论坛、发布活动，焦点切换
function getFocus($obj) {
    $obj.addClass('focus');
    $('.focus').each(function (i, element) {
        $(element).removeClass('focus')
    });
}


//导航栏主页、论坛、发布活动，焦点删除
function removeFocus() {
    $('#l1>a').removeClass('focus');
    $('#l2>a').removeClass('focus');
    $('#l3>a').removeClass('focus');
}


$('#l3>a').on('click', function () {
    var user_name = window.localStorage.getItem('user_name');
    if (user_name) {
        alert('请登录账号')
    } else {
        $.ajax({
            type: 'post',
            url: SER_URL + 'active/create',
            contentType: 'application/json',
            data: {
                'user_name': user_name
            },
            dataType: 'json',
            success: function (response) {
                if (response.code !== 200) {
                    alert(response.error)
                } else {
                    window.location.href = 'createact.html'
                }
            },
            error: function (err) {
                console.log(err)
            }
        })
    }
});





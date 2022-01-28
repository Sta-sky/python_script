$(function () {
        $('.put').css({display:'none'});

        $('#butt1').click(function () {

            var querystring = location.search;

            $.ajax({
                type:'GET',
                url:SER_URL+'user/grant'+querystring,
                dataType:'json',
                success:function (result) {
                    if (result.code == 10206) {
                        alert(result.message);
                    }else if (result.code == 200){
                        window.localStorage.clear();
                        window.localStorage.setItem('username',result.username);
                        window.localStorage.setItem('user_token',result.data);
                        $('#wait1').css({display:'none'});
                        $('#success').css({display:'block'});
                        setTimeout(function () {
                            window.location.href = SER_URL+'index.html'},3000)
                    }else if (result.code == 201) {
                        alert('进来了');
                        window.localStorage.setItem('uid',result.uid);
                        $('#limg').css({display:'none'});
                        $('#box2').css({display:'none'});
                        $('.put').css({display:'block'});
                    }
                },
                 error:function () {
                    alert('我错了');
                    alert(error.message)
                 }
            });

        });

        $('#butt2').click(function () {
            $('#wait2').css({display:'block'});
            setTimeout(function () {
                $('#wait2').css({display:'none'});
                window.location.href = 'http://176.209.104.17:7001/templates/index.html'

            },2000)
        });

//页面跳转
    $('#top_index').click(function () {
        window.location.href = STAC_URL+'index.html'
    });
     $('#top_login').click(function () {
        window.location.href = STAC_URL+'login.html'
    });




        $('#but').click(function () {
            var username = $('#username').val();
            var passwd = $('#passwd').val();
            var passwds = $('#passwds').val();
            var email = $('#email').val();
            var phone = $('#phone').val();
            var code = $('#code').val();
            var uid = window.localStorage.getItem('uid');
            alert(uid);

            result_data = {'username':username,'password':passwd,'passwords':passwds,
                'phone':phone,'code':code ,'uid':uid,'email':email};


            $.ajax({
                type: 'POST',
                dataType: 'json',
                url:SER_URL+'user/bind',
                contentType:'application/json;charset=UTF-8',
                data:JSON.stringify(result_data),
                success:function (result) {
                    if (result.code == 200){
                        alert('绑定成功');
                        window.localStorage.clear();
                        window.localStorage.setItem('username',result.username);
                        window.localStorage.setItem('user_token',result.token);
                        window.location.href = 'index.html';
                    }else if (result.code == 10206){
                        alert(result.message.error)
                    }else if (result.code == 10200){
                        alert(result.message.error);
                    } else if (result.code == 10207) {
                        alert('用户已绑定  请点击跳转首页');
                        window.location.href = 'index.html'
                        }
                    alert('nihao')
                    }
                })
            });

});
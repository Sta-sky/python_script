var user_id = GetUrlString('id');
token = window.localStorage.getItem('user_token');
interest_list = [];

$.ajax({
    type: "get",
    dataType: 'json',
    headers: {'Authorization': token},
    url: SER_URL + 'users/update?id=' + user_id,
    contentType: 'application/json;charset=UTF-8',
    success: function (result) {
        if (result.code === 200) {
            var data = result.data;
            var res = '';
            $.each(data.tag, function (index, d) {
                res += '<span class="not_sel" id="">' + d + '</span>'
            });
            $('#hobby').html(res);

            $('#nickname').prop('value', data.nickname);
            $('#signature').prop('value', data.introduction);
            $('#birth').prop('value', data.birth);
            $('#img1').prop('src', IMG_URL + data.url);

            if ($('#nan').val() == data.gender) {
                $('#nan').prop('checked', 'checked')
            }
            if ($('#nv').val() == data.gender) {
                $('#nv').prop('checked', 'checked')
            }
            if ($('#mimi').val() == data.gender) {
                $('#mimi').prop('checked', 'checked')
            }
            var cns = document.getElementById("hobby").getElementsByTagName('span');
            for (i = 0; i < cns.length; i++) {
                if (data.interest.includes(cns[i].innerText)) {
                    cns[i].className = 'be_sel';
                    interest_list.push(cns[i].innerText)
                }

            }
            var cns1 = document.getElementById("hobby").getElementsByTagName('span');
            for (var i = 0; i < cns1.length; i++) {
                cns1[i].addEventListener('click', function () {
                    if (this.className == 'be_sel') {
                        this.className = 'not_sel';
                        interest_list.pop(this.innerText)
                    } else {
                        this.className = "be_sel";
                        interest_list.push(this.innerText)
                    }
                });
            }

        } else {
            alert(result.message);
            if (result.code === 10203 || result.code === 10201 ) {
                alert(result.message)
                window.location.href('login.html');
            } else if (result.code === 10206) {
                alert(result.message)
                window.location.href('index.html')
            } else {
                alert(result.message)
                window.location.href('index.html')
            }
        }
    }
});


// 用户修改密码
$(function () {
    $('#sub').click(function () {
        alert('正在上传数据');
        var nickname = $('#nickname').val();
        var signature = $('#signature').val();
        var val = $('input:radio[name="sex"]:checked').val();
        if (val == null) {
            alert('gun')
        } else {
            var gender = val
        }
        var birth = $('#birth').val();
        var pro = $('#pro').val();
        var city = $('#city').val();

        result_data = {
            'nickname': nickname,
            'signature': signature,
            'gender': gender,
            'birth': birth,
            'pro': pro,
            'city': city,
            'interest': interest_list
        };
        console.log(result_data);

        $.ajax({
            type: "POST",
            dataType: 'json',
            headers: {'Authorization': token},
            url: SER_URL + 'users/update?id=' + user_id,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify(result_data),
            success: function (result) {
                //服务器传回的是一个json对象  可以用点语法直接获取到 key对应的值
                if (result.code == 200) {
                    alert('用户信息修改完成');
                } else {
                    alert(result.message)
                }
            }
        })
    });
});


// 上传头像
$('#go').click(function () {
    let reads = new FileReader();
    file = document.getElementById('file').files[0];
    alert(file.name)
    reads.readAsDataURL(file);
    reads.onload = function (e) {
        var data = {'data': reads.result};
        $.ajax({
            type: "POST",
            dataType: 'json',
            url: SER_URL + 'users/upload',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify(data),
            success: function (result) {
                //服务器传回的是一个json对象  可以用点语法直接获取到 key对应的值
                if (result.code == 200) {
                    alert('图片添加完成');
                } else {
                    alert(result.message)
                }
            }
        })
    };
})


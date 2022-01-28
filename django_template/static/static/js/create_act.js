// 重载页面
$('#quxiao').on('click', function () {
    window.location.reload(false)
})

// 获取创建活动信息
$('#add_act').on('click', function () {
    var token = window.localStorage.getItem('user_token');
    if (token !== '') {
        console.log('提交中')
    } else {
        alert('请先登录');
        window.location.href = 'login.html';
        return;
    }

    var kind = $('#kind').val()
    if (kind === '请选择') {
        alert('请选择活动主题');
        return;
    }
    var title = $('#title').val()
    var actintro = $('#act_intros').val()
    var starttime = $('#start-time').val()
    var endtime = $('#end-time').val()
    var addr = $('#addr').val()
    var condition = $('#condition').val()

    if (endtime < starttime) {
        alert('结束时间不能在开始时间之后');
        return
    }
    date = new Date()
    var year = starttime.split('-')[0]
    var mou = starttime.split('-')[1]
    var day = starttime.split('-')[2]
//    if (date.getFullYear() > year || date.getMonth() > mou) {
//        alert('本平台不支持穿越活动');
//        return;
//    }
//    if (date.getDate() + 2 > day) {
//        alert('时间有点仓促，请至少提前两天发布活动')
//        return;
//    }
    if (isNaN(Number(condition))) {
        alert('请输入正确的数字格式')
        return;
    }

    let img_data = ''
    let reads = new FileReader();
    var files = document.getElementById('myfile').files; 
    if (files.length === 0){
        console.log('用户没有上传图片')
        img_data = ''
        var data = {
            'kind': kind,
            'title': title,
            'content': actintro,
            'addr': addr,
            'condition': condition,
            'starttime': starttime,
            'endtime': endtime,
            'img_data': img_data,
             }
        request(data, token)
    } else {
        file = document.getElementById('myfile').files[0];
        reads.readAsDataURL(file);
        reads.onload = function () {
            img_data = reads.result
            var data = {
                'kind': kind,
                'title': title,
                'content': actintro,
                'addr': addr,
                'condition': condition,
                'starttime': starttime,
                'endtime': endtime,
                'img_data': img_data,
                 }
            request(data, token)

        }
    };

});


// 活动创建的ajax
function request(data, token) {
    $.ajax({
        data: JSON.stringify(data),
        enctype: 'multipart/form-data',
        headers: {'Authorization': token},
        type: 'POST',
        contentType: 'application/json',
        url: SER_URL + 'active/create',
        success: function (response) {
            if (response.code === 200) {
                window.location.href = 'activity.html?act_id=' + response.actid
            } else if (response.code === 10203) {
                alert("用户未登录，请重新登录")
                
            } else if (response.code === 10204 ) {
                alert('认证过期，请重新登录')

            }
        },
        error: function () {
            alert('服务器在开小差，请稍后重试!')
        }
    });
}


$.ajax({
    type: 'GET',
    contentType: 'application/json',
    url: SER_URL + 'label/option',
    success: function (response) {
        var data = response.data
        res = ''
        res += '<option>请选择</option>'
        $.each(data, function (index, val) {
            res += '<option>' + val + '</option>'
        })
        $('#kind').html(res)
    }
})


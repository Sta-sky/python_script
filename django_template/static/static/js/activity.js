var id = GetUrlString('act_id');
var token = window.localStorage.getItem('user_token');

// 加载活动内容详情
$.ajax({
    type: 'GET',
    url: SER_URL + 'active/detail?act_id=' + id,
    dataType: 'json',
    contentType: 'application/json',
    data: JSON.stringify(data),
    success: function (result) {
        if (result.code === 200) {
            console.log(result)
            info = result.data
            begtime = info.starttime;
            $('#title').text(info.subject);
            $('#nr').text(info.content);
            $('#like').text(info.like);
            var res = '';
            var year = Number(begtime.split('-')[0]);
            var month = Number(begtime.split('-')[1]);
            date = Number(begtime.split("-")[2]);
            var  day = getMonthDays(year,month);

            // alert(date);
            for (var i = 0; i < 5; i++) {
                if (date<day){
                    date +=1;
                }else {
                    var date = 0;
                    month +=1;
                    if (month > 12) {
                        month = 0;
                        month += 1;
                        year += 1;
                    }
                    date +=1;
                }
                begtime = year+'-'+month+'-'+date;
                res += '<li>' + begtime + '</li>'
            }
            $('#opt').html(res)
        } else {
            alert(result.message)
        }
    }
});


//  收藏单击事件
function changeVal(statu) {
    var data = ''
    if (statu === 'collection') {
        var nowstatus = $('#sc').text()
        data = {'collection': nowstatus, 'actid': id}
    } else {
        data = {'actid': id}
    }
    $.ajax({
        type: 'POST',
        headers: {
            'Authorization': token
        },
        url: SER_URL + 'label/' + statu,
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (result) {
            if (result.code === 200) {
                if (statu === 'collection') {
                    if (nowstatus === "收藏") {
                        $('#sc').text("已收藏");
                    } else {
                        $('#sc').text("收藏")
                    }
                } else {
                    $('#like').text(result.data)
                }
            } else {
                alert('请先登录!!')
            }
        },
        error: function () {
            alert('服务器繁忙--!')
        }
    })
}


// 收藏点击
$('#sc').on('click', function () {
    if (token){}else {return}
    changeVal('collection')
})

// 点赞点击
$('#clicklike').on('click', function () {
    changeVal('like')
})

//显示投票框
$('#fbtn').on('click', function () {
    $('#tuo').removeAttr('style')
})

// 返回
$('#btn_qx').on('click', function () {
    $('#tuo').attr('style', 'display:none')
})

// 移除样式
function rmclass() {
    $.each($('#opt>li'), function (index, ele) {
        $(ele).removeClass('hover')
    })
}

// 选择日期
$('#opt').on('click','li', function () {
    rmclass()
    $(this).addClass('hover')
})

// 免责申明
$('#jr').on('click', function () {
    $('#mz').removeAttr('style')
})

// 退出免责申明
$('#mz').on('click', function () {
    $('#mz').attr('style', 'display:none')
})


// 提交
$('#btn_qd').on('click', function () {
    if (token){}else {alert('请先登录');return}
    var result = $('.hover').text();
    if (result) {
    } else {
        alert('您还没有投票')
    }
    $.ajax({
        type: 'GET',
        headers: {
            'Authorization': token
        },
        url: SER_URL + 'label/' + id + '?date=' + result,
        success: function (result) {
            if (result.code === 200) {
                alert('投票成功')
            } else {
                alert('服务器繁忙!  敬请期待')
            }
        },
        error: function () {
            alert('服务器繁忙！')
        }
    });
});

 var tag = GetUrlString('sub')
 var tags = encodeURI(encodeURI(tag))

function webrequestpage(page) {
       act_nh = 'new'
// 页面加载初始化请求第一页
    if (typeof WebSocket != 'undefined') {
            console.log("您的浏览器支持Websocket通信协议")
        // 创建websockter对象
        ws = new WebSocket(WEBSOCKET_URL + 'active/new/' + page+ '?tag=' + tag)
        // 开始通信时的处理
        ws.onopen = function () {
            // 最新活动点击事件
            $('#z_new_act').on('click', function () {
                act_nh = 'new'
                ws.close()
                webrequestpage('1')
            })
        }

        ws.onmessage = function (mes) {
            console.log('websocket 收到消息')
            var response = JSON.parse(mes.data)
            // 将数据转换成JSON格式
            if (response.code === 200) {
                var message = response.data
                var res = ''
                $.each(message, function (index, val) {
                    res += '<div id="new_act_">'
                    res += '<a href="activity.html?act_id=' + val.id + '">'
                    res += '<img src="' + ACT_IMG_URL + val.actimg + '" alt="" act_id="' + val.id + '">'
                    res += '</a>'
                    res += '<div id="new_content">'
                    res += '<div id="n_tit" act_id="' + val.id + '">'
                    res += '<a href="activity.html?act_id=' + val.id + '">' + val.title
                    res += '</a></div>'
                    res += '<div id="n_cont" act_id="' + val.id + '">'
                    res += '<a href="activity.html?act_id=' + val.id + '"><p>' + val.content + '</p>'
                    res += '</a></div>'
                    res += '<div id="n_lt">'
                    res += '<div id="n_lab">' + val.label + '</div>'
                    res += '<div id="n_time">' + val.date + '</div>'
                    res += '</div></div></div>'
                })
                $('#b2_l2').html(res)
                var pagearr = response.page
                getpage(pagearr[0], pagearr[1])
            } else {
                $('#b2_l2').html('')
                getpage(1, 1)
            }
        }
        ws.onclose = function () {
            console.log('连接关闭')
        }
    } else {
        alert("您的浏览器不支持Websocket通信协议，请使用Chrome或者Firefox浏览器！")
    }
}

webrequestpage('1')
//=======================

// 构造html
function makeresult(data) {
    var res = ''
    $.each(data, function (index, val) {
        res += '<div id="new_act_">'
        res += '<a href="activity.html?act_id=' + val.id + '">'
        res += '<img src="' + ACT_IMG_URL + val.actimg + '" alt="" act_id="' + val.id + '">'
        res += '</a>'
        res += '<div id="new_content">'
        res += '<div id="n_tit" act_id="' + val.id + '">'
        res += '<a href="activity.html?act_id=' + val.id + '">' + val.title
        res += '</a></div>'
        res += '<div id="n_cont" act_id="' + val.id + '">'
        res += '<a href="activity.html?act_id=' + val.id + '"><p>' + val.content + '</p>'
        res += '</a></div>'
        res += '<div id="n_lt">'
        res += '<div id="n_lab">' + val.label + '</div>'
        res += '<div id="n_time">' + val.date + '</div>'
        res += '</div></div></div>'
    })
    return res
}

// 请求历史活动数据
function request_data({state, cond = '1'}) {
    console(state)
    var mes = localStorage["history" + tags + cond]
    if (mes) {
        mes = JSON.parse(mes)
        var pagea = JSON.parse(localStorage["historypage" + tags])
        console(pagea)
        $('#b2_l2').html(makeresult(mes))
        getpage(pagea[0], pagea[1])
    } else {
        $.ajax({
            type: 'GET',
            contentType: 'application/json',
            url: SER_URL + 'active/' + state + '/' + cond + '?tag=' + tag,
            // url: SER_URL + 'active/' + state + '/' + cond,
            success: function (response) {
                if (response.code === 200) {
                    var data = response.data
                    var res = makeresult(data)
                    $('#b2_l2').html(res)
                    var pagearr = response.page
                    getpage(pagearr[0], pagearr[1])
                    if (state === 'history') {
                        localStorage['history' + tags + cond] = JSON.stringify(data)
                        localStorage['historypage' + tags] = JSON.stringify(pagearr)
                    }
                }
                if (response.code === 201) {
                    $('#b2_l2').html('')
                    getpage(1, 1)
                }
            }
        })
    }
}


// 历史活动点击事件
$('#z_his_act').on('click', function () {
    act_nh = 'history'
    request_data({state: 'history'})
})


// 页码点击事件
$('#l_num>#ul').on('click', '.page', function () {

    var page = $(this).text()
    var page_now = $('#page_now').text()
    if (page === '上一页') {
        page = Number(page_now) - 1
    }
    if (page === '下一页') {
        page = Number(page_now) + 1
    }
    if (page == page_now) {
        alert('您已经在当前页面')
        return
    }
    if (act_nh === 'history') {
        request_data({state: act_nh, cond: page})
    }
    if (act_nh === 'new') {
        ws.close()
        webrequestpage(page)
    }
})



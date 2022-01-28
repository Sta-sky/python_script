function conmmniuty_index(page) {
    act_nh = 'new'
// 页面加载初始化请求第一页
    if (typeof WebSocket != 'undefined') {
            console.log("您的浏览器支持Websocket通信协议")
        // 创建websockter对象
        ws = new WebSocket(WEBSOCKET_URL + 'community/index/' + page + '?tag=' + tag)

        // 开始通信时的处理
        ws.onopen = function () {
            // 最新活动点击事件
            $('#z_new_act').on('click', function () {
                act_nh = 'new'
                ws.close()
                conmmniuty('1')
            })
        }

        ws.onmessage = function (mes) {

            // console.log(JSON.parse(mes.data).data)
            // 将数据转换成JSON格式
            var respon = JSON.parse(mes.data)
            if (respon.code === 200) {
                var message = respon.data
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
                var pagearr = JSON.parse(mes.data).page
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
conmmniuty_index('1')
//   ============
// alert('Active_user展示')
//当载入页面时，渲染活跃达人信息（从前100随机取8位）
$.ajax({
    type: 'get',
    contentType: 'application/json',
    url: SER_URL + 'v1/activitys/actvuser2',
    success: function (response) {
        var data = response.data
        if (response.code == 200) {
            var html = ''
            for (var i = 0; i < data.length; i++) {
                user_info = data[i]
                // console.log(user_info.nickname)
                // alert('Ajax 渲染了')
                html += '<div class="actv_user">'
                html += '<a href="user_info.html?id='+user_info.user_id+'"><img src=" ' +  IMG_URL + user_info.hd_pic + '" alt="" class="hd_pic"></a>'
                html += '<div class="_user">'
                html += '<a href="user_info.html?id=' + user_info.user_id+'" class="nickname"><h3>' + user_info.nickname + '</h3></a>'
                // html += '<h3 class="nickname">' + user_info.nickname + '</h3>'
                if (user_info.gender == '男') {
                    html += '<img src="../static/images/icon/boy.png" alt="" class="gender"></div>'
                } else{
                    html += '<img src="../static/images/icon/girl.png" alt="" class="gender"></div>'
                };
                html += '<p class="sign_words">' + user_info.sign_words + '</p>'
                html += '<div class="us_atv">'
                html += '<span class="sponsor">发起:' + user_info.sponsor_num+ '</span>'
                html += '<span>|</span>'
                html += '<span class="participate">参与:' + user_info.participate_num + '</span></div>'
                html += '<div id="tags"><ul class="us_tag">'
                var tags = user_info.tags
                //console.log(tags)
                for (var j = 0; j < tags.length; j++) {
                    html += '<li>' + tags[j] + '</li>'
                }
                html += '</ul></div></div>'
            }
            $('#b2_actv_user').html(html)
        }
    },
    error: function (err) {
        //console.log(333333333333)
        console.log(err)
    }
})

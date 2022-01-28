var article_id = GetUrlString('act_id');
token = window.localStorage.getItem('user_token');

// alert(article_id)
$.ajax({
    type: "get",
    dataType: 'json',
    headers: {'Authorization': token},
    url: SER_URL + 'v1/activitys/article_info?article_id=' + article_id,
    contentType: 'application/json;charset=UTF-8',
    success: function (response) {
        if (response.code == 200) {
            var articleData = response.data

            var html = ''
            html += '<div id="top"><p id="title">'+articleData.subject+'</p></div>'
            html += '<div id="num"><div class="updated_time">'+ articleData.updated_time + '</div>'
            html += '<div class="click_nums">浏览数:'+ articleData.click_nums + '</div></div>'
            html += '<hr>'
            html += '<div id="img"><img src="' +IMG_URL+ articleData.act_img + '" alt="" class="act_img" width="600px" height="320px"></div>'
            html += '<div id="paragraph">'
            for(var i=0;i<articleData.content.length;i++){
                html += '<p class="p">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + articleData.content[i] + '</p><br>'
            }
            html += '</div>'
            $('#art_info').html(html)
        } else if(response.code == 10003) {
            alert(response.message)
        } else {
            alert('未知错误')
        }
    },
    error: function (err) {
        console.log(err)
    }
})

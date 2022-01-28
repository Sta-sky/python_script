// 从后端传回的数据
// 渲染函数
var i = 0;
officialData = null;
function adminArticle() {
    $.ajax({
        type: 'get',
        contentType: 'application/json',
        url: SER_URL + 'v1/activitys/article',
        success: function (response) {
            if (response.code === 200) {
                var articleData = response.data
                var i = 0;
                var html = ''
                html += '<div class="article">'
                html += '<span id="il">&lsaquo;</span>'
                html += '<a href="adminarticle.html?uid=' + articleData[i].user_id + '&act_id=' + articleData[i].article_id + '"><img src="' + OFF_IMG_URL + articleData[i].act_img + '" alt="" class="act_img" width="600px" height="320px"></a>'
                html += '<div class="tip"><p class="p1">热点</p>'
                html += '<a href="adminarticle.html?uid=' + articleData[i].user_id + '&act_id=' + articleData[i].article_id + '"><div class="subject"><h3>' + articleData[i].subject + '</h3></div>'
                html += '<p style="table-layout: fixed" class="content">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + articleData[i].content + '</p></a>'
                html += '<div class="click_nums">浏览数:' + articleData[i].click_nums + '</div>'
                html += '<div class="updated_time">' + articleData[i].updated_time + '</div></div>'
                html += '<span id="ir">&rsaquo;</span>'
                html += '</div>'
                $('#article').html(html)
                officialData = articleData
            } else if (response.code === 10009)
                console.log('官方活动获取失败')
                // alert(response.message)
        },
        error: function (err) {
            console.log(err)
        }
    })
}

// console.log(htmldata)
// 渲染函数
function articleHtml(i) {
    var html = ''
    html += '<div class="article">'
    html += '<a href="adminarticle.html?uid=' + officialData[i].user_id + '&act_id=' + officialData[i].article_id + '"><img src="' + OFF_IMG_URL + officialData[i].act_img + '" alt="" class="act_img" width="600px" height="320px"></a>'
    html += '<div class="tip"><p class="p1">热点</p>'
    html += '<a href="adminarticle.html?uid=' + officialData[i].user_id + '&act_id=' + officialData[i].article_id + '"><div class="subject"><h3>' + officialData[i].subject + '</h3></div>'
    html += '<p style="table-layout: fixed" class="content">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + officialData[i].content + '</p></a>'
    html += '<div class="click_nums">浏览数:' + officialData[i].click_nums + '</div>'
    html += '<div class="updated_time">' + officialData[i].updated_time + '</div></div>'
    html += '</div>'
    $('#article').html(html)
    return html
    // 渲染页面
}

adminArticle()

// 点击左右屏切换
//点击qi切屏
$('#il').on('click', function () {
    // console.log(articleHtml())
    $('#article').fadeOut(500, function () {
        if (i == 0) {
            i = 3;
        } else {
            i--;
        }
        $('#article').html(articleHtml(i)).fadeIn(500);
    })
});
$('#ir').on('click', function () {
    $('#article').fadeOut(500, function () {
        if (i == 3) {
            i = 0;
        } else {
            i++;
        }
        $('#article').html(articleHtml(i)).fadeIn(500);
    })
});

function rollRight() {
    $('#article').fadeOut(500, function () {
        if (i == 3) {
            i = 0;
        } else {
            i++;
        }
        $('#article').html(articleHtml(i)).fadeIn(500);
    })
}

setInterval(rollRight, 6000);

$('#adminArticle').mouseover(function () {
    $('#il', '#ir').css('color', '#ff5c2a')
});
$(document).ready(function () {
    $("#adminArticle").mouseover(function () {
        $('#il', '#ir').css({
            'opacity': '0.8',
            'transform': 'scale(1.1)',
        });
    });
    $("#adminArticle").mouseout(function () {
        $('#il', '#ir').css({
            'color': 'white',
            'opacity': '0.5'
        });
    });
});

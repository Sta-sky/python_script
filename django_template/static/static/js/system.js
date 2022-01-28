//生成指定位数的随机数
function random(l) {
    var _n = "";
    for (var i = 0; i < l; i++) {
        _n += Math.floor(Math.random() * 10)
    }
    return _n;
}
function item(title, imgurl, p1, num) {
    var HTML = '<div class="ccon" data-scroll-reveal="bottom 10px 3 3">'
    HTML += '<div class="cctip">' + title + '</div>'
    HTML += '<div class="ccframe">'
    HTML += '<figure>'
    HTML += '<img width="300" src="' + imgurl + '" alt="">'
    HTML += '</figure>'
    HTML += '<div class="ccright">'
    HTML += '<p>' + p1 + '</p>'
    HTML += '<div class="info">' + num + '已阅读</div>'
    HTML += '</div>'
    HTML += '</div>'
    HTML += '</div>'
    return HTML;
}

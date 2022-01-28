
// 获取数字 最大值+多少个数+字符串是否加0+是否是向上取整
function getRandByParm(max, len, blnz = false, blnt = false) {
    var _arr = [];
    while (_arr.length < len) {
        if (!blnt) {
            var n = Math.floor(Math.random() * max)
        } else {
            var n = Math.ceil(Math.random() * max)
        }
        if (n < max && blnz) {
            n = '0' + n
        }
        var reg = new RegExp(n, 'g');
        if (!reg.test(_arr.toString())) {
            _arr.push(n)
        }
    }
    return _arr
}


// js获取地址栏中的指定参数, 中文也可以
function GetUrlString(name){
    // 获取参数
    var url = window.location.search;
    // 正则筛选地址栏
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    // 匹配目标参数
    var result = url.substr(1).match(reg);
    //返回参数值
    return result ? decodeURIComponent(result[2]) : null;
}

//获取每月的天数
function getMonthDays(year,month) {
    var thisDate = new Date(year, month,0); //当天数为0 js自动处理为上一月的最后一天
    return thisDate.getDate();
}

// 生成页码
function getpage(page, pagenums) {
    res = ''
    var i = page - 4
    if (i <= 0) {
        i = 1
    }
    if (page > 1) {
        res += '<li class="page" id="firstpage">上一页</li>'
    }
    for (var j = i; j <= 10; j++) {
        if (j > pagenums) break
        if (j == page) {
            res += '<li class="page" id="page_now">' + j + '</li>'
            continue
        }
        res += '<li class="page" >' + j + '</li>'
    }
    if (page < pagenums) {
        res += '<li class="page" id="lastpage">下一页</li>'
    }
    $('#l_num>ul').html(res)
}

// 短信发送时间倒计时
function time(name) {
    var step = 59;
    var but_code = name;
    var res = setInterval(function () {
        but_code.css('backgroundColor', "#cccccc");
        but_code.attr('disabled', true);
        but_code.html('重新发送&nbsp;&nbsp;' + step);
        step -= 1;
        if (step <= 0) {
            but_code.removeAttr('disabled');
            but_code.html('点击获取验证码');
            but_code.css('backgroundColor', "#21f6f9");
            clearInterval(res);
        }
    }, 1000)
}

// 邮箱格式判断
function Isemail(email){
    if (email !== '') {
    var reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,3})$/;
    if (!reg.test(email)) {
        return false
  }else {
        return true
        }
    }
}



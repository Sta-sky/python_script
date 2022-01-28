// 静态页面的url

var SER_IP = '127.0.0.1:8000';
var STIC_IP = '127.0.0.1:7000';
// 服务器地址（请求数据）




// websocket服务器地址 上传云 换8001
// var WEBSOCKET_URL = 'ws://' + SERIP + ':8001/';
var WEBSOCKET_URL = 'ws://' + SER_IP + '/';


// 服务器请求地址(请求api)
var SER_URL = 'http://' + SER_IP + '/';
// 静态页面地址(请求网页)
var STIC_URL = 'http://' + STIC_IP + '/templates/';




//   静态图片地址
// 用户头像图片地址(请求图片)
// var IMG_URL = 'http://' + STSIP + '/static/images/user_head/';
var IMG_URL = 'http://' + STIC_IP + '/static/';

// 官方活动图片地址
// var OFF_IMG_URL = 'http://' + STSIP + '/static/images/official/';
var OFF_IMG_URL = 'http://' + STIC_IP + '/static/';

// 活动图片位置
// var ACT_IMG_URL = 'http://' + STSIP + '/static/images/activity/';
var ACT_IMG_URL = 'http://' + STIC_IP + '/static/';



// 地图检索region行政区域,限成都
var REGION = '成都市';
// 百度地图秘钥  文件导入需手动修改src属性的ak参数
var BAIDUSECRETKEY = 'GK8muKdwK0w3So6HW89F8KlHc5BKzdbL';
// 百度地图搜索接口 
var BAIDUURL = 'http://api.map.baidu.com/place/v2/search';
// 静态文件常量
var LOCALLABELLIST = ['二次元', 'IT', '散步', '足球', '游戏', '音乐', '旅游', '跑步', '相亲', '滑雪', '骑行', '登山', '机车', '舞蹈', '动漫']

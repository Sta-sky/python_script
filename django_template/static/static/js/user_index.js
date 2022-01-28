
var user_id = GetUrlString('id');
token = window.localStorage.getItem('user_token');
//console.log(token);
$.ajax({
    type: 'get',
    headers: {'Authorization': token},
    contentType: 'application/json',
    url: SER_URL + 'users/home?id=' + user_id,
    success: function (response) {
        if (response.code == 200) {
            var data = response.data;
            var userInfo = data.user_info
            document.getElementById('img').src =IMG_URL+ userInfo.url;
            var res1 = '';
            res1 += '<span class="nick">' + userInfo.nickname + '</span>';
            res1 += '<span class="credit_">信誉积分:' + userInfo.credit + '</span>';
            res1 += '<span class="level_">LV' + userInfo.level + '</span>';
            res1 += '<a href="user_update.html?id=' + user_id + '" id="personal_data">编辑个人资料</a>';
            $('.user_1').html(res1);

            hidden_display(data.is_self);

            var res2 = '';
            res2 += '<ul><li class="dt"> 动态 ' + userInfo.participat_num + '</li>';
            res2 += '<li class="fans">粉丝 ' + userInfo.likes + '</li>';
            res2 += '<li class="gz">关注 ' + userInfo.likes + '</li>';
            res2 += '<li class="dl">登录 ' + userInfo.logins_days + '</li>';
            res2 += '<li class="fq">发起 ' + userInfo.sponson_num + '</li>';
            res2 += '<li class="cy">参与 ' + userInfo.participat_num + '</li></ul>';
            $('.user_2').html(res2);

            var res3 = '';
            var interest = '';
            res3 += '<span class="s1">介绍 : ' + userInfo.introduction + '</span>';
            for (var m = 0; m < userInfo.interest.length; m++) {
                interest += userInfo.interest[m]
            }
            res3 += '<span>爱好 : ' + interest + '</span>';

            res3 += '<span>性别 : ' + userInfo.gender + '</span>';
            res3 += '<span>生日 : ' + userInfo.birth + '</span>';
            res3 += '<span>城市 : ' + userInfo.city + '</span>';
            $('.user_3').html(res3);

            var res4 = '<h2>发起的活动</h2>';
            var createAct = data.create_act_info
            if (createAct.length === 0) {
                res4 += '<div class="no_active">你还没有创建任何活动哦!快点行动起来!!!</div>';
                $('#tz_l').html(res4);
            } else {
                for (var i = 0; i < createAct.length; i++) {
                    res4 += '<div class="tz_l">';
                    res4 += '<ul>';
                    res4 += '<li class="l1">[ <a class="label" href=label.html?sub=' + encodeURI(encodeURI(createAct[i].tag)) + '>' + createAct[i].tag + '</a> ] ' + '<a class="title" href="activity.html?act_id=' + createAct[i].act_id + '">' + createAct[i].subject + '</a></li>';
                    res4 += '<div><span>浏览 :' + createAct[i].click_num + '   发帖 : ' + createAct[i].create_time + '</span>';
                    res4 += '<span>回复 :' + createAct[i].click_num + '   最新评论 : ' + createAct[i].update_time + '</span>';
                    res4 += '</div></ul>';
                    res4 += '</div>';
                }
                $('#tz_l').html(res4);
            }

            var res5 = '<h2>参与的活动</h2>';
            joinAct = data.join_act_info
            if (joinAct.length === 0) {
                res5 += '<div class="no_active">点击主页快快参加活动吧</div>';
                $('#tz_r').html(res5);
            } else {
                for (var j = 0; j < joinAct.length; j++) {
                    res5 += '<div class="tz_r">';
                    res5 += '<ul>';
                    res5 += '<li class="l1">[ <a class="label" href=label.html?sub=' + encodeURI(encodeURI(joinAct[j].tag_p)) + '>' + joinAct[j].tag_p + '</a> ] ' + '<a class="title" href="activity.html?act_id=' + joinAct[j].act_id_p + '">' + joinAct[j].subject_p + '</a></li>';
                    res5 += '<div><span>浏览 :' + joinAct[j].click_num_p + '   发帖 : ' + joinAct[j].create_time_p + '</span>';
                    res5 += '<span>回复 :' + joinAct[j].collection + '   最新评论 : ' + joinAct[j].update_time_p + '</span>';
                    res5 += '</div></ul>';
                    res5 += '</div>';
                }
                $('#tz_r').html(res5);
            }

        } else if (response.code === 10201){
            alert(response.message)
            window.location.href = 'login.html'
        }

    },
});

function hidden_display(data) {
    if (data != 'yes') document.getElementById('personal_data').style.display = 'none';
}
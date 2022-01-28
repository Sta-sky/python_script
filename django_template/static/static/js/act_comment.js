var act_id = GetUrlString('act_id');
var data = {'act_id': act_id};
var token = window.localStorage.getItem('user_token');


// ==============留言开始===================
// 留言按钮
$('#send').on('click', function () {
    // alert('此功能暂未开放')
    // return
   var comment_text = $('#ly').val();
   var data={'comment_text':comment_text};
//    console.log(comment_text);
//    console.log(act_id)
   $.ajax({
    //    data: comment_text,
       type: 'post',
       dataType: 'json',
       headers: {'Authorization': token},
       url: SER_URL + 'v1/comment/act?act_id=' + act_id,
       contentType: 'application/json;charset=UTF-8',
       data: JSON.stringify(data),
       success: function (response) {
           if (response.code == 201) {
               alert('评论成功');
               window.location.reload(); 
           }else{
               alert(response.data)
           }
       },
       error: function (err) {
        console.log('网页渲染错误')
        console.log(err)
    }
   })
});
// ==============留言结束===================

// ==============回复开始===================
// 点击回复，弹出回复下拉框
//页面加载完毕后开始执行的事件
// $(function(){
$("#comment-all").on('click','.review-btn',function(){
    var review_id=$(this).attr('review_id');
    var re_user_id=$(this).attr('re_user_id');
    window.re_user_id=re_user_id;
    window.review_id=review_id;
    $(".review-textarea").remove();
    $(this).parent().append("<div class='review-textarea'><textarea class='re-text' name='review_text' cols='50' rows='2'></textarea><br/><input class='re-submit-btn' type='submit' value='回复' /></div>");
});


$("#comment-all").on('click','.re-submit-btn',function(){
    // var review_id=$(this).attr('review_id');
    var comment_text=$('.re-text').val();
    // alert(comment_text);
    // alert(review_id);
    var data={
        'act_id': act_id,
        're_user_id':re_user_id,
        'review_id':review_id,
        'comment_text':comment_text,
    };
//    console.log(comment_text);
//    console.log(act_id)
   $.ajax({
    //    data: comment_text,
       type: 'post',
       dataType: 'json',
       headers: {'Authorization': token},
       url: SER_URL + 'v1/comment/act?act_id=' + act_id,
       contentType: 'application/json;charset=UTF-8',
       data: JSON.stringify(data),
       success: function (response) {
           if (response.code == 201) {
            //    console.log(222222222222)
            // 简单起见，暂时刷新当前页面
               alert('回复成功');
               window.location.reload(); 
           }else{
               alert(response.data);
               window.location.reload(); 
           }
       },
       error: function (err) {
        console.log('网页渲染错误')
        console.log(err)
    }
   })
});

// ==============回复结束==================



// get请求时，后端传回所有评论信息
$.ajax({
    type:'GET',
    // http://127.0.0.1:8000/v1/comment/act?actvid=xx&uid=xx
    url:SER_URL+'v1/comment/act?act_id=' + act_id,
    dataType:'json',
    contentType:'application/json',
    // data:JSON.stringify(data),
    success:function(response){
        if(response.code==200){
            console.log('get请求已经发出')
            var data=response.data;
            var html='';
            html+='<ul class="cmt-list">';
            for(var i=0;i<data.length;i++){
                var cmt=data[i]
                html+='<li><div class="cmt">';
                html+='<div class="cmt-nickname">';
                html+='<a href="user_info.html?id=' + cmt.user_id+' class="nickname"><p class="nickname">['+cmt.nickname+']</p></a>';
                html+='<p class="cmt-time">'+cmt.comment_time+'</p></div>';
                html+='<div class="cmt-text">&nbsp;&nbsp;&nbsp;&nbsp;'+cmt.comment_text;
                html+='<a href="javascript:;" review_id="'+cmt.id+'" re_user_id="'+cmt.user_id+'" class="review-btn">回复</a></div></div>';
                html+='<div class="review-all"><ul class="review-list">';
                var reviews=cmt.review
                // console.log(666666666666666)
                // console.log(reviews)
                for(var j=0;j<reviews.length;j++){
                    rev=reviews[j]
                    html+='<li><div class="review"><div class="nickname">';
                    html+='<a href="user_info.html?id=' + rev.a_user_id+' class="nickname"><p class="a-nickname">['+rev.a_nickname+']</p></a>';
                    html+='<p style="color: rgb(0, 0, 0);font-size: 10px;">--></p>';
                    html+='<a href="user_info.html?id=' + rev.b_user_id+' class="nickname"><p class="b-nickname">['+rev.b_nickname+']</p></a></div>';
                    html+='<div class="review-time">'+rev.review_time+'</div>';
                    html+='<div class="review-text">&nbsp;&nbsp;&nbsp;&nbsp;'+rev.review_text;
                    html+='<a href="javascript:;" review_id="'+rev.id+'" re_user_id="'+rev.a_user_id+'" class="review-btn">回复</a></div>';
                    html+='</div></li>';
                }
                html+='</ul>';
            }
            html+='</ul>';
            $('#comment-all').html(html);
        }
    },
    error: function (err) {
        console.log('网页渲染错误')
        console.log(err)
    }
});


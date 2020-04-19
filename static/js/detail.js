window.onload=function (data) {
    // $.ajax({
    //     url:'/searchComment' + '?id=' + '1',
    //
    // })
    console.log(8)
};

var COMMON_FUNCTION = {
    randomString: function(lens) {
    　　lens = lens || 32;
    　　var $chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678';    /****默认去掉了容易混淆的字符oOLl,9gq,Vv,Uu,I1****/
    　　var maxPos = $chars.length;
    　　var pwd = '';
    　　for (i = 0; i < lens; i++) {
    　　　　pwd += $chars.charAt(Math.floor(Math.random() * maxPos));
    　　}
　　  return pwd
    }
}

function comment() {
    var content = document.getElementById('cont').value;
    var arid = $('.news_title').attr('arid');
    var name = COMMON_FUNCTION.randomString(8);
    console.log(content);
    console.log(name);
    var token = Cookies.get('csrftoken');
        // var token = $("#searchform").val();
        var heade = {"X-CSRFTOKEN": token};
    $.ajax({
        url:'/addComment',
        type:'POST',
        dataType:'json',
        headers:heade,
        data:{'reply_name': name, 'reply_content': content, 'article_id': arid},
        async: true,
        success:function (response) {
            document.getElementById('cont').value = '';
            location.reload();
        },
        error:function (response) {
            console.log('请求失败')
        }
    })
}

function searchComment() {

    $.ajax({
        url:'/searchComment?',
        type:'GET',
        dataType:'json',
        data:{'reply_name':name, 'reply_content': content},
        async: true,
        success:function (response) {
            $('#cont').innerText = '';
            searchComment();
        },
        error:function (response) {
            console.log('请求失败')
        }
    })
}

function makeRequest(){
    var arid = $('.news_title').attr('arid');
    $.get('/addLike?article_id=' + arid, function (data, status) {
        alert(111)
    })
    makeRequest('/addLike?article_id={{ data.content_info.article_id }}','GET');
}

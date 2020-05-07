
comment_submit =  function comment() {
    var content = document.getElementById('cont').value;
    var arid = $('.news_title').attr('arid');
    console.log(content);
    var token = Cookies.get('csrftoken');
        // var token = $("#searchform").val();
    var heade = {"X-CSRFTOKEN": token};
    $.ajax({
        url:'/addComment',
        type:'POST',
        dataType:'json',
        headers:heade,
        data:{'reply_content': content, 'article_id': arid},
        async: true,
        success:function (response) {
            alert(response.code);
            if (response.code == 200){
                document.getElementById('cont').value = '';
                location.reload();
            }
            if (response.code==301){
                alert(response.code);
                window.location.href = '/login'
            }
        },
        error:function (response) {
            alert(response.code);
            console.log('请求失败')
        }
    })
}

function js_alert(){

//弹出窗口的地址

var url="./static/0000";

//经过设置后的弹出窗口
    <!--
    window.open(url, "newwindow" , "height=100, width=400, top=0, left=0, toolbar=no, menubar=no, scrollbars=no, resizable=no,location=no, status=no")&nbsp;
        -->

// var name="";
//
// var iWidth=500;
//
// var iHeight=500;
//
// var iTop=(window.screen.availHeight-30-iHeight)/2;
//
// var iLeft=(window.screen.availWidth-10-iHeight)/2;
//
// //跳转
//
// window.open(url);


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

// $('#addLikes').on('click', function(event){
//     alert(2222)
//     event.preventDefault();  // 使a 标签自带的方法失效
//     var arid = $('.news_title').attr('arid');
//     console.log('arid');
//     alert(arid)
//     $.ajax({
//         url: '/addLike',
//         method:'POST',
//         dataType: 'json',
//         data:{'article_id': arid},
//         success:function (response) {
//             window.onload()
//         },
//         error:function () {
//             console.log('点赞失败')
//         }
//     });

// })

$('.diggit').onclick = function () {
    alert(12)
}



addLike = function () {
     var arid = $('.news_title').attr('arid');
console.log('arid');
var token = Cookies.get('csrftoken');
    // var token = $("#searchform").val();
    var heade = {"X-CSRFTOKEN": token};
$.ajax({
    url: '/addLike',
    method:'POST',
    dataType: 'json',
    headers: heade,
    data:{'article_id': arid},
    success:function (response) {
        if (response.code==200){
            location.reload()
        }
        else {
            window.location.href = '/login'
        }
    },
    error:function () {
        console.log('点赞失败')
    }
});
}
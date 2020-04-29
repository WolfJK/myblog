function searchRecommend() {
    $.ajax({
        url: '/searchRecommend',
            type: 'GET',
            // headers: heade,
            dataType: "json",
            async: true,
            success : function(response) {
                $('.tuijian').append(response.data)
            },
            error:function (response) {
                console.log('请求失败,请重新访问')
            }
    })
}


var ARTICLES = {
    data: {
        field: 'create_time',
        sort: 'desc',
        page: 1
    },
    searchArticles: function(page){
        _data = {'page':page, 'keyboard':$('#keyboard').val()}

        var token = Cookies.get('csrftoken');
        // var token = $("#searchform").val();
        var heade = {"X-CSRFTOKEN": token};
        $.ajax({
            url: '/searchArticles',
            data: _data,
            type: 'POST',
            headers: heade,
            dataType: "json",
            async: true,
            success : function(response) {
                // $('#a_title').innerText = 'sssd'
                // alert(response.data);
                $('.r_con').empty();
                $('.pagelist').empty();
                $('.r_con').append(response.data);
                $('.pagelist').append(response.page_data);
                console.log('success')
            },
            error:function (response) {
                console.log('请求失败,请重新访问');
                alert(3)
            }

        });
    }
};

$(function(){
    ARTICLES.searchArticles(1);
});
$(document).on('click', '.pageginator', function(){
    var p = $(this).attr('page');
    ARTICLES.searchArticles(p);
});
window.onload=searchRecommend();

// $(document).on('click', '.input_submit', function () {
//     alert(222);
//     var page = 1;
//     ARTICLES.searchArticles(page);
// });

function comment() {
    alert(55);
    $.ajax({
        url:'',
    })
}

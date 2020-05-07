var base_url = 'http://127.0.0.1:8080/';


var RegistLogin = {

    register: function(page) {
        var token = Cookies.get('csrftoken');
        // var token = $("#searchform").val();
        var heade = {"X-CSRFTOKEN": token};
        var radio = document.getElementsByClassName("userGender00");

        for (i = 0; i < radio.length; i++) {
            if (radio[i].checked) {
                var gender = radio[i].value
            }
        }
        console.log(gender);
        var username = $('#username').val();
        var password = $('#userPassword').val();
        $.ajax({
            url: '/register',
            method: 'post',
            data: {
                username: username,
                password: password,
                email: $('#userEmail').val(),
                confirm: $('#userRePassword').val(),
                tel: $('#userPhone').val(),
                gender: gender
            },
            headers: heade,
            success: function (data) {
                console.log(data.msg);
                if (data.code == 1) {
                    // $('.error_msg').empty();
                    // $('.error_msg').innerHTML = data.msg
                    $('.error_msg').text(data.msg)
                }
                if (data.code == 0) {
                    window.location.href = '/login'
                }
            },
            error: function (msg) {
                console.log('注册失败')
            }

        })
    },

    login: function () {
        var token = Cookies.get('csrftoken');
        // var token = $("#searchform").val();
        var heade = {"X-CSRFTOKEN": token};

        var username = $('#username').val();
        var password = $('#userPassword').val();
        $.ajax({
            url: '/login',
            method: 'post',
            data: {
                username: username,
                password: password
            },
            headers: heade,
            success: function (data) {
                console.log(data.msg);
                if (data.code == 1) {
                    $('.error_msg').text(data.msg)
                }
                if (data.code == 0) {
                    window.location.href = '/index';
                    $('#info').text(data.name)
                }
            },
            error: function (msg) {
                console.log('登录失败')
            }

        })
    }
}



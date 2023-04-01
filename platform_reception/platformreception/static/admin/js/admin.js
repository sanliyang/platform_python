function submit_msg() {
    let csrftoken = $("#admin_csrf").val();
    let username = $("#username").val();
    let password = window.btoa($("#password").val());
    $.ajax({
        url: "/admin/check",
        type: "POST",
        headers: {"X-CSRFToken": csrftoken},
        data: {
            username: username,
            password: password
        },
        success: function () {
            alert(this.headers.Cookies)
            window.location = "/admin/control"
        },
        error: function () {
            alert("登录失败")
        }
    });
}

function redirct_regist() {
}

function mouse_over_login(obj) {
    obj.style.backgroundColor = "aqua";
}

function mouse_leave(obj) {
    obj.style.backgroundColor = "aquamarine";
}

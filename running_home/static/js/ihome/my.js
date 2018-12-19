function logout() {

    $.get("/api/logout", function(data){
        if (0 == data.errcode) {
            location.href = "/";
        }
    })
}

$(document).ready(function(){
    $.get("/api/profile/auth", function(data){
        if ("4101" == data.errcode) {
            location.href = "/login.html";
        } else if ("0" == data.errcode) {
            if ("" == data.data.real_name || "" == data.data.id_card || null == data.data.real_name || null == data.data.id_card) {
               $(".menu-text").children().siblings().eq(2).hide()
               $(".menu-text").children().siblings().eq(3).hide()
                return;
            }

        }
    });

    $.get("/api/profile", function(data) {
        if ("4101" == data.errcode) {
            location.href = "/login.html";
        }
        else if ("0" == data.errcode) {
            console.log(data.data)
            $("#user-name").html(data.data.name);
            $("#user-mobile").html(data.data.mobile);

            $("#user-qqnum").html(data.data.qqnum);
            $("#user-telephone").html(data.data.telephone);
            if (data.data.avatar) {
                $("#user-avatar").attr("src", data.data.avatar);
            }
        }
    }, "json");
})
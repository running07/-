$(function(){

        $(".name_input").blur(function(){
           var len = $(this).val().length;
	        if(len<0){
	             $('.user_error').html('用户名不能为空').show()
	            }
        });


        $('.pass_input').blur(function() {
		   var len = $(this).val().length;
                if(len<8||len>20)
                {
                    $('.pwd_error').html('密码最少8位，最长20位')
                    $('.pwd_error').show();
                }
	    })

        if({{ name_error }}==1){
            $('.user_error').html('用户名不存在').show()
            }
        else{
            if({{ pwd_error }}==1){
                    $('.pwd_error').html('密码错误').show()
                }
            }


})
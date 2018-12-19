function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){
    $('.slide .icon li').not('.up,.down').mouseenter(function(){
		$('.slide .info').addClass('hover');
		$('.slide .info li').hide();
		$('.slide .info li.'+$(this).attr('class')).show();//.slide .info li.qq
	});
	$('.slide').mouseleave(function(){
		$('.slide .info').removeClass('hover');
	});

	$('#btn').click(function(){
		$('.slide').toggle();
		if($(this).hasClass('index_cy')){
			$(this).removeClass('index_cy');
			$(this).addClass('index_cy2');
		}else{
			$(this).removeClass('index_cy2');
			$(this).addClass('index_cy');
		}

	});



    var house_id = decodeQuery()["id"];
    console.log(house_id)
    $.get("/api/house/info?house_id="+house_id, function (data) {
        console.log('haha')
        console.log(data)
        if ("0" == data.errcode) {
            $(".swiper-container").html(template("house-image-tmpl", {"img_urls":data.data.images, "price":data.data.price}));

            $(".detail-con").html(template("house-detail-tmpl", {"house":data.data}));
            console.log($(".qq p a").text())
            console.log(data.data.qqhref)
            $(".qq p a").attr("href",data.data.qqhref)
            $(".tel p em").siblings().eq(1).text(data.data.telephone)
            $(".tel p em").siblings().eq(4).text(data.data.qqnum)

            var mySwiper = new Swiper ('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationType: 'fraction'
            })
            // data.user_id为访问页面用户,data.data.user_id为房东
            if (data.user_id != data.data.user_id) {
                $(".book-house").attr("href", "/booking.html?hid="+house_id);
                $(".book-house").show();
            }
        }
    },"json")
})
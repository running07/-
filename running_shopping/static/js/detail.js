function add(){
		
		var num=parseInt($('.num_show').val())
		num+=1
		$('.num_show').val(num)
		$('.num_show').blur()
	}


function reduce(){
	
	var num=parseInt($('.num_show').val())
	if(num>1){
		num-=1
		$('.num_show').val(num)
		$('.num_show').blur()
	}
	
}


//加入购物车
//function add_cart(gid){
//	
//	
//}


//立即购买
function detail_order(gid){
	var num=$('.num_show').val()
	
	$.get('/order/detail_order/',function(dic){
		window.location.href="/order?gid="+gid+"&num="+num
//		document.cookie = "orderids" + "=" + dic.cid + ";path=/;"
		
		
	})
}


	
$(function(){
	$('.num_show').blur(function(){
		number=$('.num_show').val()
		price=parseFloat($('.show_pirze em').text())
		re=/^[1-9][0-9]*$/
		if(re.test(number)){
			number=parseInt(number)
			total=number*price
			$('.total em').text(total.toFixed(2)+'元')
		}
		else{
			price=($('.show_pirze em').text())
			$('.num_show').val('1')
			$('.total em').text(price+'元')
		}
		
	})
		
	
	$('#comment').click(function(){
		$(this).attr('class','active')
		$('#info').attr('class','')
		$('.tab_content').hide()
		$('.discuss').show()
	})
	$('#info').click(function(){
		$(this).attr('class','active')
		$('#comment').attr('class','')
		$('.discuss').hide()
		$('.tab_content').show()
	})
	
	
//	if(!window.location.hash) {
//window.location.hash = 'here';
//}
//	$('.discuss').attr('name','here')
	url=window.location.href
	console.log(url)
	if(url.indexOf('pag')!=-1){
		$('#comment').attr('class','active')
		$('#info').attr('class','')
		$('.tab_content').hide()
		$('.discuss').show()
		window.location.hash = 'jump';
//		$('body,html').animate({scrollTop: $('#comment').offset().top}, 300);
	}
	

	
	
	
	
	
	
//	$('#like').click(function(){
//		console.log('haha')
//		num=$(this).children('b').text()
//		console.log(num,'haha')
////		num+=1
////		console.log(num)
////		$(this).text(num)
//	})
	
	//	#用户名字
//	$.each($('.discusslist'), function() {
//		username=$('#username').text()
//		username=username.slice(0,4)+'****'
//		console.log(username)
//		$('#username').text(username)
//		
//	});

//	
	
	$('.disdate').each(function(){
		
		username=$(this).children(":first").text()
		
		console.log(username)
		
		username=username.slice(0,4)+'****'
		console.log(username)
		$(this).children(":first").text(username)
		
	})
	
	
	
	//查看不同评论
	$('.discusstab a').click(function(){
	console.log('click  a')
		
		$(this).prevAll().attr('class','')
		$(this).nextAll().attr('class','')
		$(this).attr('class','current')
	
	})
	
	
	
	
})

//加入购物车
function add_cart(gid){
	var num=$('.num_show').val()
	if($('.login_btn').text().indexOf('登录')>=0){
		alert('请先登录后购买')
		location.href='/user/login';
		return
	}
//		console.log(goods.id)
	$.get('/cart/addcart'+gid+'_'+num+'/',function(dic){
	
		console.log(gid,num)
		location.href='/detail_'+gid;
		return
	})
	
	

	
	
	
}


function addlike(cid){
	likenum=parseInt($('#like'+cid).text())
	console.log(cid,likenum)
	
	$.get('/addlike?cid='+cid,function(){
		$('#like'+cid).text(likenum+1)
	})
	
}
function adddislike(cid){
	dislikenum=parseInt($('#dislike'+cid).text())
	console.log(cid,dislikenum)
	
	$.get('/adddislike?cid='+cid,function(){
		$('#dislike'+cid).text(dislikenum+1)
	})
	
}



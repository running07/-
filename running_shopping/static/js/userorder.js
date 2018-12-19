function submit(oid,pag){
	if(confirm('请确认？')){
		$.get('/user/ordersubmit?oid='+oid,function(dic){
			console.log('statu',dic.statu)
			window.location.href='/user/order/?statu='+dic.statu;
			return
		
		
		})
	}
}



function comment_textarea(oid){
	$.get('/user/addcomment?oid='+oid,function(dic){
		$('#content').children().detach()
//		$('#form_comment').append('{% csrf_token %}')
		$.each(dic.data, function(index,item) {
			console.log(item.id,item.title)
			textarea_name=item.id
			$('img').attr('value',1)
			$('#content').append('<div  class="form-group" id='+item+'>  <input style="display: none;" type="text" name="gid'+item.id+'"value="5">   <label style="width:50% ">'+item.title+'</label> <label>评分：</label><img id="1" width="20px" name="img1" src="/static/img/star1.jpg"/><img id="2" width="20px" name="img" src="/static/img/star1.jpg"/><img id="3" width="20px" name="img" src="/static/img/star1.jpg"/><img id="4" width="20px" name="img" src="/static/img/star1.jpg"/><img id="5" width="20px" name="img" src="/static/img/star1.jpg"/> ')
//			$('#content').append(' <label>评价</label><img id="1" width="20px" name="img" src="/static/img/star1.jpg"/><img id="2" width="20px" name="img" src="/static/img/star1.jpg"/><img id="3" width="20px" name="img" src="/static/img/star1.jpg"/><img id="4" width="20px" name="img" src="/static/img/star1.jpg"/><img id="5" width="20px" name="img" src="/static/img/star1.jpg"/>')
			$('#content').append('<textarea class="form-control" name='+item.id+' rows="3"></textarea></div> <br>')
			$('img').attr('value',1)
//			$('#content').append('<input  type="text" name="gid'+item.id+'"value="5">')
			imgclick(item.id)
			textarea_validate(textarea_name)
			
//			$('#form_comment').bootstrapValidator('addField',item.id,{
//				validators :{
//					notEmpty:{
//						message:'评论内容不能为空'
//					}
//				}
//			});
		});
		$('#content').append('<div class="text-center"><button class="btn btn-primary" type="submit">提交</button>&nbsp;&nbsp;&nbsp;<button class="btn btn-danger" data-dismiss="modal">取消</button></div>')
		$('#content').append('<input style="display: none;" type="text" name="oid" value='+oid+'>')
		 
		 
//		 <label>评价</label><img id="1" width="20px" name="img" src="/static/img/star1.jpg"/><img id="2" width="20px" name="img" src="/static/img/star1.jpg"/><img id="3" width="20px" name="img" src="/static/img/star1.jpg"/><img id="4" width="20px" name="img" src="/static/img/star1.jpg"/><img id="5" width="20px" name="img" src="/static/img/star1.jpg"/>
		 
		 
		 
		 
		 
		 
		 
		 
	})
}

function delete_order(oid){
	if(confirm('请确认！')){
		$.get('/user/delete_order?oid='+oid,function(){
			window.location.href='/user/order?statu=3';
			return
		})
	}
}

function imgclick(){
	$('img').click(function(){
		console.log('click')
		num=$(this).attr('value')
		id=parseInt($(this).attr('id'))
		console.log(id,num)
		if(num==1){
//			$(this).nextAll(function(){
//				cid=parseInt($(this).attr('id'))
//				if (cid>=id){
//					$(this).attr('src','/static/img/star0.jpg')
//					$(this).attr('value',0)
//				}
//			})
			$(this).attr('src','/static/img/star0.jpg')
			$(this).attr('value',0)
			$(this).nextAll().attr('src','/static/img/star0.jpg')
			$(this).nextAll().attr('value',0)
			cid=parseInt($(this).attr('id'))
			console.log('评分：',cid)
			$(this).prevAll('input').val(cid-1)
			console.log($(this).prev('input').val())
					
		}
		
		if(num==0){
			$(this).attr('src','/static/img/star1.jpg')
			$(this).attr('value',1)
			$(this).prevAll().attr('src','/static/img/star1.jpg')
			$(this).prevAll().attr('value',1)
			cid=parseInt($(this).attr('id'))
			$(this).prevAll('input').val(cid)
//			$(this).prevAll(function(){
//				cid=parseInt($(this).attr('id'))
//				if (cid<=id){
//					$(this).attr('src','/static/img/star1.jpg')
//					$(this).attr('value',1)
//				}
//			})
					
		}
		})	
	
}


function textarea_validate(textarea_name){
	console.log('validate',textarea_name)
	$('#form_comment').validate({
				rules:{
					textarea_name: {
						required: true,
							minlength: 10,
					},
				}
			})
}




//$(function(){
//	$('img').attr('value',1)
//	num=$('img').attr('value')
//	console.log(num)
//	$('img').click(function(){
//		console.log('click')
//		num=$(this).attr('value')
//		id=parseInt($(this).attr('id'))
//		
//		if(num==1){
//			$.each($('img'),function(){
//				cid=parseInt($(this).attr('id'))
//				if (cid>=id){
//					$(this).attr('src','/static/img/star0.jpg')
//					$(this).attr('value',0)
//				}
//			})
//					
//		}
//		
//		if(num==0){
//			$.each($('img'),function(){
//				cid=parseInt($(this).attr('id'))
//				if (cid<=id){
//					$(this).attr('src','/static/img/star1.jpg')
//					$(this).attr('value',1)
//				}
//			})
//					
//		}
//
//	})	
//	
//})
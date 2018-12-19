//增加商品
function add(id){
		
		var num=parseInt($('#'+id).val())
		num+=1

		$('#'+id).val(num)
		$('#'+id).blur()

	}

//减少商品
function reduce(id){
	
	var num=parseInt($('#'+id).val())
	if(num>1){
		num-=1
		$('#'+id).val(num)
		$('#'+id).blur()

	}
	else{
		alert('商品数量不能小于1！')
	}
	
}

//修改商品总计
$(function(){
	$('.num_show').blur(function(){
		
		id=$(this).attr('id')
		
		number=$(this).val()
		console.log('num->',number,'id->',id)
		price=parseFloat($('#price'+id+' em').text())
		re=/^[1-9][0-9]*$/
		if(re.test(number)){
			number=parseInt(number)
			total=number*price
			$.get('/cart/alter'+id+'_'+number+'/',function(dic){
			
			})
			$('#total'+id).text(total.toFixed(2)+'元')
		}
		else{
			
			$.get('/cart/error'+id+'/',function(dic){
				count=dic.count
				console.log('count->',count)
				$('#'+id).val(count)
			
			})
			alert('商品数量必须是大于0的整数！')

		}
		
		total_money()
		
	})
})


//计算商品总计
function total_money(){
	
	//计算每项商品的总价
	$.get('/cart/item/',function(dic){
		
		money=0
		$.each(dic.data, function(index,pk) {
			price=parseFloat($('#price'+pk+' em').text())
			count=parseInt($('#'+pk).val())
			total=price*count
			if($('#check'+pk).prop('checked')){
				money+=total
			}
			
			$('#total'+pk).text(total.toFixed(2)+'元')
			
		});
		$('.settlements .col03 em').text(money.toFixed(2))
		
	})
	
}


function record(){
	str=''
	$.get('/cart/item/',function(dic){
		$.each(dic.data, function(index,pk) {
			if($('#check'+pk).prop('checked')){
				str=str+pk+','
			}			
		});
		console.log('list->',str)
		document.cookie = "orderids" + "=" + str + ";path=/;"
	})
	
}


//更新数据库
//function alterdata(id,num){
//	$.get('/cart/alter'+id+'_'+num+'/',function(dic){
//			
//		})
//}

function delete_item(id) {
	console.log('haha')
	$.get('/cart/delete_item'+id+'/',function(dic){
		location.href='/cart';
		return
	})
}





$(function(){
	
	//计算每项商品的总价
	total_money()
	record()
	
	
	//计算勾选商品的数量
		count=$(':checked:not(#checkall)').length
		$('.settlements .col03 b').text(count)
		
	//全选，全取消
	$('#checkall').click(function(){
		state=$(this).prop('checked')
		console.log(state)
		$(':checkbox:not(#checkall)').prop('checked',state)
		total_money()
	})
	
	//单选
	$(':checkbox:not(checkall)').click(function(){
		if($(this).prop('checked')){
			if($(':checked:not(#checkall)').length+1==$(':checkbox').length){
				$('#checkall').prop('checked',true)
			}
		}
		else{
			$('#checkall').prop('checked',false)
		}
		//计算勾选商品的数量
		count=$(':checked:not(#checkall)').length
		$('.settlements .col03 b').text(count)
		
		
		total_money()
		record()
	})
	
	
	
	
	
	
	
})

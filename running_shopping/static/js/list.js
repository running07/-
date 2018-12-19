function add_cart(gid){

	
	$.get('/cart/addcart'+gid+'_'+1+'/',function(data){
		console.log(gid)
	})
	
}
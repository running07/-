
	
	function set_default(id){

       
		document.cookie = "address_id" + "=" + id + ";path=/;"
				
	}
	
	function modefysite(id){
		$.get('/user/address'+String(id)+'/',function(data){
			
			
			
			
			$.get('/user/'+data['upro']+'/', function(dic) {
					var city = $('#city')
					$.each(dic.data, function(index, item) {
						city.append('<option value=' + item[0] + '>' + item[1] + '</option>')
					})
					$('#city').val(data['ucity'])
					$.get('/user/'+data['ucity']+'/', function(dic) {
						var disc = $('#disc')
						$.each(dic.data, function(index, item) {
							disc.append('<option value=' + item[0] + '>' + item[1] + '</option>')
						})
						$('#disc').val(data['udisc'])
					})
				})
			
			$("select[class='city']").change(function() {
								$("select[class='disc']").detach()
								console.log('disc-remove')
								city_id = $(this).val()
								if(city_id != -1) {
									$.get('/user/'+city_id + '/', function(dic) {
										$('.address').append('<select class="disc" name="disc_id" ><option value="">请选择市</option></select>')
										var disc = $('.disc')
										$.each(dic.data, function(index, item) {
											disc.append('<option value=' + item[0] + '>' + item[1] + '</option>')
										})																			
										
									})
								}
							})

			
			
			$('#another_name').val(data['another_name'])
			$('#urecipients').val(data['urecipients'])
			$('#pro').val(data['upro'])
			
			
			
			$('#uaddress').val(data['uaddress'])
			$('#upostcode').val(data['upostcode'])
			$('#uaddphone').val(data['uaddphone'])
			$.cookie("modify_id",id)
		})
	}

	

	$(function() {
		
		$(' dd span').each(function(){
			phone=$(this).text()
			console.log(phone)
			phone=phone.slice(0,3)+'****'+phone.slice(7,11)
			console.log(phone)
			$(this).text(phone)
		})
		
		
		
		
		
		$.get('/user/pro/', function(dic) {
			var pro = $('.pro')
			$.each(dic.data, function(index, item) {
				pro.append('<option value=' + item[0] + '>' + item[1] + '</option>')
			})
		})
		$('.pro').change(function() {
			$("select[class='city']").detach()
			$("select[class='disc']").detach()

			pro_id = $(this).val()

			if(pro_id != -1) {
			
				$.get('/user/'+pro_id + '/', function(dic) {
					$('.address').append('<select class="city" name="city_id" ><option value="-1">请选择市</option></select>')
					city = $('.city')

					$.each(dic.data, function(index, item) {
						city.append('<option value=' + item[0] + '>' + item[1] + '</option>')
					})

					$("select[class='city']").change(function() {
						$("select[class='disc']").detach()
						city_id = $(this).val()
						if(city_id != -1) {
							$.get('/user/'+city_id + '/', function(dic) {
								$('.address').append('<select class="disc" name="disc_id" ><option value="">请选择市</option></select>')
								var disc = $('.disc')
								$.each(dic.data, function(index, item) {
									disc.append('<option value=' + item[0] + '>' + item[1] + '</option>')
								})																			
								
							})
						}
					})

				})
			}
		})
				
				
				
				
				
				
				
				
	})
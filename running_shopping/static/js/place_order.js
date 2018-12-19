function submit_order(){
	flag=confirm('请确认是否付款')
	document.cookie = "flag" + "=" + flag + ";path=/;"
	
}

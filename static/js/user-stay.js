setInterval(function() {
	var obj = document.createElement('script');
	obj.src = '/user/stay/'+forum_id+'/';
	document.body.appendChild(obj);
}, 1000*5);

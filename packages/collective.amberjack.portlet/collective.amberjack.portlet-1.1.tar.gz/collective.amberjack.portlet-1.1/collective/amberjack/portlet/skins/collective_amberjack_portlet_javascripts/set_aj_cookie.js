function set_cookie(tours_id){
	if (document.cookie.length > 0) {
		var c_start = document.cookie.indexOf("next_tours_id=");
		if (c_start != -1) {
			var cookie_date = new Date(); // current date & time
			cookie_date.setTime(cookie_date.getTime() - 100);
			document.cookie = "next_tours_id=; path= /; expires=" + cookie_date.toGMTString();
		}
	}
	document.cookie="next_tours_id=" + tours_id + "; path= /;";
}
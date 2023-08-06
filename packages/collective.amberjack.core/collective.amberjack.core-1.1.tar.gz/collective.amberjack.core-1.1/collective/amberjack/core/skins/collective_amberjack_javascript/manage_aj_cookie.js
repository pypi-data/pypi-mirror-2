function manage_cookie(){
	if (document.cookie.length > 0) {
		var c_start = document.cookie.indexOf("next_tours_id=");
		if (c_start != -1) {
			var c_val_start = c_start + "next_tours_id=".length;
			var new_val = document.cookie.substring(c_val_start,document.cookie.length);
			var c_val_end = new_val.indexOf(";");
			if (c_val_end == -1) {
				c_val_end = new_val.length;
			}
			var c_end_first_val = new_val.indexOf("|");
			new_val = new_val.substring(c_end_first_val+1,c_val_end-1);
			var cookie_date = new Date(); // current date & time
			cookie_date.setTime(cookie_date.getTime() - 100);
			document.cookie = "next_tours_id=; path= /; expires=" + cookie_date.toGMTString();
			document.cookie="next_tours_id=" + new_val + "; path= /;";
		}
	}
}
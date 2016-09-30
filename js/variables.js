$(document).ready(function(){
	App = {} ;
  window.App = App ;
	window.make_request = function make_request(data){ url =  window.process_text_url ; return $.post(url, {"text": data}) }
	window.URL = "http://localhost:8000/post_text"

});

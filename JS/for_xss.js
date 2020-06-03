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
var token = xmlDoc.querySelector('#adminForm > input[type=hidden]:nth-child(3)').name;



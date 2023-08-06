var xmlhttp = null;
var shorts = null;
var semaphore = false;

function sliceItem(list, start){
    var copy = [], i;
    
    for (i = start; i < list.length; i++) {
        copy.push(list[i]);
    }
    return copy;
}

function writeShort() {
    var short, values;
    // alert('pause');
    if (xmlhttp != null && xmlhttp.readyState == 4) {
        if (xmlhttp.status == 200) {
           response = xmlhttp.responseXML;

           values = getElementsByClassName('values', document, 'div')[0];
	   
	   short = getElementsByClassName('short', response, 'div')[0];

           values.appendChild(short);
	   values.appendChild(getElementsByClassName('jslink',values,'div')[0]);
	   values.appendChild(getElementsByClassName('rightvalues',values,'div')[0]);

	   shorts = sliceItem(shorts, 1);
	   semaphore = false;
	   uploadshortviews();
        }
    }
   
}

function uploadShort () {

    if (!semaphore) {
        semaphore = true;
	
        xmlhttp = createRequestObject();
        xmlhttp.open('GET', shorts[0].innerHTML+'/shortpage', true);
        xmlhttp.overrideMimeType('text/xml');
        xmlhttp.onreadystatechange = writeShort;
        xmlhttp.send(null);
    }
}

function uploadShortUrls() {
    var response;

    if (xmlhttp != null && xmlhttp.readyState == 4) {
        if (xmlhttp.status == 200) {
	
            response = xmlhttp.responseXML;
	   
	    shorts = response.getElementsByTagName('span');

  	    shorts = sliceItem(shorts, 3);

	    semaphor = false;

	    uploadShort();
	}
    }
}

function getShortUrls(url) {
  semaphor = true;
  xmlhttp = createRequestObject();
  xmlhttp.open('GET', url, true);
  xmlhttp.overrideMimeType('text/xml');
  xmlhttp.onreadystatechange = uploadShortUrls;
  xmlhttp.send(null);
}

function uploadshortviews() {
    var wh, bh, sh,
    elem, url, jslink;

    // window height
    wh = parseInt(window.innerHeight);
    // body height
    bh = parseInt(document.body.offsetHeight);

    // scrollbar height
    sh = (bh / (bh / wh)).toFixed(0);
    // document.body.scrollTop  is the same that window.pageYOffset
    if (window.pageYOffset > (bh - sh * 2)) {
        if (semaphore == false) {
            if (shorts != null) {
               uploadShort();
            } else {
                  jslink = getElementsByClassName('jslink', document, 'div')[0];

                  elem = jslink.getElementsByTagName('a')[0];

                  url = elem.href;

                  getShortUrls(url);
            }
        }
    }
}

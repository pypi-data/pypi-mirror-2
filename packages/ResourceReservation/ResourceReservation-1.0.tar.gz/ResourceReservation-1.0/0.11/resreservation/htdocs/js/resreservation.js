/*- coding: utf-8
 *
 * Copyright (C) 2010 Roberto Longopbardi - seccanj@gmail.com
 *
 * This software is licensed as described in the file COPYING, which
 * you should have received as part of this distribution.
 */

function editResourceReservation(evt) {
    var resDate = evt.target.getAttribute('name');
    
    /* Avoid the first cell, the one with the resource name */
    if (resDate !== 'resourceNameCell') {
        var currAssignee = evt.target.title ? evt.target.title : '';
        var resourceName = evt.target.parentNode.getAttribute('name');

        if (!currAssignee || currAssignee.length == 0 || currAssignee !== currUser) {
            newAssignee = currUser;
            newClass = 'resOwned';
        } else {
            newAssignee = '';
            newClass = '';
        }
        
        changeReservation(evt.target, resourceName, resDate, currAssignee, newAssignee, newClass);
        /* setTimeout('window.location="'+window.location+'"', 500); */
    }
}

function changeReservation(node, resourceName, resDate, currAssignee, newAssignee, newClass) {
    xmlhttp = getXmlHttp();

    var url = baseLocation+'/resreservation?command=assignresource&resourceType='+resourceType+'&resourceName='+resourceName+
        '&resDate='+resDate+'&currAssignee='+currAssignee+'&newAssignee='+newAssignee;
    
    xmlhttp.open("GET", url, false);
    xmlhttp.send(null);
    xmlDoc = xmlhttp.responseXML; 

    node.className = newClass;
    node.title = newAssignee;
}

function addResource() {
    xmlhttp = getXmlHttp();

    var resName = document.getElementById('resName').value;
    if (!resName || resName.length == 0) {
		document.getElementById('errorMsgSpan').innerHTML = 'Devi indicare un nome. Lunghezza da 4 a 30 caratteri.';
    } else {
    	resName = stripLessSpecialChars(resName); 
    	
    	if (resName.length > 30 || resName.length < 4) {
    		document.getElementById('errorMsgSpan').innerHTML = 'Lunghezza da 4 a 30 caratteri.';
    	} else {
            var url = baseLocation+'/resreservation?command=addresource&resourceType='+resourceType+'&resourceName='+resName;
        
            xmlhttp.open("GET", url, false);
            xmlhttp.send(null);
            xmlDoc = xmlhttp.responseXML; 
    
            setTimeout('window.location="'+window.location+'"', 500);
        }
    }
}

function getXmlHttp() {
    if (window.XMLHttpRequest) {
        /* code for IE7+, Firefox, Chrome, Opera, Safari */
        xmlhttp = new XMLHttpRequest();
    } else {
        /* code for IE6, IE5 */
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    
    return xmlhttp;
}

function stripLessSpecialChars(str) {
    result = str.replace(/[;#&\?]/g, '');
    return result;
}

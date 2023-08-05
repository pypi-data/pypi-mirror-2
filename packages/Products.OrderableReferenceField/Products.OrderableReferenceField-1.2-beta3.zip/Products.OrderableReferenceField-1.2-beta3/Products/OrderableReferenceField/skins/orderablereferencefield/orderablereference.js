function oref_top(obj) { /*updated from version 1.2*/
	obj = (typeof obj == "string") ? document.getElementById(obj) : obj;
	if (obj.tagName.toLowerCase() != "select" && obj.length < 2)
		return false;
	var elements = new Array();
	for (var i=0; i<obj.length; i++) {
		if (obj[i].selected) {
			elements[elements.length] = new Array((document.body.innerHTML ? obj[i].innerHTML : obj[i].text), obj[i].value, obj[i].style.color, obj[i].style.backgroundColor, obj[i].className, obj[i].id, obj[i].selected);
		}
	}
	for (i=0; i<obj.length; i++) {
		if (!obj[i].selected) {
			elements[elements.length] = new Array((document.body.innerHTML ? obj[i].innerHTML : obj[i].text), obj[i].value, obj[i].style.color, obj[i].style.backgroundColor, obj[i].className, obj[i].id, obj[i].selected);
		}
	}
	for (i=0; i<obj.length; i++) {
		if (document.body.innerHTML) obj[i].innerHTML = elements[i][0];
		else obj[i].text = elements[i][0];
		obj[i].value = elements[i][1];
		obj[i].style.color = elements[i][2];
		obj[i].style.backgroundColor = elements[i][3];
		obj[i].className = elements[i][4];
		obj[i].id = elements[i][5];
		obj[i].selected = elements[i][6];
	}
}

function oref_bottom(obj) { /*updated from version 1.2*/
	obj = (typeof obj == "string") ? document.getElementById(obj) : obj;
	if (obj.tagName.toLowerCase() != "select" && obj.length < 2)
		return false;
	var elements = new Array();
	for (var i=0; i<obj.length; i++) {
		if (!obj[i].selected) {
			elements[elements.length] = new Array((document.body.innerHTML ? obj[i].innerHTML : obj[i].text), obj[i].value, obj[i].style.color, obj[i].style.backgroundColor, obj[i].className, obj[i].id, obj[i].selected);
		}
	}
	for (i=0; i<obj.length; i++) {
		if (obj[i].selected) {
			elements[elements.length] = new Array((document.body.innerHTML ? obj[i].innerHTML : obj[i].text), obj[i].value, obj[i].style.color, obj[i].style.backgroundColor, obj[i].className, obj[i].id, obj[i].selected);
		}
	}
	for (i=obj.length-1; i>-1; i--) {
		if (document.body.innerHTML) obj[i].innerHTML = elements[i][0];
		else obj[i].text = elements[i][0];
		obj[i].value = elements[i][1];
		obj[i].style.color = elements[i][2];
		obj[i].style.backgroundColor = elements[i][3];
		obj[i].className = elements[i][4];
		obj[i].id = elements[i][5];
		obj[i].selected = elements[i][6];
	}
}

function oref_up(obj) { /*updated from version 1.2*/
	var obj_string = obj;
	obj = (typeof obj == "string") ? document.getElementById(obj) : obj;
	if (obj.tagName.toLowerCase() != "select" && obj.length < 2)
		return false;
	var sel = new Array();
	for (var i=0; i<obj.length; i++) {
		if (obj[i].selected == true) {
			sel[sel.length] = i;
		}
	}
	for (i in sel) {
	    if (sel[i] != 0) {
			if (obj[sel[i]-1]) {
				if (!obj[sel[i]-1].selected) {
				var tmp = new Array((document.body.innerHTML ? obj[sel[i]-1].innerHTML : obj[sel[i]-1].text), obj[sel[i]-1].value, obj[sel[i]-1].style.color, obj[sel[i]-1].style.backgroundColor, obj[sel[i]-1].className, obj[sel[i]-1].id);
				if (document.body.innerHTML) obj[sel[i]-1].innerHTML = obj[sel[i]].innerHTML;
				else obj[sel[i]-1].text = obj[sel[i]].text;
				obj[sel[i]-1].value = obj[sel[i]].value;
				obj[sel[i]-1].style.color = obj[sel[i]].style.color;
				obj[sel[i]-1].style.backgroundColor = obj[sel[i]].style.backgroundColor;
				obj[sel[i]-1].className = obj[sel[i]].className;
				obj[sel[i]-1].id = obj[sel[i]].id;
				if (document.body.innerHTML) obj[sel[i]].innerHTML = tmp[0];
				else obj[sel[i]].text = tmp[0];
				obj[sel[i]].value = tmp[1];
				obj[sel[i]].style.color = tmp[2];
				obj[sel[i]].style.backgroundColor = tmp[3];
				obj[sel[i]].className = tmp[4];
				obj[sel[i]].id = tmp[5];
				obj[sel[i]-1].selected = true;
				obj[sel[i]].selected = false;
				}
			}
		}
	}
	inout_selectAllWords(obj_string);
}

function oref_down(obj) {
	var obj_string = obj;
	obj = (typeof obj == "string") ? document.getElementById(obj) : obj;
	if (obj.tagName.toLowerCase() != "select" && obj.length < 2)
		return false;
	var sel = new Array();
	for (var i=obj.length-1; i>-1; i--) {
		if (obj[i].selected == true) {
			sel[sel.length] = i;
		}
	}
	for (i in sel) {
		if (sel[i] != obj.length-1) {
			if (obj[sel[i]+1]) {
				if (!obj[sel[i]+1].selected) {
					var tmp = new Array((document.body.innerHTML ? obj[sel[i]+1].innerHTML : obj[sel[i]+1].text), obj[sel[i]+1].value, obj[sel[i]+1].style.color, obj[sel[i]+1].style.backgroundColor, obj[sel[i]+1].className, obj[sel[i]+1].id);
					if (document.body.innerHTML) obj[sel[i]+1].innerHTML = obj[sel[i]].innerHTML;
					else obj[sel[i]+1].text = obj[sel[i]].text;
					obj[sel[i]+1].value = obj[sel[i]].value;
					obj[sel[i]+1].style.color = obj[sel[i]].style.color;
					obj[sel[i]+1].style.backgroundColor = obj[sel[i]].style.backgroundColor;
					obj[sel[i]+1].className = obj[sel[i]].className;
					obj[sel[i]+1].id = obj[sel[i]].id;
					if (document.body.innerHTML) obj[sel[i]].innerHTML = tmp[0];
					else obj[sel[i]].text = tmp[0];
					obj[sel[i]].value = tmp[1];
					obj[sel[i]].style.color = tmp[2];
					obj[sel[i]].style.backgroundColor = tmp[3];
					obj[sel[i]].className = tmp[4];
					obj[sel[i]].id = tmp[5];
					obj[sel[i]+1].selected = true;
					obj[sel[i]].selected = false;
				}
			}
		}
	}
	inout_selectAllWords(obj_string);
}


/* from in and out */
function inout_selectAllWords(theList) {
  myList = document.getElementById(theList);
  for (var x=0; x < myList.length; x++) {
    myList[x].selected="selected";
  }
}

function inout_addNewKeyword(toList, newText, newValue) {
  theToList=document.getElementById(toList);
  for (var x=0; x < theToList.length; x++) {
    if (theToList[x].text == newText) {
      return false;
    }
  }
  theLength = theToList.length;
  theToList[theLength] = new Option(newText);
  theToList[theLength].value = newValue;
}

function inout_moveKeywords(fromList,toList,selectThese) {
  theFromList=document.getElementById(fromList);
  for (var x=0; x < theFromList.length; x++) {
    if (theFromList[x].selected) {
      inout_addNewKeyword(toList, theFromList[x].text, theFromList[x].value);
    }
  }
  theToList=document.getElementById(fromList);
  for (var x=theToList.length-1; x >= 0 ; x--) {
    if (theToList[x].selected) {
      theToList[x] = null;
    }
  }
  inout_selectAllWords(selectThese);
}



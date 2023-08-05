function M_getEventTarget(a){return a.srcElement?a.srcElement:a.target}
function M_keyPressCommon(a,b,d){if(a=a?a:event?event:null){var c=M_getEventTarget(a),e=c.nodeName,g,f;if(a.keyCode)f=a.keyCode;else if(a.which)f=a.which;g=String.fromCharCode(f);if(e=="TEXTAREA"||e=="INPUT"){if(typeof d!="undefined")return d(a,c,f,g);return true}if(a.altKey||a.altLeft||a.ctrlKey||a.ctrlLeft||a.metaKey)return true;if(g=="?"||f==(window.event?27:a.DOM_VK_ESCAPE)){if((a=document.getElementById("help"))&&typeof helpDisplayed!="undefined"){if(helpDisplayed||g=="?")helpDisplayed=!helpDisplayed;
a.style.display=helpDisplayed?"":"none"}return false}return b(a,c,f,g)}return true}var M_getWindowHeightGetters_={ieQuirks_:function(a){return a.document.body.clientHeight},ieStandards_:function(a){return a.document.documentElement.clientHeight},dom_:function(a){return a.innerHeight}},M_getScrollTopGetters_={ieQuirks_:function(a){return a.document.body.scrollTop},ieStandards_:function(a){return a.document.documentElement.scrollTop},dom_:function(a){return a.pageYOffset}};
function M_getWindowPropertyByBrowser_(a,b){try{if(!M_isKHTML()&&"compatMode"in a.document&&a.document.compatMode=="CSS1Compat")return b.ieStandards_(a);else if(M_isIE())return b.ieQuirks_(a)}catch(d){}return b.dom_(a)}function M_getWindowHeight(a){return M_getWindowPropertyByBrowser_(a,M_getWindowHeightGetters_)}function M_getScrollTop(a){return M_getWindowPropertyByBrowser_(a,M_getScrollTopGetters_)}
function M_scrollIntoView(a,b,d){var c=M_getPageOffsetTop(b),e=M_getWindowHeight(a);c=c-e/3;e=M_getScrollTop(a);if(d>=0&&e<c||d<=0&&e>c)a.scrollTo(M_getPageOffsetLeft(b),c)}function M_getPageOffsetTop(a){var b=a.offsetTop;if(a.offsetParent!=null)b+=M_getPageOffsetTop(a.offsetParent);return b}function M_getPageOffsetLeft(a){var b=a.offsetLeft;if(a.offsetParent!=null)b+=M_getPageOffsetLeft(a.offsetParent);return b}
function M_isElementVisible(a,b){b=M_getPageOffsetTop(b);var d=M_getWindowHeight(a);a=M_getScrollTop(a);if(b<a||b>a+d)return false;return true};

function JS_inputShortcutHandler(evt, src, code, key) {
   if (code == (window.event ? 27 /* ASCII code for Escape */
                : evt.DOM_VK_ESCAPE)) {
     meine_abbrechen_funktion();
   } else if ((evt.ctrlKey || evt.ctrlLeft) &&
              (key == 's' || code == 19)) {
     meine_speichern_funktion();
   } else {
     return true;
   }
   return false;
 }

/**
 * A click handler common to just about every page, set in global.html.
 * @param {Event} evt The event object that triggered this handler.
 * @return false if the event was handled.
 */
function JS_clickCommon(evt) {
  if (helpDisplayed) {
    var help = document.getElementById("help");
    help.style.display = "none";
    helpDisplayed = false;
    return false;
  }
  return true;
}

 /**
 * Create a new XMLHttpRequest in a cross-browser-compatible way.
 * @return XMLHttpRequest object
 */
function JS_getXMLHttpRequest() {
  try {
    return new XMLHttpRequest();
  } catch (e) { }
  try {
    return new ActiveXObject("Msxml2.XMLHTTP");
  } catch (e) { }
  try {
    return new ActiveXObject("Microsoft.XMLHTTP");
  } catch (e) { }
  return null;
}

/**
 * Finds the element position.
 */
function JS_getElementPosition(obj) {
  var curleft = curtop = 0;
  if (obj.offsetParent) {
    do {
      curleft += obj.offsetLeft;
      curtop += obj.offsetTop;
    } while (obj = obj.offsetParent);
  }
  return [curleft,curtop];
}

/**
 * Position the booking info popup according to the mouse event coordinates
 */
function JS_positionInfoPopup(obj, popupDiv) {
  pos = JS_getElementPosition(obj);
  popupDiv.style.left = pos[0] + "px";
  popupDiv.style.top = pos[1] + 20 + "px";
}

function JS_showInfoPopup(obj, divId, urlPart, urlMapper) {
  var popupDiv = document.getElementById(divId);
  var url = obj.getAttribute("href")
  var index = url.indexOf(urlPart);
  var key = url.substring(index + urlPart.length + 1);

  if (!popupDiv) {
    var popupDiv = document.createElement("div");
    popupDiv.className = "popup";
    popupDiv.id = divId;
    popupDiv.filter = 'alpha(opacity=85)';
    popupDiv.opacity = '0.85';
    popupDiv.innerHTML = "";
    popupDiv.onmouseout = function() {
      popupDiv.style.visibility = 'hidden';
    }
    document.body.appendChild(popupDiv);
  }
  JS_positionInfoPopup(obj, popupDiv);

  var httpreq = JS_getXMLHttpRequest();
  if (!httpreq) {
    return true;
  }

  var aborted = false;
  var httpreq_timeout = setTimeout(function() {
    aborted = true;
    httpreq.abort();
  }, 5000);

  httpreq.onreadystatechange = function () {
    if (httpreq.readyState == 4 && !aborted) {
      clearTimeout(httpreq_timeout);
      if (httpreq.status == 200) {
        popupDiv = document.getElementById(divId);
        popupDiv.innerHTML=httpreq.responseText;
        popupDiv.style.visibility = "visible";
      } else {
        //Better fail silently here because it's not
        //critical functionality
      }
    }
  }
  httpreq.open("GET", urlMapper + key, true);
  httpreq.send(null);
  obj.onmouseout = function() {
    aborted = true;
    popupDiv.style.visibility = 'hidden';
    obj.onmouseout = null;
  }
}

/**
 * Toggle the visibility of a section. The little indicator triangle will also
 * be toggled.
 * @param {String} id The id of the target element
 */
function JS_toggleSection(id) {
  var pointer = document.getElementById(id + "-pointer");
  var sectionStyle = document.getElementById(id).style;
  var pointerStyle = document.getElementById(id + "-pointer").style;
  var image = document.getElementById(id + "-image");
  if (sectionStyle.display == "none") {
    if (image != null) {
	  image.className = "sprite minus";
	}
    /*pointer.className = "toggled-section opentriangle";*/
    sectionStyle.display = "";
  } else {
    if (image != null) {
      image.className = "sprite plus";
    }
    /*pointer.className = "toggled-section closedtriangle";*/
    sectionStyle.display = "none";
  }
}

/**
 * Toggle the timeline view
 * @param {String} Id of the div element
 */
function JS_toggleTimeline(id) {
  var desc = document.getElementById(id + "-short-description");
  JS_toggleSection(id);
  if (desc.style.display == "none") {
    desc.style.display = "";
  } else {
    desc.style.display = "none";
  }
}

/**
 * Clears an options box
 * @param {String} element The HTML element
 * @param {String} first_label Label of the first element to be displayed
 */
function JS_clearDropdown(element, first_label) {
  $(element).empty();
  if (first_label != undefined) {
    $(element).append('<option value="0">' + first_label + '</option>')
  }
}

/**
 * Fill an option box with data elements
 * @param {String} element The HTML element
 * @param {?} data The data dictionary
 * @param {String} first_label Label of the first element to be displayed
 */
function JS_fillDropdown(element, data, first_label, field) {
  JS_clearDropdown(element, first_label);
  for (var i = 0; i < data.length; i++) {
    if (data.length == 1 && first_label != undefined) {
      // If there is only one option dispite the first label,
      // preselect this option.
      $(element).append('<option value="' + data[i].pk + '" selected>' + data[i].fields[field] + '</option>');
    }
    else {
      $(element).append('<option value="' + data[i].pk + '">' + data[i].fields[field] + '</option>');
    }
  };
}

function JS_shortcutHandler(evt) {
  return M_keyPressCommon(evt, function(evt, src, code, key)
    {
      // TODO: g+x event handling
      if (key == 'd') {
	log('d', this);
	//document.location.href = '/dashboard';
      } else if (key == 'v') {
	JS_gotoNextDay();
      } else if (key == 'c') {
	JS_gotoCurrentDay();
      } else if (key == 'x') {
	JS_gotoPreviousDay();
      } else if (key == '+') {
	JS_addTimer();
      } else if (key == '\r' || key == '\n') {
	hier_passiert_was_bei_return();
      } else {
	return true;
      }
      return false;
    }, JS_inputShortcutHandler);
}

function JS_gotoPreviousDay() {
  var url = window.location.pathname;
  var index = url.indexOf("/day");
  var day = url.substring(index + 5);
  window.location.href = '/previous_day/' + day;
}

function JS_gotoCurrentDay() {
  var today = new Date();
  window.location.href = '/time/' + today.getFullYear() + '/' + (today.getMonth() + 1) + '/' + today.getDate();
}

function JS_gotoNextDay() {
  var url = window.location.pathname;
  var index = url.indexOf("/day");
  var day = url.substring(index + 5);
  window.location.href = '/next_day/' + day;
}

/**
 * Call a star function
 * @param {id} Id of the booking entry
 * @param {url} URL of the JSON method
 * @param {name} Name of the element
 */
function JS_setBookingStar(id, url, name) {
  var httpreq = JS_getXMLHttpRequest();
  if (!httpreq) {
    return true;
  }
  httpreq.onreadystatechange = function () {
    if (httpreq.readyState == 4) {
      if (httpreq.status == 200) {
          var elem = document.getElementById(name + "-star-" + id);
          elem.innerHTML = httpreq.responseText;
      }
    }
  }
  httpreq.open("POST", "/" + id + url, true);
  httpreq.send("");
}

/**
 * Add a booking star
 * @param {id} Id of the booking entry
 */
function JS_addBookingStar(id) {
  return JS_setBookingStar(id, "/star_booking", "booking");
}

/**
 * Remove a booking
 * @param {id} Id of the booking
 */
function JS_removeBookingStar(id) {
  return JS_setBookingStar(id, "/unstar_booking", "booking");
}

function JS_setProjects(index) {
  $.getJSON("/json/get_customer_projects", {"index": index}, function(data) {
	      JS_fillDropdown('#id_project', data, gettext('Please select'), 'name');
	      JS_clearDropdown('#id_step', gettext('Please select'));
	      JS_clearDropdown('#id_tracker', gettext('Please select'));
	      $('#id_project').val(0);
	      if ($('#id_project').val() != 0) {
		JS_setProjectsteps($('#id_project').val());
		JS_setTracker($('#id_project').val());
	      }
	    });
}

function JS_setProjectsteps(index) {
  $.getJSON("/json/get_project_steps", {"index": index}, function(data) {
	JS_fillDropdown('#id_step', data, gettext('Please select'), 'name');
	/*
	$.getJSON("/json/get_default_projectstep", {"index": index}, function(data) {
	  if (data > 0) {
		$('#id_step').val(data);
	  }
	  });
	  */
	JS_setTracker(index);
	/*
	$.getJSON("/json/get_default_tracker", {"index": index}, function(data) {
	  if (data > 0) {
		$('#id_tracker').val(data);
	  }
	  else {
		$('#id_tracker').empty();
	  }
	  });
	  */
	});
}

function JS_setTracker(index) {
  $.getJSON("/json/get_project_tracker", {"index": index}, function(data) {
	JS_fillDropdown('#id_tracker', data, gettext('Please select'), 'name');
	});
}

function JS_setTimer(id, url) {
  var httpreq = JS_getXMLHttpRequest();
  if (!httpreq) {
    return true;
  }
  httpreq.open("POST", "/" + id + url, true);
  httpreq.send("");
}

function JS_addTimer() {
  var httpreq = JS_getXMLHttpRequest();
  if (!httpreq) {
    return true;
  }
  httpreq.open("POST", "/add_timer", true);
  httpreq.send("");
  // Wait for read state before reloading the current page
  httpreq.onreadystatechange = function () { window.location.reload(); }
  // TODO: add the HTML element without reloading the page
}

function JS_startTimer(id) {
  var startImage = document.getElementById("start-image-" + id);
  var pauseImage = document.getElementById("pause-image-" + id);
  var timerImage = document.getElementById("timer-image-" + id);
  var stopImage = document.getElementById("stop-image-" + id);
  var watchdisplay = document.getElementById("watchdisplay-" + id);
  stopImage.className = "sprite stop_disabled";
  stopImage.style.display = "none";
  timerImage.className = "sprite timer";
  startImage.className = "sprite start_disabled";
  pauseImage.className = "sprite pause";
  pauseImage.onclick = function() { return JS_pauseTimer(id) };
  watchdisplay.onclick = function() { return false };
  window['watch' + id].start();
  return JS_setTimer(id, "/start_timer");
}

function JS_pauseTimer(id) {
  var startImage = document.getElementById("start-image-" + id);
  var pauseImage = document.getElementById("pause-image-" + id);
  var timerImage = document.getElementById("timer-image-" + id);
  var stopImage = document.getElementById("stop-image-" + id);
  var watchdisplay = document.getElementById("watchdisplay-" + id);
  stopImage.className = "sprite stop";
  stopImage.style.display = "";
  timerImage.className = "sprite timer_disabled";
  startImage.className = "sprite start";
  startImage.onclick = function() { return JS_startTimer(id) };
  watchdisplay.onclick = function() { return JS_applyTimer(id) };
  //pauseImage.className = "sprite pause_disabled";
  pauseImage.className = "sprite stop";
  pauseImage.onclick = function() { return JS_clearTimer(id) };
  stopImage.className = "sprite remove";
  stopImage.onclick = function() { return JS_removeTimer(id) };
  window['watch' + id].stop();
  return JS_setTimer(id, "/pause_timer");
}

/**
 * Reset the timer
 * @param {id} The timer id
 */
function JS_clearTimer(id) {
  var startImage = document.getElementById("start-image-" + id);
  var pauseImage = document.getElementById("pause-image-" + id);
  var stopImage = document.getElementById("stop-image-" + id);
  var timerImage = document.getElementById("timer-image-" + id);
  var watchdisplay = document.getElementById("watchdisplay-" + id);
  timerImage.className = "sprite timer_disabled";
  startImage.className = "sprite start";
  pauseImage.className = "sprite pause_disabled";
  stopImage.style.display = "none";
  watchdisplay.onclick = function() { return false };
  window['watch' + id].stop();
  window['watch' + id].setElapsed(0, 0, 0);
  document.getElementById('watchdisplay-' + id).innerHTML = window['watch' + id].toString();
  return JS_setTimer(id, "/clear_timer");
}

/**
 * Remove a timer
 * @param {id} Id of the timer
 */
function JS_removeTimer(id) {
  var httpreq = JS_getXMLHttpRequest();
  if (!httpreq) {
    return true;
  }
  httpreq.open("POST", "/" + id + "/remove_timer", true);
  httpreq.send("");
  httpreq.onreadystatechange = function () {
    // Remove the row and hide, if necessary, the whole div
    var tr = document.getElementById('timer-row-' + id);
    if (tr != null) {
      var table = tr.parentNode;
      table.removeChild(tr);
      if (table.getElementsByTagName('tr').length == 0) {
	document.getElementById('timers').style.display = 'none';
      }
    }
  }
}

/**
 * Edit the timer title
 * @param {timer_id} The timer id
 * @param {title} The current timer title (default)
 */
function JS_editTimerMessage(timer_id, title) {
  var form = document.getElementById('timer-message-form');
  //var note = document.getElementById('edit-image-'+timer_id);
  var lbl = document.getElementById('timer-title-'+timer_id);
  //note.style.display = "none";
  lbl.style.display = "none";
  form = form.cloneNode(true);
  if (typeof form.title == 'undefined') {
    var form_template = document.getElementById('timer-message-form');
    form = document.createElement('form');
    form.setAttribute('method', 'POST');
    form.setAttribute('action', form_template.getAttribute('action'));
    form.innerHTML = form_template.innerHTML;
  }
  container = document.getElementById('timer-message-'+timer_id);
  container.appendChild(form);
  container.style.display = '';
  form.discard.onclick = function () {
    //document.getElementById('message-reply-href-'+message_id).style.display = "";
    document.getElementById('timer-message-'+timer_id).innerHTML = "";
	//note.style.display = "";
	lbl.style.display = "";
  }
  //var title = document.getElementById('timer-title');
  form.title.value = title;
  form.timer_id.value = timer_id;
  //form.title.focus();
}

/**
 * Create a new booking with the timer data
 * @param {timer_id} The timer id
 */
function JS_applyTimer(timer_id) {
  var today = new Date();
  window.location.href = "/time/" + today.getFullYear() + '/' + (today.getMonth() + 1) + '/' + today.getDate() + '/new?timer_id=' + timer_id;
}
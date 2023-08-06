goog.provide('inhouse');
goog.provide('inhouse.admin');
goog.provide('inhouse.input');
goog.provide('inhouse.shortcuts');
goog.provide('inhouse.timeline');
goog.provide('inhouse.tracking');

goog.require('goog.dom');
goog.require('goog.dom.forms');
goog.require('goog.events');
goog.require('goog.events.FocusHandler');
goog.require('goog.net.XhrIo');
goog.require('goog.ui.AutoComplete.EventType');
goog.require('goog.ui.AutoComplete.Remote');
goog.require('goog.ui.InputDatePicker');
goog.require('goog.ui.LabelInput');
goog.require('goog.ui.KeyboardShortcutHandler');
goog.require('goog.ui.Tooltip');

inhouse.shortcuts.show_help = function() {
  var help = goog.dom.getElement("help");
  if (help_displayed) {
    help.style.display = "none";
    help_displayed = false;
  }
  else {
    help.style.display = "";
    help_displayed = true;
  }
}

inhouse.shortcuts.handle = function(event) {
  switch (event.identifier) {
    case "SHIFT_H":
      inhouse.shortcuts.show_help();
      break;
    case "GD":
      document.location.href = '/dashboard';
      break;
    }
}

inhouse.shortcuts.init_handler = function() {
  var shortcutHandler = new goog.ui.KeyboardShortcutHandler(document);
  var CTRL = goog.ui.KeyboardShortcutHandler.Modifiers.CTRL;
  var SHIFT = goog.ui.KeyboardShortcutHandler.Modifiers.SHIFT;
  var NONE = goog.ui.KeyboardShortcutHandler.Modifiers.NONE;
  shortcutHandler.registerShortcut('SHIFT_H',
    goog.events.KeyCodes.H, SHIFT);
  shortcutHandler.registerShortcut('GD',goog.events.KeyCodes.G, NONE,
    goog.events.KeyCodes.D);
  goog.events.listen(
    shortcutHandler,
    goog.ui.KeyboardShortcutHandler.EventType.SHORTCUT_TRIGGERED,
    inhouse.shortcuts.handle);
}

/**
  * Display a tooltip
  * @param {Object} obj Object
  * @param {String} url_part
  * @param {String} url_mapper
  */
inhouse.show_popup = function (obj, url_part, url_mapper) {
  var url = obj.getAttribute("href");
  var index = url.indexOf(url_part);
  var key = url.substring(index + url_part.length + 1);
  var xhr = new goog.net.XhrIo();
  goog.net.XhrIo.send(url_mapper + key, function(e) {
    var xhr = e.target;
    var response = xhr.getResponseText();
    var tooltip = new goog.ui.Tooltip(obj);
    tooltip.setHtml(response);
    tooltip.setShowDelayMs(300);
  });
}

/**
 * Check or uncheck all checkboxes within a table element.
 * @param id The id of the table element.
 * @param value The value to set.
 */
inhouse.toggle_checkboxes = function(id, value) {
  var table = goog.dom.getElement(id);
  var inputs = table.getElementsByTagName('input');
  for (n = 0; n < inputs.length; n++) {
    var e = inputs[n];
    if (e.type && e.type.toLowerCase() == 'checkbox') {
      e.checked = value;
    }
    inhouse.toggle_row_color(e, id);
  }
}

/**
 * Toggle a table's row color by selecting a checkbox.
 * @param input_element
 * @param table_id
 */
inhouse.toggle_row_color = function(input_element, table_id) {
  if (input_element.type && input_element.type.toLowerCase() == 'checkbox') {
      var td = input_element.parentElement;
      var tr = td.parentElement;
      if (input_element.checked == true) {
          var class_name = 'selected';
      }
      else {
          var class_name = '';
      }
      tds = tr.getElementsByTagName('td');
      for (i = 0; i < tds.length; i++) {
          var x = tds[i];
          if (i == 0) {
              x.className = 'first ' + class_name;
          }
          else if (i == tds.length - 1) {
              x.className = 'last ' + class_name;
          }
          else {
            x.className = class_name;
          }
      }
  }
}

/**
 * Clear all dropdown elements.
 * @param id
 */
inhouse.input.clear_dropdown = function(id) {
  var el = goog.dom.getElement(id);
  for (var i = 0; i = el.options.length; i++) {
    el.remove(el.options[i]);
  }
}

inhouse.input.fill_dropdown = function(id, data, first_label, field) {
  var el = goog.dom.getElement(id);
  inhouse.input.clear_dropdown(id);
  if (data.length != 0  && first_label != undefined) {
    var child = goog.dom.createElement('option');
    child.text = first_label;
    child.value = 0;
    child.selected = true;
    el.options.add(child);
  }
  for (var i = 0; i < data.length; i++) {
    var child = goog.dom.createElement('option');
    if (data.length == 1 && first_label != undefined) {
      child.selected = true;
    }
    if (data[i].fields['default'] == true) {
      child.selected = true;
    }
    child.text = data[i].fields[field];
    child.value = data[i].pk;
    el.options.add(child);
  }
}

/**
  * Toggle a section
  * @param {String} id The div id
  */
inhouse.toggle_section = function(id) {
  var pointer = goog.dom.getElement(id + "-pointer");
  var sectionStyle = goog.dom.getElement(id).style;
  var image = goog.dom.getElement(id + "-image");
  if (sectionStyle.display == "none") {
    if (image != null) {
      image.className = "sprite minus";
    }
    sectionStyle.display = "";
  } else {
    if (image != null) {
      image.className = "sprite plus";
    }
    sectionStyle.display = "none";
  }
}

/**
 * Expand a single timeline entry.
 * @param {String} id The element id
 */
inhouse.timeline.expand = function(id) {
  var desc = goog.dom.getElement(id + "-short-description");
  inhouse.toggle_section(id);
    if (desc.style.display == "none") {
      desc.style.display = "";
    }
    else {
      desc.style.display = "none";
    }
}

/**
  * Expand all timeline entries within a table
  * @param {String} id The table id
  */
inhouse.timeline.expand_all = function(id) {
  var table = goog.dom.getElement(id);
  var divs = table.getElementsByTagName('div');
  for (i = 0; i < divs.length; i++) {
    var e = divs[i];
    if (e.className == 'details') {
      e.style.display = '';
    }
  }
  var spans = table.getElementsByTagName('span');
  for (i = 0; i < spans.length; i++) {
    var e = spans[i];
    if (e.className == 'sprite plus') {
      e.className = 'sprite minus';
    }
    else if (e.id.match(/^.*short-description$/)) {
      e.style.display = 'none';
    }
  }
};

/**
  * Collapse all timeline entries within a table
  * @param {String} id The table id
  */
inhouse.timeline.collapse_all = function(id) {
  var table = goog.dom.getElement(id);
  var divs = table.getElementsByTagName('div');
  for (i = 0; i < divs.length; i++) {
    var e = divs[i];
    if (e.className == 'details') {
      e.style.display = 'none';
    }
  }
  var spans = table.getElementsByTagName('span');
  for (i = 0; i < spans.length; i++) {
    var e = spans[i];
    if (e.className == 'sprite minus') {
      e.className = 'sprite plus';
    }
    else if (e.id.match(/^.*short-description$/)) {
      e.style.display = '';
    }
  }
};

/**
  * Select a customer's projects
  * @param {Integer} index The selected customer id
  */
inhouse.tracking.set_projects = function(index) {
  goog.net.XhrIo.send('/json/get_customer_projects?index=' + index, function(event) {
    var data = event.target.getResponseJson();
    inhouse.input.fill_dropdown('id_project', data, 'Please select', 'name');
    goog.dom.forms.setValue(goog.dom.getElement('id_step'), '');
    goog.dom.forms.setValue(goog.dom.getElement('id_tracker'), '');
    var project = goog.dom.getElement('id_project');
    if (project.value != "") {
      inhouse.tracking.set_project_steps(project.value);
    }
  });
}

/**
  * Select a project's steps and preselect by the user's default step
  * @param {Integer} index The selected project id
  * @param {Integer} with_default Preselect the user's default step?
  */
inhouse.tracking.set_project_steps = function(index) {
  goog.net.XhrIo.send('/json/get_project_steps?index=' + index + '&with_default=1', function(event) {
    var data = event.target.getResponseJson();
    inhouse.input.fill_dropdown('id_step', data, 'Please select', 'name');
    inhouse.tracking.set_project_tracker(index);
  });
}

/**
  * Select a project's issue trackers
  * @param {Integer} index The selected project id
  */
inhouse.tracking.set_project_tracker = function(index) {
goog.net.XhrIo.send('/json/get_project_tracker?index=' + index, function(event) {
  var data = event.target.getResponseJson();
  inhouse.input.fill_dropdown('id_tracker', data, 'Please select', 'name');
});
goog.dom.forms.setValue(goog.dom.getElement('id_issue_no'), '');
}

/**
  * Event by selecting an issue tracker
  * @param {Integer} index The selected tracker id
  */
inhouse.tracking.on_select_tracker = function(index) {
  goog.dom.forms.setValue(goog.dom.getElement('id_issue_no'), '');
}

/**
  * Add or remove a booking star.
  * @param {Integer} id Id of the booking entry
  * @param {String} url
  * @param {String} name
  */
inhouse.tracking.set_booking_star = function(id, url, name) {
  var xhr = new goog.net.XhrIo();
  goog.net.XhrIo.send('/' + id + url, function(e) {
    var xhr = e.target;
    var response = xhr.getResponseText();
    var el = goog.dom.getElement(name + '-star-' + id);
    el.innerHTML = response;
  });
}

inhouse.tracking.add_booking_star = function(id) {
  inhouse.tracking.set_booking_star(id, '/star_booking', 'booking');
}

inhouse.tracking.remove_booking_star = function(id) {
  inhouse.tracking.set_booking_star(id, '/unstar_booking', 'booking');
}

inhouse.admin.set_project_steps = function(index) {
  goog.net.XhrIo.send('/json/get_project_steps?index=' + index + '&with_default=0', function(event) {
    var data = event.target.getResponseJson();
    inhouse.input.fill_dropdown('id_step', data, 'No selection', 'name');
  });
}

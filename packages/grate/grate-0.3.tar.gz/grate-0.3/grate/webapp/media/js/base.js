function reload_messages() {
  $.ajax({
    url: "/messages/",
    success: function(data) {
      $("#messages").html(data);
    }
  });
}

function remove_access(e) {
  e.preventDefault();
  $.ajax({
    type: "POST",
    url: this.href,
    context: $(this).parent(),
    success: function() {
      $(this).remove();
      reload_messages();
    }
  });
}

/* key_index */
function strip_newline(text) {
  var x = "";
  for (var i = 0; i < text.length; i++) {
    if (text[i] != "\n") {
      x += text[i];
    }
  }
  return x;
}

function split_into_lines(text, cols) {
  var x = "";
  for (var i = 0; i < text.length; i++) {
    x += text[i];
    if (((i + 1) % cols) == 0 && (text.length != (i + 1))) {
      x += "\n";
    }
  }
  return x;
}

function pubkey_handler(e) {
  var text = $(this).val();
  if (e.which == "\r".charCodeAt(0)) {
    if (text.length > 100) {
      $("input:submit", $(this).parent()).click();
      return;
    }
  }
  var cols = parseInt($(this).attr('cols'));
  text = strip_newline(text);
  text = split_into_lines(text, cols);
  $(this).val(text);
}

/* repo_index */
function change_prefix(new_prefix, type) {
  $('input[name="prefix-type"]').val(type);
  $('input[name="prefix"]').val(new_prefix);
  $("#repo-prefix").text(new_prefix + "/");
}

function show_prefix_dialog(groups) {
  var root = $('<div id="prefix-dialog" title="Select prefix"></div>');
  for (var i in groups) {
    var group = groups[i];
    root.append("<div class='repo-select-group'>" + group + "</div>");
  }
  root.dialog({
    close: function() {root.remove();}
  });
  $(".repo-select-group").click(function(e) {
    e.preventDefault();
    change_prefix($(this).text(), "group");
    root.dialog('close');
    root = false;
  });
}

/* From http://docs.djangoproject.com/en/1.2/releases/1.2.5/ */
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0, clen = cookies.length; i < clen; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

$(function() {
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      /* XXX This grabs the csrftoken from the page. */
      xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
//    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
//      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
//    }
    }
  });
});

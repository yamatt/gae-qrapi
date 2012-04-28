var tips = [
    "Shorter codes are better.",
    "Put http:// on the front to make a URL."
]

var base_url = "/";

$(document).ready(function() {
  var image_area = $('<div></div>');
  image_area.attr('class', 'fat-border padding top-spacer');
  var container = $('#container');
    
  $('form').submit(function (event) {
    event.preventDefault();
    value = get_value_from_form($(this), 'value');
    qr_url = base_url + encodeURIComponent(value)
    $.getJSON(qr_url, {
        "info": true
    },
    function (data) {
        if (data['success']){
            qr_image = $("<img />");
            qr_image.attr('src', qr_url);
            image_area.remove();
            image_area.empty();
            image_area.hide();
            image_area.append(qr_image);
            container.append(image_area);
            image_area.fadeIn();
        }
        else {
            alert("Sadly we could not get you your QR code because:\n" + data['message'])
        }
    });
  });
});

function get_value_from_form(form, name) {
    var form_inputs = form.serializeArray()
    for (input in form_inputs) {
        if (form_inputs[0]['name'] == name) {
            return form_inputs[0]['value']
        }
    }
    return false
}

/*
 * This file is part of QR API.
 * 
 * QR API is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.

 * QR API is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with QR API.  If not, see <http://www.gnu.org/licenses/>.
 * 
 */


var tips = [
    "Shorter codes are better.",
    "Put http:// on the front to make a URL."
]
var tip_delay = 5 * 1000
var base_url = "/";

$(document).ready(function() {
  var image_area = $('<div></div>');
  image_area.attr('class', 'fat-border padding top-spacer');
  var container = $('#container');
  
  add_tip_to($('#tips'))
    
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

function add_tip_to(element){
    element.fadeOut("normal", function () {
        $(this).text(get_random_tip());
        $(this).fadeIn("normal", function () {
            setTimeout(function () {
                add_tip_to(element)
            }, 5000);
        });
    });
}

function get_random_tip(){
    var tip_no = Math.round(Math.random() * tips.length)
    return tips[tip_no]
}

function get_value_from_form(form, name) {
    var form_inputs = form.serializeArray()
    for (input in form_inputs) {
        if (form_inputs[0]['name'] == name) {
            return form_inputs[0]['value']
        }
    }
    return false
}

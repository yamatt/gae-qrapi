
#~ This file is part of QR API.
#~ 
#~ QR API is free software: you can redistribute it and/or modify
#~ it under the terms of the GNU General Public License as published by
#~ the Free Software Foundation, either version 3 of the License, or
#~ (at your option) any later version.
#~ 
#~ QR API is distributed in the hope that it will be useful,
#~ but WITHOUT ANY WARRANTY; without even the implied warranty of
#~ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#~ GNU General Public License for more details.
#~ 
#~ You should have received a copy of the GNU General Public License
#~ along with QR API.  If not, see <http://www.gnu.org/licenses/>.

from webapp2 import WSGIApplication, RequestHandler, Route, uri_for
import os
import jinja2
from json import dumps as dict_to_json_string
from urllib import quote_plus as urlencode, unquote as urldecode
from google.appengine.ext.webapp import template
from qrmodels import QRKey, QRStore, QRValueError

SITE_URL = "http://qrthisurl.appspot.com/"

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))

def jsonify(response, out_dict):
    out_json = dict_to_json_string(out_dict)
    response.headers['Content-Type'] = "application/json"
    response.out.write(out_json)

def render(response, template_file, template_values=None):
    template = jinja_environment.get_template(template_file)
    response.out.write(template.render(template_values))

class FrontPage(RequestHandler):
    def get(self):
        if self.request.get('value') and len(self.request.get('value')) >= 6:
            self.redirect(uri_for('qrimage', value=urlencode(self.request.get('value'))))
        elif not self.request.get('value'):
            render(self.response, 'frontpage.html', {'value': SITE_URL})
        else:
            render(self.response, 'frontpage.html', {'value': self.request.get('value')})

class QRImage(RequestHandler):
    def get(self, value):
        value = urldecode(value)
        qr_key = QRKey.from_value(value)
        try:
            qr_image = QRStore.get(qr_key)
            if not qr_image:
                qr_image = QRStore(value)
            
            qr_image.put()  # saves the image if new, but otherwise just updates the access time
            if self.request.get('info'):
                jsonify(self.response, {"success": True, "message": "QR code now stored in database."})
            else:
                self.response.headers['Content-Type'] = "image/png"
                self.response.out.write(qr_image.get_image())
                
        except QRValueError:
            jsonify(self.response, {"success": False, "message": "Value too short."})
        

app = WSGIApplication([
        Route('/', handler=FrontPage, name='home'),
        Route('/<value:.*>', handler=QRImage, name='qrimage')
    ],
    debug=True
)

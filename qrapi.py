from webapp2 import WSGIApplication, RequestHandler, Route, uri_for
import os
import jinja2
from json import dumps as dict_to_json_string
from urllib import quote_plus as urlencode, unquote as urldecode
from google.appengine.ext.webapp import template
from qrparse import GetQR

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
        else:
            render(self.response, 'frontpage.html', {'value': self.request.get('value')})

class QRImage(RequestHandler):
    def get(self, value):
        value = urldecode(value)
        qr = GetQR(value)
        errors = qr.has_errors()
        if errors:
            jsonify(self.response, {"success": False, "message": errors})
        else:
            png = qr.get_image()
            if self.request.get('info'):
                jsonify(self.response, {"success": True, "message": "Image generated. Saved to database."})
            else:
                self.response.headers['Content-Type'] = "image/png"
                self.response.out.write(png)

app = WSGIApplication([
        Route('/', handler=FrontPage, name='home'),
        Route('/<value:.*>', handler=QRImage, name='qrimage')
    ],
    debug=True
)

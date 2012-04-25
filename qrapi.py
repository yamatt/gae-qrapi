from webapp2 import WSGIApplication, RequestHandler, Route, uri_for
import os
import jinja2
from json import dumps as dict_to_json_string
from urllib import quote_plus as urlencode, unquote as urldecode
from google.appengine.ext.webapp import template
from qrparse import GetQR

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class FrontPage(RequestHandler):
    def render(self, template_file, template_values=None):
        path = os.path.join(os.path.dirname(__file__), 'templates', template_file)
        self.response.out.write(template.render(path, template_values))

    def get(self):
        if self.request.get('value'):
            self.redirect(uri_for('qrimage', value=urlencode(self.request.get('value'))))
        else:
            self.render('frontpage.html')

class QRImage(RequestHandler):
    def get(self, value):
        value = urldecode(value)
        qr = GetQR(value)
        png = qr.get_image()
#        self.response.headers['Content-Type'] = "plain/text"
        self.response.headers['Content-Type'] = "image/png"
        self.response.out.write(png)

app = WSGIApplication([
        Route('/', handler=FrontPage, name='home'),
        Route('/<value>', handler=QRImage, name='qrimage')
    ],
    debug=True
)

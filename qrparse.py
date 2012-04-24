from pyqrcode import MakeQR
from StringIO import StringIO
from png import Writer as PNGWriter

from google.appengine.api.images import Image
from google.appengine.ext import db

class GetQR(object):
    def __init__(self, value, type=None):
        self.value = value
        self.type = type
        
    def get_image(self, size=300):
    	qr = MakeQR(self.value)
    	nodes = map(lambda row: map(lambda data: False if data else True, row), qr.modules)
    	rows = len(nodes)
    	columns = len(nodes[0])
    	
    	buff = StringIO()
    	w = PNGWriter(rows, columns, greyscale=True, bitdepth=1)
    	w.write(buff, nodes)
    	qr_image = buff.getvalue()
    	image = Image(image_data=qr_image)
    	image.resize(height=size)
    	image.execute_transforms()
    	return image._image_data

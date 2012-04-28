from pyqrcode import MakeQR
from StringIO import StringIO
from png import Writer as PNGWriter
from hashlib import sha512
from datetime import datetime
import logging

from google.appengine.api.images import Image
from google.appengine.ext import db

class QRCode(db.Model):
    created = db.DateTimeProperty(auto_now_add=True)
    last_used = db.DateTimeProperty(auto_now=True)
    image = db.BlobProperty()
    version = db.IntegerProperty(default=1)

class GetQR(object):
    def __init__(self, value):
        self.value = value
        self.hash_key = sha512(value).hexdigest()
        
    def has_errors(self):
        if len(self.value) < 6:
            return "Value specified is too short. It must be 6 characters or longer."
        
    def make_image(self, size=300):
    	qr = MakeQR(self.value)
    	nodes = map(lambda row: map(lambda data: False if data else True, row), qr.modules)
    	rows = len(nodes)
    	columns = len(nodes[0])
    	
    	buff = StringIO()
    	w = PNGWriter(rows, columns, greyscale=True, bitdepth=1)
    	w.write(buff, nodes)
    	qr_image = buff.getvalue()
    	return qr_image
        
    def store_new_image(self, image_obj):
        qr_store = QRCode(key_name=self.hash_key, image=image_obj)
        qr_store.put()
        
    def access_image(self):
        """
        Get the image, update the last access time and return image
        """
        k = db.Key.from_path("QRCode", self.hash_key)
        qr_store = db.get(k)
        qr_image = qr_store.image
        qr_store.put()
        return qr_image
        
    def has_image(self):
        """
        returns true if entry exists for qr
        """
        k = db.Key.from_path("QRCode", self.hash_key)
        return (db.get(k))
        
    def scale_image(self, image_obj, size=300):
    	image = Image(image_data=image_obj)
    	image.resize(height=size)
    	image.execute_transforms()
        return image._image_data
        
    def get_image(self):
        if self.has_image():
            logging.info("Has image for: %s" % self.value)
            qr_image = self.access_image()
        else:
            logging.info("Generating image: %s" % self.value)
            qr_image = self.make_image()
            self.store_new_image(qr_image)
        qr_image = self.scale_image(qr_image)
        return qr_image

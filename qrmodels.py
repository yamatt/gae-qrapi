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

from pyqrcode import MakeQR
from StringIO import StringIO
from png import Writer as PNGWriter
from hashlib import sha512
from datetime import datetime
import logging

from pickle import loads as unpickle, dumps as pickle, PicklingError
from zlib import compress, decompress, error as ZlibError

from google.appengine.api.images import Image
from google.appengine.ext import db

class QRImageProperty(db.BlobProperty):
    def validate(self, value):
        try:
            obj = pickle(value)
            obj = compress(obj)
            return value
        except PicklingError, e:
            return super(QRImageProperty, self).validate(value)
        except ZlibError, e:
            return super(QRImageProperty, self).validate(value)
            
    def get_value_for_datastore(self, model_instance):
        result = super(QRImageProperty, self).get_value_for_datastore(model_instance)
        result = pickle(result)
        result = compress(result)
        return db.Blob(result)
        
    def make_value_from_datastore(self, value):
        try:
            value = decompress(value)
            value = unpickle(value)
        except:
            pass
        return super(QRImageProperty, self).make_value_from_datastore(value)
        
class QRKey(db.Key):
    @classmethod
    def from_value(cls, value):
        hash_value = sha512(value).hexdigest()
        return super(QRKey, cls).from_path("QRCode", hash_value)

class QRStore(db.Model):
    created = db.DateTimeProperty(auto_now_add=True)
    last_used = db.DateTimeProperty(auto_now=True)
    raw_qr_image = QRImageProperty()
    
    def __init__(self, value):
        hash_value = sha512(value).hexdigest()
        raw_qr_image = MakeQR(value).modules
        raw_qr_image = self.__clean_modules(raw_qr_image)
        super(QRStore, self).__init__(key_name=hash_value, raw_qr_image=raw_qr_image)
        
    def __clean_modules(self, modules):
        return map(lambda row: map(lambda data: False if data else True, row), modules)
    
    @staticmethod
    def render_image(image_raw, fg_colour, bg_colour):
        rows = len(image_raw)
        columns = len(image_raw[0])
        palette=[fg_colour, bg_colour]
        buff = StringIO()
        w = PNGWriter(rows, columns, palette=palette, bitdepth=1)
        w.write(buff, image_raw)
        qr_image = buff.getvalue()
        return qr_image
    
    @staticmethod
    def scale_image(image_raw, size=10):
        enlarged_image = []
        for row in image_raw:
            new_row = ()
            for d in row:
                new_row += (d,) * size
            for i in range(size):
                enlarged_image.append(new_row)
        return enlarged_image
    
    def get_image(self, scale=10, fg_colour=(0,0,0,255), bg_colour=(255,255,255,255)):
        raw_qr_image = self.raw_qr_image
        raw_qr_image = self.scale_image(raw_qr_image, scale)
        qr_image = self.render_image(raw_qr_image, fg_colour, bg_colour)
        return qr_image

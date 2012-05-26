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
from hashlib import sha512
from datetime import datetime
import logging

from pyqrcode import MakeQRImage

from pickle import loads as unpickle, dumps as pickle, PicklingError
from zlib import compress, decompress, error as ZlibError

from google.appengine.api.images import Image
from google.appengine.ext import db
        
class QRKey(db.Key):
    @classmethod
    def from_value(cls, value):
        hash_value = sha512(value).hexdigest()
        return super(QRKey, cls).from_path("QRCode", hash_value)

class QRStore(db.Model):
    created = db.DateTimeProperty(auto_now_add=True)
    last_used = db.DateTimeProperty(auto_now=True)
    qr_image = db.BlobProperty()
    
    def __init__(self, value):
        if len(value) > 6:
            hash_value = sha512(value).hexdigest()
            image = MakeQRImage(value)
            s = StringIO()
            image.save(s, format="PNG")
            qr_image = s.getvalue()
            super(QRStore, self).__init__(key_name=hash_value, qr_image=qr_image)
        else:
            raise QRValueError("QR value too short.")
    
    def get_image(self):
        qr_image = self.qr_image
        return qr_image

class QRValueError(Exception):
    pass

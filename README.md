# QR API
Is an API that allows you to directly create images with QR patterns in them to be generated dynamically through a web interface

## Why
There does exist some Google App Engine based sites that generate QR codes using the Google Chart API but I found a way to do it entirely in Python without the need for external API.

## Status
Beta. This code is working and in use. There still may be some bugs I would like to solve before adding new features.

## API
The API is pretty simple.
Route: /
Result: Gives you the web interface static page

Route: /<value>
Result: Anything in value that is URL escaped will be put in to a QR code unless there is a problem in which case a JSON error message is returned in the format {'error': True, 'message': 'The value was to long'}
Query Strings: If you want to check on the likely success of a value first put a ?info=true query string on the end of the URL. This will generate the QR code in the background, insert it in to the database and report if it succeeded.

## Future plans
* A query string parameter for the size of the QR code you would like
* A query string parameter for the background and foreground colour.

## License
GPLv3
    This file is part of QR API.

    QR API is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    QR API is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with QR API.  If not, see <http://www.gnu.org/licenses/>.

from cStringIO import StringIO

import qrcode
from django.http import HttpResponse


def generate_qrcode(request, data):
	img = qrcode.make(data)

	buf = StringIO()
	img.save(buf)
	image_stream = buf.getvalue()

	response = HttpResponse(image_stream, content_type="image/png")
	response['Last-Modified'] = 'Mon, 27 Apr 2015 02:05:03 GMT'
	response['Cache-Control'] = 'max-age=31536000'
	return response

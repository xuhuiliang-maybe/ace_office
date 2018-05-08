# coding=utf-8
import traceback

from django import forms
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import View


class ImageUploadForm(forms.Form):
	"""Image upload form."""
	image = forms.ImageField()


class ProfileUploadPhotoView(View):
	def post(self, request, *args, **kwargs):
		try:
			form = ImageUploadForm(request.POST, request.FILES)  # 有文件上传要传如两个字段

			if form.is_valid():
				user_obj = User.objects.get(pk="")
				user_obj.photo = form.cleaned_data['image']  # 直接在这里使用 字段名获取即可
				user_obj.save()
				return HttpResponse('image upload success')
			return HttpResponseForbidden('allowed only via POST')  # 返回403
		except:
			traceback.print_exc()

"""
          <form action="{% url upload_pic %}" method="post" enctype="multipart/form-data">{% csrf_token %}
                <p>
                      <input id="id_image" type="file" class="" name="image"> <!-- 这一行应该是form.image，省事写的 -->
                </p>
                <input type="submit" value="Submit" />
          </form>
"""
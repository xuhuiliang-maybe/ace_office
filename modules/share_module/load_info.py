# coding=utf-8
from django import forms


class LoadInfoUploadForm(forms.Form):
	"""导入信息表单"""
	load_info = forms.FileField()

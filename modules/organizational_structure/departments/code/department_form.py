# coding=utf-8
from django import forms

from modules.organizational_structure.departments.models import Department


class DepartmentForm(forms.ModelForm):
	""" 部门表单 , 默认必填"""

	name = forms.CharField(label='部门名称', max_length=100)
	parent_dept = forms.CharField(label='上级部门', max_length=100)

	class Meta:
		model = Department
		fields = ("name",)

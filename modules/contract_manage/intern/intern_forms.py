# coding=utf-8
from django import forms

from modules.contract_manage.models import *


class ContractInternForm(forms.ModelForm):
	workplace = forms.CharField(label=u'实习地点')
	post = forms.CharField(label=u'实习岗位')
	payroll_standard = forms.CharField(label=u'实习劳务费标准')

	def __init__(self, *args, **kwargs):
		super(ContractInternForm, self).__init__(*args, **kwargs)

	class Meta:
		model = ContractIntern
		fields = [
			"project_name",
			"name",
			"identity_card_number",
			"sex",
			"birthday",
			"nation",
			"address",
			"phone_number",
			"receive_address",
			"emergency_contact_name",
			"emergency_contact_phone",
			"start_date",
			"end_date",
			"deadline",
			"probation",
			"workplace",
			"post",
			"payroll_standard",
			"payroll_grant",
			"grant_date",
		]

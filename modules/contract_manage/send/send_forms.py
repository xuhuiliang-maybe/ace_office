# coding=utf-8
from django import forms

from modules.contract_manage.models import *


class ContractSendForm(forms.ModelForm):
	workplace = forms.CharField(label=u'派遣工作地点')
	post = forms.CharField(label=u'派遣岗位')

	def __init__(self, *args, **kwargs):
		super(ContractSendForm, self).__init__(*args, **kwargs)

	class Meta:
		model = ContractSend
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
			"start_send_deadline",
			"end_send_deadline",
			"workplace",
			"post",
			"payroll_standard",
			"payroll_grant",
			"grant_date",
		]

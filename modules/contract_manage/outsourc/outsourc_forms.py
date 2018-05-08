# coding=utf-8
from django import forms

from modules.contract_manage.models import *


class ContractOutsourcForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ContractOutsourcForm, self).__init__(*args, **kwargs)

	class Meta:
		model = ContractOutsourc
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

# coding=utf-8
from django import forms

from modules.contract_manage.models import *


class ContractHourlyForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ContractHourlyForm, self).__init__(*args, **kwargs)

	class Meta:
		model = ContractHourly
		fields = [
			"project_name",
			"project_date",
			"name",
			"identity_card_number",
			"sex",
			"phone_number",
			"start_date",
			"end_date",
			"workplace",
			"post",
			"payroll_standard",
			"start_work_date",
			"end_work_date",
			"work_days",
			"work_hours",
			"grant_money",
			"recipients",
			"grant_user",
			"grant_time",
			"recruiters",
			"remark",
		]

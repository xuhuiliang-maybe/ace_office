# coding=utf-8
import traceback
from django import template
from django.db.models import Sum
from django.template.defaultfilters import stringfilter
from modules.payroll_manage.payroll_detail.models import PayrollDetail

register = template.Library()


@register.filter
def get_project_name(payroll_detail_dict):
	try:
		return PayrollDetail.objects.filter(**payroll_detail_dict).values(
			"project_name__full_name").first().get("project_name__full_name", "")
	except:
		traceback.print_exc()
		return ""


@register.filter
def get_company_subject(payroll_detail_dict):
	try:
		return PayrollDetail.objects.filter(**payroll_detail_dict).values(
			"project_name__company_subject__name").first().get("project_name__company_subject__name", "")
	except:
		traceback.print_exc()
		return ""


@register.filter
def get_department(payroll_detail_dict):
	try:
		return PayrollDetail.objects.filter(**payroll_detail_dict).values(
			"project_name__department__name").first().get("project_name__department__name", "")
	except:
		traceback.print_exc()
		return ""


@register.filter
def get_settle_accounts_month(payroll_detail_dict):
	try:
		return PayrollDetail.objects.filter(**payroll_detail_dict).values(
			"settle_accounts_month").first().get("settle_accounts_month", "")
	except:
		traceback.print_exc()
		return ""


@register.filter
def get_wages_should_be(payroll_detail_dict):
	try:
		sum_wages_should_be = PayrollDetail.objects.filter(**payroll_detail_dict) \
			.aggregate(Sum('wages_should_be'))
		return sum_wages_should_be["wages_should_be__sum"]
	except:
		traceback.print_exc()
		return ""


@register.filter
def get_person_social_security(payroll_detail_dict):
	try:
		sum_wages_should_be = PayrollDetail.objects.filter(**payroll_detail_dict) \
			.aggregate(Sum('person_social_security'))
		return sum_wages_should_be["person_social_security__sum"]
	except:
		traceback.print_exc()
		return ""


@register.filter
def get_person_provident_fund(payroll_detail_dict):
	try:
		sum_wages_should_be = PayrollDetail.objects.filter(**payroll_detail_dict) \
			.aggregate(Sum('person_provident_fund'))
		return sum_wages_should_be["person_provident_fund__sum"]
	except:
		traceback.print_exc()
		return ""


@register.filter
def get_pre_tax_adjustment(payroll_detail_dict):
	try:
		sum_wages_should_be = PayrollDetail.objects.filter(**payroll_detail_dict) \
			.aggregate(Sum('pre_tax_adjustment'))
		return sum_wages_should_be["pre_tax_adjustment__sum"]
	except:
		traceback.print_exc()
		return ""


@register.filter
def get_pre_tax_wage(payroll_detail_dict):
	try:
		sum_wages_should_be = PayrollDetail.objects.filter(**payroll_detail_dict) \
			.aggregate(Sum('pre_tax_wage'))
		return sum_wages_should_be["pre_tax_wage__sum"]
	except:
		traceback.print_exc()
		return ""


@register.filter
def get_tax(payroll_detail_dict):
	try:
		sum_wages_should_be = PayrollDetail.objects.filter(**payroll_detail_dict) \
			.aggregate(Sum('tax'))
		return sum_wages_should_be["tax__sum"]
	except:
		traceback.print_exc()
		return ""


@register.filter
def get_tax_rate(payroll_detail_dict):
	try:
		sum_wages_should_be = PayrollDetail.objects.filter(**payroll_detail_dict) \
			.aggregate(Sum('tax_rate'))
		return sum_wages_should_be["tax_rate__sum"]
	except:
		traceback.print_exc()
		return ""


@register.filter
def get_quick_deduction(payroll_detail_dict):
	try:
		sum_wages_should_be = PayrollDetail.objects.filter(**payroll_detail_dict) \
			.aggregate(Sum('quick_deduction'))
		return sum_wages_should_be["quick_deduction__sum"]
	except:
		traceback.print_exc()
		return ""


@register.filter
def get_tax_adjustments(payroll_detail_dict):
	try:
		sum_wages_should_be = PayrollDetail.objects.filter(**payroll_detail_dict) \
			.aggregate(Sum('tax_adjustments'))
		return sum_wages_should_be["tax_adjustments__sum"]
	except:
		traceback.print_exc()
		return ""


@register.filter
def get_real_hair_wage(payroll_detail_dict):
	try:
		sum_wages_should_be = PayrollDetail.objects.filter(**payroll_detail_dict) \
			.aggregate(Sum('real_hair_wage'))
		return sum_wages_should_be["real_hair_wage__sum"]
	except:
		traceback.print_exc()
		return ""


@register.filter
def get_social_security_unit(payroll_detail_dict):
	try:
		sum_wages_should_be = PayrollDetail.objects.filter(**payroll_detail_dict) \
			.aggregate(Sum('social_security_unit'))
		return sum_wages_should_be["social_security_unit__sum"]
	except:
		traceback.print_exc()
		return ""


@register.filter
def get_provident_fund_unit(payroll_detail_dict):
	try:
		sum_wages_should_be = PayrollDetail.objects.filter(**payroll_detail_dict) \
			.aggregate(Sum('provident_fund_unit'))
		return sum_wages_should_be["provident_fund_unit__sum"]
	except:
		traceback.print_exc()
		return ""


@register.filter
def get_social_security_pay_unit(payroll_detail_dict):
	try:
		sum_wages_should_be = PayrollDetail.objects.filter(**payroll_detail_dict) \
			.aggregate(Sum('social_security_pay_unit'))
		return sum_wages_should_be["social_security_pay_unit__sum"]
	except:
		traceback.print_exc()
		return ""


@register.filter
def get_provident_fund_pay_unit(payroll_detail_dict):
	try:
		sum_wages_should_be = PayrollDetail.objects.filter(**payroll_detail_dict) \
			.aggregate(Sum('provident_fund_pay_unit'))
		return sum_wages_should_be["provident_fund_pay_unit__sum"]
	except:
		traceback.print_exc()
		return ""


@register.filter
def get_social_security_provident_fund_sum_unit(payroll_detail_dict):
	try:
		sum_wages_should_be = PayrollDetail.objects.filter(**payroll_detail_dict) \
			.aggregate(Sum('social_security_provident_fund_sum_unit'))
		return sum_wages_should_be["social_security_provident_fund_sum_unit__sum"]
	except:
		traceback.print_exc()
		return ""


@register.filter
def get_employer(payroll_detail_dict):
	try:
		sum_wages_should_be = PayrollDetail.objects.filter(**payroll_detail_dict) \
			.aggregate(Sum('employer'))
		return sum_wages_should_be["employer__sum"]
	except:
		traceback.print_exc()
		return ""


@register.filter
def get_security_for_disabled(payroll_detail_dict):
	try:
		sum_wages_should_be = PayrollDetail.objects.filter(**payroll_detail_dict) \
			.aggregate(Sum('security_for_disabled'))
		return sum_wages_should_be["security_for_disabled__sum"]
	except:
		traceback.print_exc()
		return ""


@register.filter
def get_management_fee(payroll_detail_dict):
	try:
		sum_wages_should_be = PayrollDetail.objects.filter(**payroll_detail_dict) \
			.aggregate(Sum('management_fee'))
		return sum_wages_should_be["management_fee__sum"]
	except:
		traceback.print_exc()
		return ""


@register.filter
def get_total(payroll_detail_dict):
	try:
		sum_wages_should_be = PayrollDetail.objects.filter(**payroll_detail_dict) \
			.aggregate(Sum('total'))
		return sum_wages_should_be["total__sum"]
	except:
		traceback.print_exc()
		return ""

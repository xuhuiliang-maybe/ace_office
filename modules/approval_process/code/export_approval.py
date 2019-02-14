# coding=utf-8
from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic import View

from modules.approval_process.billing_pre_pay.models import *
from modules.approval_process.demand_turnover.models import *
from modules.approval_process.leave.models import *
from modules.approval_process.recruited_billing.models import *
from modules.approval_process.templatetags.approval_process_tags import *
from modules.approval_process.temporary_write_offs_billing.models import *
from modules.approval_process.wage.models import *
from modules.approval_process.wage_replacement.models import *
from modules.approval_process.write_offs.models import *
from modules.share_module.download import download_file
from modules.share_module.export import ExportExcel
from modules.share_module.formater import *
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs

"""
根据回传申请类型，导出相对应申请信息
"""


# 导出招聘统计
@class_view_decorator(login_required)
# @class_view_decorator(permission_required('social_security_detail.export_socialsecuritydetail', raise_exception=True))
class ApprovalExportView(View):
	def get(self, request, *args, **kwargs):
		self.field_list = ["id", "title", "note", "apply_user"]
		self.head_list = [u"编号", u"标题", u"申请说明", u"申请人"]

		self.end_field_list = ["created", "handle_user", "handle_date", "reason", "status"]
		self.end_head_list = [u"申请时间", u"审批人", u"审批时间", u"审批回复", u"审批状态"]

		try:
			# 查询条件
			self.apply_type = self.request.GET.get("apply_type", "")  # 申请类型
			self.title = self.request.GET.get("title", "")
			self.status = self.request.GET.get("status", "")
			self.month = self.request.GET.get("month", "")  # 月份
			self.dept_name = self.request.GET.get("dept_name", "")  # 部门名称
			self.project_name = self.request.GET.get("project_name", "")  # 项目名称

			created_year = ""
			created_month = ""
			if self.month:
				created_date = date_formater(self.month, "%Y/%m/%d")
				created_year = created_date.year
				created_month = created_date.month

			self.search_condition = {
				"title__icontains": self.title,
				"status": self.status,
				"created__year": created_year,
				"created__month": created_month,
				"apply_user__attribution_dept__icontains": self.dept_name,
			}

			if not self.request.user.is_superuser:
				self.search_condition.update({"apply_user": self.request.user})

			if self.apply_type == "leave":  # 请假申请
				self.field_list += ["begin_date", "end_date", "leave_type"] + self.end_field_list
				self.head_list += [u"请假起始日期", u"请假终止日期", u"请假类型"] + self.end_head_list
				return self.leave_apply_export()

			elif self.apply_type == "loan":  # 备用金
				self.field_list += ["money", "borrowing_date", "repayment_date",
						    "loan_budget_details"] + self.end_field_list
				self.head_list += [u"申请金额", u"借款日期", u"还款日期", u"费用预算明细"] + self.end_head_list
				return self.loan_apply_export()

			elif self.apply_type == "temporary_write_offs_billing":  # 临时工销账与开票
				self.field_list += [
							   "billing_month",
							   "project_name",
							   "billing_date",
							   "billing_content",
							   "billing_type",
							   "main_business_income",
							   "management_fee",
							   "wage_receive",
							   "shuttle_fee_receive",
							   "meals_receive",
							   "dormitory_fee_receive",
							   "daily_receive",
							   "compensate_reparation_receive",
							   "actual_outlay",
							   "main_business_outlay",
							   "wage_outlay",
							   "shuttle_fee_outlay",
							   "meals_outlay",
							   "daily_outlay",
							   "compensate_reparation_outlay",
							   "borrow_loan",
							   "remark1",
							   "difference",
							   "is_billing",
						   ] + self.end_field_list
				self.head_list += [
							  u"结算月份",
							  u"项目名称",
							  u"结算周期",
							  u"结算内容",
							  u"结算方式",
							  u"主营业收入",
							  u"管理费",
							  u"工资(收)",
							  u"班车费(收)",
							  u"餐费(收)",
							  u"宿舍费(收)",
							  u"商报(收)",
							  u"赔付款(收)",
							  u"实际支出",
							  u"主营业支出",
							  u"工资(付)",
							  u"班车费(付)",
							  u"餐费(付)",
							  u"商报(付)",
							  u"赔偿/补偿金(付)",
							  u"已借备用金",
							  u"备注",
							  u"差额",
							  u"是否开票",
						  ] + self.end_head_list
				return self.temporary_write_offs_billing_apply_export()

			elif self.apply_type == "wage":  # 工资与职位调整
				self.field_list += ["money"] + self.end_field_list
				self.head_list += [u"申请金额"] + self.end_head_list
				return self.wage_apply_export()

			elif self.apply_type == "wage_replacement":  # 工资补发申请
				self.field_list += ["wage_replacement_details"] + self.end_field_list
				self.head_list += [u"补发明细"] + self.end_head_list
				return self.wage_replacement_apply_export()

			elif self.apply_type == "write_offs":  # 报销与销账
				self.field_list += ["writeoffs_total", "borrow_imprest", "imprest_explain",
						    "difference", "writeoffs_type",
						    "remark"] + self.end_field_list
				self.head_list += [u"报销/销账总额", u"已借备用金", u"备用金说明", u"差额",
						   u"销账类型", u"备注"] + self.end_head_list
				return self.write_offs_apply_export()

			elif self.apply_type == "demand_turnover":  # 管理人员需求与离职
				self.field_list += self.end_field_list
				self.head_list += self.end_head_list
				return self.demand_turnover_apply_export()

			elif self.apply_type == "billing_pre_pay":  # 结算与发薪
				self.search_condition.update({"project_name__full_name__icontains": self.project_name})
				self.field_list += ["billingprepay_month",
						    "project_name",
						    "billing_date",
						    "billing_content",
						    "main_business_income",
						    "management_fee",
						    "wage_receive",
						    "social_security_receive",
						    "provident_fund_receive",
						    "union_fee_receive",
						    "disablement_gold",
						    "shuttle_fee_receive",
						    "meals_receive",
						    "dormitory_fee_receive",
						    "daily_receive",
						    "compensate_reparation_receive",
						    "bonus_receive",
						    "other_receive",
						    "grant_total",
						    "ccb",
						    "merchants_bank",
						    "icbc",
						    "other_bank",
						    "remark1",
						    ] + self.end_field_list
				self.head_list += [u"结算与发薪月份", u"结算项目名称",
						   u"结算周期",
						   u"结算内容",
						   u"主营业收入",
						   u"管理费",
						   u"工资(收)",
						   u"社保(收)",
						   u"公积金(收)",
						   u"工会费(收)",
						   u"残保金",
						   u"班车费(收)",
						   u"餐费(收)",
						   u"宿舍费(收)",
						   u"商报(收)",
						   u"偿/赔偿金(收)",
						   u"奖金类(收)",
						   u"其他收入",
						   u"发放总额",
						   u"建行",
						   u"招行",
						   u"工行",
						   u"其他银行",
						   u"备注",
						   ] + self.end_head_list
				return self.billing_pre_pay_apply_export()
			elif self.apply_type == "recruitedbilling":  # 待招结算与销账
				self.field_list += ["project_name", "billing_month", "settlement_amount",
						    "is_billing", "content", "recruitedbilling_details"] + self.end_field_list
				self.head_list += [u"项目名称", u"结算月份", u"结算金额", u"是否开票", u"说明", u"报销/销账明细"] + self.end_head_list
				return self.recruitedbilling_apply_export()
		except:
			traceback.print_exc()

	def format_none(self, value):
		try:
			if value:
				return str(value)
			return ""
		except:
			traceback.print_exc()
			return ""

	def format_date(self, val):
		try:
			if val:
				return val.strftime("%Y-%m-%d %X")
			return ""
		except:
			traceback.print_exc()
			return ""

	def format_date_day(self, val):
		try:
			if val:
				return val.strftime("%Y-%m-%d")
			return ""
		except:
			traceback.print_exc()
			return ""

	# 请假申请，导出
	def leave_apply_export(self):
		try:
			kwargs = get_kwargs(self.search_condition)
			apply_info_list = Leave.objects.filter(**kwargs)

			# 组装导出数据
			rows_list = list()
			for one_apply in apply_info_list:
				one_row_dict = defaultdict(str)
				one_row_dict["id"] = str(one_apply.id)
				one_row_dict["title"] = one_apply.title
				one_row_dict["note"] = one_apply.note
				try:
					one_row_dict["apply_user"] = one_apply.apply_user.first_name
				except:
					one_row_dict["apply_user"] = ""

				one_row_dict["begin_date"] = self.format_date(one_apply.begin_date)
				one_row_dict["end_date"] = self.format_date(one_apply.end_date)
				one_row_dict["leave_type"] = ",".join(
					one_apply.leave_type.all().values_list("name", flat=True))

				one_row_dict["created"] = self.format_date(one_apply.created)
				try:
					one_row_dict["handle_user"] = one_apply.handle_user.first_name
				except:
					one_row_dict["handle_user"] = ""
				one_row_dict["handle_date"] = self.format_date(one_apply.handle_date)
				one_row_dict["reason"] = self.format_none(one_apply.reason)
				one_row_dict["status"] = one_apply.get_status_display()
				rows_list.append(one_row_dict.copy())
			if rows_list:
				name = "leave_apply"
				param = dict(sheetname=name, head_title_list=self.head_list, field_name_list=self.field_list,
							 data_obj_list=rows_list, filename=name)
				export_excel = ExportExcel(**param)
				filepath, filename = export_excel.export()

				# 页面下载导出文件
				response = download_file(filepath, filename, False)
				return response
			else:
				# 导出代表头空文件
				return redirect(reverse('download', args=("leave_apply",)))
		except:
			traceback.print_exc()
			return redirect(reverse('download', args=("leave_apply",)))

	# 备用金申请，导出
	def loan_apply_export(self):
		try:
			kwargs = get_kwargs(self.search_condition)
			apply_info_list = Loan.objects.filter(**kwargs)

			# 组装导出数据
			rows_list = list()
			for one_apply in apply_info_list:
				one_row_dict = defaultdict(str)
				one_row_dict["id"] = str(one_apply.id)
				one_row_dict["title"] = one_apply.title
				one_row_dict["note"] = one_apply.note
				try:
					one_row_dict["apply_user"] = one_apply.apply_user.first_name
				except:
					one_row_dict["apply_user"] = ""

				one_row_dict["money"] = one_apply.money
				one_row_dict["borrowing_date"] = self.format_date(one_apply.borrowing_date)
				one_row_dict["repayment_date"] = self.format_date(one_apply.repayment_date)
				one_row_dict["loan_budget_details"] = get_loan_budget_details(one_apply)

				one_row_dict["created"] = self.format_date(one_apply.created)
				try:
					one_row_dict["handle_user"] = one_apply.handle_user.first_name
				except:
					one_row_dict["handle_user"] = ""
				one_row_dict["handle_date"] = self.format_date(one_apply.handle_date)
				one_row_dict["reason"] = self.format_none(one_apply.reason)
				one_row_dict["status"] = one_apply.get_status_display()
				rows_list.append(one_row_dict.copy())
			if rows_list:
				name = "loan_apply"
				param = dict(sheetname=name, head_title_list=self.head_list, field_name_list=self.field_list,
							 data_obj_list=rows_list, filename=name)
				export_excel = ExportExcel(**param)
				filepath, filename = export_excel.export()

				# 页面下载导出文件
				response = download_file(filepath, filename, True)
				return response
			else:
				# 导出代表头空文件
				return redirect(reverse('download', args=("loan_apply",)))
		except:
			traceback.print_exc()
			return redirect(reverse('download', args=("loan_apply",)))

	# 临时工销账与开票申请，导出
	def temporary_write_offs_billing_apply_export(self):
		try:
			kwargs = get_kwargs(self.search_condition)
			apply_info_list = TemporaryWriteOffsBilling.objects.filter(**kwargs)

			# 组装导出数据
			rows_list = list()
			for one_apply in apply_info_list:
				one_row_dict = defaultdict(str)
				one_row_dict["id"] = str(one_apply.id)
				one_row_dict["title"] = one_apply.title
				one_row_dict["note"] = one_apply.note
				try:
					one_row_dict["apply_user"] = one_apply.apply_user.first_name
				except:
					one_row_dict["apply_user"] = ""

				one_row_dict["billing_month"] = self.format_date(one_apply.billing_month)
				one_row_dict["project_name"] = one_apply.project_name.full_name

				one_row_dict["billing_date"] = self.format_date_day(
					one_apply.billing_date_start) + " -- " + self.format_date_day(
					one_apply.billing_date_end)
				one_row_dict["billing_content"] = one_apply.billing_content
				one_row_dict["billing_type"] = one_apply.get_billing_type_display()
				one_row_dict["main_business_income"] = self.format_none(one_apply.main_business_income)
				one_row_dict["management_fee"] = self.format_none(one_apply.management_fee)
				one_row_dict["wage_receive"] = self.format_none(one_apply.wage_receive)
				one_row_dict["shuttle_fee_receive"] = self.format_none(one_apply.shuttle_fee_receive)
				one_row_dict["meals_receive"] = self.format_none(one_apply.meals_receive)
				one_row_dict["dormitory_fee_receive"] = self.format_none(
					one_apply.dormitory_fee_receive)
				one_row_dict["daily_receive"] = self.format_none(one_apply.daily_receive)
				one_row_dict["compensate_reparation_receive"] = self.format_none(
					one_apply.compensate_reparation_receive)

				one_row_dict["actual_outlay"] = self.format_none(one_apply.actual_outlay)
				one_row_dict["main_business_outlay"] = self.format_none(one_apply.main_business_outlay)
				one_row_dict["wage_outlay"] = self.format_none(one_apply.wage_outlay)
				one_row_dict["shuttle_fee_outlay"] = self.format_none(one_apply.shuttle_fee_outlay)
				one_row_dict["meals_outlay"] = self.format_none(one_apply.meals_outlay)
				one_row_dict["daily_outlay"] = self.format_none(one_apply.daily_outlay)
				one_row_dict["compensate_reparation_outlay"] = self.format_none(
					one_apply.compensate_reparation_outlay)
				one_row_dict["borrow_loan"] = self.format_none(one_apply.borrow_loan)
				one_row_dict["remark1"] = one_apply.remark1
				one_row_dict["difference"] = self.format_none(one_apply.difference)
				one_row_dict["is_billing"] = one_apply.get_is_billing_display()

				one_row_dict["created"] = self.format_date(one_apply.created)
				try:
					one_row_dict["handle_user"] = one_apply.handle_user.first_name
				except:
					one_row_dict["handle_user"] = ""
				one_row_dict["handle_date"] = self.format_date(one_apply.handle_date)
				one_row_dict["reason"] = self.format_none(one_apply.reason)
				one_row_dict["status"] = one_apply.get_status_display()
				rows_list.append(one_row_dict.copy())
			if rows_list:
				name = "temporary_write_offs_billing_apply"
				param = dict(sheetname=name, head_title_list=self.head_list, field_name_list=self.field_list,
							 data_obj_list=rows_list, filename=name)
				export_excel = ExportExcel(**param)
				export_excel.head_title_list = self.head_list
				export_excel.field_name_list = self.field_list
				export_excel.data_obj_list = rows_list
				export_excel.sheetname = "temporary_write_offs_billing_apply"
				export_excel.filename = "temporary_write_offs_billing_apply"
				filepath, filename = export_excel.export()

				# 页面下载导出文件
				response = download_file(filepath, filename, True)
				return response
			else:
				# 导出代表头空文件
				return redirect(reverse('download', args=("temporary_write_offs_billing_apply",)))
		except:
			traceback.print_exc()
			return redirect(reverse('download', args=("temporary_write_offs_billing_apply",)))

	# 工资与职位调整申请，导出
	def wage_apply_export(self):
		try:
			kwargs = get_kwargs(self.search_condition)
			apply_info_list = Wage.objects.filter(**kwargs)

			# 组装导出数据
			rows_list = list()
			for one_apply in apply_info_list:
				one_row_dict = defaultdict(str)
				one_row_dict["id"] = str(one_apply.id)
				one_row_dict["title"] = one_apply.title
				one_row_dict["note"] = one_apply.note
				try:
					one_row_dict["apply_user"] = one_apply.apply_user.first_name
				except:
					one_row_dict["apply_user"] = ""

				one_row_dict["money"] = one_apply.money

				one_row_dict["created"] = self.format_date(one_apply.created)
				try:
					one_row_dict["handle_user"] = one_apply.handle_user.first_name
				except:
					one_row_dict["handle_user"] = ""
				one_row_dict["handle_date"] = self.format_date(one_apply.handle_date)
				one_row_dict["reason"] = self.format_none(one_apply.reason)
				one_row_dict["status"] = one_apply.get_status_display()
				rows_list.append(one_row_dict.copy())
			if rows_list:
				name = "wage_apply"
				param = dict(sheetname=name, head_title_list=self.head_list, field_name_list=self.field_list,
							 data_obj_list=rows_list, filename=name)
				export_excel = ExportExcel(**param)
				filepath, filename = export_excel.export()

				# 页面下载导出文件
				response = download_file(filepath, filename, True)
				return response
			else:
				# 导出代表头空文件
				return redirect(reverse('download', args=("wage_apply",)))
		except:
			traceback.print_exc()
			return redirect(reverse('download', args=("wage_apply",)))

	# 工资补发申请，导出
	def wage_replacement_apply_export(self):
		try:
			kwargs = get_kwargs(self.search_condition)
			apply_info_list = WageReplacement.objects.filter(**kwargs)

			# 组装导出数据
			rows_list = list()
			for one_apply in apply_info_list:
				one_row_dict = defaultdict(str)
				one_row_dict["id"] = str(one_apply.id)
				one_row_dict["title"] = one_apply.title
				one_row_dict["note"] = one_apply.note
				try:
					one_row_dict["apply_user"] = one_apply.apply_user.first_name
				except:
					one_row_dict["apply_user"] = ""

				one_row_dict["wage_replacement_details"] = ""

				one_row_dict["created"] = self.format_date(one_apply.created)
				try:
					one_row_dict["handle_user"] = one_apply.handle_user.first_name
				except:
					one_row_dict["handle_user"] = ""
				one_row_dict["handle_date"] = self.format_date(one_apply.handle_date)
				one_row_dict["reason"] = self.format_none(one_apply.reason)
				one_row_dict["status"] = one_apply.get_status_display()
				rows_list.append(one_row_dict.copy())
			if rows_list:
				name = "wage_replacement_apply"
				param = dict(sheetname=name, head_title_list=self.head_list, field_name_list=self.field_list,
							 data_obj_list=rows_list, filename=name)
				export_excel = ExportExcel(**param)
				filepath, filename = export_excel.export()

				# 页面下载导出文件
				response = download_file(filepath, filename, True)
				return response
			else:
				# 导出代表头空文件
				return redirect(reverse('download', args=("wage_replacement_apply",)))
		except:
			traceback.print_exc()
			return redirect(reverse('download', args=("wage_replacement_apply",)))

	# 报销与销账申请，导出
	def write_offs_apply_export(self):
		try:
			kwargs = get_kwargs(self.search_condition)
			apply_info_list = WriteOffs.objects.filter(**kwargs)

			# 组装导出数据
			rows_list = list()
			for one_apply in apply_info_list:
				one_row_dict = defaultdict(str)
				one_row_dict["id"] = str(one_apply.id)
				one_row_dict["title"] = one_apply.title
				one_row_dict["note"] = one_apply.note
				try:
					one_row_dict["apply_user"] = one_apply.apply_user.first_name
				except:
					one_row_dict["apply_user"] = ""

				one_row_dict["writeoffs_total"] = one_apply.writeoffs_total
				one_row_dict["borrow_imprest"] = one_apply.borrow_imprest
				one_row_dict["imprest_explain"] = one_apply.imprest_explain
				one_row_dict["difference"] = format_difference(one_apply.difference)
				one_row_dict["writeoffs_type"] = one_apply.get_writeoffs_type_display()
				# one_row_dict["write_offs_details"] = get_write_offs_details(one_apply)
				one_row_dict["remark"] = one_apply.remark

				one_row_dict["created"] = self.format_date(one_apply.created)
				try:
					one_row_dict["handle_user"] = one_apply.handle_user.first_name
				except:
					one_row_dict["handle_user"] = ""
				one_row_dict["handle_date"] = self.format_date(one_apply.handle_date)
				one_row_dict["reason"] = self.format_none(one_apply.reason)
				one_row_dict["status"] = one_apply.get_status_display()
				rows_list.append(one_row_dict.copy())
			if rows_list:
				name = "write_offs_apply"
				param = dict(sheetname=name, head_title_list=self.head_list, field_name_list=self.field_list,
							 data_obj_list=rows_list, filename=name)
				export_excel = ExportExcel(**param)
				filepath, filename = export_excel.export()

				# 页面下载导出文件
				response = download_file(filepath, filename, True)
				return response
			else:
				# 导出代表头空文件
				return redirect(reverse('download', args=("write_offs_apply",)))
		except:
			traceback.print_exc()
			return redirect(reverse('download', args=("write_offs_apply",)))

	# 管理人员需求与离职申请，导出
	def demand_turnover_apply_export(self):
		try:
			kwargs = get_kwargs(self.search_condition)
			apply_info_list = DemandTurnover.objects.filter(**kwargs)

			# 组装导出数据
			rows_list = list()
			for one_apply in apply_info_list:
				one_row_dict = defaultdict(str)
				one_row_dict["id"] = str(one_apply.id)
				one_row_dict["title"] = one_apply.title
				one_row_dict["note"] = one_apply.note
				try:
					one_row_dict["apply_user"] = one_apply.apply_user.first_name
				except:
					one_row_dict["apply_user"] = ""

				one_row_dict["created"] = self.format_date(one_apply.created)
				try:
					one_row_dict["handle_user"] = one_apply.handle_user.first_name
				except:
					one_row_dict["handle_user"] = ""
				one_row_dict["handle_date"] = self.format_date(one_apply.handle_date)
				one_row_dict["reason"] = self.format_none(one_apply.reason)
				one_row_dict["status"] = one_apply.get_status_display()
				rows_list.append(one_row_dict.copy())
			if rows_list:
				name = "demand_turnover_apply"
				param = dict(sheetname=name, head_title_list=self.head_list, field_name_list=self.field_list,
							 data_obj_list=rows_list, filename=name)
				export_excel = ExportExcel(**param)
				filepath, filename = export_excel.export()

				# 页面下载导出文件
				response = download_file(filepath, filename, True)
				return response
			else:
				# 导出代表头空文件
				return redirect(reverse('download', args=("demand_turnover_apply",)))
		except:
			traceback.print_exc()
			return redirect(reverse('download', args=("demand_turnover_apply",)))

	# 结算与发薪申请，导出
	def billing_pre_pay_apply_export(self):
		try:
			kwargs = get_kwargs(self.search_condition)
			apply_info_list = BillingPrePay.objects.filter(**kwargs)

			# 组装导出数据
			rows_list = list()
			for one_apply in apply_info_list:
				one_row_dict = defaultdict(str)
				one_row_dict["id"] = str(one_apply.id)
				one_row_dict["title"] = one_apply.title
				one_row_dict["note"] = one_apply.note
				try:
					one_row_dict["apply_user"] = one_apply.apply_user.first_name
				except:
					one_row_dict["apply_user"] = ""

				one_row_dict["billingprepay_month"] = self.format_date(one_apply.billingprepay_month)
				one_row_dict["project_name"] = one_apply.project_name.full_name

				one_row_dict["billing_date"] = self.format_date_day(
					one_apply.billing_date_start) + " -- " + self.format_date_day(
					one_apply.billing_date_end)
				one_row_dict["billing_content"] = one_apply.billing_content
				one_row_dict["main_business_income"] = self.format_none(one_apply.main_business_income)
				one_row_dict["management_fee"] = self.format_none(one_apply.management_fee)
				one_row_dict["wage_receive"] = self.format_none(one_apply.wage_receive)
				one_row_dict["social_security_receive"] = self.format_none(
					one_apply.social_security_receive)
				one_row_dict["provident_fund_receive"] = self.format_none(
					one_apply.provident_fund_receive)
				one_row_dict["union_fee_receive"] = self.format_none(one_apply.union_fee_receive)
				one_row_dict["disablement_gold"] = self.format_none(one_apply.disablement_gold)
				one_row_dict["shuttle_fee_receive"] = self.format_none(one_apply.shuttle_fee_receive)
				one_row_dict["meals_receive"] = self.format_none(one_apply.meals_receive)
				one_row_dict["dormitory_fee_receive"] = self.format_none(
					one_apply.dormitory_fee_receive)
				one_row_dict["daily_receive"] = self.format_none(one_apply.daily_receive)
				one_row_dict["compensate_reparation_receive"] = self.format_none(
					one_apply.compensate_reparation_receive)
				one_row_dict["bonus_receive"] = self.format_none(one_apply.bonus_receive)
				one_row_dict["other_receive"] = self.format_none(one_apply.other_receive)
				one_row_dict["grant_total"] = self.format_none(one_apply.grant_total)
				one_row_dict["ccb"] = self.format_none(one_apply.ccb)
				one_row_dict["merchants_bank"] = self.format_none(one_apply.merchants_bank)
				one_row_dict["icbc"] = self.format_none(one_apply.icbc)
				one_row_dict["other_bank"] = self.format_none(one_apply.other_bank)
				one_row_dict["remark1"] = one_apply.remark1

				one_row_dict["created"] = self.format_date(one_apply.created)
				try:
					one_row_dict["handle_user"] = one_apply.handle_user.first_name
				except:
					one_row_dict["handle_user"] = ""
				one_row_dict["handle_date"] = self.format_date(one_apply.handle_date)
				one_row_dict["reason"] = self.format_none(one_apply.reason)
				one_row_dict["status"] = one_apply.get_status_display()
				rows_list.append(one_row_dict.copy())
			if rows_list:
				name = "billing_pre_pay_apply"
				param = dict(sheetname=name, head_title_list=self.head_list, field_name_list=self.field_list,
							 data_obj_list=rows_list, filename=name)
				export_excel = ExportExcel(**param)
				filepath, filename = export_excel.export()

				# 页面下载导出文件
				response = download_file(filepath, filename, True)
				return response
			else:
				# 导出代表头空文件
				return redirect(reverse('download', args=("billing_pre_pay_apply",)))
		except:
			traceback.print_exc()
			return redirect(reverse('download', args=("billing_pre_pay_apply",)))

	# 待招结算与销账申请，导出
	def recruitedbilling_apply_export(self):
		try:
			kwargs = get_kwargs(self.search_condition)
			apply_info_list = RecruitedBilling.objects.filter(**kwargs)

			# 组装导出数据
			rows_list = list()
			for one_apply in apply_info_list:
				one_row_dict = defaultdict(str)
				one_row_dict["id"] = str(one_apply.id)
				one_row_dict["title"] = one_apply.title
				one_row_dict["note"] = one_apply.note
				try:
					one_row_dict["apply_user"] = one_apply.apply_user.first_name
				except:
					one_row_dict["apply_user"] = ""

				one_row_dict["project_name"] = one_apply.project_name.full_name
				one_row_dict["billing_month"] = self.format_date(one_apply.billing_month)
				one_row_dict["settlement_amount"] = one_apply.settlement_amount
				one_row_dict["is_billing"] = one_apply.get_is_billing_display()
				one_row_dict["content"] = one_apply.content
				one_row_dict["recruitedbilling_details"] = get_recruitedbilling_details(one_apply)

				one_row_dict["created"] = self.format_date(one_apply.created)
				try:
					one_row_dict["handle_user"] = one_apply.handle_user.first_name
				except:
					one_row_dict["handle_user"] = ""
				one_row_dict["handle_date"] = self.format_date(one_apply.handle_date)
				one_row_dict["reason"] = self.format_none(one_apply.reason)
				one_row_dict["status"] = one_apply.get_status_display()
				rows_list.append(one_row_dict.copy())
			if rows_list:
				name = "recruited_billing_apply"
				param = dict(sheetname=name, head_title_list=self.head_list, field_name_list=self.field_list,
							 data_obj_list=rows_list, filename=name)
				export_excel = ExportExcel(**param)
				filepath, filename = export_excel.export()

				# 页面下载导出文件
				response = download_file(filepath, filename, True)
				return response
			else:
				# 导出代表头空文件
				return redirect(reverse('download', args=("recruited_billing_apply",)))
		except:
			traceback.print_exc()
			return redirect(reverse('download', args=("loan_apply",)))

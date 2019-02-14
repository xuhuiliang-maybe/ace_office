# coding=utf-8
from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect
from django.views.generic import View

from modules.finance.social_security_audit.models import *
from modules.share_module.download import download_file
from modules.share_module.export import ExportExcel
from modules.share_module.formater import *
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs


@class_view_decorator(login_required)
@class_view_decorator(permission_required('social_security_audit.export_socialsecurityaudit', raise_exception=True))
class SocialSecurityAuditExportView(View):
	def get(self, request, *args, **kwargs):

		head_list = [u"编号", u'姓名', u'身份证号', u'入职时间', u'离职时间', u'项目名称', u"部门", u"项目负责人", u'社保月份',
			     u'社保结算', u'社保支出', u'社保平衡', u'公积金结算', u'公积金支出',
			     u'公积金平衡', u'备注']
		field_list = ["id", "name", "identity_card_number", "entry_date", "departure_date",
			      "project_name_full_name",
			      "job_dept", "project_name_principal", "social_security_date", "social_security_billing",
			      "social_security_outlay", "social_security_balance", "provident_fund_billing",
			      "provident_fund_outlay", "provident_fund_balance", "remark"]

		try:
			self.social_security_date = self.request.GET.get("social_security_date", "")  # 社保月份
			self.name = self.request.GET.get("name", "")  # 姓名
			self.identity_card_number = self.request.GET.get("identity_card_number", "")  # 身份证号
			self.job_dept = self.request.GET.get("job_dept", "")  # 部门名称
			self.project_name = self.request.GET.get("project_name", "")  # 项目名称
			self.social_security_balance = self.request.GET.get("social_security_balance", "")  # 社保平衡
			self.provident_fund_balance = self.request.GET.get("provident_fund_balance", "")  # 公积金平衡

			if self.social_security_date:
				social_security_date = date_formater(self.social_security_date, "%Y-%m-%d")
				social_security_date_year = social_security_date.year
				social_security_date_month = social_security_date.month
			else:
				social_security_date_year = timezone.now().year
				social_security_date_month = timezone.now().month
				self.social_security_date = timezone.now().strftime("%Y-%m-%d")

			search_condition = {
				"social_security_date__year": social_security_date_year,
				"social_security_date__month": social_security_date_month,
				"name__icontains": self.name,
				"identity_card_number__icontains": self.identity_card_number,
				"employee__job_dept__icontains": self.job_dept,
				"employee__project_name__full_name__icontains": self.project_name,
				"social_security_balance": self.social_security_balance,
				"provident_fund_balance": self.provident_fund_balance,
			}

			kwargs = get_kwargs(search_condition)
			social_security_audit_list = SocialSecurityAudit.objects.filter(**kwargs)

			# 组装导出数据
			rows_list = list()
			for one_data in social_security_audit_list:
				one_row_dict = defaultdict(str)
				one_row_dict["id"] = one_data.id  # 编号
				one_row_dict["name"] = one_data.name  # 姓名
				one_row_dict["identity_card_number"] = one_data.identity_card_number

				if one_data.employee:
					# 入职日期
					one_row_dict["entry_date"] = one_data.employee.entry_date.strftime(
						"%Y-%m-%d") if one_data.employee.entry_date else ''

					# 离职日期
					one_row_dict[
						"departure_date"] = one_data.employee.departure_date.strftime(
						"%Y-%m-%d") if one_data.employee.departure_date else ''

					# 项目名称, 项目负责人
					if one_data.employee.project_name:
						one_row_dict[
							"project_name_full_name"] = one_data.employee.project_name.full_name
						one_row_dict["job_dept"] = one_data.employee.job_dept  # 部门
						one_row_dict[
							"project_name_principal"] = one_data.employee.project_name.principal.first_name
					else:
						one_row_dict["project_name_full_name"] = ""  # 项目名称
						one_row_dict["job_dept"] = one_data.employee.job_dept  # 部门
						one_row_dict["project_name_principal"] = ""  # 项目负责人

				else:
					one_row_dict["entry_date"] = ""  # 入职时间
					one_row_dict["departure_date"] = ""  # 离职时间
					one_row_dict["project_name_full_name"] = ""  # 项目名称
					one_row_dict["job_dept"] = ""  # 部门
					one_row_dict["project_name_principal"] = ""  # 项目负责人

				# 社保月份
				one_row_dict["social_security_date"] = one_data.social_security_date.strftime(
					"%Y-%m") if one_data.social_security_date else ''

				# 社保结算
				one_row_dict["social_security_billing"] = one_data.social_security_billing
				# 社保支出
				one_row_dict["social_security_outlay"] = one_data.social_security_outlay
				# 社保平衡
				one_row_dict["social_security_balance"] = one_data.get_social_security_balance_display()

				# 公积金结算
				one_row_dict["provident_fund_billing"] = one_data.provident_fund_billing
				# 公积金支出
				one_row_dict["provident_fund_outlay"] = one_data.provident_fund_outlay
				# 公积金平衡
				one_row_dict["provident_fund_balance"] = one_data.get_provident_fund_balance_display()
				one_row_dict["remark"] = one_data.remark  # 备注
				rows_list.append(one_row_dict.copy())

			if rows_list:
				name = "social_security_audit"
				param = dict(sheetname=name, head_title_list=head_list, field_name_list=field_list,
							 data_obj_list=rows_list, filename=name)

				export_excel = ExportExcel(**param)
				filepath, filename = export_excel.export()
				# 页面下载导出文件
				response = download_file(filepath, filename, True)
				return response
			else:
				# 导出代表头空文件
				return redirect(reverse('download', args=("social_security_audit",)))
		except:
			traceback.print_exc()

# coding=utf-8
from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import View

from modules.finance.arrival_and_billing.models import *
from modules.share_module.download import download_file
from modules.share_module.export import ExportExcel
from modules.share_module.formater import *
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs


@class_view_decorator(login_required)
@class_view_decorator(permission_required('arrival_and_billing.export_arrivalandbilling', raise_exception=True))
class ArrivalAndBillingExportView(View):
	def get(self, request, *args, **kwargs):

		head_list = [u"编号", u'项目名称', u'结算月份', u'结算金额（长期业务）', u'结算金额（临时工）', u'结算合计', u"到账金额合计", u"到账时间",
			     u"到账情况", u"开票金额合计", u"开票时间", u"开票情况"]
		field_list = ["id", "project_name", "settlement_date", "settlement_amount_long",
			      "settlement_amount_snap", "settlement_tatol", "credited_amount_total",
			      "credited_date", "credited_state", "billing_amount_total",
			      "billing_date", "billing_state"]

		try:
			self.settlement_date = self.request.GET.get("settlement_date", "")  # 项目名称

			settlement_date_year = ""
			settlement_date_month = ""
			if self.settlement_date:
				settlement_date_date = date_formater(self.settlement_date, "%Y-%m-%d")
				settlement_date_year = settlement_date_date.year
				settlement_date_month = settlement_date_date.month

			search_condition = {
				"settlement_date__year": settlement_date_year,
				"settlement_date__month": settlement_date_month,
			}
			if not self.request.user.is_superuser and self.view_type == "1":
				search_condition.update({"apply_user": self.request.user})

			kwargs = get_kwargs(search_condition)
			arrival_and_billing_list = ArrivalAndBilling.objects.filter(**kwargs)

			# 组装导出数据
			rows_list = list()
			for one_data in arrival_and_billing_list:
				one_row_dict = defaultdict(str)
				one_row_dict["id"] = one_data.id  # 编号
				one_row_dict["project_name"] = one_data.project_name.full_name  # 项目名称

				# 结算月份
				one_row_dict["settlement_date"] = one_data.settlement_date.strftime(
					"%Y-%m-%d") if one_data.settlement_date else ''
				one_row_dict["settlement_amount_long"] = one_data.settlement_amount_long  # 结算金额（长期业务）
				one_row_dict["settlement_amount_snap"] = one_data.settlement_amount_snap  # 结算金额（临时工）
				one_row_dict["settlement_tatol"] = one_data.settlement_tatol  # 结算合计
				one_row_dict["credited_amount_total"] = one_data.credited_amount_total  # 到账金额合计
				one_row_dict["credited_date"] = one_data.credited_date.strftime(
					"%Y-%m-%d") if one_data.credited_date else ''  # 到账时间
				one_row_dict["credited_state"] = one_data.get_credited_state_display()  # 到账情况
				one_row_dict["billing_amount_total"] = one_data.billing_amount_total  # 开票金额合计
				one_row_dict["billing_date"] = one_data.billing_date.strftime(
					"%Y-%m-%d") if one_data.billing_date else ''  # 开票时间
				one_row_dict["billing_state"] = one_data.get_billing_state_display()  # 开票情况

				rows_list.append(one_row_dict.copy())

			if rows_list:
				param = dict(sheetname="arrival_and_billing", head_title_list=head_list, field_name_list=field_list,
							 data_obj_list=rows_list, filename="arrival_and_billing")
				export_excel = ExportExcel(**param)
				filepath, filename = export_excel.export()
				# 页面下载导出文件
				response = download_file(filepath, filename, True)
				return response
			else:
				# 导出代表头空文件
				return redirect(reverse('download', args=("arrival_and_billing",)))
		except:
			traceback.print_exc()

# coding=utf-8
from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import View

from modules.finance.loans_and_write_offs.models import *
from modules.share_module.download import download_file
from modules.share_module.export import ExportExcel
from modules.share_module.formater import *
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs


@class_view_decorator(login_required)
@class_view_decorator(permission_required('loans_and_write_offs.export_loansandwriteoffs', raise_exception=True))
class LoansAndWriteOffsExportView(View):
	def get(self, request, *args, **kwargs):

		head_list = [u"编号", u'姓名', u'借款时间', u'借款用途', u'借款金额', u'销账金额', u"销账时间", u"备注"]
		field_list = ["id", "apply_user", "borrowing_date", "note", "money", "amount_write_offs",
			      "write_offs_date", "remark"]

		try:
			self.name = self.request.GET.get("name", "")  # 姓名
			self.start_borrowing_date = self.request.GET.get("start_borrowing_date", "")  # 起始借款时间
			self.end_borrowing_date = self.request.GET.get("end_borrowing_date", "")  # 终止借款时间
			self.money = self.request.GET.get("money", "")  # 借款金额

			start_borrowing_date, end_borrowing_date = "", ""
			if self.start_borrowing_date and self.end_borrowing_date:
				start_borrowing_date = datetime.datetime.strptime(self.start_borrowing_date, "%Y-%m-%d")
				end_borrowing_date = datetime.datetime.strptime(self.end_borrowing_date, "%Y-%m-%d")

			search_condition = {
				"loan__apply_user__first_name__icontains": self.name,
				"loan__money": self.money,
				"loan__borrowing_date__gte": start_borrowing_date,
				"loan__borrowing_date__lte": end_borrowing_date,
			}
			kwargs = get_kwargs(search_condition)
			loans_and_write_offs_list = LoansAndWriteOffs.objects.filter(**kwargs)

			# 组装导出数据
			rows_list = list()
			for one_data in loans_and_write_offs_list:
				one_row_dict = defaultdict(str)
				if one_data.loan:
					one_row_dict["id"] = one_data.id  #
					one_row_dict["apply_user"] = one_data.loan.apply_user.first_name  # 姓名

					# 借款时间
					one_row_dict["borrowing_date"] = one_data.loan.borrowing_date.strftime(
						"%Y-%m-%d") if one_data.loan.borrowing_date else ''
					one_row_dict["note"] = one_data.loan.note  # 借款用途
					one_row_dict["money"] = one_data.loan.money  # 借款金额
				else:
					one_row_dict["name"] = ""  # 姓名
					one_row_dict["borrowing_date"] = ""  # 借款时间
					one_row_dict["note"] = ""  # 借款用途
					one_row_dict["money"] = ""  # 借款金额
				one_row_dict["amount_write_offs"] = one_data.amount_write_offs  # 项目负责人
				one_row_dict["write_offs_date"] = one_data.write_offs_date.strftime(
					"%Y-%m-%d") if one_data.write_offs_date else ''  # 销账时间
				one_row_dict["remark"] = one_data.remark  # 备注

				rows_list.append(one_row_dict.copy())

			if rows_list:
				# 实例化导出类
				export_excel = ExportExcel()
				export_excel.sheetname = "loans_and_write_offs"
				export_excel.head_title_list = head_list
				export_excel.field_name_list = field_list
				export_excel.data_obj_list = rows_list
				export_excel.filename = "loans_and_write_offs"
				filepath, filename = export_excel.export()
				# 页面下载导出文件
				response = download_file(filepath, filename, True)
				return response
			else:
				# 导出代表头空文件
				return redirect(reverse('download', args=("loans_and_write_offs",)))
		except:
			traceback.print_exc()

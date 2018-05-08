# coding=utf-8
from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import ListView, View

from modules.recruitment_manage.templatetags.recruitment_manage_tags import *
from modules.share_module.download import download_file
from modules.share_module.export import ExportExcel
from modules.share_module.formater import *
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs
from config.conf_core import PAGINATE
"""
招聘统计
"""


# 招聘统计
@class_view_decorator(login_required)
@class_view_decorator(permission_required('admin_account.browse_job_statistic', raise_exception=True))
class JobStatisticListView(ListView):
	context_object_name = "employee_list"
	template_name = "job_statistic.html"
	allow_empty = True
	paginate_by = PAGINATE

	def get_queryset(self):
		try:
			self.project_name = self.request.GET.get("project_name", "")  # 项目名称
			self.recruitment_attache = self.request.GET.get("recruitment_attache", "")  # 招聘人员
			self.query_month = self.request.GET.get("query_month", "")  # 查询月度

			search_condition = {
				"project_name__full_name__icontains": self.project_name,
				"recruitment_attache__first_name__icontains": self.recruitment_attache,
			}

			if not self.query_month:
				# 默认显示当月入职
				search_condition.update({
					"entry_date__year": timezone.now().year,
					"entry_date__month": timezone.now().month
				})
			else:
				# 按查询月份筛选
				query_month = date_formater(self.query_month, "%Y/%m/%d")
				search_condition.update(
					{
						"entry_date__year": query_month.year,
						"entry_date__month": query_month.month
					})
			# 动态组合去重条件

			kwargs = get_kwargs(search_condition)
			# order_by配合distinct，去重，values决定取那些参数
			emps_dict = Employee.objects.values(
				"recruitment_attache",
				"project_name"
			).order_by("recruitment_attache").distinct().filter(**kwargs)

			# 计算招聘人数合计
			self.total_recruitment = 0
			for one_dict in emps_dict:
				self.total_recruitment += project_emp_count(one_dict)

			return emps_dict
		except:
			traceback.print_exc()

	def get_context_data(self, **kwargs):
		context = super(JobStatisticListView, self).get_context_data(**kwargs)
		context["project_name"] = self.project_name
		context["recruitment_attache"] = self.recruitment_attache
		context["total_recruitment"] = self.total_recruitment
		context["export_url"] = reverse('recruitment:job_statistic_export')
		context["query_month"] = self.query_month
		return context


# 导出招聘统计
@class_view_decorator(login_required)
@class_view_decorator(permission_required('admin_account.export_job_statistic', raise_exception=True))
class JobStatisticExportView(View):
	def get(self, request, *args, **kwargs):
		head_list = [u'招聘人员', u'项目名称', u'招聘人数,合计：', u'累计在职天数',
			     u'招聘提成', u'临时工招聘提成']
		field_list = ["recruitment_attache", "project_name", "hiring", "in_service_days",
			      "recruitment_commission", "temporary_recruitment_commission"]

		try:
			project_name = self.request.GET.get("project_name", "")  # 项目名称
			recruitment_attache = self.request.GET.get("recruitment_attache", "")  # 招聘人员
			query_month = self.request.GET.get("query_month", "")  # 查询月度

			search_condition = {
				"project_name__full_name__icontains": project_name,
				"recruitment_attache__first_name__icontains": recruitment_attache,
			}

			if not query_month:
				# 默认显示当月入职
				search_condition.update({
					"entry_date__year": timezone.now().year,
					"entry_date__month": timezone.now().month
				})
			else:
				# 按查询月份筛选
				query_month = date_formater(query_month, "%Y/%m/%d")
				search_condition.update(
					{
						"entry_date__year": query_month.year,
						"entry_date__month": query_month.month
					})

			kwargs = get_kwargs(search_condition)
			emps_dict_list = Employee.objects.values("recruitment_attache", "project_name").order_by(
				"recruitment_attache").distinct().filter(**kwargs)

			# 组装导出数据
			rows_list = list()
			total_recruitment = 0
			for emps_dict in emps_dict_list:
				total_recruitment += project_emp_count(emps_dict)  # 计算招聘人数合计
				one_row_dict = defaultdict(str)
				one_row_dict["recruitment_attache"] = get_recruitment_attache(emps_dict)  # 招聘人员
				one_row_dict["project_name"] = get_project_name(emps_dict)  # 项目名称
				one_row_dict["hiring"] = project_emp_count(emps_dict)  # 招聘人数
				one_row_dict["in_service_days"] = grand_total_work_days(emps_dict)  # 累计在职天数
				one_row_dict["recruitment_commission"] = grand_total_recruitment_commission(emps_dict,
													    "employee")  # 招聘提成
				one_row_dict["temporary_recruitment_commission"] = grand_total_recruitment_commission(
					emps_dict, "temporary")  # 临时工招聘提成
				rows_list.append(one_row_dict.copy())

			head_list[2] += str(total_recruitment)  # 为表头-招聘人数，增加合计数

			if rows_list:
				# 实例化导出类
				export_excel = ExportExcel()
				export_excel.head_title_list = head_list
				export_excel.field_name_list = field_list
				export_excel.data_obj_list = rows_list
				export_excel.sheetname = "JobStatistic"
				export_excel.filename = "JobStatistic"
				filepath, filename = export_excel.export()

				# 页面下载导出文件
				response = download_file(filepath, filename, True)
				return response
			else:
				# 导出代表头空文件
				return redirect(reverse('download', args=("job_statistic_info",)))
		except:
			traceback.print_exc()

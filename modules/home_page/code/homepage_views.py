# coding=utf-8
from __future__ import division

import datetime
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import View

from modules.approval_process.billing_pre_pay.models import BillingPrePay
from modules.approval_process.demand_turnover.models import DemandTurnover
from modules.approval_process.leave.models import Leave
from modules.approval_process.loan.models import Loan
from modules.approval_process.models import *
from modules.approval_process.recruited_billing.models import RecruitedBilling
from modules.approval_process.temporary_write_offs_billing.models import TemporaryWriteOffsBilling
from modules.approval_process.wage.models import Wage
from modules.approval_process.wage_replacement.models import WageReplacement
from modules.approval_process.write_offs.models import WriteOffs
from modules.personnel_operation.models import *
from modules.share_module.permissionMixin import class_view_decorator

COLOR_LIST = [
	"#6666FF", "#FFFF66", "#66CC99", "#FF6699", "#CCCC66", "#CC99FF", "#999966", "#CC6666",
	"#666666", "#FF66FF", "#99FF66", "#CCCCCC", "#FFFFCC", "#669999", "#888888", "#990000",
	"#6666FF", "#FFFF66", "#66CC99", "#FF6699", "#CCCC66", "#CC99FF", "#999966", "#CC6666",
]


@class_view_decorator(login_required)
@class_view_decorator(permission_required('admin_account.browse_index', raise_exception=True))
class IndexView(View):
	def get(self, request, *args, **kwargs):
		self.result_dict = dict()  # 视图最终返回数据结构

		try:
			# 获取基础数据
			self.get_init_data()

			# 服务人数
			self.get_number_of_incumbency()  # 获取在职人数
			self.get_number_of_entry()  # 获取入职人数
			self.get_number_of_departure()  # 获取离职人数

			# 操作失误
			self.get_number_of_operational_errors()  # 获取操作失误数

			# 审批
			self.get_about_approval()  # 获取关于审批数据
		except:
			traceback.print_exc()

		return render_to_response("index.html", self.result_dict, context_instance=RequestContext(request))

	def get_init_data(self):
		try:
			self.now = datetime.datetime.now()
			self.employee_obj = Employee.objects
			self.all_emp_count = self.employee_obj.count()  # 所有员工数
			self.is_active_emp_count = self.employee_obj.filter(status="1").count()  # 所有在职员工
			self.projects_for_login_user = Project.objects.filter(principal=self.request.user)  # 当前用户负责项目

			self.kefu_list = list()  # 客服部子部门名称
			self.kefu_obj_list = list()  # 客服部子部门对象
			customer_service_dept = Department.objects.filter(name=u"客服部")
			if customer_service_dept.exists():
				self.kefu_obj_list = customer_service_dept[0].AllChildren()
				for one_kefu in self.kefu_obj_list:
					self.kefu_list.append(one_kefu.name)

			self.result_dict.update({"all_emp_count": self.all_emp_count})  # 全部员工数
			self.result_dict.update({"is_active_emp_count": self.is_active_emp_count})  # 全部在职员工数
		except:
			traceback.print_exc()

	# 获取在职人数
	def get_number_of_incumbency(self):
		try:
			# 目前公司在职人数及各客服部人数占比，饼状图,number_of_incumbency_a
			data_list = list()

			# 各客服部占比
			kefu_scale = 0
			for index, one_kefu in enumerate(self.kefu_list):
				one_kefu_count = self.employee_obj.filter(status="1", project_name__department__name=one_kefu).count()
				try:
					scale = round(one_kefu_count / self.all_emp_count, 4)
				except:
					traceback.print_exc()
					scale = 0
				color = COLOR_LIST[index + 1]
				data_list.append({"label": one_kefu, "data": scale, "color": color})
				kefu_scale += scale

			# 其他部门占比
			other_dept_count = self.employee_obj.filter(status="1").exclude(project_name__department__name__in=self.kefu_list).count()
			try:
				other_dept_scale = round(other_dept_count / self.all_emp_count, 4)
			except:
				traceback.print_exc()
				other_dept_scale = 0
			data_list.append({"label": u"其他部门", "data": other_dept_scale, "color": COLOR_LIST[len(self.kefu_list) + 1]})

			# 其他占比
			other_scale = round(1 - kefu_scale - other_dept_scale, 4)
			data_list.append({"label": u"其他", "data": other_scale, "color": COLOR_LIST[len(self.kefu_list) + 2]})
			self.result_dict.update({"number_of_incumbency_a": json.dumps(data_list)})

			# 目前公司在职人数及登陆用户负责项目人数占比，饼状图，number_of_incumbency_b
			data_list = list()
			login_user_emp_count = 0  # 登录用户负责项目员工数
			if self.projects_for_login_user:
				login_user_emp_count = self.employee_obj.filter(project_name__in=self.projects_for_login_user).count()
			try:
				scale = round(login_user_emp_count / self.all_emp_count, 4)
			except:
				scale = 0
			data_list.append({"label": u"我负责项目", "data": scale, "color": COLOR_LIST[0]})

			other_project_emp_count = self.employee_obj.exclude(project_name__in=self.projects_for_login_user).count()
			try:
				other_project_scale = round(other_project_emp_count / self.all_emp_count, 4)
			except:
				other_project_scale = 0
			data_list.append({"label": u"其他项目", "data": other_project_scale, "color": COLOR_LIST[1]})

			data_list.append({"label": u"其他", "data": round(1 - scale - other_project_scale, 4), "color": COLOR_LIST[2]})
			self.result_dict.update({"login_user_emp_count": login_user_emp_count}) # 登录用户负责项目员工数
			self.result_dict.update({"number_of_incumbency_b": json.dumps(data_list)})
		except:
			traceback.print_exc()

	# 获取入职人数
	def get_number_of_entry(self):
		try:
			# 当月公司整体入职人数，及各客服部入职人数与占比，饼状图
			data_list = list()
			tist_month_join_count = self.employee_obj.filter(entry_date__year=self.now.year, entry_date__month=self.now.month).count()

			kefu_scale = 0
			for index, one_kefu in enumerate(self.kefu_list):
				one_kefu_count = self.employee_obj.filter(entry_date__year=self.now.year,
									 entry_date__month=self.now.month,
									 project_name__department__name=one_kefu).count()
				try:
					scale = round(one_kefu_count / self.all_emp_count, 4)
				except:
					scale = 0
				color = COLOR_LIST[index + 1]
				data_list.append({"label": one_kefu, "data": scale, "color": color})
				kefu_scale += scale

			other_dept_emp_count = self.employee_obj.filter(
				entry_date__year=self.now.year,
				entry_date__month=self.now.month).exclude(project_name__department__name__in=self.kefu_list).count()
			try:
				other_dept_scale = round(other_dept_emp_count / self.all_emp_count, 4)
			except:
				other_dept_scale = 0

			data_list.append({"label": u"其他部门", "data": other_dept_scale, "color": COLOR_LIST[len(self.kefu_list) + 1]})
			other_scale = round(1 - kefu_scale - other_dept_scale, 4)
			data_list.append({"label": u"其他", "data": other_scale, "color": COLOR_LIST[len(self.kefu_list) + 2]})
			self.result_dict.update({"number_of_entry_a": json.dumps(data_list)})
			self.result_dict.update({"tist_month_join_count": tist_month_join_count})

			# 当月，自己负责项目的入职人数，及占比（整个公司占比），饼状图
			data_list = list()
			login_user_emp_count = self.employee_obj.filter(entry_date__year=self.now.year,
								       entry_date__month=self.now.month,
								       project_name__in=self.projects_for_login_user).count()
			try:
				scale = round(login_user_emp_count / self.all_emp_count, 4)
			except:
				scale = 0
			data_list.append({"label": u"我负责项目", "data": scale, "color": COLOR_LIST[0]})

			other_project_emp_count = self.employee_obj.filter(
				entry_date__year=self.now.year,
				entry_date__month=self.now.month).exclude(project_name__in=self.projects_for_login_user).count()
			try:
				other_project_scale = round(other_project_emp_count / self.all_emp_count, 4)
			except:
				other_project_scale = 0

			data_list.append({"label": u"其他项目", "data": other_project_scale, "color": COLOR_LIST[1]})
			data_list.append({"label": u"其他", "data": round(1 - scale - other_project_scale, 4), "color": COLOR_LIST[2]})
			self.result_dict.update({"number_of_entry_b": json.dumps(data_list)})

			# 昨天整个公司入职人数，及各客服部入职人数与占比，饼状图
			data_list = list()
			yesterday = self.now - datetime.timedelta(days=1)

			yesterday_kefu_scale = 0
			for index, one_kefu in enumerate(self.kefu_list):
				one_kefu_count = self.employee_obj.filter(entry_date=yesterday, project_name__department__name=one_kefu).count()
				try:
					scale = round(one_kefu_count / self.all_emp_count, 4)
				except:
					scale = 0
				color = COLOR_LIST[index + 1]
				data_list.append({"label": one_kefu, "data": scale, "color": color})
				yesterday_kefu_scale += scale

			other_dept_emp_count = self.employee_obj.filter(entry_date=yesterday).exclude(
				project_name__department__name__in=self.kefu_list).count()
			try:
				other_dept_scale = round(other_dept_emp_count / self.all_emp_count, 4)
			except:
				other_dept_scale = 0

			data_list.append(
				{"label": u"其他部门", "data": other_dept_scale,
				 "color": COLOR_LIST[len(self.kefu_list) + 1]})
			data_list.append({"label": u"其他", "data": round(1 - yesterday_kefu_scale - other_dept_scale, 4),
					  "color": COLOR_LIST[len(self.kefu_list) + 2]})
			self.result_dict.update({"number_of_entry_c": json.dumps(data_list)})

			# 昨天，自己负责项目的入职人数，及占比（整个公司占比），饼状图
			data_list = list()
			yesterday_login_user_for_emp_count = self.employee_obj.filter(entry_date=yesterday,
										     project_name__in=self.projects_for_login_user).count()
			try:
				scale = round(yesterday_login_user_for_emp_count / self.all_emp_count, 4)
			except:
				scale = 0
			data_list.append({"label": u"我负责项目", "data": scale, "color": COLOR_LIST[0]})

			other_project_emp_count = self.employee_obj.filter(entry_date=yesterday).exclude(
				project_name__in=self.projects_for_login_user).count()
			try:
				other_project_scale = round(other_project_emp_count / self.all_emp_count, 4)
			except:
				other_project_scale = 0

			data_list.append({"label": u"其他项目", "data": other_project_scale, "color": COLOR_LIST[1]})
			data_list.append(
				{"label": u"其他", "data": round(1 - yesterday_login_user_for_emp_count - other_project_scale, 4),
				 "color": COLOR_LIST[2]})

			self.result_dict.update({"number_of_entry_d": json.dumps(data_list)})
		except:
			traceback.print_exc()

	# 获取离职人数
	def get_number_of_departure(self):
		try:
			# 当月公司整体离职人数，及各客服部离职人数与占比，饼状图
			data_list = list()
			tist_month_departure_count = self.employee_obj.filter(departure_date__year=self.now.year,
									     departure_date__month=self.now.month).count()

			kefu_scale = 0
			for index, one_kefu in enumerate(self.kefu_list):
				one_kefu_count = self.employee_obj.filter(departure_date__year=self.now.year,
									 departure_date__month=self.now.month,
									 project_name__department__name=one_kefu).count()
				try:
					scale = round(one_kefu_count / self.all_emp_count, 4)
				except:
					scale = 0
				color = COLOR_LIST[index + 1]
				data_list.append({"label": one_kefu, "data": scale, "color": color})
				kefu_scale += scale

			other_dept_emp_count = self.employee_obj.filter(
				departure_date__year=self.now.year,
				departure_date__month=self.now.month).exclude(project_name__department__name__in=self.kefu_list).count()
			try:
				other_dept_scale = round(other_dept_emp_count / self.all_emp_count, 4)
			except:
				other_dept_scale = 0

			data_list.append(
				{"label": u"其他部门", "data": other_dept_scale,
				 "color": COLOR_LIST[len(self.kefu_list) + 1]})
			other_scale = 1 - kefu_scale - other_dept_scale
			data_list.append(
				{"label": u"其他", "data": round(other_scale, 4), "color": COLOR_LIST[len(self.kefu_list) + 2]})
			self.result_dict.update({"number_of_departure_a": json.dumps(data_list)})
			self.result_dict.update({"tist_month_departure_count": tist_month_departure_count})

			# 当月，自己负责项目的离职人数，及占比（整个公司占比），饼状图
			data_list = list()
			login_user_emp_count = self.employee_obj.filter(departure_date__year=self.now.year,
								       departure_date__month=self.now.month,
								       project_name__in=self.projects_for_login_user).count()
			try:
				scale = round(login_user_emp_count / self.all_emp_count, 4)
			except:
				scale = 0
			data_list.append({"label": u"我负责项目", "data": scale, "color": COLOR_LIST[0]})

			other_project_emp_count = self.employee_obj.filter(
				departure_date__year=self.now.year,
				departure_date__month=self.now.month).exclude(
				project_name__in=self.projects_for_login_user).count()
			try:
				other_project_scale = round(other_project_emp_count / self.all_emp_count, 4)
			except:
				other_project_scale = 0

			data_list.append({"label": u"其他项目", "data": other_project_scale, "color": COLOR_LIST[1]})
			data_list.append(
				{"label": u"其他", "data": round(1 - scale - other_project_scale, 4), "color": COLOR_LIST[2]})
			self.result_dict.update({"number_of_departure_b": json.dumps(data_list)})

			# 昨天整个公司离职人数，及各客服部离职人数与占比，饼状图
			data_list = list()
			yesterday = self.now - datetime.timedelta(days=1)

			yesterday_kefu_scale = 0
			for index, one_kefu in enumerate(self.kefu_list):
				one_kefu_count = self.employee_obj.filter(departure_date=yesterday,
									 project_name__department__name=one_kefu).count()
				try:
					scale = round(one_kefu_count / self.all_emp_count, 4)
				except:
					scale = 0
				color = COLOR_LIST[index + 1]
				data_list.append({"label": one_kefu, "data": scale, "color": color})
				yesterday_kefu_scale += scale

			other_dept_emp_count = self.employee_obj.filter(departure_date=yesterday).exclude(
				project_name__department__name__in=self.kefu_list).count()
			try:
				other_dept_scale = round(other_dept_emp_count / self.all_emp_count, 4)
			except:
				other_dept_scale = 0

			data_list.append(
				{"label": u"其他部门", "data": other_dept_scale,
				 "color": COLOR_LIST[len(self.kefu_list) + 1]})
			data_list.append({"label": u"其他", "data": round(1 - yesterday_kefu_scale - other_dept_scale ,4),
					  "color": COLOR_LIST[len(self.kefu_list) + 2]})
			self.result_dict.update({"number_of_departure_c": json.dumps(data_list)})

			# 昨天，自己负责项目的离职人数，及占比（整个公司占比），饼状图
			data_list = list()
			yesterday_login_user_for_emp_count = self.employee_obj.filter(departure_date=yesterday,
										     project_name__in=self.projects_for_login_user).count()
			try:
				scale = round(yesterday_login_user_for_emp_count / self.all_emp_count, 4)
			except:
				scale = 0
			data_list.append({"label": u"我负责项目", "data": scale, "color": COLOR_LIST[0]})

			other_project_emp_count = self.employee_obj.filter(departure_date=yesterday).exclude(
				project_name__in=self.projects_for_login_user).count()
			try:
				other_project_scale = round(other_project_emp_count / self.all_emp_count, 4)
			except:
				other_project_scale = 0

			data_list.append({"label": u"其他项目", "data": other_project_scale, "color": COLOR_LIST[1]})
			data_list.append(
				{"label": u"其他", "data": round(1 - yesterday_login_user_for_emp_count - other_project_scale, 4),
				 "color": COLOR_LIST[2]})

			self.result_dict.update({"number_of_departure_d": json.dumps(data_list)})
		except:
			traceback.print_exc()

	# 获取操作失误数
	def get_number_of_operational_errors(self):
		try:
			# 当月公司整体操作失误数及各客服部操作失误数占比，饼状图
			data_list = list()
			tist_month_muff_count = QualityAssurance.objects.filter(create_date__year=self.now.year,
										create_date__month=self.now.month).count()

			kefu_scale = 0
			for index, one_kefu in enumerate(self.kefu_obj_list):
				one_kefu_count = QualityAssurance.objects.filter(create_date__year=self.now.year,
										 create_date__month=self.now.month,
										 department=one_kefu).count()
				try:
					scale = round(one_kefu_count / self.all_emp_count, 4)
				except:
					scale = 0
				color = COLOR_LIST[index + 1]
				data_list.append({"label": one_kefu.name, "data": scale, "color": color})
				kefu_scale += scale

			other_dept_muff_count = QualityAssurance.objects.filter(
				create_date__year=self.now.year,
				create_date__month=self.now.month).exclude(department__in=self.kefu_obj_list).count()
			try:
				other_dept_scale = round(other_dept_muff_count / self.all_emp_count, 4)
			except:
				other_dept_scale = 0

			data_list.append(
				{"label": u"其他部门", "data": other_dept_scale,
				 "color": COLOR_LIST[len(self.kefu_list) + 1]})
			other_scale = 1 - kefu_scale - other_dept_scale
			data_list.append(
				{"label": u"其他", "data": other_scale, "color": COLOR_LIST[len(self.kefu_list) + 2]})
			self.result_dict.update({"number_of_operational_a": json.dumps(data_list)})
			self.result_dict.update({"tist_month_muff_count": tist_month_muff_count})

			# 当月，自己的操作失误数，及占比（整个公司占比），饼状图
			data_list = list()
			login_user_muff_count = QualityAssurance.objects.filter(create_date__year=self.now.year,
										create_date__month=self.now.month,
										provider=self.request.user).count()
			try:
				scale = round(login_user_muff_count / self.all_emp_count, 4)
			except:
				scale = 0
			data_list.append({"label": u"我操作失误", "data": scale, "color": COLOR_LIST[0]})

			other_user_muff_count = QualityAssurance.objects.filter(
				create_date__year=self.now.year,
				create_date__month=self.now.month).exclude(provider=self.request.user).count()
			try:
				other_user_muff_scale = round(other_user_muff_count / self.all_emp_count, 4)
			except:
				other_user_muff_scale = 0

			data_list.append({"label": u"其他人操作失误", "data": other_user_muff_scale, "color": COLOR_LIST[1]})
			data_list.append(
				{"label": u"其他", "data": round(1 - scale - other_user_muff_scale, 4), "color": COLOR_LIST[2]})
			self.result_dict.update({"number_of_operational_b": json.dumps(data_list)})
			self.result_dict.update({"login_user_muff_count": login_user_muff_count})

			# 到目前为止，没有改善的操作失误数（需要重点提示）-点击后能跳到操作失误数的页面
			is_not_improve_count = QualityAssurance.objects.filter(improve_status__name=u"持续").count()
			is_not_improve_url = reverse('personnel_info:personnel_list', args=()) + "?improve_status=2"
			self.result_dict.update({"is_not_improve_count": is_not_improve_count})  # 为改善数量
			self.result_dict.update({"is_not_improve_url": is_not_improve_url})  # 未改善超链
		except:
			traceback.print_exc()

	# 获取关于审批数据
	def get_about_approval(self):
		try:
			# 需要自己审批的申请数量（需要重点提示），以及自己审批过的申请数量，点击后进入审批页面
			self_approval_count = self.get_self_approval_count()
			self_approval_count_url = reverse('approval:pending_list') + "?handle_user=" + str(self.request.user.id)
			self.result_dict.update({"self_approval_count": self_approval_count})
			self.result_dict.update({"self_approval_count_url": self_approval_count_url})

			# 所有抄送我的审批中我还没有点开浏览的数量（重点提示），抄送给我的审批总数，点击后可跳到抄送给我的审批页面

			# 自己走的申请，还没有批完的数量，和自己已经提报的申请数量，点击进入自己已经提报的申请页面
			self.get_self_apply_count()
		except:
			traceback.print_exc()

	# 当前登录用户各个类型申请数量，超链信息
	def get_self_apply_count(self):
		kwargs = {"apply_user": self.request.user}
		try:
			# 请假
			self_apply_leave_count = Leave.objects.filter(**kwargs).count()
			self_apply_leave_count_url = reverse('approval:leave_list')
			self.result_dict.update({"self_apply_leave_count": self_apply_leave_count})
			self.result_dict.update({"self_apply_leave_count_url": self_apply_leave_count_url})

			# 备用金
			self_apply_loan_count = Loan.objects.filter(**kwargs).count()
			self_apply_loan_count_url = reverse('approval:loan_list')
			self.result_dict.update({"self_apply_loan_count": self_apply_loan_count})
			self.result_dict.update({"self_apply_loan_count_url": self_apply_loan_count_url})

			# 报销与销账
			self_apply_writeoffs_count = WriteOffs.objects.filter(**kwargs).count()
			self_apply_writeoffs_count_url = reverse('approval:write_offs_list')
			self.result_dict.update({"self_apply_writeoffs_count": self_apply_writeoffs_count})
			self.result_dict.update({"self_apply_writeoffs_count_url": self_apply_writeoffs_count_url})

			# 工资与职位调整
			self_apply_wage_count = Wage.objects.filter(**kwargs).count()
			self_apply_wage_count_url = reverse('approval:wage_list')
			self.result_dict.update({"self_apply_wage_count": self_apply_wage_count})
			self.result_dict.update({"self_apply_wage_count_url": self_apply_wage_count_url})

			# 工资补发申请
			self_apply_wagereplacement_count = WageReplacement.objects.filter(**kwargs).count()
			self_apply_wagereplacement_count_url = reverse('approval:wage_replacement_list')
			self.result_dict.update({"self_apply_wagereplacement_count": self_apply_wagereplacement_count})
			self.result_dict.update(
				{"self_apply_wagereplacement_count_url": self_apply_wagereplacement_count_url})

			# 结算与发薪
			self_apply_billingprepay_count = BillingPrePay.objects.filter(**kwargs).count()
			self_apply_billingprepay_count_url = reverse('approval:billing_pre_pay_list')
			self.result_dict.update({"self_apply_billingprepay_count": self_apply_billingprepay_count})
			self.result_dict.update(
				{"self_apply_billingprepay_count_url": self_apply_billingprepay_count_url})

			# 管理人员需求与离职
			self_apply_demandturnover_count = DemandTurnover.objects.filter(**kwargs).count()
			self_apply_demandturnover_count_url = reverse('approval:demand_turnover_list')
			self.result_dict.update({"self_apply_demandturnover_count": self_apply_demandturnover_count})
			self.result_dict.update(
				{"self_apply_demandturnover_count_url": self_apply_demandturnover_count_url})

			# 临时工销账与开票
			self_apply_temporarywriteoffsbilling_count = TemporaryWriteOffsBilling.objects.filter(
				**kwargs).count()
			self_apply_temporarywriteoffsbilling_count_url = reverse(
				'approval:temporary_write_offs_billing_list')
			self.result_dict.update({
				"self_apply_temporarywriteoffsbilling_count": self_apply_temporarywriteoffsbilling_count})
			self.result_dict.update({
				"self_apply_temporarywriteoffsbilling_count_url": self_apply_temporarywriteoffsbilling_count_url})

			# 代招结算与销账
			self_apply_recruitedbilling_count = RecruitedBilling.objects.filter(**kwargs).count()
			self_apply_recruitedbilling_count_url = reverse('approval:recruitedbilling_list')
			self.result_dict.update(
				{"self_apply_recruitedbilling_count": self_apply_recruitedbilling_count})
			self.result_dict.update(
				{"self_apply_recruitedbilling_count_url": self_apply_recruitedbilling_count_url})
		except:
			traceback.print_exc()

	# 自己审批过的申请数量
	def get_self_approval_count(self):
		self_approval_count = 0
		kwargs = {"handle_user": self.request.user}
		try:
			self_approval_count += Leave.objects.filter(**kwargs).count()  # 请假
			self_approval_count += Loan.objects.filter(**kwargs).count()  # 备用金
			self_approval_count += WriteOffs.objects.filter(**kwargs).count()  # 报销与销账
			self_approval_count += Wage.objects.filter(**kwargs).count()  # 工资与职位调整
			self_approval_count += WageReplacement.objects.filter(**kwargs).count()  # 工资补发申请
			self_approval_count += BillingPrePay.objects.filter(**kwargs).count()  # 结算与发薪
			self_approval_count += DemandTurnover.objects.filter(**kwargs).count()  # 管理人员需求与离职
			self_approval_count += TemporaryWriteOffsBilling.objects.filter(**kwargs).count()  # 临时工销账与开票
			self_approval_count += RecruitedBilling.objects.filter(**kwargs).count()  # 代招结算与销账
		except:
			traceback.print_exc()
		finally:
			return self_approval_count

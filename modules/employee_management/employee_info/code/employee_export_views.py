# coding=utf-8
from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import View

from modules.employee_management.employee_info.models import Employee
from modules.share_module.download import download_file
from modules.share_module.export import ExportExcel
from modules.share_module.formater import *
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs


@class_view_decorator(login_required)
@class_view_decorator(permission_required('employee_info.export_employee', raise_exception=True))
class EmployeeExportView(View):
	def get(self, request, *args, **kwargs):

		employee_type = self.request.GET.get("employee_type", "")
		head_list = list()
		field_list = list()
		if employee_type == "employee":
			head_list = [u'姓名（必填）', u'服务部门', u'身份证号（必填）', u'目前状态(在职/离职)', u'项目名称（必填）', u'银行卡号', u'开户银行',
				     u'部门', u'职务', u'性别(男/女)', u'民族', u'学历', u'出生年月(2016-01-01)', u'员工年龄', u'户口所在地',
				     u'户口邮编', u'户口性质', u'工作地', u'社保地', u'人员属性', u'合同属性', u'合同主体',
				     u'入职日期(2016-01-01)', u'#DIV/0!01+', u"社保支付卡", u"开户银行", u'#DIV/0!02+',
				     u'公积金增员日期(2016-01-01)', u'合同开始日期(2016-01-01)', u'试用期限', u'合同期限', u'试用到期日期(2016-01-01)',
				     u'合同到期日期(2016-01-01)', u'合同续签次数', u'离职日期(2016-01-01)', u'离职手续', u'离职原因',
				     u'#DIV/0!01-', u'#DIV/0!02-', u'公积金减员日期(2016-01-01)', u'联系电话', u'紧急联系人',
				     u'与联系人关系', u'紧急联系人电话', u'招聘渠道', u'招聘人员', u'客服专员', u'客服主管',
				     u'外包主管', u'客服经理', u'其他负责人']
			field_list = ["name", "attribution_dept", "identity_card_number", "status", "project_name",
				      "salary_card_number", "bank_account", "job_dept", "position", "sex", "nation",
				      "education",
				      "birthday", "age", "register_address", "register_postcode", "register_type",
				      "work_address", "insured_place", "person_type", "contract_type",
				      "contract_subject",
				      "entry_date", "social_insurance_increase_date", "social_security_payment_card",
				      "use_bank",
				      "business_insurance_increase_date", "provident_fund_increase_date",
				      "contract_begin_date",
				      "probation_period", "contract_period", "probation_end_date", "contract_end_date",
				      "contract_renew_times", "departure_date", "departure_procedure",
				      "departure_cause",
				      "social_insurance_reduce_date", "business_insurance_reduce_date",
				      "provident_fund_reduce_date", "phone_number", "contact_person",
				      "contact_relationship",
				      "contact_person_phone", "recruitment_channel", "recruitment_attache",
				      "customer_service_staff", "customer_service_charge", "outsource_director",
				      "customer_service_director", "other_responsible_person"]
		elif employee_type == "temporary":
			head_list = [u"姓名", u"性别", u"身份证号", u"项目名称", u"服务部门", u"招聘人员", u"联系电话", u"开始工作日",
				     u"结束工作日", u"工作天数", u"小时数", u"发放金额", u"发放人", u"发放时间", u"备注1"]
			field_list = ["name", "sex", "identity_card_number", "project_name", "attribution_dept",
				      "recruitment_attache", "phone_number", "start_work_date",
				      "end_work_date", "work_days", "hours", "amount_of_payment", "release_user",
				      "release_time", "remark1"]

		try:
			# 员工查询
			status = self.request.GET.get("status", "")  # 目前状态
			project_name = self.request.GET.get("project_name", "")  # 项目名称
			dept_name = self.request.GET.get("dept_name", "")  # 服务部门
			principal = self.request.GET.get("principal", "")  # 项目负责人
			name = self.request.GET.get("name", "")  # 姓名
			identity_card_number = self.request.GET.get("identity_card_number", "")  # 身份证号
			person_type = int(self.request.GET.get("person_type", 0))  # 人员属性
			contract_type = self.request.GET.get("contract_type", "")  # 合同属性

			# 临时员工查询
			phone_number = self.request.GET.get("phone_number", "")  # 联系方式
			recruitment_attache = self.request.GET.get("recruitment_attache", "")  # 招聘人员
			st_release_time = self.request.GET.get("st_release_time", "")  # 发放起始时间
			et_release_time = self.request.GET.get("et_release_time", "")  # 发放终止日期
			self.start_time = self.request.GET.get("start_time", "")  # 创建起始时间
			self.end_time = self.request.GET.get("end_time", "")  # 创建终止时间

			if self.start_time and self.end_time:
				self.start_time += " 00:00:01"
				self.end_time +=" 23:59:59"
				self.start_time = date_formater(self.start_time, "%Y/%m/%d %X")
				self.end_time = date_formater(self.end_time, "%Y/%m/%d %X")

			try:
				user_position = self.request.user.position.name  # 用户岗位
			except:
				user_position = ""
			position_list = [u"客服专员", u"客服主管", u"外包主管", u"客服经理"]
			if user_position in position_list:  # 登录用户在客服部，只能查看所在部门员工信息
				dept_name = self.request.user.attribution_dept

			search_condition = {
				"status": status,
				"project_name__full_name__icontains": project_name,
				"project_name__principal__first_name__icontains": principal,
				"name__icontains": name,
				"identity_card_number__icontains": identity_card_number,
				"person_type": person_type,
				"contract_type": contract_type,
				"phone_number": phone_number,
				"recruitment_attache__first_name__icontains": recruitment_attache,
				"release_time__gte": st_release_time,
				"release_time__lte": et_release_time,
				"create_time__gte": self.start_time,
				"create_time__lte": self.end_time
			}
			if dept_name:
				search_condition.update(
					{"project_name__department__name__in": dept_name.split(",")})

			kwargs = get_kwargs(search_condition)
			if employee_type == "employee":  # 查看员工信息
				kwargs.update({"is_temporary": False})
			elif employee_type == "temporary":  # 查看临时工信息
				kwargs.update({"is_temporary": True})
			employee_obj_list = Employee.objects.filter(**kwargs)

			# 组装导出数据
			rows_list = list()
			if employee_type == "employee":
				for one_employee_obj in employee_obj_list:
					one_row_dict = defaultdict(str)
					one_row_dict["name"] = one_employee_obj.name  # 姓名
					if one_employee_obj.project_name:
						one_row_dict["attribution_dept"] = one_employee_obj.project_name.department.name if one_employee_obj.project_name.department else ""  # 服务部门
					else:
						one_row_dict["attribution_dept"] = ""  # 服务部门
					one_row_dict["identity_card_number"] = one_employee_obj.identity_card_number  # 身份证号
					one_row_dict["status"] = one_employee_obj.get_status_display()  # 目前状态
					if one_employee_obj.project_name:
						one_row_dict[
							"project_name"] = one_employee_obj.project_name.full_name  # 项目名称
					else:
						one_row_dict["project_name"] = ""  # 项目名称
					one_row_dict["salary_card_number"] = one_employee_obj.salary_card_number  # 银行卡号
					one_row_dict["bank_account"] = one_employee_obj.bank_account  # 开户银行
					one_row_dict["job_dept"] = one_employee_obj.job_dept  # 部门
					one_row_dict["position"] = one_employee_obj.position  # 职务
					one_row_dict["sex"] = one_employee_obj.get_sex_display()  # 性别
					one_row_dict["nation"] = one_employee_obj.get_nation_display()  # 民族
					one_row_dict["education"] = one_employee_obj.get_education_display()  # 学历
					one_row_dict["birthday"] = one_employee_obj.birthday.strftime(
						"%Y-%m-%d") if one_employee_obj.birthday else ''  # 出生年月
					if one_employee_obj.age:
						one_row_dict["age"] = int(one_employee_obj.age)  # 年龄
					else:
						one_row_dict["age"] = ""
					one_row_dict["register_address"] = one_employee_obj.register_address  # 户口所在地
					one_row_dict["register_postcode"] = one_employee_obj.register_postcode  # 户口邮编
					one_row_dict[
						"register_type"] = one_employee_obj.get_register_type_display()  # 户口性质
					one_row_dict["work_address"] = one_employee_obj.work_address  # 工作地
					one_row_dict["insured_place"] = one_employee_obj.insured_place  # 社保地
					if one_employee_obj.person_type:
						one_row_dict["person_type"] = one_employee_obj.person_type.name  # 人员属性
					else:
						one_row_dict["person_type"] = ""  # 人员属性
					one_row_dict[
						"contract_type"] = one_employee_obj.get_contract_type_display()  # 合同属性
					if one_employee_obj.contract_subject:
						one_row_dict[
							"contract_subject"] = one_employee_obj.contract_subject.name  # 合同主体
					else:
						one_row_dict["contract_subject"] = ""  # 合同主体
					one_row_dict["entry_date"] = one_employee_obj.entry_date.strftime(
						"%Y-%m-%d") if one_employee_obj.entry_date else ''  # 入职日期
					one_row_dict[
						"social_insurance_increase_date"] = one_employee_obj.social_insurance_increase_date.strftime(
						"%Y-%m-%d") if one_employee_obj.social_insurance_increase_date else ''  # 社保增员日期
					one_row_dict[
						"social_security_payment_card"] = one_employee_obj.social_security_payment_card
					one_row_dict["use_bank"] = one_employee_obj.use_bank
					one_row_dict[
						"business_insurance_increase_date"] = one_employee_obj.business_insurance_increase_date.strftime(
						"%Y-%m-%d") if one_employee_obj.business_insurance_increase_date else ''  # 商保增员日期
					one_row_dict[
						"provident_fund_increase_date"] = one_employee_obj.provident_fund_increase_date.strftime(
						"%Y-%m-%d") if one_employee_obj.provident_fund_increase_date else ''  # 公积金增员日期
					one_row_dict[
						"contract_begin_date"] = one_employee_obj.contract_begin_date.strftime(
						"%Y-%m-%d") if one_employee_obj.contract_begin_date else ''  # 合同开始日期
					if one_employee_obj.probation_period:
						one_row_dict["probation_period"] = int(
							one_employee_obj.probation_period)  # 使用期限
					else:
						one_row_dict["probation_period"] = ""
					if one_employee_obj.contract_period:
						one_row_dict["contract_period"] = int(
							one_employee_obj.contract_period)  # 合同期限
					else:
						one_row_dict["contract_period"] = ""
					one_row_dict[
						"probation_end_date"] = one_employee_obj.probation_end_date.strftime(
						"%Y-%m-%d") if one_employee_obj.probation_end_date else ''  # 试用到期日期
					one_row_dict["contract_end_date"] = one_employee_obj.contract_end_date.strftime(
						"%Y-%m-%d") if one_employee_obj.contract_end_date else ''  # 合同到期日期
					if one_employee_obj.contract_renew_times:
						one_row_dict["contract_renew_times"] = int(
							one_employee_obj.contract_renew_times)  # 合同续签次数
					else:
						one_row_dict["contract_renew_times"] = ""
					one_row_dict["departure_date"] = one_employee_obj.departure_date.strftime(
						"%Y-%m-%d") if one_employee_obj.departure_date else ''  # 离职日期
					one_row_dict[
						"departure_procedure"] = one_employee_obj.get_departure_procedure_display()  # 离职手续
					one_row_dict["departure_cause"] = one_employee_obj.departure_cause  # 离职原因
					one_row_dict[
						"social_insurance_reduce_date"] = one_employee_obj.social_insurance_reduce_date.strftime(
						"%Y-%m-%d") if one_employee_obj.social_insurance_reduce_date else ''  # 社保减员日期
					one_row_dict[
						"business_insurance_reduce_date"] = one_employee_obj.business_insurance_reduce_date.strftime(
						"%Y-%m-%d") if one_employee_obj.business_insurance_reduce_date else ''  # 商保减员日期
					one_row_dict[
						"provident_fund_reduce_date"] = one_employee_obj.provident_fund_reduce_date.strftime(
						"%Y-%m-%d") if one_employee_obj.provident_fund_reduce_date else ''  # 公积金减员日期
					one_row_dict["phone_number"] = one_employee_obj.phone_number  # 联系电话
					one_row_dict["contact_person"] = one_employee_obj.contact_person  # 紧急联系人
					one_row_dict[
						"contact_relationship"] = one_employee_obj.contact_relationship  # 与联系人关系
					one_row_dict[
						"contact_person_phone"] = one_employee_obj.contact_person_phone  # 紧急联系人电话
					one_row_dict[
						"recruitment_channel"] = one_employee_obj.get_recruitment_channel_display()  # 招聘渠道
					try:
						one_row_dict[
							"recruitment_attache"] = one_employee_obj.recruitment_attache.first_name  # 招聘人员
					except:
						one_row_dict["recruitment_attache"] = ""  # 招聘人员
					try:
						one_row_dict["customer_service_staff"] = one_employee_obj.project_name.customer_service_staff.first_name  # 客户专员
					except:
						one_row_dict["customer_service_staff"] = ""
					try:
						one_row_dict["customer_service_charge"] = one_employee_obj.project_name.customer_service_charge.first_name  # 客服主管
					except:
						one_row_dict["customer_service_director"] = ""
					try:
						one_row_dict[
							"outsource_director"] = one_employee_obj.project_name.outsource_director.first_name  # 外包主管
					except:
						one_row_dict["outsource_director"] = ""
					try:
						one_row_dict[
							"customer_service_director"] = one_employee_obj.project_name.customer_service_director.first_name  # 客服经理
					except:
						one_row_dict["customer_service_director"] = ""
					try:
						one_row_dict["other_responsible_person"] = one_employee_obj.project_name.other_responsible_person.first_name  # 其他负责人
					except:
						one_row_dict["other_responsible_person"] = ""
					rows_list.append(one_row_dict.copy())
			elif employee_type == "temporary":
				for one_employee_obj in employee_obj_list:
					one_row_dict = defaultdict(str)
					one_row_dict["name"] = one_employee_obj.name  # 姓名
					one_row_dict["sex"] = one_employee_obj.get_sex_display()  # 性别
					one_row_dict[
						"identity_card_number"] = one_employee_obj.identity_card_number  # 身份证号
					if one_employee_obj.project_name:
						one_row_dict[
							"project_name"] = one_employee_obj.project_name.full_name  # 项目名称
					else:
						one_row_dict["project_name"] = ""  # 项目名称
					one_row_dict["attribution_dept"] = one_employee_obj.project_name.department.name  # 服务部门
					try:
						one_row_dict["recruitment_attache"] = one_employee_obj.recruitment_attache.first_name  # 招聘人员
					except:
						one_row_dict["recruitment_attache"] = ""  # 招聘人员
					one_row_dict["phone_number"] = one_employee_obj.phone_number  # 联系电话
					one_row_dict["start_work_date"] = one_employee_obj.start_work_date.strftime(
						"%Y-%m-%d") if one_employee_obj.start_work_date else ''  # 开始工作日
					one_row_dict["end_work_date"] = one_employee_obj.end_work_date.strftime(
						"%Y-%m-%d") if one_employee_obj.end_work_date else ''  # 结束工作日
					one_row_dict["work_days"] = one_employee_obj.work_days  # 工作天数
					one_row_dict["hours"] = one_employee_obj.hours  # 小时数
					one_row_dict["amount_of_payment"] = one_employee_obj.amount_of_payment  # 发放金额
					try:
						one_row_dict["release_user"] = one_employee_obj.release_user.first_name  # 发放人
					except:
						one_row_dict["release_user"] = ""  # 发放人
					one_row_dict["release_time"] = one_employee_obj.release_time.strftime(
						"%Y-%m-%d") if one_employee_obj.release_time else ''  # 发放时间
					one_row_dict["remark1"] = one_employee_obj.remark1  # 备注1

					rows_list.append(one_row_dict.copy())

			if rows_list:
				# 实例化导出类
				export_excel = ExportExcel()
				export_excel.head_title_list = head_list
				export_excel.field_name_list = field_list
				export_excel.data_obj_list = rows_list
				if employee_type == "employee":
					export_excel.sheetname = "Employee"
					export_excel.filename = "Employee"
				elif employee_type == "temporary":
					export_excel.sheetname = "Temporary"
					export_excel.filename = "Temporary"

				filepath, filename = export_excel.export()

				# 页面下载导出文件
				response = download_file(filepath, filename, True)
				return response
			else:
				# 导出只有表头信息的空文件
				if employee_type == "employee":
					return redirect(reverse('download', args=("employee_info",)))
				elif employee_type == "temporary":
					return redirect(reverse('download', args=("temporary_info",)))
		except:
			traceback.print_exc()

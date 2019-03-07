# coding=utf-8
import xlrd
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.views.generic import View

from modules.employee_management.employee_info.models import *
from modules.organizational_structure.profiles.models import Profile
from modules.project_manage.models import Project
from modules.share_module.formater import *
from modules.share_module.get_path import *
from modules.share_module.load_info import LoadInfoUploadForm
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
class LoadEmployeeView(View):
	def post(self, request, *args, **kwargs):
		emp_type = kwargs.get("emp_type", "")  # 导入员工类型
		perm = self.request.user.has_perm('employee_info.add_%s' % emp_type)
		if not perm:
			raise PermissionDenied
		try:
			upload_form = LoadInfoUploadForm(request.POST, request.FILES)
			if upload_form.is_valid():
				upload_file_obj = upload_form.cleaned_data['load_info']  # 上传文件对象
				upload_file_name = upload_file_obj.name
				upload_file_path = os.path.join(get_media_sub_path("tmp"), upload_file_name)

				# 将上传文件暂存tmp目录
				data = ""
				for chunk in upload_file_obj.chunks():
					data += chunk
				f = file(upload_file_path, "wb")
				f.write(data)
				f.close()

				# 执行导入数据库
				if emp_type == "employee":  # 员工信息
					return self.load_employee(upload_file_path)
				elif emp_type == "temporary":  # 临时工信息
					return self.load_temporary(upload_file_path)

			messages.warning(self.request, u"无文件上传！")
			if emp_type == "employee":  # 员工信息
				return redirect(reverse('employee_info:list', args=("employee",)))
			elif emp_type == "temporary":  # 临时工信息
				return redirect(reverse('employee_info:list', args=("temporary",)))
		except:
			traceback.print_exc()
			messages.warning(self.request, u"导入异常！")
			if emp_type == "employee":  # 员工信息
				return redirect(reverse('employee_info:list', args=("employee",)))
			elif emp_type == "temporary":  # 临时工信息
				return redirect(reverse('employee_info:list', args=("temporary",)))

	def get_choice_dict(self, choice_tuple):
		return_dict = dict()
		for one_choice in choice_tuple:
			return_dict.update({one_choice[1]: one_choice[0]})
		return return_dict

	def load_employee(self, filepath):
		"""执行导入
		:param filepath:导入文件路径
		:return:total："total": 总行数, "import": 成功导入数, "repeat": 已存在未导入数
		"""
		login_user = self.request.user
		try:
			# 读取模板
			data = xlrd.open_workbook(filepath)
			table = data.sheets()[0]  # 通过索引顺序获取,工作表
			nrows = table.nrows  # 行数
			# ncols = table.ncols  # 列数

			# 组装数据
			# colnames = table.row_values(0)  # 表头数据
			import_num = 0  # 导入数
			repeat_num = 0  # 重复导入
			competence_num = 0  # 非负责项目
			no_project_num = 0  # 无项目信息
			total = nrows - 1

			nation_dict = self.get_choice_dict(NATION_CHOICES)  # 民族字典
			education_dict = self.get_choice_dict(EDUCATION_CHOICES)  # 学历字典
			registertype_dict = self.get_choice_dict(REGISTERTYPE_CHOICES)  # 户口性质字典
			is_work_dict = self.get_choice_dict(IS_WORK)  # 目前状态字典
			gender_dict = self.get_choice_dict(GENDER_CHOICES)  # 性别字典
			recruitment_channel_dict = self.get_choice_dict(RECRUITMENTCHANNEL_CHOICES)  # 招聘渠道
			contract_type_dict = self.get_choice_dict(CONTRACT_CHOICES)  # 合同属性
			departure_procedure_dict = self.get_choice_dict(DIMISSION_PROCEDURE_CHOICES)  # 离职手续

			messages_warning = ""
			for rowindex in xrange(1, nrows):  # 默认略过标题行,从第一行开始
				row = table.row_values(rowindex)
				if row:
					if not row[5]:
						no_project_num += 1
						continue

					project_name = Project.get_project_by_full_name_or_short_name(row[5])  # 项目信息
					try:
						if not login_user.is_superuser:
							principal = project_name.principal
							if login_user != principal:
								competence_num += 1
								continue
					except:
						traceback.print_exc()
					try:
						# 身份证号+姓名重复时，更新员工原有信息
						emp_obj = Employee.objects.filter(identity_card_number=row[3], name=row[1], status="1")
						if emp_obj.exists():
							repeat_num += 1
							emp_obj.update(
								salary_card_number=row[6],  # 银行卡号
								bank_account=row[7],  # 开户银行
								project_name=project_name,
								birthday=get_excel_date(row[13]),  # 出生年月
								entry_date=get_excel_date(row[23]),  # 入职日期
								call_out_time=get_excel_date(row[24]),  # 调出日期
								into_time=get_excel_date(row[25]),  # 转入日期

								social_insurance_increase_date=get_excel_date(row[26]),  # 社保增员日期
								provident_fund_increase_date=get_excel_date(row[30]),  # 公积金增员日期
								contract_begin_date=get_excel_date(row[32]),  # 合同开始日期
								departure_date=get_excel_date(row[37]),  # 离职日期
								social_insurance_reduce_date=get_excel_date(row[40]),  # 社保减员日期
								business_insurance_reduce_date=get_excel_date(row[41]),  # 商保减员日期
								provident_fund_reduce_date=get_excel_date(row[42]),  # 公积金减员日期
							)
							continue

						create_result = Employee.objects.create(
							name=row[1],  # 姓名
							identity_card_number=row[3],  # 身份证号
							status=is_work_dict.get(row[4], "1"),  # 目前状态
							project_name=project_name,  # 项目名称
							salary_card_number=row[6],  # 银行卡号
							bank_account=row[7],  # 开户银行
							job_dept=row[8],  # 部门
							position=row[9],  # 职务
							sex=gender_dict.get(row[10], ""),  # 性别
							nation=nation_dict.get(row[11], "1"),  # 民族
							education=education_dict.get(row[12], ""),  # 学历
							birthday=get_excel_date(row[13]),  # 出生年月
							age=get_excel_int(row[14]),  # 员工年龄
							register_address=row[15],  # 户口所在地
							register_postcode=str(get_excel_int(row[16], True)),  # 户口邮编
							register_type=registertype_dict.get(row[17], ""),  # 户口性质
							work_address=row[18],  # 工作地
							insured_place=row[19],  # 社保地
							person_type=ContractType.get_dict_item_by_name(row[20]),  # 人员属性
							contract_type=contract_type_dict.get(row[21], ""),  # 合同属性
							contract_subject=CompanySubject.get_dict_item_by_name(row[22]),  # 合同主体
							entry_date=get_excel_date(row[23]),  # 入职日期
							call_out_time=get_excel_date(row[24]),  # 调出日期
							into_time=get_excel_date(row[25]),  # 转入日期
							social_insurance_increase_date=get_excel_date(row[26]),  # 社保增员日期
							social_security_payment_card=row[27],  # 社保支付卡
							use_bank=row[28],  # 开户银行
							business_insurance_increase_date=get_excel_date(row[29]),  # 商保增员日期
							provident_fund_increase_date=get_excel_date(row[30]),  # 公积金增员日期
							contract_begin_date=get_excel_date(row[31]),  # 合同开始日期
							probation_period=get_excel_int(row[32]),  # 试用期限
							contract_period=get_excel_int(row[33]),  # 合同期限
							probation_end_date=get_excel_date(row[34]),  # 试用期日期
							contract_end_date=get_excel_date(row[35]),  # 合同到期日期
							contract_renew_times=get_excel_int(row[36]),  # 合同续签次数
							departure_date=get_excel_date(row[37]),  # 离职日期
							departure_procedure=departure_procedure_dict.get(row[38], ""),  # 离职手续
							departure_cause=row[39],  # 离职原因
							social_insurance_reduce_date=get_excel_date(row[40]),  # 社保减员日期
							business_insurance_reduce_date=get_excel_date(row[41]),  # 商保减员日期
							provident_fund_reduce_date=get_excel_date(row[42]),  # 公积金减员日期
							phone_number=str(get_excel_int(row[43], True)),  # 联系电话
							contact_person=row[44],  # 紧急联系人
							contact_relationship=row[45],  # 与联系人关系
							contact_person_phone=str(get_excel_int(row[46], True)),  # 紧急联系人电话
							recruitment_channel=recruitment_channel_dict.get(row[47], ""),  # 招聘渠道
							recruitment_attache=Profile.get_user_by_username_or_first_name(row[48]),  # 招聘人员
						)
						import_num += 1
					except:
						messages_warning += str(rowindex) + ","
						traceback.print_exc()

			os.remove(filepath)

			if messages_warning:
				messages.warning(self.request, messages_warning + u"行数据格式错误！")

			msg = u"导入成功，记录总数共%s条，" % total
			if import_num: msg += u"新增%s条，" % import_num
			if repeat_num: msg += u"更新(银行卡号)：%s条，" % repeat_num
			if competence_num: msg += u"非负责项目(未录入)：%s条，" % competence_num
			if no_project_num: msg += u"无项目信息(未录入)：%s条," % no_project_num
			messages.success(self.request, msg)
			return redirect(reverse('employee_info:list', args=("employee",)))
		except:
			traceback.print_exc()
			messages.warning(self.request, u"第%s行数据导入异常！" % (rowindex))
			return redirect(reverse('employee_info:list', args=("employee",)))

	def load_temporary(self, filepath):
		"""执行导入
		:param filepath:导入文件路径
		:return:total："total": 总行数, "import": 成功导入数, "repeat": 已存在未导入数
		"""
		login_user = self.request.user
		try:
			# 读取模板
			data = xlrd.open_workbook(filepath)
			table = data.sheets()[0]  # 通过索引顺序获取,工作表
			nrows = table.nrows  # 行数
			# ncols = table.ncols  # 列数

			# 组装数据
			# colnames = table.row_values(0)  # 表头数据
			import_num = 0  # 导入数
			repeat_num = 0  # 重复导入
			competence_num = 0  # 非负责项目
			no_project_num = 0  # 无责项目信息
			total = nrows - 1

			gender_dict = self.get_choice_dict(GENDER_CHOICES)  # 性别字典

			messages_warning = ""
			for rowindex in xrange(1, nrows):  # 默认略过标题行,从第一行开始
				row = table.row_values(rowindex)
				if row:
					if not row[3]:
						no_project_num += 1
						continue

					project_name = None
					if not login_user.is_superuser:
						project_name = Project.get_project_by_full_name_or_short_name(row[3])  # 项目信息
						principal = ""
						if project_name:
							principal = project_name.principal
						if login_user != principal:
							competence_num += 1
					try:
						emp_obj = Employee.objects.filter(name=row[0], identity_card_number=row[2])
						if emp_obj.exists():
							repeat_num += 1
							continue

						create_result = Employee.objects.create(
							is_temporary=True,
							name=row[0],  # 姓名
							sex=gender_dict.get(row[1], ""),  # 性别
							identity_card_number=row[2],  # 身份证号
							project_name=project_name,  # 项目名称
							job_dept=row[4],  # 服务部门
							recruitment_attache=Profile.get_user_by_username_or_first_name(row[5]),  # 招聘人员
							phone_number=row[6],  # 联系电话
							start_work_date=get_excel_date(row[7]),  # 开始工作日
							end_work_date=get_excel_date(row[8]),  # 结束工作日
							work_days=get_excel_int(row[9]),  # 工作天数
							hours=get_excel_int(row[10]),  # 小时数
							amount_of_payment=get_excel_int(row[11]),  # 发放金额
							release_user=Profile.get_user_by_username_or_first_name(row[12]),  # 发放人
							release_time=get_excel_date(row[13]),  # 发放时间
							remark1=row[14],  # 备注1
						)
						if not create_result[1]:
							repeat_num += 1
						else:
							import_num += 1
					except:
						messages_warning += str(rowindex) + ","
						traceback.print_exc()
			os.remove(filepath)

			if messages_warning:
				messages.warning(self.request, messages_warning + u"行数据格式错误！")

			msg = u"导入成功，记录总数：%s，" % total
			if import_num: msg += u"成功导入：%s，" % import_num
			if repeat_num: msg += u"重复记录(未录入)：%s，" % repeat_num
			if competence_num: msg += u"非负责项目(未录入)：%s，" % competence_num
			if no_project_num: msg += u"无项目信息(未录入)：%s," % no_project_num
			messages.success(self.request, msg)

			return redirect(reverse('employee_info:list', args=("temporary",)))
		except:
			traceback.print_exc()
			messages.warning(self.request, u"第%s行数据导入异常！" % (rowindex))
			return redirect(reverse('employee_info:list', args=("temporary",)))

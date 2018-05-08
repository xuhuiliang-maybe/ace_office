# coding=utf-8
import xlrd
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import View

from modules.dict_table.models import *
from modules.share_module.formater import *
from modules.share_module.get_path import *
from modules.share_module.load_info import LoadInfoUploadForm
from modules.share_module.permissionMixin import class_view_decorator
from modules.social_security.social_security_detail.models import *


@class_view_decorator(login_required)
@class_view_decorator(permission_required('social_security_detail.add_socialsecuritydetail', raise_exception=True))
class SocialSecurityDetailLoadView(View):
	def post(self, request, *args, **kwargs):
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
				return self.load_data(upload_file_path)

			messages.warning(self.request, u"无文件上传！")
			return redirect(reverse('project_manage:project_list', args=("basic_info",)))
		except:
			traceback.print_exc()
			messages.warning(self.request, u"导入异常！")
			return redirect(reverse('project_manage:project_list', args=("basic_info",)))

	def get_choice_dict(self, choice_tuple):
		return_dict = dict()
		for one_choice in choice_tuple:
			return_dict.update({one_choice[1]: one_choice[0]})
		return return_dict

	def load_data(self, filepath):
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
			no_service_company = 0  # 服务公司
			no_identity_card_number = 0  # 身份证号
			no_name = 0  # 姓名
			no_insured_month = 0  # 参保月份
			no_project_num = 0  # 无项目信息
			total = nrows - 1

			service_company = self.get_choice_dict(SERVICE_COMPANY)  # 服务公司
			messages_warning = ""
			for rowindex in xrange(1, nrows):  # 默认略过标题行,从第一行开始
				row = table.row_values(rowindex)
				if row:

					if not row[1]:  # 服务公司
						no_service_company += 1
						continue

					if not row[3]:  # 姓名
						no_name += 1
						continue

					if not row[4]:  # 项目名称
						no_project_num += 1
						continue

					if not row[6]:  # 身份证号
						no_identity_card_number += 1
						continue

					if not row[8]:  # 参保月份
						no_insured_month += 1
						continue

					project_name = None
					if not login_user.is_superuser:
						project_name = Project.get_project_by_full_name_or_short_name(row[4])
						principal = ""
						if project_name:
							principal = project_name.principal
						if login_user != principal:
							competence_num += 1
					try:
						create_result = SocialSecurityDetail.objects.get_or_create(
							computer_number=row[0],
							service_company=service_company.get(row[1], "1"),
							proxy_company=row[2],
							name=row[3],
							project_name=project_name,
							account_nature=row[5],
							identity_card_number=row[6],
							insured_address=row[7],
							insured_month=get_excel_date(row[8]),
							social_security_company=get_excel_int(row[9]),
							provident_fund_company=get_excel_int(row[10]),
							company_month_sum=get_excel_int(row[11]),
							social_security_person=get_excel_int(row[12]),
							provident_fund_person=get_excel_int(row[13]),
							person_month_sum=get_excel_int(row[14]),
							social_security_pay_company=get_excel_int(row[15]),
							social_security_pay_person=get_excel_int(row[16]),
							provident_fund_pay_company=get_excel_int(row[17]),
							provident_fund_pay_person=get_excel_int(row[18]),
							penalty=get_excel_int(row[19]),
							big_subsidy_refunds=get_excel_int(row[20]),
							social_security_refunds=get_excel_int(row[21]),
							provident_fund_refunds=get_excel_int(row[22]),
							employers_liability_insurance=get_excel_int(row[23]),
							disablement_gold=get_excel_int(row[24]),
							social_security_card_fees=get_excel_int(row[25]),
							agency_fees_expenses=get_excel_int(row[26]),
							agency_fees_revenue=get_excel_int(row[27]),
							remarecruitment_fees=get_excel_int(row[28]),
							lump_sum=get_excel_int(row[29])
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
			if no_service_company: msg += u"无服务公司(未录入)：%s," % no_service_company
			if no_name: msg += u"无姓名(未录入)：%s," % no_name
			if no_identity_card_number: msg += u"无身份证号(未录入)：%s," % no_identity_card_number
			if no_insured_month: msg += u"无参保月份(未录入)：%s," % no_insured_month
			messages.success(self.request, msg)

			return redirect(reverse('social_security_detail:reduction_list'))
		except:
			traceback.print_exc()
			messages.warning(self.request, u"导入异常！")
			return redirect(reverse('social_security_detail:reduction_list'))

# coding=utf-8
from django.core.urlresolvers import reverse
from django.db.models import F
from django.shortcuts import redirect
from django.views.generic import View

from modules.contract_manage.models import *
from modules.share_module.download import download_file
from modules.share_module.export import *


class DownloadContractView(View):
	def get(self, request, *args, **kwargs):
		try:
			self.contract_type = self.kwargs.get("contract_type", "")
			self.contractid = request.GET.get("contractid", "")
			contract_model = CONTRACT_DICT.get(self.contract_type, "")

			if self.contract_type == "1" and contract_model:
				return self.get_send_data(contract_model)

			if self.contract_type == "2" and contract_model:
				return self.get_outsourc_data(contract_model)

			if self.contract_type == "3" and contract_model:
				return self.get_intern_data(contract_model)

			if self.contract_type == "4" and contract_model:
				return self.get_service_data(contract_model)

			if self.contract_type == "5" and contract_model:
				return self.get_hourly_data(contract_model)
		except:
			return redirect(reverse('prompt', args=()))

	def download(self, titles, content_list, filename, filepath):
		if content_list:
			# 生成word
			word_obj = ExportTxt()
			word_obj.titles = titles
			word_obj.content_list = content_list
			word_obj.filename = filename
			word_obj.filepath = filepath
			word_obj.generate()

			file_name_list = filename.split(".")
			filename = file_name_list[0] + ".doc"

			filepath = os.path.join(filepath, filename)
			response = download_file(filepath, filename, True, "application/vnd.ms-word")
			return response
		else:
			# 导出代表头空文件
			return redirect(reverse('download', args=("loans_and_write_offs",)))

	def format_date(self, date):
		try:
			if date:
				return date.strftime("%Y-%m-%d")
			return "-"
		except:
			traceback.print_exc()
		return "-"

	def get_send_data(self, contract_model):
		try:
			contract_obj_list = contract_model.objects.filter(id=self.contractid)
			contract_obj = contract_obj_list.first()
			if contract_obj.download_times >= 2:
				return redirect(reverse('prompt', args=()))
			contract_obj_list.update(download_times=F('download_times') + 1)

			# 组装导出数据
			titles = u"派遣合同 附件一"
			content_list = list()
			filename = contract_obj.identity_card_number + "-" + contract_model._meta.object_name + ".txt"
			tmp_path = get_media_sub_path("tmp")  # 员工合同目录
			filepath = os.path.join(tmp_path)  # 导出文件路径

			content_list.append(u"项目名称：" + contract_obj.project_name.full_name)
			content_list.append(u"姓名：" + contract_obj.name)
			content_list.append(u"身份证号：" + contract_obj.identity_card_number)
			content_list.append(u"性别：" + contract_obj.get_sex_display())
			content_list.append(u"出生日期：" + self.format_date(contract_obj.birthday))
			content_list.append(u"民族：" + contract_obj.get_nation_display())
			content_list.append(u"住址：" + contract_obj.address)
			content_list.append(u"联系电话：" + contract_obj.phone_number)
			content_list.append(u"指定通知接收地址：" + contract_obj.receive_address)
			content_list.append(u"紧急联系人姓名：" + contract_obj.emergency_contact_name)
			content_list.append(u"紧急联系人电话：" + contract_obj.emergency_contact_phone)
			content_list.append(u"合同开始时间：" + self.format_date(contract_obj.start_date))
			content_list.append(u"合同结束时间：" + self.format_date(contract_obj.end_date))
			content_list.append(u"合同期限：" + contract_obj.get_deadline_display())
			content_list.append(u"试用期：" + contract_obj.get_probation_display())
			content_list.append(
				u"派遣期限：" + self.format_date(
					contract_obj.start_send_deadline) + " -- " + self.format_date(
					contract_obj.end_send_deadline))
			content_list.append(u"派遣工作地点：" + contract_obj.workplace)
			content_list.append(u"派遣岗位：" + contract_obj.post)
			content_list.append(u"派遣单位：" + contract_obj.project_name.customer)
			content_list.append(u"薪资标准：" + contract_obj.payroll_standard)
			content_list.append(u"发薪方式：" + contract_obj.get_payroll_grant_display())
			content_list.append(u"发薪时间：" + contract_obj.grant_date)
			return self.download(titles, content_list, filename, filepath)
		except:
			traceback.print_exc()

	def get_outsourc_data(self, contract_model):
		try:
			contract_obj_list = contract_model.objects.filter(id=self.contractid)
			contract_obj = contract_obj_list.first()
			if contract_obj.download_times >= 2:
				return redirect(reverse('prompt', args=()))
			contract_obj_list.update(download_times=F('download_times') + 1)

			# 组装导出数据
			titles = u"外包合同 附件一"
			content_list = list()
			filename = contract_obj.identity_card_number + "-" + contract_model._meta.object_name + ".txt"
			tmp_path = get_media_sub_path("tmp")  # 员工合同目录
			filepath = os.path.join(tmp_path)  # 导出文件路径

			content_list.append(u"项目名称：" + contract_obj.project_name.full_name)
			content_list.append(u"姓名：" + contract_obj.name)
			content_list.append(u"身份证号：" + contract_obj.identity_card_number)
			content_list.append(u"性别：" + contract_obj.get_sex_display())
			content_list.append(u"出生日期：" + self.format_date(contract_obj.birthday))
			content_list.append(u"民族：" + contract_obj.get_nation_display())
			content_list.append(u"住址：" + contract_obj.address)
			content_list.append(u"联系电话：" + contract_obj.phone_number)
			content_list.append(u"指定通知接收地址：" + contract_obj.receive_address)
			content_list.append(u"紧急联系人姓名：" + contract_obj.emergency_contact_name)
			content_list.append(u"紧急联系人电话：" + contract_obj.emergency_contact_phone)
			content_list.append(u"合同开始时间：" + self.format_date(contract_obj.start_date))
			content_list.append(u"合同结束时间：" + self.format_date(contract_obj.end_date))
			content_list.append(u"合同期限：" + contract_obj.get_deadline_display())
			content_list.append(u"试用期：" + contract_obj.get_probation_display())
			content_list.append(u"工作地点：" + contract_obj.workplace)
			content_list.append(u"岗位：" + contract_obj.post)
			content_list.append(u"薪资标准：" + contract_obj.payroll_standard)
			content_list.append(u"发薪方式：" + contract_obj.get_payroll_grant_display())
			content_list.append(u"发薪时间：" + contract_obj.grant_date)
			return self.download(titles, content_list, filename, filepath)
		except:
			traceback.print_exc()

	def get_intern_data(self, contract_model):
		try:
			contract_obj_list = contract_model.objects.filter(id=self.contractid)
			contract_obj = contract_obj_list.first()
			if contract_obj.download_times >= 2:
				return redirect(reverse('prompt', args=()))
			contract_obj_list.update(download_times=F('download_times') + 1)

			# 组装导出数据
			titles = u"实习生合同 附件一"
			content_list = list()
			filename = contract_obj.identity_card_number + "-" + contract_model._meta.object_name + ".txt"
			tmp_path = get_media_sub_path("tmp")  # 员工合同目录
			filepath = os.path.join(tmp_path)  # 导出文件路径

			content_list.append(u"项目名称：" + contract_obj.project_name.full_name)
			content_list.append(u"姓名：" + contract_obj.name)
			content_list.append(u"身份证号：" + contract_obj.identity_card_number)
			content_list.append(u"性别：" + contract_obj.get_sex_display())
			content_list.append(u"出生日期：" + self.format_date(contract_obj.birthday))
			content_list.append(u"民族：" + contract_obj.get_nation_display())
			content_list.append(u"住址：" + contract_obj.address)
			content_list.append(u"联系电话：" + contract_obj.phone_number)
			content_list.append(u"指定通知接收地址：" + contract_obj.receive_address)
			content_list.append(u"紧急联系人姓名：" + contract_obj.emergency_contact_name)
			content_list.append(u"紧急联系人电话：" + contract_obj.emergency_contact_phone)
			content_list.append(u"合同开始时间：" + self.format_date(contract_obj.start_date))
			content_list.append(u"合同结束时间：" + self.format_date(contract_obj.end_date))
			content_list.append(u"合同期限：" + contract_obj.get_deadline_display())
			content_list.append(u"试用期：" + contract_obj.get_probation_display())
			content_list.append(u"实习地点：" + contract_obj.workplace)
			content_list.append(u"实习岗位：" + contract_obj.post)
			content_list.append(u"实习劳务费标准：" + contract_obj.payroll_standard)
			content_list.append(u"实习劳务费发放方式：" + contract_obj.get_payroll_grant_display())
			content_list.append(u"实习劳务费发放时间：" + contract_obj.grant_date)
			return self.download(titles, content_list, filename, filepath)
		except:
			traceback.print_exc()

	def get_service_data(self, contract_model):
		try:
			contract_obj_list = contract_model.objects.filter(id=self.contractid)
			contract_obj = contract_obj_list.first()
			if contract_obj.download_times >= 2:
				return redirect(reverse('prompt', args=()))
			contract_obj_list.update(download_times=F('download_times') + 1)

			# 组装导出数据
			titles = u"劳务合同 附件一"
			content_list = list()
			filename = contract_obj.identity_card_number + "-" + contract_model._meta.object_name + ".txt"
			tmp_path = get_media_sub_path("tmp")  # 员工合同目录
			filepath = os.path.join(tmp_path)  # 导出文件路径

			content_list.append(u"项目名称：" + contract_obj.project_name.full_name)
			content_list.append(u"姓名：" + contract_obj.name)
			content_list.append(u"身份证号：" + contract_obj.identity_card_number)
			content_list.append(u"性别：" + contract_obj.get_sex_display())
			content_list.append(u"出生日期：" + self.format_date(contract_obj.birthday))
			content_list.append(u"民族：" + contract_obj.get_nation_display())
			content_list.append(u"住址：" + contract_obj.address)
			content_list.append(u"联系电话：" + contract_obj.phone_number)
			content_list.append(u"指定通知接收地址：" + contract_obj.receive_address)
			content_list.append(u"紧急联系人姓名：" + contract_obj.emergency_contact_name)
			content_list.append(u"紧急联系人电话：" + contract_obj.emergency_contact_phone)
			content_list.append(u"合同开始时间：" + self.format_date(contract_obj.start_date))
			content_list.append(u"合同结束时间：" + self.format_date(contract_obj.end_date))
			content_list.append(u"合同期限：" + contract_obj.get_deadline_display())
			content_list.append(u"试用期：" + contract_obj.get_probation_display())
			content_list.append(u"工作地点：" + contract_obj.workplace)
			content_list.append(u"岗位：" + contract_obj.post)
			content_list.append(u"劳务费标准：" + contract_obj.payroll_standard)
			content_list.append(u"劳务费发放方式：" + contract_obj.get_payroll_grant_display())
			content_list.append(u"劳务费发放时间：" + contract_obj.grant_date)
			return self.download(titles, content_list, filename, filepath)
		except:
			traceback.print_exc()

	def get_hourly_data(self, contract_model):
		try:
			contract_obj_list = contract_model.objects.filter(id=self.contractid)
			contract_obj = contract_obj_list.first()
			if contract_obj.download_times >= 2:
				return redirect(reverse('prompt', args=()))
			contract_obj_list.update(download_times=F('download_times') + 1)

			# 组装导出数据
			titles = u"小时工合同 附件一"
			content_list = list()
			filename = contract_obj.identity_card_number + "-" + contract_model._meta.object_name + ".txt"
			tmp_path = get_media_sub_path("tmp")  # 员工合同目录
			filepath = os.path.join(tmp_path)  # 导出文件路径

			content_list.append(u"项目名称：" + contract_obj.project_name.full_name)
			content_list.append(u"项目时间：" + contract_obj.project_date)
			content_list.append(u"服务部门：" + contract_obj.project_name.department)
			content_list.append(u"姓名：" + contract_obj.name)
			content_list.append(u"身份证号：" + contract_obj.identity_card_number)
			content_list.append(u"性别：" + contract_obj.get_sex_display())
			content_list.append(u"手机号码：" + contract_obj.phone_number)
			content_list.append(u"项目名称：" + contract_obj.project_name.full_name)
			content_list.append(u"服务部门：" + contract_obj.project_name.department)
			content_list.append(u"合同开始时间：" + self.format_date(contract_obj.start_date))
			content_list.append(u"合同结束时间：" + self.format_date(contract_obj.end_date))
			content_list.append(u"工作地点：" + contract_obj.workplace)
			content_list.append(u"岗位或内容：" + contract_obj.post)
			content_list.append(u"劳务费标准：" + contract_obj.payroll_standard)
			content_list.append(u"开始工作日：" + self.format_date(contract_obj.start_work_date))
			content_list.append(u"结束工作日：" + self.format_date(contract_obj.end_work_date))
			content_list.append(u"工作天数：" + contract_obj.grant_date)
			content_list.append(u"小时数：" + contract_obj.work_days)
			content_list.append(u"发放金额：" + contract_obj.grant_money)
			content_list.append(u"领取人：" + contract_obj.recipients)
			content_list.append(u"发放人：" + contract_obj.grant_user.first_name)
			content_list.append(u"发放时间：" + self.format_date(contract_obj.grant_time))
			content_list.append(u"招聘人：" + contract_obj.recruiters.first_name)
			content_list.append(u"备注：" + contract_obj.remark)
			return self.download(titles, content_list, filename, filepath)
		except:
			traceback.print_exc()

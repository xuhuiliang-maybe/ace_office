# coding=utf-8
import traceback
from collections import defaultdict

from django.contrib.auth.models import User
from django.views.generic import View

from modules.share_module.download import download_file
from modules.share_module.export import ExportExcel
from modules.share_module.formater import true_false_formater
from modules.share_module.utils import get_kwargs


class ProfileExportView(View):
	def format_none(self, value):
		try:
			if value:
				return str(value)
			return ""
		except:
			traceback.print_exc()
			return ""

	def get(self, request, *args, **kwargs):

		head_list = [u'公司名称', u'一级部门', u'二级部门', u'用户名', u'姓名', u'性别', u'岗位', u'直线上级', u'邮箱',
			     u'手机号', u'座机号', u'办公通讯地址', u'审批假条(天)', u'审批借款(元)', u'审批涨薪(元)', u'入职时间',
			     u'在职(有效)', u'部门负责人状态', u'超级用户状态', u'职员状态']
		field_list = ["company", "one_level_dept", "attribution_dept", "username", "first_name",
			      "gender", "position", "higher_up", "email", "mobile_phone", "telephone", "address",
			      "authorize_leave", "authorize_loan", "authorize_wage", "date_joined",
			      "is_active", "dept_head",
			      "is_superuser",
			      "is_staff"]

		try:
			self.dept_ids = self.request.GET.get("dept_ids", "")
			self.dept_name = self.request.GET.get("dept_name", "")
			self.first_name = self.request.GET.get("first_name", "")

			search_condition = {
			    "first_name__icontains": self.first_name,
			}
			if self.dept_name:
				search_condition.update({"attribution_dept__in": self.dept_name.split(",")})
			kwargs = get_kwargs(search_condition)
			user_obj_list = User.objects.filter(**kwargs)

			# 组装导出数据
			rows_list = list()
			for one_user_obj in user_obj_list:
				one_row_dict = defaultdict(str)
				one_row_dict["company"] = one_user_obj.company  # 公司名称
				one_row_dict["one_level_dept"] = one_user_obj.one_level_dept  # 一级部门
				one_row_dict["attribution_dept"] = one_user_obj.attribution_dept  # 二级部门
				one_row_dict["username"] = one_user_obj.username  # 用户名
				one_row_dict["first_name"] = one_user_obj.first_name  # 姓名
				one_row_dict["gender"] = one_user_obj.get_gender_display()  # 性别
				try:
					one_row_dict["position"] = one_user_obj.position.name  # 岗位
				except:
					one_row_dict["position"] = "-"
				one_row_dict["higher_up"] = one_user_obj.higher_up  # 直线上级
				one_row_dict["email"] = one_user_obj.email
				one_row_dict["mobile_phone"] = one_user_obj.mobile_phone  # 手机号
				one_row_dict["telephone"] = one_user_obj.telephone  # 座机号
				one_row_dict["address"] = one_user_obj.address  # 办公通讯地址
				one_row_dict["authorize_leave"] = int(one_user_obj.authorize_leave)  # 审批请假天数
				one_row_dict["authorize_loan"] = int(one_user_obj.authorize_loan)  # 审批借款金额
				one_row_dict["authorize_wage"] = int(one_user_obj.authorize_wage)  # 审批工资金额
				try:
					one_row_dict["date_joined"] = one_user_obj.date_joined.strftime("%Y-%m-%d")  # 入职时间（加入日期）
				except:
					one_row_dict["date_joined"] = ""
					traceback.print_exc()
				one_row_dict["is_active"] = true_false_formater(one_user_obj.is_active)  # 是否活跃，是否在职
				one_row_dict["dept_head"] = true_false_formater(one_user_obj.dept_head)  # 是否部门负责人
				one_row_dict["is_superuser"] = true_false_formater(one_user_obj.is_superuser)  # 是否超级管理员
				one_row_dict["is_staff"] = true_false_formater(one_user_obj.is_staff)  # 是否登录
				rows_list.append(one_row_dict.copy())

			# 实例化导出类
			export_excel = ExportExcel()
			export_excel.sheetname = "Profile"
			export_excel.head_title_list = head_list
			export_excel.field_name_list = field_list
			export_excel.data_obj_list = rows_list
			export_excel.filename = "Profile"
			export_excel.path = "tmp"
			filepath, filename = export_excel.export()
			# 页面下载导出文件
			response = download_file(filepath, filename, True)
			return response
		except:
			traceback.print_exc()

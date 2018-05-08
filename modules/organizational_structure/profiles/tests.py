# coding=utf-8
from django.test import TestCase
import xlrd
from django.contrib.auth.models import User
from modules.organizational_structure.departments.models import Department
from modules.share_module.get_path import *
from modules.share_module.formater import *

"""
用户信息单元测试
项目下运行：python manage.py test modules.organizational_structure.profiles
"""


class ProfileTestCase(TestCase):
	def setUp(self):
		pass

	def test_load_profile_info(self):
		"""测试导入用户信息"""

		# 获取测试模板路径
		tmp_info_path = get_media_sub_path("tmp")
		info_template_path = os.path.join(tmp_info_path, "test", "Profile_20160123194700.xls")

		data = xlrd.open_workbook(info_template_path)
		table = data.sheets()[0]  # 通过索引顺序获取,工作表
		nrows = table.nrows  # 行数
		# ncols = table.ncols  # 列数

		# 组装数据
		# colnames = table.row_values(0)  # 表头数据
		import_num = 0  # 导入数
		repeat_num = 0  # 重复导入
		total = nrows - 1
		result = {"total": total, "import": 0, "repeat": 0}
		for rowindex in xrange(1, nrows):  # 默认略过标题行,从第一行开始
			row = table.row_values(rowindex)
			if row:
				# 基础信息
				# user.set_password("111111")# 默认密码

				# 归属部门信息 能找到二级部门那么一定可以找到一级部门
				dept_id = Department.objects.filter(name=row[3])
				if dept_id.exists():
					dept_obj = dept_id[0]
				else:
					dept_obj = Department.objects.first()

				# 性别
				gender = row[6]
				if gender == u"男":
					genders = "M"
				elif gender == u"女":
					genders = "F"
				else:
					genders = ""

				create_result = User.objects.get_or_create(
					company=row[1],  # 公司名称
					attribution_dept_id=dept_obj.id,  # 归属部门
					username=row[4],  # 用户名
					first_name=row[5],  # 姓名
					gender=genders,  # 性别
					position=row[7],  # 职务
					higher_up=row[8],  # 直线上级
					email=row[9],
					mobile_phone=row[10],  # 手机挂号
					telephone=row[11],  # 座机号
					address=row[12],  # 办公通讯地址
					authorize_leave=row[13],  # 审批请假天数
					authorize_loan=row[14],  # 审批借款金额
					authorize_wage=row[15],  # 审批涨薪金额
					date_joined=date_formater(row[16], "%Y-%m-%d"),  # 入职时间（加入日期）
					is_active=true_false_unformat(row[17]),  # 是否在职
					dept_head=true_false_unformat(row[18]),  # 是否部门负责人
					is_superuser=true_false_unformat(row[19]),  # 是否超级用户
					is_staff=true_false_unformat(row[20])  # 是否登陆
				)
				if not create_result:
					repeat_num += 1
				else:
					import_num += 1

		# 读取导入用户数据
		print u"总行数=", total
		print u"成功导入数=", import_num
		print u"数据重复，忽略数=", repeat_num
		alluser = User.objects.all()
		print alluser

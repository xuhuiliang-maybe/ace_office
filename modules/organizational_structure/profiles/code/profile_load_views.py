# coding=utf-8
import xlrd
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import View

from modules.organizational_structure.profiles.models import *
from modules.share_module.formater import *
from modules.share_module.get_path import *
from modules.share_module.load_info import LoadInfoUploadForm
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('auth.add_user', raise_exception=True))
class ProfileLoadView(View):
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
			return redirect(reverse('employee_info:list'))
		except:
			traceback.print_exc()
			messages.warning(self.request, u"导入异常！")
			return redirect(reverse('employee_info:list'))

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
		try:
			# 读取模板
			data = xlrd.open_workbook(filepath)
			table = data.sheets()[0]  # 通过索引顺序获取,工作表
			nrows = table.nrows  # 行数
			# ncols = table.ncols  # 列数

			# 组装数据
			# colnames = table.row_values(0)  # 表头数据
			import_num = 0  # 导入数
			update_num = 0  # 重复导入
			total = nrows - 1

			# 性别字典
			gender_dict = self.get_choice_dict(GENDER_CHOICES)

			for rowindex in xrange(1, nrows):  # 默认略过标题行,从第一行开始
				row = table.row_values(rowindex)
				if row:
					obj, is_created = User.objects.update_or_create(username=row[4])

					# 信息已存在，没有创建新的，对已有数据做更新
					if not is_created:
						update_num += 1  # 更新导入数
					else:
						import_num += 1  # 新增导入

					User.objects.filter(username=row[4]).update(
						password=make_password("111111"),
						company=row[1],  # 公司名称
						one_level_dept=row[2],  # 一级部门
						attribution_dept=row[3],  # 二级，归属部门
						# username=row[4],  # 用户名
						first_name=row[5],  # 姓名
						gender=gender_dict.get(row[6], ""),  # 性别
						position=Position.get_dict_item_by_name(row[7]),  # 岗位
						higher_up=row[8],  # 直线上级
						email=row[9],
						mobile_phone=str(get_excel_int(row[10])),  # 手机号
						telephone=str(get_excel_int(row[11])),  # 座机号
						address=row[12],  # 办公通讯地址
						authorize_leave=get_excel_int(row[13]),  # 审批请假天数
						authorize_loan=get_excel_int(row[14]),  # 审批借款金额
						authorize_wage=get_excel_int(row[15]),  # 审批涨薪金额
						date_joined=get_excel_date(row[16], True),  # 入职时间（加入日期）
						is_active=true_false_unformat(row[17]),  # 是否在职
						dept_head=true_false_unformat(row[18]),  # 是否部门负责人
						is_superuser=true_false_unformat(row[19]),  # 是否超级用户
						is_staff=true_false_unformat(row[20])  # 是否登陆
					)

			os.remove(filepath)
			messages.success(self.request,
					 u"导入成功，记录总数：%s，成功导入：%s，更新记录：%s。" % (total, import_num, update_num))
			return redirect(reverse('organizational_structure:profile:profile_list'))
		except:
			traceback.print_exc()
			messages.warning(self.request, u"导入异常！")
			return redirect(reverse('organizational_structure:profile:profile_list'))

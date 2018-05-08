# coding=utf-8

from django.db.models.signals import post_syncdb
from django.dispatch import receiver

from modules.dict_table import models as dict_table_app
from modules.dict_table.models import *


@receiver(post_syncdb, sender=dict_table_app)  # 信号的名字，发送者
def init_dict_table_info(sender, **kwargs):  # 回调函数，收到信号后的操作
	"""初始化字典表
	:param sender:
	:param kwargs:
	:return:
	"""
	try:
		print "Init dict table:"
		# 公司主体信息
		init_name = [u"北京邦泰", u"天津杰博"]
		save_dict_name(init_name, CompanySubject)

		# 合同类别信息
		init_name = [u"派遣", u"外包", u"临时工", u"代理", u"代招", u"其他"]
		save_dict_name(init_name, ContractType)

		# 项目类别信息
		init_name = [u"派遣", u"外包A", u"外包B"]
		save_dict_name(init_name, ProjectType)

		# 项目目前状态信息
		init_name = [u"持续", u"停止"]
		save_dict_name(init_name, ProgressState)

		# 销售类型信息
		init_name = [u"信息", u"协助"]
		save_dict_name(init_name, SalesType)

		# 社保险种信息
		init_name = [u"养老", u"工伤", u"医疗", u"失业", u"生育", u"其他"]
		save_dict_name(init_name, SocialSecurityType)

		# 社保账户类型
		init_name = [u"自有账户", u"代理账户"]
		save_dict_name(init_name, SocialSecurityAccountType)

		# 商保公司
		init_name = [u"泰康", u"太平洋", u"中国人寿"]
		save_dict_name(init_name, BusinessInsuranceCompany)

		# 时间周期
		init_name = [u"日", u"周", u"月", u"年"]
		save_dict_name(init_name, Cycle)

		# 工资发放方式
		init_name = [u"垫付", u"代发"]
		save_dict_name(init_name, WageGrantType)

		# 岗位类型
		init_name = [u"总经理", u"副总经理", u"会计", u"出纳", u"薪酬结算专员", u"社保专员", u"档案专员",
			u"人事专员", u"招聘主管", u"招聘专员", u"职介店员", u"客服专员", u"客服经理",
			u"客服主管", u"外包主管", u"销售人员"]
		save_dict_name(init_name, Position)

		# 发票类型
		init_name = [u"全额专票", u"全额普票", u"差额专票", u"差额普票", u"拆分（全额专票+差额普票）",
			u"拆分（全额普票+差额普票）", u"普通发票", u"增值税发票", u"增值税专票"]
		save_dict_name(init_name, InvoiceType)

		# 档案类型
		init_name = [u"发函资料", u"入职资料", u"离职资料"]
		save_dict_name(init_name, ArchiveType)

		# 费用类型
		init_name = [u"工资", u"福利费", u"折旧费", u"办公费", u"差旅费", u"运输费", u"保险费", u"租赁费", u"修理费", u"咨询费", u"绿化费",
			u"招待费"u"水电费"]
		save_dict_name(init_name, ExpenseType)

		# 改善状态
		init_name = [u"改善", u"持续"]
		save_dict_name(init_name, ImproveStatus)

		# 请假类型
		init_name = [u"年假", u"病假", u"事假", u"婚假", u"产假", u"丧假"]
		save_dict_name(init_name, LeaveType)

	except:
		traceback.print_exc()


def save_dict_name(init_name, model_name):
	"""保存初始化字典信息
	:param init_name: 字典表项
	:param model_name: 字典表模型
	:return:
	"""
	try:
		[model_name.objects.get_or_create(name=name) for name in init_name]
		print " Init %s ... ok" % getattr(model_name, '__name__')
	except:
		traceback.print_exc()

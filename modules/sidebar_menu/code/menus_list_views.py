# encoding=utf-8
import json
import traceback

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import View

from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
class SidebarMenusList(View):
	def get(self, request, *args, **kwargs):
		try:
			self.user = request.user
			result_menu_list = self.get_menu_list()
			result = json.dumps({"data": result_menu_list})
			return HttpResponse(result, content_type="application/json")
		except:
			traceback.print_exc()

	def get_menu_list(self):
		try:
			menu_list = [
				{'permissions': 'admin_account.browse_index', "show": True, "text": u"我的主页",
				 "icon": "menu-icon fa fa-tachometer", "url": "/homepage/index"},

				{'permissions': 'admin_account.browse_mysite', "show": True, "text": u"我的地盘",
				 "icon": "menu-icon fa fa-user", "url": "",
				 "menus": [
					 {'permissions': 'admin_account.browse_personal', "show": True,
					  "text": u"我的个人信息", "icon": "", "url": "/mysite/personal"},
					 # {'permissions': '',"text": "我的邮箱", "icon": "", "url": "/mysite/emails"},
				 ]},

				{'permissions': 'admin_account.browse_organizational', "show": True, "text": u"组织架构",
				 "icon": "menu-icon fa fa-sitemap",
				 "url": "",
				 "menus": [
					 {'permissions': 'admin_account.browse_structure', "show": True,
					  "text": u"组织架构图", "icon": "", "url": "/organizational/structure"},
					 {'permissions': 'departments.browse_department', "show": True, "text": u"部门信息",
					  "icon": "", "url": "/organizational/departments/list"},
					 {'permissions': 'admin_account.browse_user', "show": True, "text": u"管理人员",
					  "icon": "", "url": "/organizational/profile/list"},
				 ]},

				{'permissions': 'admin_account.browse_project_manage', "show": True, "text": u"项目管理",
				 "icon": "menu-icon fa fa-briefcase", "url": "",
				 "menus": [
					 {"permissions": "project_manage.browse_basic_info", "show": True,
					  "text": u"项目基础信息",
					  "icon": "", "url": "/projectmanage/project/basic_info"},

					 {"permissions": "project_manage.browse_social_security_info", "show": True,
					  "text": u"项目福利信息",
					  "icon": "", "url": "/projectmanage/project/social_security_info"},

					 {"permissions": "project_manage.browse_settle_accounts_info", "show": True,
					  "text": u"项目结算信息",
					  "icon": "", "url": "/projectmanage/project/settle_accounts_info"},

					 {"permissions": "project_manage.browse_billing_info", "show": True,
					  "text": u"项目开票信息",
					  "icon": "", "url": "/projectmanage/project/billing_info"},

					 {"permissions": "project_manage.browse_sales_info", "show": True,
					  "text": u"项目销售信息",
					  "icon": "", "url": "/projectmanage/project/sales_info"},

					 {"permissions": "project_manage.browse_recruitment_unit", "show": True,
					  "text": u"项目招聘单价",
					  "icon": "", "url": "/projectmanage/project/recruitment_unit"},
				 ]},

				{"permissions": "admin_account.browse_employee_manage", "show": True, "text": u"员工管理",
				 "icon": "menu-icon fa fa-users", "url": "",
				 "menus": [
					 {"permissions": "employee_info.browse_employee", "show": True, "text": u"员工信息",
					  "icon": "", "url": "/employeemanage/employee/list"},
					 {"permissions": "employee_info.browse_archive", "show": True,
					  "text": u"员工档案信息",
					  "icon": "", "url": "/archive/list"},
					 {"permissions": "employee_info.browse_temporary", "show": True,
					  "text": u"临时工信息",
					  "icon": "", "url": "/employeemanage/temporary/list"},
				 ]},

				{"permissions": "admin_account.browse_socialsecurity", "show": True, "text": u"社保福利",
				 "icon": "menu-icon fa fa-coffee",
				 "menus": [
					 {"permissions": "increase_info.browse_increase", "show": True,
					  "text": u"增员信息", "icon": "", "url": "/increase/list"},
					 {"permissions": "reduction_info.browse_reduction", "show": True,
					  "text": u"减员信息", "icon": "", "url": "/reduction/list"},
					 {"permissions": "social_security_detail.browse_social_security_detail",
					  "show": True,
					  "text": u"社保明细", "icon": "", "url": "/social_security_detail/list"},
				 ]},

				{"permissions": "settlement_pay.browse_payroll", "show": True, "text": u"结算发薪",
				 "icon": "menu-icon fa fa-gift", "url": "/payroll/list"},

				{"permissions": "admin_account.browse_recruitment", "show": True, "text": u"招聘管理",
				 "icon": "menu-icon fa fa-filter", "url": "/recruitment/list",
				 "menus": [
					 {"permissions": "admin_account.browse_month_entry_job_details", "show": True,
					  "text": u"当月入职招聘明细",
					  "icon": "", "url": "/recruitment/month_entry_job_details"},
					 {"permissions": "admin_account.browse_individual_job", "show": True,
					  "text": u"个人招聘",
					  "icon": "", "url": "/recruitment/individual_job"},
					 {"permissions": "admin_account.browse_job_statistic", "show": True,
					  "text": u"招聘统计",
					  "icon": "", "url": "/recruitment/job_statistic"},
				 ]},

				{"permissions": "admin_account.browse_approval", "show": True, "text": u"审批流程",
				 "icon": "menu-icon glyphicon glyphicon-retweet", "url": "",
				 "menus": [
					 {"permissions": "admin_account.browse_apply_info_template", "show": True,
					  "text": u"申请信息模板",
					  "icon": "", "url": "/approval/"},
					 {"permissions": "admin_account.browse_approval_pending", "show": True,
					  "text": u"待审批信息", "icon": "", "url": "/approval/pending"},
				 ]},

				{"permissions": "expense_manage.browse_expense", "show": True, "text": u"费用管理",
				 "icon": "menu-icon glyphicon glyphicon-usd", "url": "/expense/list"},

				{"permissions": "admin_account.browse_payroll_manage", "show": True, "text": u"薪资管理",
				 "icon": "menu-icon fa fa-money", "url": "",
				 "menus": [
					 {"permissions": "payroll_detail.browse_payrolldetail", "show": True,
					  "text": u"薪资明细",
					  "icon": "", "url": "/payroll_manage/detail/list"},
					 {"permissions": "payroll_gather.browse_payrollgather", "show": True,
					  "text": u"薪资汇总",
					  "icon": "", "url": "/payroll_manage/gather/list"},
				 ]},

				{"permissions": "admin_account.browse_qualityassurance_manage", "show": True,
				 "text": u"人事操作质量", "icon": "menu-icon fa fa-check-square-o", "url": "",
				 "menus": [{"permissions": "personnel_operation.browse_qualityassurance", "show": True,
					    "text": u"个人操作质量", "icon": "", "url": "/personnel/list"},
					   {"permissions": "admin_account.browse_qualityassurance_gather",
					    "show": True, "text": u"操作质量汇总", "icon": "",
					    "url": "/personnel/gather"}, ]},

				{"permissions": "admin_account.browse_finance", "show": True, "text": u"财务管理",
				 "icon": "menu-icon fa fa-pencil-square-o",
				 "menus": [
					 {"permissions": "social_security_audit.browse_socialsecurityaudit",
					  "show": True,
					  "text": u"社保审核", "icon": "", "url": "/finance/social_security_audit/list"},
					 {"permissions": "arrival_and_billing.browse_arrivalandbilling", "show": True,
					  "text": u"到账与开票", "icon": "", "url": "/finance/arrival_and_billing/list"},
					 {"permissions": "loans_and_write_offs.browse_loansandwriteoffs",
					  "show": True,
					  "text": u"借款与销账", "icon": "", "url": "/finance/loans_and_write_offs/list"},
				 ]},

				{"permissions": "admin_account.browse_contract", "show": True, "text": u"合同管理",
				 "icon": "menu-icon fa fa-file-text-o",
				 "menus": [
					 {"permissions": "contract_manage.browse_contractsend", "show": True,
					  "text": u"派遣", "icon": "", "url": "/contract/send"},

					 {"permissions": "contract_manage.browse_contractoutsourc", "show": True,
					  "text": u"外包", "icon": "", "url": "/contract/outsourc"},

					 {"permissions": "contract_manage.browse_contractintern", "show": True,
					  "text": u"实习生", "icon": "", "url": "/contract/intern"},

					 {"permissions": "contract_manage.browse_contractservice", "show": True,
					  "text": u"劳务", "icon": "", "url": "/contract/service"},

					 {"permissions": "contract_manage.browse_contracthourly", "show": True,
					  "text": u"小时工", "icon": "", "url": "/contract/hourly"},

					 {"permissions": "contract_manage.browse_contractpreviewcode", "show": True,
					  "text": u"合同预览", "icon": "", "url": "/contract/preview"},
				 ]},

				{"permissions": "admin_account.browse_system", "show": True, "text": u"系统相关",
				 "icon": "menu-icon fa fa-cogs", "url": "",
				 "menus": [
					 {"permissions": "admin_account.browse_admin", "show": True, "text": u"权限管理",
					  "icon": "", "url": "/admin"},
					 {"permissions": "system.browse_systemconfig", "show": True,
					  "text": u"系统设置", "icon": "", "url": "/system/config"},
					 {"permissions": "system.data_backup", "show": True,
					  "text": u"数据备份", "icon": "", "url": "/system/data_backup"},
				 ]},

				{"permissions": "admin_account.browse_dict", "show": True, "text": u"字典表",
				 "icon": "menu-icon fa fa-book", "url": "",
				 "menus": [
					 {"permissions": "dict_table.browse_companysubject", "show": True,
					  "text": u"公司主体", "icon": "", "url": "/dicttable/companysubject"},
					 {"permissions": "dict_table.browse_contracttype", "show": True,
					  "text": u"合同类型", "icon": "", "url": "/dicttable/contracttype"},
					 {"permissions": "dict_table.browse_projecttype", "show": True, "text": u"项目类型",
					  "icon": "", "url": "/dicttable/projecttype"},
					 {"permissions": "dict_table.browse_progressstate", "show": True,
					  "text": u"项目目前状态", "icon": "", "url": "/dicttable/progressstate"},
					 {"permissions": "dict_table.browse_salestype", "show": True, "text": u"销售类型",
					  "icon": "", "url": "/dicttable/salestype"},
					 {"permissions": "dict_table.browse_socialsecuritytype", "show": True,
					  "text": u"社保险种", "icon": "", "url": "/dicttable/socialsecuritytype"},
					 {"permissions": "dict_table.browse_socialsecurityaccounttype", "show": True,
					  "text": u"社保账户类型", "icon": "", "url": "/dicttable/socialsecurityaccounttype"},
					 {"permissions": "dict_table.browse_businessinsurancecompany", "show": True,
					  "text": u"商保公司", "icon": "", "url": "/dicttable/businessinsurancecompany"},
					 {"permissions": "dict_table.browse_cycle", "show": True, "text": u"时间周期",
					  "icon": "", "url": "/dicttable/cycle"},
					 {"permissions": "dict_table.browse_wagegranttype", "show": True,
					  "text": u"工资发放方式", "icon": "", "url": "/dicttable/wagegranttype"},
					 {"permissions": "dict_table.browse_invoicetype", "show": True, "text": u"发票类型",
					  "icon": "", "url": "/dicttable/invoicetype"},
					 {"permissions": "dict_table.browse_position", "show": True, "text": u"岗位类型",
					  "icon": "", "url": "/dicttable/position"},
					 {"permissions": "dict_table.browse_archivetype", "show": True, "text": u"档案类型",
					  "icon": "", "url": "/dicttable/archivetype"},
					 {"permissions": "dict_table.browse_expensetype", "show": True, "text": u"费用类型",
					  "icon": "", "url": "/dicttable/expensetype"},
					 {"permissions": "dict_table.browse_improvestatus", "show": True,
					  "text": u"改善状态", "icon": "", "url": "/dicttable/improvestatus"},
					 {"permissions": "dict_table.browse_leavetype", "show": True,
					  "text": u"请假类型", "icon": "", "url": "/dicttable/leavetype"},
					 {"permissions": "dict_table.browse_subject", "show": True,
					  "text": u"科目", "icon": "", "url": "/dicttable/subject"},
				 ]},
			]

			menu_list_new = list()
			if not self.user.is_superuser:
				for one_menu in menu_list:
					if not self.user.has_perm(one_menu["permissions"]):
						one_menu["show"] = False
						continue
					else:
						if one_menu.has_key("menus"):
							for sub in one_menu["menus"]:
								if not self.user.has_perm(sub["permissions"]):
									sub["show"] = False
					menu_list_new.append(one_menu)
			else:
				return menu_list

			return menu_list_new
		except:
			traceback.print_exc()
			return list()

# coding=utf-8
from django.db import models


class Purview(models.Model):
	class Meta:
		verbose_name = u"菜单浏览权限"
		permissions = (
			("browse_index", u"浏览 我的主页"),

			("browse_mysite", u"浏览 我的地盘"),
			("browse_personal", u"浏览 我的个人信息"),

			("browse_organizational", u"浏览 组织架构"),
			("browse_structure", u"浏览 组织架构图"),
			("browse_project_manage", u"浏览 项目管理"),
			("browse_user", u"浏览 管理人员"),

			("browse_employee_manage", u"浏览 员工管理"),

			("browse_socialsecurity", u"浏览 社保福利"),

			("browse_recruitment", u"浏览 招聘管理"),
			("browse_month_entry_job_details", u"浏览 当月入职招聘明细"),
			("browse_individual_job", u"浏览 个人招聘"),
			("browse_job_statistic", u"浏览 招聘统计"),
			("export_job_statistic", u"导出 招聘统计"),

			("browse_approval", u"浏览 审批流程"),
			("browse_apply_info_template", u"浏览 申请信息模板"),
			("browse_approval_pending", u"浏览 待审批信息"),

			("browse_qualityassurance_manage", u"浏览 人事操作质量"),
			("browse_qualityassurance_gather", u"浏览 操作质量汇总"),

			("browse_system", u"浏览 系统相关"),
			("browse_admin", u"浏览 权限管理"),

			("browse_dict", u"浏览 字典表"),

			("browse_payroll_manage", u"浏览 薪资管理"),

			("browse_finance", u"浏览 财务管理"),
			("browse_contract", u"浏览 合同管理"),
		)

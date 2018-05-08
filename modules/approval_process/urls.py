# coding=utf-8
from django.conf.urls import url

from modules.approval_process.billing_pre_pay.code import billing_pre_pay_add_views, billing_pre_pay_delete, \
	billing_pre_pay_views, billing_pre_pay_edit_views
from modules.approval_process.billing_pre_pay.models import BillingPrePay
from modules.approval_process.code import (
	pending_views,
	pending_action_views,
	apply_info_template_views,
	export_approval
)
from modules.approval_process.demand_turnover.code import demand_turnover_add_views, demand_turnover_delete, \
	demand_turnover_views, demand_turnover_edit_views
from modules.approval_process.demand_turnover.models import DemandTurnover
from modules.approval_process.leave.code import leave_views, leave_delete, leave_add_views, leave_edit_views
from modules.approval_process.leave.models import Leave
from modules.approval_process.loan.code import loan_views, loan_delete, loan_add_views, loan_edit_views
from modules.approval_process.loan.models import *
from modules.approval_process.recruited_billing.code import recruitedbilling_add_views, recruitedbilling_delete, \
	recruitedbilling_edit_views, recruitedbilling_views
from modules.approval_process.recruited_billing.models import *
from modules.approval_process.temporary_write_offs_billing.code import temporary_write_offs_billing_add_views, \
	temporary_write_offs_billing_delete, temporary_write_offs_billing_views, temporary_write_offs_billing_edit_views
from modules.approval_process.temporary_write_offs_billing.models import *
from modules.approval_process.wage.code import wage_views, wage_delete, wage_add_views, wage_edit_views
from modules.approval_process.wage.models import Wage
from modules.approval_process.wage_replacement.code import wage_relacement_add_views, wage_relacement_delete, \
	wage_relacement_views, wage_relacement_edit_views
from modules.approval_process.wage_replacement.models import *
from modules.approval_process.write_offs.code import write_offs_views, write_offs_delete, write_offs_add_views, \
	write_offs_edit_views
from modules.approval_process.write_offs.models import *

# 审批流程
urlpatterns = [
	url(r'^$', apply_info_template_views.ApplyTemplateInfoView.as_view()),  # 默认不显示任何申请模板

	# 待审批相关
	url(r'^pending$', pending_views.PendingApprovalListView.as_view(), name="pending_list"),  # 待审批信息
	url(r'^pending/edit$', pending_action_views.PendingActionView.as_view(), name="pending_edit"),  # 待审批信息编辑
	url(r'^export$', export_approval.ApprovalExportView.as_view(), name="export_approval"),  # 根据申请类型，导出

	# 请假
	url(r'^leave$', leave_views.LeaveListView.as_view(), name="leave_list"),  # 请假申请
	url(r'^leave/(?P<pk>[0-9]+)/(?P<view_type>[0-9]+)$', leave_views.LeaveListView.as_view(), name="leave_one"),
	url(r'^leave_add$', leave_add_views.LeaveCreate.as_view(), name="leave_add"),  # 新增
	url(r'^leave_(?P<pk>[0-9]+)/edit$', leave_edit_views.LeaveUpdate.as_view(), {"model_name": Leave},
	    name="leave_edit"),  # 编辑
	url(r'^leave_(?P<pk>[0-9]+)/delete$', leave_delete.LeaveDelete.as_view(), {"model_name": Leave},
	    name="leave_delete"),  # 删除

	# 备用金
	url(r'^loan$', loan_views.LoanListView.as_view(), name="loan_list"),  # 借款申请
	url(r'^loan/(?P<pk>[0-9]+)/(?P<view_type>[0-9]+)$', loan_views.LoanListView.as_view(), name="loan_one"),  # 借款申请
	url(r'^loan_add$', loan_add_views.LoanCreate.as_view(), name="loan_add"),  # 新增
	# 编辑
	url(r'^loan_(?P<pk>[0-9]+)/edit$', loan_edit_views.LoanUpdate.as_view(), {"model_name": Loan},
	    name="loan_edit", ),
	# 删除
	url(r'^loan_(?P<pk>[0-9]+)/delete$', loan_delete.LoanDelete.as_view(), {"model_name": Loan},
	    name="loan_delete"),

	# 备用金，费用预算明细
	url(r'^loan/(?P<applicants>[0-9]+)/(?P<view_type>[0-9]+)/budget_details$',
	    loan_views.LoanBudgetDetailsListView.as_view(),
	    name="loan_budget_details_list"),  # 借款申请
	url(r'^loan/(?P<applicants>[0-9]+)/budget_details/add$', loan_add_views.LoanBudgetDetailsCreate.as_view(),
	    name="loan_budget_details_add"),  # 新增
	# 编辑
	url(r'^loan_budget_details_(?P<pk>[0-9]+)/(?P<applicants>[0-9]+)/edit$',
	    loan_edit_views.LoanBudgetDetailsUpdate.as_view(), {"model_name": LoanBudgetDetails},
	    name="loan_budget_details_edit"),
	# 删除
	url(r'^loan_budget_details_(?P<pk>[0-9]+)/(?P<applicants>[0-9]+)/delete$',
	    loan_delete.LoanBudgetDetailsDelete.as_view(), {"model_name": LoanBudgetDetails},
	    name="loan_budget_details_delete"),

	# 报销与销账
	url(r'^write_offs$', write_offs_views.WriteOffsListView.as_view(), name="write_offs_list"),  # 报销与销账
	url(r'^write_offs/(?P<pk>[0-9]+)/(?P<view_type>[0-9]+)$', write_offs_views.WriteOffsListView.as_view(),
	    name="writeoffs_one"),
	# 借款申请
	url(r'^write_offs_add$', write_offs_add_views.WriteOffsCreate.as_view(), name="write_offs_add"),  # 新增
	url(r'^write_offs_(?P<pk>[0-9]+)/edit$', write_offs_edit_views.WriteOffsUpdate.as_view(),
	    {"model_name": WriteOffs}, name="write_offs_edit"),  # 编辑
	url(r'^write_offs_(?P<pk>[0-9]+)/delete$', write_offs_delete.WriteOffsDelete.as_view(),
	    {"model_name": WriteOffs}, name="write_offs_delete"),  # 删除

	# 报销与销账，明细
	url(r'^write_offs/(?P<applicants>[0-9]+)/(?P<view_type>[0-9]+)/details$',
	    write_offs_views.WriteOffsDetailsListView.as_view(),
	    name="write_offs_details_list"),  # 报销与销账
	url(r'^write_offs/(?P<applicants>[0-9]+)/details/add$', write_offs_add_views.WriteOffsDetailsCreate.as_view(),
	    name="write_offs_details_add"),  # 新增
	url(r'^write_offs_(?P<pk>[0-9]+)/(?P<applicants>[0-9]+)/edit$',
	    write_offs_edit_views.WriteOffsDetailsUpdate.as_view(),
	    {"model_name": WriteOffsDetails}, name="write_offs_details_edit"),  # 编辑
	url(r'^write_offs_(?P<pk>[0-9]+)/(?P<applicants>[0-9]+)/delete$',
	    write_offs_delete.WriteOffsDetailsDelete.as_view(),
	    {"model_name": WriteOffsDetails}, name="write_offs_details_delete"),  # 删除

	# 工资与职位调整
	url(r'^wage$', wage_views.WageListView.as_view(), name="wage_list"),  # 工资申请
	url(r'^wage/(?P<pk>[0-9]+)/(?P<view_type>[0-9]+)$', wage_views.WageListView.as_view(), name="wage_one"),  # 工资申请
	url(r'^wage_add$', wage_add_views.WageCreate.as_view(), name="wage_add"),  # 新增
	url(r'^wage_(?P<pk>[0-9]+)/edit$', wage_edit_views.WageUpdate.as_view(), {"model_name": Wage},
	    name="wage_edit"),  # 编辑
	url(r'^wage_(?P<pk>[0-9]+)/delete$', wage_delete.WageDelete.as_view(), {"model_name": Wage},
	    name="wage_delete"),  # 删除

	# 工资补发申请
	url(r'^wage_replacement$', wage_relacement_views.WageReplacementListView.as_view(),
	    name="wage_replacement_list"),  # 工资补发申请
	url(r'^wage_replacement/(?P<pk>[0-9]+)/(?P<view_type>[0-9]+)$',
	    wage_relacement_views.WageReplacementListView.as_view(), name="wagereplacement_one"),
	url(r'^wage_replacement_add$', wage_relacement_add_views.WageReplacementCreate.as_view(),
	    name="wage_replacement_add"),  # 新增
	url(r'^wage_replacement_(?P<pk>[0-9]+)/edit$', wage_relacement_edit_views.WageReplacementUpdate.as_view(),
	    {"model_name": WageReplacement}, name="wage_replacement_edit"),  # 编辑
	url(r'^wage_replacement_(?P<pk>[0-9]+)/delete$', wage_relacement_delete.WageReplacementDelete.as_view(),
	    {"model_name": WageReplacement}, name="wage_replacement_delete"),  # 删除

	# 工资补发申请，明细
	url(r'^wage_replacement/(?P<applicants>[0-9]+)/(?P<view_type>[0-9]+)/details$',
	    wage_relacement_views.WageReplacementDetailsListView.as_view(),
	    name="wage_replacement_details_list"),  # 工资补发申请
	url(r'^wage_replacement/(?P<applicants>[0-9]+)/details/add$',
	    wage_relacement_add_views.WageReplacementDetailsCreate.as_view(),
	    name="wage_replacement_details_add"),  # 新增
	url(r'^wage_replacement_(?P<pk>[0-9]+)/(?P<applicants>[0-9]+)/edit$',
	    wage_relacement_edit_views.WageReplacementDetailsUpdate.as_view(),
	    {"model_name": WageReplacementDetails}, name="wage_replacement_details_edit"),  # 编辑
	url(r'^wage_replacement_(?P<pk>[0-9]+)/(?P<applicants>[0-9]+)/delete$',
	    wage_relacement_delete.WageReplacementDetailsDelete.as_view(),
	    {"model_name": WageReplacementDetails}, name="wage_replacement_details_delete"),  # 删除

	# 结算与发薪
	url(r'^billing_pre_pay$', billing_pre_pay_views.BillingPrePayListView.as_view(), name="billing_pre_pay_list"),
	url(r'^billing_pre_pay/(?P<pk>[0-9]+)/(?P<view_type>[0-9]+)$',
	    billing_pre_pay_views.BillingPrePayListView.as_view(), name="billingprepay_one"),
	# 工资申请
	url(r'^billing_pre_pay_add$', billing_pre_pay_add_views.BillingPrePayCreate.as_view(),
	    name="billing_pre_pay_add"),  # 新增
	url(r'^billing_pre_pay_(?P<pk>[0-9]+)/edit$', billing_pre_pay_edit_views.BillingPrePayUpdate.as_view(),
	    {"model_name": BillingPrePay}, name="billing_pre_pay_edit"),  # 编辑
	url(r'^billing_pre_pay_(?P<pk>[0-9]+)/delete$', billing_pre_pay_delete.BillingPrePayDelete.as_view(),
	    {"model_name": BillingPrePay}, name="billing_pre_pay_delete"),  # 删除

	# 管理员需求与离职
	url(r'^demand_turnover$', demand_turnover_views.DemandTurnoverListView.as_view(), name="demand_turnover_list"),
	url(r'^demand_turnover/(?P<pk>[0-9]+)/(?P<view_type>[0-9]+)$',
	    demand_turnover_views.DemandTurnoverListView.as_view(), name="demandturnover_one"),
	# 工资申请
	url(r'^demand_turnover_add$', demand_turnover_add_views.DemandTurnoverCreate.as_view(),
	    name="demand_turnover_add"),  # 新增
	url(r'^demand_turnover_(?P<pk>[0-9]+)/edit$', demand_turnover_edit_views.DemandTurnoverUpdate.as_view(),
	    {"model_name": DemandTurnover}, name="demand_turnover_edit"),  # 编辑
	url(r'^demand_turnover_(?P<pk>[0-9]+)/delete$', demand_turnover_delete.DemandTurnoverDelete.as_view(),
	    {"model_name": DemandTurnover}, name="demand_turnover_delete"),  # 删除

	# 临时工销账与开票
	url(r'^temporary_write_offs_billing$',
	    temporary_write_offs_billing_views.TemporaryWriteOffsBillingListView.as_view(),
	    name="temporary_write_offs_billing_list"),  # 查
	url(r'^temporary_write_offs_billing/(?P<pk>[0-9]+)/(?P<view_type>[0-9]+)$',
	    temporary_write_offs_billing_views.TemporaryWriteOffsBillingListView.as_view(),
	    name="temporarywriteoffsbilling_one"),  # 审核时-查
	url(r'^temporary_write_offs_billing_add$',
	    temporary_write_offs_billing_add_views.TemporaryWriteOffsBillingCreate.as_view(),
	    name="temporary_write_offs_billing_add"),  # 增
	url(r'^temporary_write_offs_billing_(?P<pk>[0-9]+)/edit$',
	    temporary_write_offs_billing_edit_views.TemporaryWriteOffsBillingUpdate.as_view(),
	    {"model_name": TemporaryWriteOffsBilling}, name="temporary_write_offs_billing_edit"),  # 编辑
	url(r'^temporary_write_offs_billing_(?P<pk>[0-9]+)/delete$',
	    temporary_write_offs_billing_delete.TemporaryWriteOffsBillingDelete.as_view(),
	    {"model_name": TemporaryWriteOffsBilling}, name="temporary_write_offs_billing_delete"),  # 删

	# 临时工销账与开票,明细
	url(r'^temporary_write_offs_billing/(?P<applicants>[0-9]+)/(?P<view_type>[0-9]+)/details$',
	    temporary_write_offs_billing_views.TemporaryWriteOffsBillingDetailsListView.as_view(),
	    name="temporary_write_offs_billing_details_list"),  # 查
	url(r'^temporary_write_offs_billing/(?P<applicants>[0-9]+)/details/add$',
	    temporary_write_offs_billing_add_views.TemporaryWriteOffsBillingDetailsCreate.as_view(),
	    name="temporary_write_offs_billing_details_add"),  # 增
	url(r'^temporary_write_offs_billing_details/(?P<pk>[0-9]+)/(?P<applicants>[0-9]+)/edit$',
	    temporary_write_offs_billing_edit_views.TemporaryWriteOffsBillingDetailsUpdate.as_view(),
	    {"model_name": TemporaryWriteOffsBillingDetails},
	    name="temporary_write_offs_billing_details_edit"),  # 改
	url(r'^temporary_write_offs_billing_details/(?P<pk>[0-9]+)/(?P<applicants>[0-9]+)/delete$',
	    temporary_write_offs_billing_delete.TemporaryWriteOffsBillingDetailsDelete.as_view(),
	    {"model_name": TemporaryWriteOffsBillingDetails},
	    name="temporary_write_offs_billing_details_delete"),  # 删

	# 待招结算与销账
	url(r'^recruitedbilling$', recruitedbilling_views.RecruitedBillingListView.as_view(),
	    name="recruitedbilling_list"),
	url(r'^recruitedbilling/(?P<pk>[0-9]+)/(?P<view_type>[0-9]+)$',
	    recruitedbilling_views.RecruitedBillingListView.as_view(), name="recruitedbilling_one"),
	url(r'^recruitedbilling_add$', recruitedbilling_add_views.RecruitedBillingCreate.as_view(),
	    name="recruitedbilling_add"),  # 新增
	# 编辑
	url(r'^recruitedbilling_(?P<pk>[0-9]+)/edit$', recruitedbilling_edit_views.RecruitedBillingUpdate.as_view(),
	    {"model_name": RecruitedBilling},
	    name="recruitedbilling_edit", ),
	# 删除
	url(r'^recruitedbilling_(?P<pk>[0-9]+)/delete$', recruitedbilling_delete.RecruitedBillingDelete.as_view(),
	    {"model_name": RecruitedBilling},
	    name="recruitedbilling_delete"),

	# 待招结算与销账，报销/销账明细
	url(r'^recruitedbilling/(?P<applicants>[0-9]+)/(?P<view_type>[0-9]+)/details$',
	    recruitedbilling_views.RecruitedBillingDetailsListView.as_view(),
	    name="recruitedbilling_details_list"),
	url(r'^recruitedbilling/(?P<applicants>[0-9]+)/details/add$',
	    recruitedbilling_add_views.RecruitedBillingBudgetDetailsCreate.as_view(),
	    name="recruitedbilling_details_add"),  # 新增
	# 编辑
	url(r'^recruitedbilling_details_(?P<pk>[0-9]+)/(?P<applicants>[0-9]+)/edit$',
	    recruitedbilling_edit_views.RecruitedBillingDetailsUpdate.as_view(), {"model_name": RecruitedBillingDetails},
	    name="recruitedbilling_details_edit"),
	# 删除
	url(r'^recruitedbilling_details_(?P<pk>[0-9]+)/(?P<applicants>[0-9]+)/delete$',
	    recruitedbilling_delete.RecruitedBillingDetailsDelete.as_view(), {"model_name": RecruitedBillingDetails},
	    name="recruitedbilling_details_delete"),
]

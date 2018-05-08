# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView

from modules.approval_process.billing_pre_pay.models import BillingPrePay
from modules.approval_process.demand_turnover.models import DemandTurnover
from modules.approval_process.leave.models import Leave
from modules.approval_process.loan.models import Loan
from modules.approval_process.models import *
from modules.approval_process.recruited_billing.models import RecruitedBilling
from modules.approval_process.temporary_write_offs_billing.models import TemporaryWriteOffsBilling
from modules.approval_process.wage.models import Wage
from modules.approval_process.wage_replacement.models import WageReplacement
from modules.approval_process.write_offs.models import WriteOffs
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs
from config.conf_core import PAGINATE


@class_view_decorator(login_required)
@class_view_decorator(permission_required('approval_process.browse_pendingapproval', raise_exception=True))
class PendingApprovalListView(ListView):
	"""待审批信息 """
	context_object_name = "pending_approval_list"
	template_name = "pending_approval_list.html"
	allow_empty = True
	paginate_by = PAGINATE

	def get_queryset(self):
		try:
			self.apply_types = self.request.GET.get("apply_types", "")
			self.apply_user = self.request.GET.get("apply_user", "")
			self.status = self.request.GET.get("status", "")
			self.handle_user = self.request.GET.get("handle_user", "")

			search_condition = {
				"apply_types": self.apply_types,
				"apply_user__first_name__icontains": self.apply_user,
				"status": self.status,
				"handle_user": self.handle_user
			}
			kwargs = get_kwargs(search_condition)
			return self.get_pending_apply(kwargs)
		except:
			traceback.print_exc()

	def get_pending_apply(self, kwargs):
		result_pending = list()
		try:
			# 请假
			find_leaves = Leave.objects.filter(**kwargs)
			leave_pend = PendingApproval.objects.filter(object_id__in=find_leaves, apply_type="1")

			# 备用金
			find_loans = Loan.objects.filter(**kwargs)
			loan_pend = PendingApproval.objects.filter(object_id__in=find_loans, apply_type="2")

			# 报销与销账
			find_writeoffs = WriteOffs.objects.filter(**kwargs)
			writeoffs_pend = PendingApproval.objects.filter(object_id__in=find_writeoffs, apply_type="3")

			# 工资与职位调整
			find_wages = Wage.objects.filter(**kwargs)
			wage_pend = PendingApproval.objects.filter(object_id__in=find_wages, apply_type="4")

			# 工资补发申请
			find_wagereplacement = WageReplacement.objects.filter(**kwargs)
			wagereplacement_pend = PendingApproval.objects.filter(object_id__in=find_wagereplacement,
									      apply_type="5")

			# 结算与发薪
			find_billingprepay = BillingPrePay.objects.filter(**kwargs)
			billingprepay_pend = PendingApproval.objects.filter(object_id__in=find_billingprepay,
									    apply_type="6")

			# 管理人员需求与离职
			find_demandturnover = DemandTurnover.objects.filter(**kwargs)
			demandturnover_pend = PendingApproval.objects.filter(object_id__in=find_demandturnover,
									     apply_type="7")

			# 临时工销账与开票
			find_temporarywriteoffsbilling = TemporaryWriteOffsBilling.objects.filter(**kwargs)
			temporarywriteoffsbilling_pend = PendingApproval.objects.filter(
				object_id__in=find_temporarywriteoffsbilling, apply_type="8")

			# 代招结算与销账
			find_recruitedbilling = RecruitedBilling.objects.filter(**kwargs)
			recruitedbilling_pend = PendingApproval.objects.filter(
				object_id__in=find_recruitedbilling, apply_type="9")
			result_pending = leave_pend | loan_pend | writeoffs_pend | wage_pend | wagereplacement_pend | billingprepay_pend | demandturnover_pend | temporarywriteoffsbilling_pend | recruitedbilling_pend
		except:
			traceback.print_exc()
		finally:
			return result_pending

	def get_context_data(self, **kwargs):
		context = super(PendingApprovalListView, self).get_context_data(**kwargs)
		context["apply_user"] = self.apply_user
		context["status"] = self.status
		context["list_status"] = APPLY_STATUS_CHOICES
		context["apply_types"] = self.apply_types
		context["list_apply_types"] = APPLY_TYPE_CHOICES
		return context

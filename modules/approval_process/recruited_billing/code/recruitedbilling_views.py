# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.views.generic import ListView

from modules.approval_process.recruited_billing.models import *
from modules.share_module.formater import *
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs
from config.conf_core import PAGINATE


@class_view_decorator(login_required)
@class_view_decorator(permission_required('recruited_billing.browse_recruitedbilling', raise_exception=True))
class RecruitedBillingListView(ListView):
	context_object_name = "recruitedbilling_list"
	template_name = "all_apply_list.html"
	allow_empty = True
	paginate_by = PAGINATE

	def get_queryset(self):
		try:
			self.pk = self.kwargs.get("pk", "")
			self.view_type = self.kwargs.get("view_type", "1")
			self.title = self.request.GET.get("title", "")
			self.status = self.request.GET.get("status", "")
			self.month = self.request.GET.get("month", "")  # 月份
			self.dept_name = self.request.GET.get("dept_name", "")  # 部门名称

			created_year = ""
			created_month = ""
			if self.month:
				created_date = date_formater(self.month, "%Y/%m/%d")
				created_year = created_date.year
				created_month = created_date.month

			search_condition = {
				"pk": self.pk,
				"title__icontains": self.title,
				"status": self.status,
				"created__year": created_year,
				"created__month": created_month,
				"apply_user__attribution_dept__icontains": self.dept_name,
			}
			if not self.request.user.is_superuser and self.view_type == "1":
				search_condition.update({"apply_user": self.request.user})

			kwargs = get_kwargs(search_condition)
			return RecruitedBilling.objects.filter(**kwargs)
		except:
			traceback.print_exc()

	def get_context_data(self, **kwargs):
		context = super(RecruitedBillingListView, self).get_context_data(**kwargs)
		context["title"] = self.title
		context["status"] = self.status
		context["month"] = self.month  # 申请月份
		context["dept_name"] = self.dept_name  # 部门
		context["apply_type"] = "recruitedbilling"
		context["add_url"] = reverse('approval:recruitedbilling_add')  # 新增url
		# 查看方式，# 1:由明细表返回，申请页面带查询条件，2：由待审批超链进去，不带查询条件
		context["view_type"] = self.view_type
		return context


@class_view_decorator(login_required)
@class_view_decorator(permission_required('recruited_billing.browse_recruitedbillingdetails ', raise_exception=True))
class RecruitedBillingDetailsListView(ListView):
	context_object_name = "recruited_billing_details_list"
	template_name = "recruited_billing_details_list.html"
	allow_empty = True
	paginate_by = PAGINATE

	def get_queryset(self):
		try:
			self.applicants = self.kwargs.get("applicants", "")
			self.view_type = self.kwargs.get("view_type", "1")
			search_condition = {"applicants": self.applicants}
			kwargs = get_kwargs(search_condition)
			return RecruitedBillingDetails.objects.filter(**kwargs)
		except:
			traceback.print_exc()

	def get_context_data(self, **kwargs):
		context = super(RecruitedBillingDetailsListView, self).get_context_data(**kwargs)
		context["add_url"] = reverse('approval:recruitedbilling_details_add', args=(self.applicants,))  # 新增url
		# 1:由明细表返回，申请页面带查询条件，2：由待审批超链进去，不带查询条件
		context["return_url"] = reverse('approval:recruitedbilling_one', args=(self.applicants, self.view_type))  # 返回url
		context["view_type"] = self.view_type
		context["applicants"] = self.applicants
		context["apply_info"] = RecruitedBilling.objects.filter(id=self.applicants).first()
		return context

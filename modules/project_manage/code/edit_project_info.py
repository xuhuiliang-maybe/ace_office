# coding=utf-8
import traceback

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView

from modules.project_manage.models import Project
from modules.share_module.check_decorator import check_principal
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs


@class_view_decorator(login_required)
@class_view_decorator(permission_required('project_manage.change_project', raise_exception=True))
@class_view_decorator(check_principal)
class ProjectUpdate(SuccessMessageMixin, UpdateView):
    """基础信息"""
    model = Project
    template_name = "projects_edit.html"
    success_message = u"%(full_name)s 成功修改"
    fields = [
        "number", "short_name", "full_name", "principal", "department", "customer", "business_city",
        "company_subject", "contract_type", "project_type", "start_date", "end_date",
        "progress_state", "customer_service_staff", "customer_service_charge",
        "outsource_director", "customer_service_director", "other_responsible_person"
    ]

    def get_success_url(self):
        url = reverse('project_manage:project_list', args=("basic_info",))
        referrer = self.request.POST.get("referrer", "")
        if referrer:
            url = referrer

        _addanother = self.request.POST.get("_addanother", "")
        if _addanother:
            url = reverse('project_manage:project-add')
        return url

    def get_context_data(self, **kwargs):
        kwargs["form_content"] = u"编辑项目基础信息"
        kwargs["referrer"] = self.request.META.get('HTTP_REFERER', "")
        return super(ProjectUpdate, self).get_context_data(**kwargs)

    def form_valid(self, form):
        try:
            principal = ""
            customer_service_staff = self.request.POST.get("customer_service_staff", "")  # 客服专员
            customer_service_charge = self.request.POST.get("customer_service_charge", "")  # 客服主管
            outsource_director = self.request.POST.get("outsource_director", "")  # 外包主管
            customer_service_director = self.request.POST.get("customer_service_director", "")  # 客服经理
            other_responsible_person = self.request.POST.get("other_responsible_person", "")  # 其他负责人
            if customer_service_staff:
                principal = customer_service_staff
            elif customer_service_charge:
                principal = customer_service_charge
            elif outsource_director:
                principal = outsource_director
            elif customer_service_director:
                principal = customer_service_director
            elif other_responsible_person:
                principal = other_responsible_person

            search_condition = {"id": principal}
            kwargs = get_kwargs(search_condition)
            if kwargs:
                temp_user = User.objects.filter(**kwargs)
                if temp_user.exists():
                    form.instance.principal = temp_user.first()
            return super(ProjectUpdate, self).form_valid(form)
        except:
            traceback.print_exc()


@class_view_decorator(login_required)
@class_view_decorator(permission_required('project_manage.change_social_security_info', raise_exception=True))
@class_view_decorator(check_principal)
class ProjectSocialSecurityInfoUpdate(SuccessMessageMixin, UpdateView):
    """福利信息"""
    model = Project
    template_name = "projects_edit.html"
    success_message = u"%(insured_place)s 成功修改"
    fields = [
        "insured_place", "social_security_type", "social_security_account_type",
        "social_security_account_name", "social_security_node_require",
        "social_security_settlement_cycle", "business_insurance_company",
        "business_insurance_settlement_cycle", "business_insurance_standard",
        "business_insurance_payment", "business_insurance_node_require",
        "accumulation_fund_place_province", "proportion", "radix",
    ]

    def get_success_url(self):
        self.url = reverse('project_manage:project_list', args=("social_security_info",))
        referrer = self.request.POST.get("referrer", "")
        if referrer:
            self.url = referrer
        return self.url

    def get_context_data(self, **kwargs):
        kwargs["form_content"] = u"编辑项目福利信息"
        kwargs["referrer"] = self.request.META.get('HTTP_REFERER', "")
        return super(ProjectSocialSecurityInfoUpdate, self).get_context_data(**kwargs)


@class_view_decorator(login_required)
@class_view_decorator(permission_required('project_manage.change_settle_accounts_info', raise_exception=True))
@class_view_decorator(check_principal)
class ProjectSettleAccountsInfoUpdate(SuccessMessageMixin, UpdateView):
    """结算信息"""
    model = Project
    template_name = "projects_edit.html"
    success_message = u"%(service_standard)s 成功修改"
    fields = [
        "service_standard", "service_cost_node_require", "residual_premium_cycle",
        "residual_premium_place", "settlement_report_day", "cost_arrival_day",
        "wage_grant_day", "wage_grant_type", "settlement_person", "abnormal_settlement",
        "wage_service_cost_settlement_cycle", "other_project",
    ]

    def get_success_url(self):
        url = reverse('project_manage:project_list', args=("settle_accounts_info",))
        referrer = self.request.POST.get("referrer", "")
        if referrer:
            url = referrer
        return url

    def get_context_data(self, **kwargs):
        kwargs["form_content"] = u"编辑项目结算信息"
        kwargs["referrer"] = self.request.META.get('HTTP_REFERER', "")
        return super(ProjectSettleAccountsInfoUpdate, self).get_context_data(**kwargs)


@class_view_decorator(login_required)
@class_view_decorator(permission_required('project_manage.change_billing_info', raise_exception=True))
@class_view_decorator(check_principal)
class ProjectBillingInfoUpdate(SuccessMessageMixin, UpdateView):
    """开票信息"""
    model = Project
    template_name = "projects_edit.html"
    success_message = u"%(invoice_title)s 成功修改"
    fields = [
        "invoice_title",
        "invoice_mode",
        "special_subject",
        "special_cost",
        "special_desc",
        "general_subject",
        "general_cost",
        "general_desc",
        "invoice_receiver",
        "invoice_phone",
        "invoice_mail",
        "fast_mail_desc",
        "invoice_open_date",
        "is_general_taxpayer",
        "taxpayer_identifier",
        "address",
        "phone",
        "bank",
        "account_number",
    ]

    def get_success_url(self):
        url = reverse('project_manage:project_list', args=("billing_info",))
        referrer = self.request.POST.get("referrer", "")
        if referrer:
            url = referrer
        return url

    def get_context_data(self, **kwargs):
        kwargs["form_content"] = u"编辑项目开票信息"
        kwargs["referrer"] = self.request.META.get('HTTP_REFERER', "")
        return super(ProjectBillingInfoUpdate, self).get_context_data(**kwargs)


@class_view_decorator(login_required)
@class_view_decorator(permission_required('project_manage.change_sales_info', raise_exception=True))
@class_view_decorator(check_principal)
class ProjectSalesInfoUpdate(SuccessMessageMixin, UpdateView):
    """销售信息"""
    model = Project
    template_name = "projects_edit.html"
    success_message = u"%(salesman)s 成功修改"
    fields = [
        "salesman", "sales_type",
        "dispatch_commission", "remark1",
        "outsourc_commission", "remark2",
        "proxy_personnel_commission", "remark3",
        "proxy_recruitment_commission", "remark4",
        "hourly_commission", "remark5",
    ]

    def get_success_url(self):
        url = reverse('project_manage:project_list', args=("sales_info",))
        referrer = self.request.POST.get("referrer", "")
        if referrer:
            url = referrer
        return url

    def get_context_data(self, **kwargs):
        kwargs["form_content"] = u"编辑项目销售信息"
        kwargs["referrer"] = self.request.META.get('HTTP_REFERER', "")
        return super(ProjectSalesInfoUpdate, self).get_context_data(**kwargs)


@class_view_decorator(login_required)
@class_view_decorator(permission_required('project_manage.change_recruitment_unit', raise_exception=True))
@class_view_decorator(check_principal)
class ProjectRecruitmentUnitUpdate(SuccessMessageMixin, UpdateView):
    """招聘单价"""
    model = Project
    template_name = "projects_edit.html"
    success_url = "/projectmanage/project/recruitment_unit"
    success_message = u"%(recruit_difficulty)s 成功修改"
    fields = [
        "recruit_difficulty", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug",
        "sep", "oct", "nov", "dec",
    ]

    def get_success_url(self):
        url = reverse('approval:leave_list', args=())
        referrer = self.request.POST.get("referrer", "")
        if referrer:
            url = referrer
        return url

    def get_context_data(self, **kwargs):
        kwargs["form_content"] = u"编辑项目招聘单价"
        kwargs["referrer"] = self.request.META.get('HTTP_REFERER', "")
        return super(ProjectRecruitmentUnitUpdate, self).get_context_data(**kwargs)

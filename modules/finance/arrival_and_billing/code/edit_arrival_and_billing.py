# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView

from modules.approval_process.billing_pre_pay.models import BillingPrePay
from modules.approval_process.temporary_write_offs_billing.models import TemporaryWriteOffsBilling
from modules.finance.arrival_and_billing.models import *
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('arrival_and_billing.change_arrivalandbilling', raise_exception=True))
# @class_view_decorator(check_principal)  # 校验是否负责该项目
class ArrivalAndBillingUpdate(SuccessMessageMixin, UpdateView):
    model = ArrivalAndBilling
    template_name = "arrival_and_billing_edit.html"
    success_message = u"%(project_name)s 成功修改"
    fields = ["project_name", "settlement_date"]

    def get_success_url(self):
        self.url = self.model.get_absolute_url()

        referrer = self.request.POST.get("referrer", "")
        if referrer:
            self.url = referrer

        _addanother = self.request.POST.get("_addanother", "")
        if _addanother:
            self.url = reverse('finance:arrival_and_billing:add_arrivalandbilling')

        return self.url

    # 增加返回参数
    def get_context_data(self, **kwargs):
        context = super(ArrivalAndBillingUpdate, self).get_context_data(**kwargs)
        context["form_content"] = u"修改到账与开票"
        referrer = self.request.META.get('HTTP_REFERER', "")
        context["referrer"] = referrer
        return context

    # 表单处理
    def form_valid(self, form):
        project_name = self.request.POST.get("project_name", "")  # 项目名称
        settlement_date = self.request.POST.get("settlement_date", "")  # 结算月份

        # 结算金额（长期业务）
        settlement_amount_long = 0
        try:
            billingprepay = BillingPrePay.objects.filter(
                project_name=project_name,
                billingprepay_month=settlement_date)
        except:
            settlement_date = settlement_date.replace('/', '-')
            billingprepay = BillingPrePay.objects.filter(
                project_name=project_name,
                billingprepay_month=settlement_date)
        if billingprepay.exists():
            settlement_amount_long = billingprepay.first().main_business_income
        form.instance.settlement_amount_long = settlement_amount_long

        # 结算金额（临时工）
        settlement_amount_snap = 0
        temporarywriteoffsbilling = TemporaryWriteOffsBilling.objects.filter(
            project_name=project_name,
            billing_month=settlement_date)
        if temporarywriteoffsbilling.exists():
            if temporarywriteoffsbilling.first().billing_type != "2":
                settlement_amount_snap = temporarywriteoffsbilling.first().main_business_income
        form.instance.settlement_amount_snap = settlement_amount_snap

        # 结算合计
        settlement_tatol = settlement_amount_long + settlement_amount_snap
        form.instance.settlement_tatol = settlement_tatol

        # 到账金额合计
        credited_amount_total = 0
        credited_amount_s = CreditedDetails.objects.filter(arrival=form.instance).aggregate(
            Sum('credited_amount'))
        credited_amount_sum = credited_amount_s["credited_amount__sum"]
        if credited_amount_sum:
            credited_amount_total = credited_amount_sum
        form.instance.credited_amount_total = credited_amount_total  # 默认0

        # 到账时间
        crediteddetails = CreditedDetails.objects.filter(arrival=form.instance).order_by("-credited_date")
        if crediteddetails.exists():
            form.instance.credited_date = crediteddetails.first().credited_date

        # 到账情况
        if credited_amount_total == 0:
            form.instance.credited_state = "4"
        elif settlement_tatol > credited_amount_total:
            form.instance.credited_state = "1"
        elif settlement_tatol == credited_amount_total:
            form.instance.credited_state = "2"
        elif settlement_tatol < credited_amount_total:
            form.instance.credited_state = "3"

        # 开票金额合计
        billing_amount_total = 0
        billingdetails_s = BillingDetails.objects.filter(billing=form.instance).aggregate(
            Sum('billing_amount'))
        billing_amount_sum = billingdetails_s["billing_amount__sum"]
        if billing_amount_sum:
            billing_amount_total = billing_amount_sum
        form.instance.billing_amount_total = billing_amount_total  # 默认0

        # 开票时间
        billingdetails = BillingDetails.objects.filter(billing=form.instance).order_by("-billing_date")
        if billingdetails.exists():
            form.instance.billing_date = billingdetails.first().billing_date

        # 开票情况
        if billing_amount_total == 0:
            form.instance.billing_state = "4"
        elif settlement_tatol > billing_amount_total:
            form.instance.billing_state = "1"
        elif settlement_tatol == billing_amount_total:
            form.instance.billing_state = "2"
        elif settlement_tatol < billing_amount_total:
            form.instance.billing_state = "3"

        return super(ArrivalAndBillingUpdate, self).form_valid(form)


@class_view_decorator(login_required)
class CreditedDetailsUpdate(SuccessMessageMixin, UpdateView):
    model = CreditedDetails
    template_name = "arrival_and_billing_edit.html"
    success_message = u"%(credited_amount)s 成功修改"
    fields = ["credited_amount", "credited_date"]

    # 增加返回参数
    def get_context_data(self, **kwargs):
        context = super(CreditedDetailsUpdate, self).get_context_data(**kwargs)
        context["form_content"] = u"修改到账明细"
        referrer = self.request.META.get('HTTP_REFERER', "")
        context["referrer"] = referrer
        return context

    # 表单处理
    def form_valid(self, form):
        return super(CreditedDetailsUpdate, self).form_valid(form)

    def get_success_url(self):
        arrivalandbilling = self.kwargs.get("arrivalandbilling", 0)
        self.url = reverse('finance:arrival_and_billing:list_crediteddetails', args=(arrivalandbilling))
        referrer = self.request.POST.get("referrer", "")
        if referrer:
            self.url = referrer

        _addanother = self.request.POST.get("_addanother", "")
        if _addanother:
            self.url = reverse('finance:arrival_and_billing:add_crediteddetails', args=(self.arrivalandbilling))

        return self.url


@class_view_decorator(login_required)
class BillingDetailsUpdate(SuccessMessageMixin, UpdateView):
    model = BillingDetails
    template_name = "billing_details_edit.html"
    success_message = u"%(billing_amount)s 成功修改"
    fields = ["billing_amount", "billing_date"]

    # 增加返回参数
    def get_context_data(self, **kwargs):
        context = super(BillingDetailsUpdate, self).get_context_data(**kwargs)
        context["form_content"] = u"修改开票明细"
        referrer = self.request.META.get('HTTP_REFERER', "")
        context["referrer"] = referrer
        return context

    # 表单处理
    def form_valid(self, form):
        return super(BillingDetailsUpdate, self).form_valid(form)

    def get_success_url(self):
        arrivalandbilling = self.kwargs.get("arrivalandbilling", 0)
        self.url = reverse('finance:arrival_and_billing:list_billingdetails', args=(arrivalandbilling))
        referrer = self.request.POST.get("referrer", "")
        if referrer:
            self.url = referrer
        _addanother = self.request.POST.get("_addanother", "")
        if _addanother:
            self.url = reverse('finance:arrival_and_billing:add_billingdetails', args=(self.arrivalandbilling))

        return self.url

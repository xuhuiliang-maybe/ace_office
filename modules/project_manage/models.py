# coding=utf-8
from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import ModelChoiceField, TypedChoiceField
from model_utils.models import TimeStampedModel

from modules.dict_table.models import *
from modules.organizational_structure.departments.models import Department


class Project(TimeStampedModel):
    """项目信息 """
    IS_GENERAL_TAXPAYER = (
        ('1', u'是'),
        ('2', u'否'),
    )
    number = models.CharField(u"项目编号", max_length=11)  # 唯一
    short_name = models.CharField(u"项目简称", max_length=50, blank=True)
    full_name = models.CharField(u"项目名称", max_length=200, blank=True)
    principal = models.ForeignKey(User, verbose_name=u"项目负责人", related_name="principal", on_delete=models.SET_NULL,
                                  blank=True, null=True)
    department = models.ForeignKey(Department, verbose_name=u"负责部门", blank=True, null=True, on_delete=models.SET_NULL)

    # 基础信息
    customer = models.CharField(u"客户名称", max_length=200, blank=True)
    business_city = models.CharField(u"业务城市", max_length=256, blank=True)
    company_subject = models.ForeignKey(CompanySubject, verbose_name=u"公司主体", on_delete=models.SET_NULL, blank=True,
                                        null=True)
    contract_type = models.ForeignKey(ContractType, verbose_name=u"合同类别", on_delete=models.SET_NULL, blank=True,
                                      null=True)
    project_type = models.ForeignKey(ProjectType, verbose_name=u"项目类别", on_delete=models.SET_NULL, blank=True,
                                     null=True)
    start_date = models.DateField(u"起始时间", blank=True, null=True)
    end_date = models.DateField(u"终止时间", blank=True, null=True)
    progress_state = models.ForeignKey(ProgressState, verbose_name=u"目前状态", on_delete=models.SET_NULL, blank=True,
                                       null=True)
    customer_service_staff = models.ForeignKey(User, verbose_name=u"客服专员", on_delete=models.SET_NULL,
                                               related_name="customer_service_staff",
                                               limit_choices_to={'position__name': u"客服专员"}, blank=True, null=True)
    customer_service_charge = models.ForeignKey(User, verbose_name=u"客服主管", related_name="customer_service_charge",
                                                limit_choices_to={'position__name': u"客服主管"}, on_delete=models.SET_NULL,
                                                blank=True, null=True)
    outsource_director = models.ForeignKey(User, verbose_name=u"外包主管", related_name="outsource_director",
                                           limit_choices_to={'position__name': u"外包主管"}, on_delete=models.SET_NULL,
                                           blank=True, null=True)
    customer_service_director = models.ForeignKey(User, verbose_name=u"客服经理", null=True,
                                                  related_name="customer_service_director",
                                                  limit_choices_to={'position__name': u"客服经理"}, blank=True,
                                                  on_delete=models.SET_NULL)
    other_responsible_person = models.ForeignKey(User, verbose_name=u"其他负责人", blank=True, null=True,
                                                 related_name="other_responsible_person", on_delete=models.SET_NULL)

    # 福利信息
    insured_place = models.CharField(u"参保地", max_length=100, blank=True)  # 省+市
    social_security_type = models.ManyToManyField(SocialSecurityType, verbose_name=u"社保险种", blank=True,
                                                  help_text=u"按住 ”Control“，或者Mac上的 “Command”，可以选择多个。")
    social_security_account_type = models.ForeignKey(SocialSecurityAccountType, verbose_name=u"社保账户类型", blank=True,
                                                     null=True, on_delete=models.SET_NULL)
    social_security_account_name = models.CharField(u"社保账户名称", max_length=100, blank=True)
    social_security_node_require = models.TextField(u"社保节点要求", blank=True)
    social_security_settlement_cycle = models.CharField(u"社保结算周期", max_length=100, blank=True)
    business_insurance_company = models.ManyToManyField(BusinessInsuranceCompany, verbose_name=u"商保公司", blank=True,
                                                        help_text=u"按住 ”Control“，或者Mac上的 “Command”，可以选择多个。")
    business_insurance_settlement_cycle = models.ForeignKey(Cycle, verbose_name=u"商保结算周期", blank=True, null=True,
                                                            related_name="business_insurance_settlement_cycle",
                                                            on_delete=models.SET_NULL)
    business_insurance_standard = models.CharField(u"商保收取标准", max_length=100, help_text=u"请录入一个周期的商保费用标准", blank=True,
                                                   null=True)
    business_insurance_payment = models.CharField(u"商保赔付额度", max_length=100, blank=True)
    business_insurance_node_require = models.CharField(u"商保节点要求", max_length=100, blank=True)
    accumulation_fund_place_province = models.CharField(u"公积金地点", max_length=100, blank=True)  # 省
    proportion = models.CharField(u"比例", max_length=10, blank=True)
    radix = models.CharField(u"基数", max_length=100, blank=True)

    # 结算信息
    service_standard = models.TextField(u"服务费标准", blank=True)
    service_cost_node_require = models.TextField(u"服务费节点要求", blank=True)
    residual_premium_cycle = models.ForeignKey(Cycle, verbose_name=u"残保金收取周期", blank=True, null=True,
                                               related_name="residual_premium_cycle", on_delete=models.SET_NULL)
    residual_premium_place = models.CharField(u"残保金收取地", max_length=100, blank=True, )  # 省市县
    settlement_report_day = models.CharField(u"提供结算表时间", max_length=200, blank=True)  # 只选日期
    cost_arrival_day = models.CharField(u"费用到账时间", max_length=200, blank=True)  # 只选日期
    wage_grant_day = models.CharField(u"工资发放时间", max_length=200, blank=True)
    wage_grant_type = models.ForeignKey(WageGrantType, verbose_name=u"工资发放方式", blank=True, null=True,
                                        on_delete=models.SET_NULL)
    settlement_person = models.TextField(u"结算对接人及联系方式", blank=True)
    abnormal_settlement = models.TextField(u"异常结算情况", help_text=u"请列出不结算工资的情况", blank=True)
    wage_service_cost_settlement_cycle = models.CharField(u"工资服务费结算周期", max_length=100, blank=True)
    other_project = models.CharField(u"其他需要我司代收代付项目", max_length=100, blank=True)

    # 开票信息
    invoice_type = models.ForeignKey(InvoiceType, verbose_name=u"发票类型", blank=True, null=True,
                                     on_delete=models.SET_NULL, editable=False)
    invoice_title = models.CharField(u"发票抬头", max_length=200, blank=True)
    invoice_mode = models.CharField(u"开票方式", max_length=200, blank=True)
    special_subject = models.CharField(u"专票科目", max_length=200, blank=True)
    special_cost = models.TextField(u"专票费用内容 ", blank=True)
    special_desc = models.TextField(u"专票说明 ", blank=True)
    general_subject = models.CharField(u"普票科目 ", max_length=200, blank=True)
    general_cost = models.TextField(u"普票费用内容 ", blank=True)
    general_desc = models.TextField(u"普票说明 ", blank=True)
    invoice_receiver = models.CharField(u"发票接收人 ", max_length=200, blank=True)
    invoice_phone = models.CharField(u"电话 ", max_length=200, blank=True)
    invoice_mail = models.TextField(u"地址", blank=True)
    fast_mail_desc = models.TextField(u"快递说明 ", blank=True)
    invoice_open_date = models.CharField(u"发票开具时间", max_length=200, blank=True)
    is_general_taxpayer = models.CharField(u"是否一般纳税人", max_length=2, blank=True, choices=IS_GENERAL_TAXPAYER,
                                           default="2")
    taxpayer_identifier = models.CharField(u"纳税人识别号", max_length=200, blank=True)
    address = models.CharField(u"地址", max_length=200, blank=True)
    phone = models.CharField(u"电话", max_length=200, blank=True)
    bank = models.CharField(u"开户行", max_length=200, blank=True)
    account_number = models.CharField(u"账号", max_length=200, blank=True)

    # 销售信息
    salesman = models.ForeignKey(User, verbose_name=u"销售人员", related_name="salesman", blank=True, null=True,
                                 on_delete=models.SET_NULL)
    sales_type = models.ForeignKey(SalesType, verbose_name=u"销售类型", blank=True, null=True, on_delete=models.SET_NULL)

    dispatch_commission = models.FloatField(u"派遣提成标准", blank=True, null=True)
    remark1 = models.CharField(u"备注", max_length=256, blank=True)

    outsourc_commission = models.FloatField(u"外包提成标准", blank=True, null=True)
    remark2 = models.CharField(u"备注", max_length=256, blank=True)

    proxy_personnel_commission = models.FloatField(u"代理人事提成标准", blank=True, null=True)
    remark3 = models.CharField(u"备注", max_length=256, blank=True)

    proxy_recruitment_commission = models.FloatField(u"代理招聘提成标准", blank=True, null=True)
    remark4 = models.CharField(u"备注", max_length=256, blank=True)

    hourly_commission = models.FloatField(u"小时工提成标准", blank=True, null=True)
    remark5 = models.CharField(u"备注", max_length=256, blank=True)

    # 招聘单价
    recruit_difficulty = models.CharField(u"招聘难度系数", max_length=256, blank=True)
    jan = models.CharField(u"1月", max_length=256, blank=True, null=True)
    feb = models.CharField(u"2月", max_length=256, blank=True, null=True)
    mar = models.CharField(u"3月", max_length=256, blank=True, null=True)
    apr = models.CharField(u"4月", max_length=256, blank=True, null=True)
    may = models.CharField(u"5月", max_length=256, blank=True, null=True)
    jun = models.CharField(u"6月", max_length=256, blank=True, null=True)
    jul = models.CharField(u"7月", max_length=256, blank=True, null=True)
    aug = models.CharField(u"8月", max_length=256, blank=True, null=True)
    sep = models.CharField(u"9月", max_length=256, blank=True, null=True)
    oct = models.CharField(u"10月", max_length=256, blank=True, null=True)
    nov = models.CharField(u"11月", max_length=256, blank=True, null=True)
    dec = models.CharField(u"12月", max_length=256, blank=True, null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = u"项目信息"
        verbose_name_plural = u"项目信息s"
        ordering = ['-id']  # id倒叙
        permissions = (
            ("browse_basic_info", u"浏览 项目基础信息"),

            ("browse_social_security_info", u"浏览 项目社保信息"),
            ("change_social_security_info", u"修改 项目社保信息"),

            ("browse_settle_accounts_info", u"浏览 项目结算信息"),
            ("change_settle_accounts_info", u"修改 项目结算信息"),

            ("browse_billing_info", u"浏览 项目开票信息"),
            ("change_billing_info", u"修改 项目开票信息"),

            ("browse_sales_info", u"浏览 项目销售信息"),
            ("change_sales_info", u"修改 项目销售信息"),

            ("browse_recruitment_unit", u"浏览 项目招聘单价"),
            ("change_recruitment_unit", u"修改 项目招聘单价"),
        )

    def get_absolute_url(self):
        return "/projectmanage/project/basic_info"

    def get_unit_price(self, month_str):
        price = 0
        try:
            unit_price = {
                "1": self.jan, "2": self.feb, "3": self.mar, "4": self.apr,
                "5": self.may, "6": self.jun, "7": self.jul, "8": self.aug,
                "9": self.sep, "10": self.oct, "11": self.nov, "12": self.dec,
            }
            price = unit_price.get(month_str) or 0
            if not str(price).isdigit():
                price = 0
        except:
            traceback.print_exc()
        finally:
            return price

    @staticmethod
    def get_project_by_full_name_or_short_name(name_str):
        try:
            project_obj = Project.objects.filter(Q(short_name=name_str) | Q(full_name=name_str))
            if project_obj.exists():
                return project_obj.first()
            return None
        except:
            traceback.print_exc()


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != "department":
                if isinstance(field, ModelChoiceField) or isinstance(field, TypedChoiceField):
                    field.widget.attrs.update({'class': 'select2'})

    class Meta:
        model = Project
        fields = "__all__"


class ProjectEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != "department":
                if isinstance(field, ModelChoiceField) or isinstance(field, TypedChoiceField):
                    field.widget.attrs.update({'class': 'select2'})

    class Meta:
        model = Project
        fields = [
            "number", "short_name", "full_name", "principal", "department", "customer", "business_city",
            "company_subject", "contract_type", "project_type", "start_date", "end_date",
            "progress_state", "customer_service_staff", "customer_service_charge",
            "outsource_director", "customer_service_director", "other_responsible_person"
        ]

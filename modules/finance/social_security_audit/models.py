# coding=utf-8
from django import forms

from modules.employee_management.employee_info.models import Employee
from modules.payroll_manage.payroll_detail.models import *
from modules.social_security.social_security_detail.models import *

SOCIAL_SECURITY_BALANCE = (
    ('1', u'平衡'),
    ('2', u'盈余'),
    ('3', u'亏损'),
)


# 社保审核
class SocialSecurityAudit(models.Model):
    name = models.CharField(u"姓名", max_length=255)
    identity_card_number = models.CharField(u"身份证号", max_length=18)

    # 员工外键带出=入职时间，离职时间，项目名称，部门，项目负责人
    employee = models.ForeignKey(Employee, verbose_name=u"员工编号", blank=True, null=True)
    social_security_date = models.DateField(u"社保月份")
    social_security_billing = models.PositiveIntegerField(u"社保结算", blank=True, null=True)
    social_security_outlay = models.PositiveIntegerField(u"社保支出", blank=True, null=True)
    social_security_balance = models.CharField(u"社保平衡", max_length=1, choices=SOCIAL_SECURITY_BALANCE)
    provident_fund_billing = models.PositiveIntegerField(u"公积金结算", blank=True, null=True)
    provident_fund_outlay = models.PositiveIntegerField(u"公积金支出", blank=True, null=True)
    provident_fund_balance = models.CharField(u"公积金平衡", max_length=1, choices=SOCIAL_SECURITY_BALANCE)
    remark = models.CharField(u"备注", max_length=255, blank=True, null=True)

    def __str__(self):
        return self.remark

    @staticmethod
    def get_absolute_url():
        return reverse('finance:social_security_audit:list_socialsecurityaudit', args=())

    class Meta:
        verbose_name = u"社保审核"
        ordering = ['-id']  # id倒叙
        permissions = (
            ("browse_socialsecurityaudit", u"浏览 社保审核"),
            ("export_socialsecurityaudit", u"导出 社保审核"),
        )


class SocialSecurityAuditForm(forms.ModelForm):
    identity_card_number = forms.ChoiceField(label=u'身份证号')

    def __init__(self, *args, **kwargs):
        super(SocialSecurityAuditForm, self).__init__(*args, **kwargs)

        # 组装身份证号，从相同月份的社保明细和薪资汇总明细中的所有身份证号码不重复地显示出来
        socialsecuritydetail_id = SocialSecurityDetail.objects.values_list("identity_card_number", flat=True)
        payrolldetail_id = PayrollDetail.objects.values_list("identity_card_number", flat=True)
        identity_card_number_list = list(set(list(socialsecuritydetail_id) + list(payrolldetail_id)))
        self.fields['identity_card_number'].choices = ((x, x) for x in identity_card_number_list)

    class Meta:
        model = SocialSecurityAudit
        fields = ['identity_card_number', 'social_security_date', 'remark']

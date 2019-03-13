# coding=utf-8
import traceback

from django.core.urlresolvers import reverse
from django.db import models

url_prefix = "dicttable:list"


class PublicDict(models.Model):
    """ 字典表公用模型 """
    name = models.CharField(u"名称", max_length=100, blank=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

    @classmethod
    def get_dict_item_by_name(cls, name):
        """
        :param name:
        :return:
        """
        try:
            return cls.objects.get(name=name)
        except:
            traceback.print_exc()
            return None


class CompanySubject(PublicDict):
    """公司主体字典表 """

    class Meta:
        verbose_name = u"公司主体信息"
        ordering = ['-id']
        permissions = (
            ("browse_companysubject", u"浏览 公司主体信息"),
        )

    @staticmethod
    def get_absolute_url():
        """
        :return:
        """
        return reverse(url_prefix, args=("companysubject",))


class ProjectType(PublicDict):
    """项目类型字典表"""

    class Meta:
        verbose_name = u"项目类型信息"
        ordering = ['-id']
        permissions = (
            ("browse_projecttype", u"浏览 项目类型信息"),
        )

    @staticmethod
    def get_absolute_url():
        """
        :return:
        """
        return reverse(url_prefix, args=("projecttype",))


class ContractType(PublicDict):
    """合同类型字典表"""

    class Meta:
        verbose_name = u"合同类型信息"
        ordering = ['-id']
        permissions = (
            ("browse_contracttype", u"浏览 合同类型信息"),
        )

    @staticmethod
    def get_absolute_url():
        """
        :return:
        """
        return reverse(url_prefix, args=("contracttype",))


class ProgressState(PublicDict):
    """项目目前状态字典表"""

    class Meta:
        verbose_name = u"项目目前状态信息"
        ordering = ['-id']
        permissions = (
            ("browse_progressstate", u"浏览项 目目前状态信息"),
        )

    @staticmethod
    def get_absolute_url():
        """
        :return:
        """
        return reverse(url_prefix, args=("progressstate",))


class SalesType(PublicDict):
    """销售类型字典表"""

    class Meta:
        verbose_name = u"销售类型信息"
        ordering = ['-id']
        permissions = (
            ("browse_salestype", u"浏览 销售类型信息"),
        )

    @staticmethod
    def get_absolute_url():
        """
        :return:
        """
        return reverse(url_prefix, args=("salestype",))


class SocialSecurityType(PublicDict):
    """社保险种字典表 """

    class Meta:
        verbose_name = u"社保险种信息"
        ordering = ['-id']
        permissions = (
            ("browse_socialsecuritytype", u"浏览 社保险种信息"),
        )

    @staticmethod
    def get_absolute_url():
        """
        :return:
        """
        return reverse(url_prefix, args=("socialsecuritytype",))


class SocialSecurityAccountType(PublicDict):
    """社保账户类型字典表"""

    class Meta:
        verbose_name = u"社保账户类型信息"
        ordering = ['-id']
        permissions = (
            ("browse_socialsecurityaccounttype", u"浏览 社保账户类型信息"),
        )

    @staticmethod
    def get_absolute_url():
        """
        :return:
        """
        return reverse(url_prefix, args=("socialsecurityaccounttype",))


class BusinessInsuranceCompany(PublicDict):
    """商保公司字典表"""

    class Meta:
        verbose_name = u"商保公司信息"
        ordering = ['-id']
        permissions = (
            ("browse_businessinsurancecompany", u"浏览 商保公司信息"),
        )

    @staticmethod
    def get_absolute_url():
        """
        :return:
        """
        return reverse(url_prefix, args=("businessinsurancecompany",))


class Cycle(PublicDict):
    """周期字典表"""

    class Meta:
        verbose_name = u"时间周期信息"
        ordering = ['-id']
        permissions = (
            ("browse_cycle", u"浏览 时间周期信息"),
        )

    @staticmethod
    def get_absolute_url():
        """
        :return:
        """
        return reverse(url_prefix, args=("cycle",))


class Position(PublicDict):
    """岗位类型字典表"""

    class Meta:
        verbose_name = u"岗位信息"
        ordering = ['-id']
        permissions = (
            ("browse_position", u"浏览 岗位信息"),
        )

    @staticmethod
    def get_absolute_url():
        """
        :return:
        """
        return reverse(url_prefix, args=("position",))


class WageGrantType(PublicDict):
    """工资发放方式字典表"""

    class Meta:
        verbose_name = u"工资发放方式信息"
        ordering = ['-id']
        permissions = (
            ("browse_wagegranttype", u"浏览 工资发放方式信息"),
        )

    @staticmethod
    def get_absolute_url():
        """
        :return:
        """
        return reverse(url_prefix, args=("wagegranttype",))


class InvoiceType(PublicDict):
    """发票类型字典表"""

    class Meta:
        verbose_name = u"发票类型信息"
        ordering = ['-id']
        permissions = (
            ("browse_invoicetype", u"浏览 发票类型信息"),
        )

    @staticmethod
    def get_absolute_url():
        """
        :return:
        """
        return reverse(url_prefix, args=("invoicetype",))


class ArchiveType(PublicDict):
    """档案类型字典表"""

    class Meta:
        verbose_name = u"档案类型信息"
        ordering = ['-id']
        permissions = (
            ("browse_archivetype", u"浏览 档案类型信息"),
        )

    @staticmethod
    def get_absolute_url():
        """
        :return:
        """
        return reverse(url_prefix, args=("archivetype",))


class ExpenseType(PublicDict):
    """费用类型字典表"""

    class Meta:
        verbose_name = u"费用类型信息"
        ordering = ['-id']
        permissions = (
            ("browse_expensetype", u"浏览 费用类型信息"),
        )

    @staticmethod
    def get_absolute_url():
        """
        :return:
        """
        return reverse(url_prefix, args=("expensetype",))


class ImproveStatus(PublicDict):
    """改善状态"""

    class Meta:
        verbose_name = u"改善状态信息"
        ordering = ['-id']
        permissions = (
            ("browse_improvestatus", u"浏览 改善状态信息"),
        )

    @staticmethod
    def get_absolute_url():
        """
        :return:
        """
        return reverse(url_prefix, args=("improvestatus",))


class LeaveType(PublicDict):
    """请假类型"""

    class Meta:
        verbose_name = u"请假类型"
        ordering = ['-id']
        permissions = (
            ("browse_leavetype", u"浏览 请假类型"),
        )

    @staticmethod
    def get_absolute_url():
        return reverse(url_prefix, args=("leavetype",))


class Subject(PublicDict):
    """科目字典表 """

    class Meta:
        verbose_name = u"科目信息"
        ordering = ['-id']
        permissions = (
            ("browse_subject", u"浏览 科目信息"),
        )

    @staticmethod
    def get_absolute_url():
        """
        :return:
        """
        return reverse(url_prefix, args=("subject",))


class ManagementRights(PublicDict):
    """管理权信息字典表"""

    class Meta:
        verbose_name = u"管理权信息"
        ordering = ['-id']
        permissions = (
            ("browse_management_rights", u"浏览 管理权信息"),
        )

    @staticmethod
    def get_absolute_url():
        """
        :return:
        """
        return reverse(url_prefix, args=("management_rights",))

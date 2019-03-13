# coding=utf-8
from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import View

from modules.share_module.download import download_file
from modules.share_module.export import ExportExcel
from modules.share_module.formater import *
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs
from modules.social_security.social_security_detail.models import SocialSecurityDetail

"""
导出社保明细
"""


# 导出招聘统计
@class_view_decorator(login_required)
@class_view_decorator(permission_required('social_security_detail.export_socialsecuritydetail', raise_exception=True))
class SocialSecurityDetailExportView(View):
    def get(self, request, *args, **kwargs):
        field_list = [
            "id",
            "computer_number",
            "service_company",
            "proxy_company",
            "name",
            "project_name",
            "account_nature",
            "identity_card_number",
            "insured_address",
            "insured_month",
            "social_security_company",
            "provident_fund_company",
            "company_month_sum",
            "social_security_person",
            "provident_fund_person",
            "person_month_sum",
            "social_security_pay_company",
            "social_security_pay_person",
            "provident_fund_pay_company",
            "provident_fund_pay_person",
            "penalty",
            "big_subsidy_refunds",
            "social_security_refunds",
            "provident_fund_refunds",
            "employers_liability_insurance",
            "disablement_gold",
            "social_security_card_fees",
            "agency_fees_expenses",
            "agency_fees_revenue",
            "remarecruitment_fees",
            "lump_sum"
        ]
        head_list = [
            u"序号",
            u"社保电脑号",
            u"服务公司",
            u"代理公司",
            u"姓名",
            u"项目名称",
            u"户口性质",
            u"身份证号",
            u"参保地",
            u"参保月份",
            u"社保公司",
            u"公积金公司",
            u"公司当月总合计",
            u"社保个人",
            u"公积金个人",
            u"个人当月合计",
            u"社保补缴公司",
            u"社保补缴个人",
            u"公积金补缴公司",
            u"公积金补缴个人",
            u"滞纳金",
            u"大额补助退费",
            u"社保退费",
            u"公积金退费",
            u"雇主责任险",
            u"残保金",
            u"社保卡费",
            u"代理费(支付)",
            u"代理费(收入)",
            u"招聘费",
            u"总额"
        ]

        try:
            # 查询条件
            self.project_name = self.request.GET.get("project_name", "")  # 项目名称
            self.dept_name = self.request.GET.get("dept_name", "")
            self.dept_ids = self.request.GET.get("dept_ids", "")
            self.identity_card_number = self.request.GET.get("identity_card_number", "")  # 身份证号
            self.name = self.request.GET.get("name", "")  # 姓名
            self.insured_month = self.request.GET.get("insured_month", "")  # 参保月份

            if self.insured_month:
                insured_month = date_formater(self.insured_month, "%Y-%m-%d")
                insured_month_year = insured_month.year
                insured_month_month = insured_month.month
            else:
                insured_month_year = timezone.now().year
                insured_month_month = timezone.now().month

            search_condition = {
                "project_name__full_name__icontains": self.project_name,
                "identity_card_number__icontains": self.identity_card_number,
                "name__icontains": self.name,
                "insured_month__year": insured_month_year,
                "insured_month__month": insured_month_month,
            }

            # 判断是否是客服部,是，只显示当前用户所属部门下信息
            self.customer_service = 0
            try:
                user_position = self.request.user.position.name  # 用户岗位
            except:
                user_position = ""
            position_list = [u"客服专员", u"客服主管", u"外包主管", u"客服经理"]
            if user_position in position_list:  # 登录用户在客服部，只能查看所在部门项目信息
                self.dept_name = self.request.user.attribution_dept
                self.customer_service = 1

            if self.dept_name:
                search_condition.update(
                    {"project_name__department__name__in": self.dept_name.split(",")})
            kwargs = get_kwargs(search_condition)
            detail_list = SocialSecurityDetail.objects.filter(**kwargs)

            # 组装导出数据
            rows_list = list()
            for detail in detail_list:
                one_row_dict = defaultdict(str)
                one_row_dict["id"] = str(detail.id)
                one_row_dict["computer_number"] = self.format_none(detail.computer_number)
                one_row_dict["service_company"] = detail.get_service_company_display()
                one_row_dict["proxy_company"] = self.format_none(detail.proxy_company)
                one_row_dict["name"] = detail.name
                one_row_dict["project_name"] = detail.project_name.full_name
                one_row_dict["account_nature"] = self.format_none(detail.account_nature)
                one_row_dict["identity_card_number"] = detail.identity_card_number
                one_row_dict["insured_address"] = self.format_none(detail.insured_address)
                one_row_dict["insured_month"] = detail.insured_month.strftime(
                    "%Y-%m-%d") if detail.insured_month else ''
                one_row_dict["social_security_company"] = self.format_none(detail.social_security_company)
                one_row_dict["provident_fund_company"] = self.format_none(detail.provident_fund_company)
                one_row_dict["company_month_sum"] = self.format_none(detail.company_month_sum)
                one_row_dict["social_security_person"] = self.format_none(detail.social_security_person)
                one_row_dict["provident_fund_person"] = self.format_none(detail.provident_fund_person)
                one_row_dict["person_month_sum"] = self.format_none(detail.person_month_sum)
                one_row_dict["social_security_pay_company"] = self.format_none(detail.social_security_pay_company)
                one_row_dict["social_security_pay_person"] = self.format_none(detail.social_security_pay_person)
                one_row_dict["provident_fund_pay_company"] = self.format_none(detail.provident_fund_pay_company)
                one_row_dict["provident_fund_pay_person"] = self.format_none(detail.provident_fund_pay_person)
                one_row_dict["penalty"] = self.format_none(detail.penalty)
                one_row_dict["big_subsidy_refunds"] = self.format_none(detail.big_subsidy_refunds)
                one_row_dict["social_security_refunds"] = self.format_none(detail.social_security_refunds)
                one_row_dict["provident_fund_refunds"] = self.format_none(detail.provident_fund_refunds)
                one_row_dict["employers_liability_insurance"] = self.format_none(detail.employers_liability_insurance)
                one_row_dict["disablement_gold"] = self.format_none(detail.disablement_gold)
                one_row_dict["social_security_card_fees"] = self.format_none(detail.social_security_card_fees)
                one_row_dict["agency_fees_expenses"] = self.format_none(detail.agency_fees_expenses)
                one_row_dict["agency_fees_revenue"] = self.format_none(detail.agency_fees_revenue)
                one_row_dict["remarecruitment_fees"] = self.format_none(detail.remarecruitment_fees)
                one_row_dict["lump_sum"] = self.format_none(detail.lump_sum)
                rows_list.append(one_row_dict.copy())
            if rows_list:
                name = "social_security_detail"
                param = dict(sheetname=name, head_title_list=head_list, field_name_list=field_list,
                             data_obj_list=rows_list, filename=name)

                export_excel = ExportExcel(**param)
                filepath, filename = export_excel.export()

                # 页面下载导出文件
                response = download_file(filepath, filename, True)
                return response
            else:
                # 导出代表头空文件
                return redirect(reverse('download', args=("social_security_detail",)))
        except:
            traceback.print_exc()

    def format_none(self, value):
        try:
            if value:
                return str(value)
            return ""
        except:
            traceback.print_exc()
            return ""

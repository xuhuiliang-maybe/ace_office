# encoding: utf-8
from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import View

from modules.project_manage.models import Project
from modules.share_module.download import download_file
from modules.share_module.export import ExportExcel
from modules.share_module.formater import *
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs, get_strftime


def write_excel(project_obj_list):
    """
    :param project_obj_list:
    :return:
    """
    filepath, file_name = "", ""
    try:
        head_list = ["项目编号", "项目简称", "项目名称", "项目负责人", "负责部门", "客户名称", "业务城市", "公司主体", "合同类型", "项目类别", "起始日期", "终止日期",
                     "目前状态", "客服专员", "客服主管", "外包主管", "客服经理",
                     "其他负责人", "参保地", "社保险种", "社保账户类型", "社保账户名称", "社保节点要求",
                     "社保结算周期（月/日）", "商保公司",
                     "商保结算周期（年/月/日）", "商保收取标准", "商报赔付额度", "商保节点要求", "公积金地点",
                     "比例", "基数", "服务费标准", "服务费节点要求", "残保金收取周期（年/月/日）", "残保金收取地",
                     "提供结算表时间(2016-01-01)",
                     "费用到账时间(2016-01-01)",
                     "工资发放时间(2016-01-01)",
                     "工资发放方式", "结算对接人和联系方式", "异常结算情况", "工资服务结算周期", "其他需要我司代收代付项目", "发票抬头", "开票方式", "专票科目", "专票费用内容",
                     "专票说明", "普票科目", "普票费用内容", "普票说明", "发票接收人", "电话", "地址", "快递说明", "发票开具日期(2016-01-01)",
                     "是否一般纳税人(是 / 否)", "纳税人识别号", "地址", "电话", "开户行", "账号", "销售人员", "销售类型", "派遣提成标准", "备注", "外包提成标准",
                     "备注",
                     "代理人事提成标准", "备注", "代理招聘提成标准", "备注", "小时工提成标准", "备注", "招聘难度系数", "1月", "2月", "3月", "4月", "5月", "6月",
                     "7月", "8月", "9月", "10月", "11月", "12月"
                     ]
        field_list = [
            "number",
            "short_name",
            "full_name",
            "principal",
            "department",
            "customer",
            "business_city",
            "company_subject",
            "contract_type",
            "project_type",
            "start_date",
            "end_date",
            "progress_state",
            "customer_service_staff",
            "customer_service_charge",
            "outsource_director",
            "customer_service_director",
            "other_responsible_person",
            "insured_place",
            "social_security_type",
            "social_security_account_type",
            "social_security_account_name",
            "social_security_node_require",
            "social_security_settlement_cycle",
            "business_insurance_company",
            "business_insurance_settlement_cycle",
            "business_insurance_standard",
            "business_insurance_payment",
            "business_insurance_node_require",
            "accumulation_fund_place_province",
            "proportion",
            "radix",
            "service_standard",
            "service_cost_node_require",
            "residual_premium_cycle",
            "residual_premium_place",
            "settlement_report_day",
            "cost_arrival_day",
            "wage_grant_day",
            "wage_grant_type",
            "settlement_person",
            "abnormal_settlement",
            "wage_service_cost_settlement_cycle",
            "other_project",
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
            "salesman",
            "sales_type",
            "dispatch_commission",
            "remark1",
            "outsourc_commission",
            "remark2",
            "proxy_personnel_commission",
            "remark3",
            "proxy_recruitment_commission",
            "remark4",
            "hourly_commission",
            "remark5",
            "recruit_difficulty",
            "jan",
            "feb",
            "mar",
            "apr",
            "may",
            "jun",
            "jul",
            "aug",
            "sep",
            "oct",
            "nov",
            "dec",
        ]

        # 组装导出数据
        rows_list = list()
        for index, one_project in enumerate(project_obj_list):
            one_row_dict = defaultdict(str)
            one_row_dict["index"] = str(index + 1)  # 序号
            one_row_dict["number"] = one_project.number
            one_row_dict["short_name"] = one_project.short_name
            one_row_dict["full_name"] = one_project.full_name
            one_row_dict["principal"] = one_project.principal.first_name if one_project.principal else ""
            one_row_dict["department"] = one_project.department.name if one_project.department else ""
            one_row_dict["customer"] = one_project.customer
            one_row_dict["business_city"] = one_project.business_city
            one_row_dict["company_subject"] = one_project.company_subject.name if one_project.company_subject else ""
            one_row_dict["contract_type"] = one_project.contract_type.name if one_project.contract_type else ""
            one_row_dict["project_type"] = one_project.project_type.name if one_project.project_type else ""
            one_row_dict["start_date"] = get_strftime(one_project.start_date,
                                                      "%Y-%m-%d") if one_project.start_date else ''
            one_row_dict["end_date"] = get_strftime(one_project.end_date, "%Y-%m-%d") if one_project.end_date else ''
            one_row_dict["progress_state"] = one_project.progress_state.name if one_project.progress_state else ''
            one_row_dict[
                "customer_service_staff"] = one_project.customer_service_staff.first_name if one_project.customer_service_staff else ''
            one_row_dict[
                "customer_service_charge"] = one_project.customer_service_charge.first_name if one_project.customer_service_charge else ''
            one_row_dict[
                "outsource_director"] = one_project.outsource_director.first_name if one_project.outsource_director else ''
            one_row_dict[
                "customer_service_director"] = one_project.customer_service_director.first_name if one_project.customer_service_director else ''
            one_row_dict[
                "other_responsible_person"] = one_project.other_responsible_person.first_name if one_project.other_responsible_person else ''
            one_row_dict["insured_place"] = one_project.insured_place
            one_row_dict["social_security_type"] = ",".join(
                [one.name for one in one_project.social_security_type.all()])
            one_row_dict[
                "social_security_account_type"] = one_project.social_security_account_type.name if one_project.social_security_account_type else ''
            one_row_dict["social_security_account_name"] = one_project.social_security_account_name
            one_row_dict["social_security_node_require"] = one_project.social_security_node_require
            one_row_dict["social_security_settlement_cycle"] = one_project.social_security_settlement_cycle
            one_row_dict["business_insurance_company"] = ",".join(
                [one.name for one in one_project.business_insurance_company.all()])
            one_row_dict[
                "business_insurance_settlement_cycle"] = one_project.business_insurance_settlement_cycle.name if one_project.business_insurance_settlement_cycle else ''
            one_row_dict["business_insurance_standard"] = one_project.business_insurance_standard
            one_row_dict["business_insurance_payment"] = one_project.business_insurance_payment
            one_row_dict["business_insurance_node_require"] = one_project.business_insurance_node_require
            one_row_dict["accumulation_fund_place_province"] = one_project.accumulation_fund_place_province
            one_row_dict["proportion"] = one_project.proportion
            one_row_dict["radix"] = one_project.radix
            one_row_dict["service_standard"] = one_project.service_standard
            one_row_dict["service_cost_node_require"] = one_project.service_cost_node_require
            one_row_dict[
                "residual_premium_cycle"] = one_project.residual_premium_cycle.name if one_project.residual_premium_cycle else ""
            one_row_dict["residual_premium_place"] = one_project.residual_premium_place
            one_row_dict["settlement_report_day"] = one_project.settlement_report_day
            one_row_dict["cost_arrival_day"] = one_project.cost_arrival_day
            one_row_dict["wage_grant_day"] = one_project.wage_grant_day
            one_row_dict["wage_grant_type"] = one_project.wage_grant_type.name if one_project.wage_grant_type else ""
            one_row_dict["settlement_person"] = one_project.settlement_person
            one_row_dict["abnormal_settlement"] = one_project.abnormal_settlement
            one_row_dict["wage_service_cost_settlement_cycle"] = one_project.wage_service_cost_settlement_cycle
            one_row_dict["other_project"] = one_project.other_project
            one_row_dict["invoice_title"] = one_project.invoice_title
            one_row_dict["invoice_mode"] = one_project.invoice_mode
            one_row_dict["special_subject"] = one_project.special_subject
            one_row_dict["special_cost"] = one_project.special_cost
            one_row_dict["special_desc"] = one_project.special_desc
            one_row_dict["general_subject"] = one_project.general_subject
            one_row_dict["general_cost"] = one_project.general_cost
            one_row_dict["general_desc"] = one_project.general_desc
            one_row_dict["invoice_receiver"] = one_project.invoice_receiver
            one_row_dict["invoice_phone"] = one_project.invoice_phone
            one_row_dict["invoice_mail"] = one_project.invoice_mail
            one_row_dict["fast_mail_desc"] = one_project.fast_mail_desc
            one_row_dict["invoice_open_date"] = one_project.invoice_open_date
            one_row_dict["is_general_taxpayer"] = one_project.is_general_taxpayer
            one_row_dict["taxpayer_identifier"] = one_project.taxpayer_identifier
            one_row_dict["address"] = one_project.address
            one_row_dict["phone"] = one_project.phone
            one_row_dict["bank"] = one_project.bank
            one_row_dict["account_number"] = one_project.account_number
            one_row_dict["salesman"] = one_project.salesman.first_name if one_project.salesman else ""
            one_row_dict["sales_type"] = one_project.sales_type.name if one_project.sales_type else ""
            one_row_dict["dispatch_commission"] = one_project.dispatch_commission
            one_row_dict["remark1"] = one_project.remark1
            one_row_dict["outsourc_commission"] = one_project.outsourc_commission
            one_row_dict["remark2"] = one_project.remark2
            one_row_dict["proxy_personnel_commission"] = one_project.proxy_personnel_commission
            one_row_dict["remark3"] = one_project.remark3
            one_row_dict["proxy_recruitment_commission"] = one_project.proxy_recruitment_commission
            one_row_dict["remark4"] = one_project.remark4
            one_row_dict["hourly_commission"] = one_project.hourly_commission
            one_row_dict["remark5"] = one_project.remark5
            one_row_dict["recruit_difficulty"] = one_project.recruit_difficulty
            one_row_dict["jan"] = one_project.jan
            one_row_dict["feb"] = one_project.feb
            one_row_dict["mar"] = one_project.mar
            one_row_dict["apr"] = one_project.apr
            one_row_dict["may"] = one_project.may
            one_row_dict["jun"] = one_project.jun
            one_row_dict["jul"] = one_project.jul
            one_row_dict["aug"] = one_project.aug
            one_row_dict["sep"] = one_project.sep
            one_row_dict["oct"] = one_project.oct
            one_row_dict["nov"] = one_project.nov
            one_row_dict["dec"] = one_project.dec
            rows_list.append(one_row_dict.copy())
        if rows_list:
            name = "project"
            param = dict(
                sheetname=name,
                head_title_list=head_list,
                field_name_list=field_list,
                data_obj_list=rows_list,
                filename=name,
                path="export_project"
            )

            export_excel = ExportExcel(**param)
            export_excel.sheetname = "Project"
            export_excel.filename = "Project"
            filepath, file_name = export_excel.export()
    except:
        traceback.print_exc()
    finally:
        return filepath, file_name


@class_view_decorator(login_required)
@class_view_decorator(permission_required('project_manage.export_project', raise_exception=True))
class ProjectExportView(View):
    """导出项目信息"""

    def get(self, request, *args, **kwargs):
        try:
            # 员工查询
            dept_name = self.request.GET.get("dept_name", "")  # 部门
            search_name = self.request.GET.get("search_name", "")  # 项目名称
            progress_state = self.request.GET.get("progress_state", "")  # 目前状态

            filter_kwargs = {
                "full_name__icontains": search_name,
                "progress_state__id": progress_state
            }
            if dept_name:
                filter_kwargs.update({"department__name__in": dept_name.split(",")})
            else:
                if not self.request.user.is_superuser:
                    managements = map(int, self.request.user.remark2.split(",")) if self.request.user.remark2 else []
                    filter_kwargs.update({"project_name__department__id__in": managements})

            # 普通管理员只查询自己负责项目的员工信息
            if not self.request.user.is_superuser and not self.request.user.dept_head:
                filter_kwargs.update({"principal": self.request.user})
            filter_kwargs = get_kwargs(filter_kwargs)
            project_obj_list = Project.objects.filter(**filter_kwargs)

            filepath, file_name = write_excel(project_obj_list)

            if filepath and file_name:
                # 页面下载导出文件
                response = download_file(filepath, file_name, False)
                return response
            else:
                # 导出只有表头信息的空文件
                return redirect(reverse('download', args=("project_info",)))
        except:
            traceback.print_exc()

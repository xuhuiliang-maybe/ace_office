# coding=utf-8
from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import View

from modules.employee_management.employee_info.code import employee_head_list, employee_field_list, temporary_head_list, \
    temporary_field_list
from modules.employee_management.employee_info.models import Employee
from modules.share_module.download import download_file
from modules.share_module.export import *
from modules.share_module.formater import *
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs, get_strftime


def write_excel(employee_type, employee_obj_list):
    filepath, file_name = "", ""
    head_list, field_list = [], []
    try:
        if employee_type == "employee":
            head_list = employee_head_list
            field_list = employee_field_list
        elif employee_type == "temporary":
            head_list = temporary_head_list
            field_list = temporary_field_list

        # 组装导出数据
        rows_list = list()
        if employee_type == "employee":
            for index, one_emp in enumerate(employee_obj_list):
                one_row_dict = defaultdict(str)
                one_row_dict["index"] = str(index + 1)  # 序号
                one_row_dict["name"] = one_emp.name  # 姓名
                one_row_dict["create_time"] = get_strftime(one_emp.create_time,
                                                           "%Y-%m-%d %X") if one_emp.create_time else "--"
                one_row_dict["modified"] = get_strftime(one_emp.modified, "%Y-%m-%d %X") if one_emp.modified else "--"
                if one_emp.project_name:
                    one_row_dict[
                        "attribution_dept"] = one_emp.project_name.department.name if one_emp.project_name.department else "--"  # 服务部门
                else:
                    one_row_dict["attribution_dept"] = "--"  # 服务部门
                one_row_dict["identity_card_number"] = one_emp.identity_card_number  # 身份证号
                one_row_dict["status"] = one_emp.get_status_display()  # 目前状态
                if one_emp.project_name:
                    one_row_dict[
                        "project_name"] = one_emp.project_name.full_name  # 项目名称
                else:
                    one_row_dict["project_name"] = "--"  # 项目名称
                one_row_dict["salary_card_number"] = one_emp.salary_card_number  # 银行卡号
                one_row_dict["bank_account"] = one_emp.bank_account  # 开户银行
                one_row_dict["bank_address"] = one_emp.bank_address  # 开户地
                one_row_dict["job_dept"] = one_emp.job_dept  # 部门
                one_row_dict["position"] = one_emp.position  # 职务
                one_row_dict["sex"] = one_emp.get_sex_display()  # 性别
                one_row_dict["nation"] = one_emp.get_nation_display()  # 民族
                one_row_dict["education"] = one_emp.get_education_display()  # 学历
                one_row_dict["birthday"] = get_strftime(one_emp.birthday,
                                                        "%Y-%m-%d") if one_emp.birthday else ''  # 出生年月
                if one_emp.age:
                    one_row_dict["age"] = int(one_emp.age)  # 年龄
                else:
                    one_row_dict["age"] = "--"
                one_row_dict["register_address"] = one_emp.register_address  # 户口所在地
                one_row_dict["register_postcode"] = one_emp.register_postcode  # 户口邮编
                one_row_dict[
                    "register_type"] = one_emp.get_register_type_display()  # 户口性质
                one_row_dict["work_address"] = one_emp.work_address  # 工作地
                one_row_dict["insured_place"] = one_emp.insured_place  # 社保地
                if one_emp.person_type:
                    one_row_dict["person_type"] = one_emp.person_type.name  # 人员属性
                else:
                    one_row_dict["person_type"] = "--"  # 人员属性
                one_row_dict[
                    "contract_type"] = one_emp.get_contract_type_display()  # 合同属性
                if one_emp.contract_subject:
                    one_row_dict[
                        "contract_subject"] = one_emp.contract_subject.name  # 合同主体
                else:
                    one_row_dict["contract_subject"] = "--"  # 合同主体
                one_row_dict["entry_date"] = get_strftime(one_emp.entry_date,
                                                          "%Y-%m-%d") if one_emp.entry_date else ''  # 入职日期
                one_row_dict["call_out_time"] = get_strftime(one_emp.call_out_time,
                                                             "%Y-%m-%d") if one_emp.call_out_time else ''  # 调出时间
                one_row_dict["into_time"] = get_strftime(one_emp.into_time,
                                                         "%Y-%m-%d") if one_emp.into_time else ''  # 转入时间
                one_row_dict["social_insurance_increase_date"] = get_strftime(one_emp.social_insurance_increase_date,
                                                                              "%Y-%m-%d") if one_emp.social_insurance_increase_date else ''  # 社保增员日期
                one_row_dict[
                    "social_security_payment_card"] = one_emp.social_security_payment_card
                one_row_dict["use_bank"] = one_emp.use_bank
                one_row_dict["business_insurance_increase_date"] = get_strftime(
                    one_emp.business_insurance_increase_date,
                    "%Y-%m-%d") if one_emp.business_insurance_increase_date else ''  # 商保增员日期
                one_row_dict["provident_fund_increase_date"] = get_strftime(one_emp.provident_fund_increase_date,
                                                                            "%Y-%m-%d") if one_emp.provident_fund_increase_date else ''  # 公积金增员日期
                one_row_dict["contract_begin_date"] = get_strftime(one_emp.contract_begin_date,
                                                                   "%Y-%m-%d") if one_emp.contract_begin_date else ''  # 合同开始日期
                if one_emp.probation_period:
                    one_row_dict["probation_period"] = int(one_emp.probation_period)  # 使用期限
                else:
                    one_row_dict["probation_period"] = "--"
                if one_emp.contract_period:
                    one_row_dict["contract_period"] = int(one_emp.contract_period)  # 合同期限
                else:
                    one_row_dict["contract_period"] = "--"
                one_row_dict["probation_end_date"] = get_strftime(one_emp.probation_end_date,
                                                                  "%Y-%m-%d") if one_emp.probation_end_date else ''  # 试用到期日期
                one_row_dict["contract_end_date"] = get_strftime(one_emp.contract_end_date,
                                                                 "%Y-%m-%d") if one_emp.contract_end_date else ''  # 合同到期日期 if one_emp.contract_renew_times:
                if one_emp.contract_renew_times:
                    one_row_dict["contract_renew_times"] = int(one_emp.contract_renew_times)  # 合同续签次数
                else:
                    one_row_dict["contract_renew_times"] = "--"
                one_row_dict["departure_date"] = get_strftime(one_emp.departure_date,
                                                              "%Y-%m-%d") if one_emp.departure_date else ''  # 离职日期
                one_row_dict[
                    "departure_procedure"] = one_emp.get_departure_procedure_display()  # 离职手续
                one_row_dict["departure_cause"] = one_emp.departure_cause  # 离职原因
                one_row_dict[
                    "social_insurance_reduce_date"] = get_strftime(one_emp.social_insurance_reduce_date,
                                                                   "%Y-%m-%d") if one_emp.social_insurance_reduce_date else ''  # 社保减员日期
                one_row_dict[
                    "business_insurance_reduce_date"] = get_strftime(one_emp.business_insurance_reduce_date,
                                                                     "%Y-%m-%d") if one_emp.business_insurance_reduce_date else ''  # 商保减员日期
                one_row_dict[
                    "provident_fund_reduce_date"] = get_strftime(one_emp.provident_fund_reduce_date,
                                                                 "%Y-%m-%d") if one_emp.provident_fund_reduce_date else ''  # 公积金减员日期
                one_row_dict["phone_number"] = one_emp.phone_number  # 联系电话
                one_row_dict["contact_person"] = one_emp.contact_person  # 紧急联系人
                one_row_dict[
                    "contact_relationship"] = one_emp.contact_relationship  # 与联系人关系
                one_row_dict[
                    "contact_person_phone"] = one_emp.contact_person_phone  # 紧急联系人电话
                one_row_dict[
                    "recruitment_channel"] = one_emp.get_recruitment_channel_display()  # 招聘渠道
                try:
                    one_row_dict[
                        "recruitment_attache"] = one_emp.recruitment_attache.first_name  # 招聘人员
                except:
                    one_row_dict["recruitment_attache"] = "--"  # 招聘人员
                try:
                    one_row_dict["customer_service_staff"] = one_emp.project_name.customer_service_staff.first_name  # 客户专员
                except:
                    one_row_dict["customer_service_staff"] = "--"
                try:
                    one_row_dict[
                        "customer_service_charge"] = one_emp.project_name.customer_service_charge.first_name  # 客服主管
                except:
                    one_row_dict["customer_service_director"] = "--"
                try:
                    one_row_dict[
                        "outsource_director"] = one_emp.project_name.outsource_director.first_name  # 外包主管
                except:
                    one_row_dict["outsource_director"] = "--"
                try:
                    one_row_dict[
                        "customer_service_director"] = one_emp.project_name.customer_service_director.first_name  # 客服经理
                except:
                    one_row_dict["customer_service_director"] = "--"
                try:
                    one_row_dict[
                        "other_responsible_person"] = one_emp.project_name.other_responsible_person.first_name  # 其他负责人
                except:
                    one_row_dict["other_responsible_person"] = "--"

                rows_list.append(one_row_dict.copy())
        elif employee_type == "temporary":
            for index, one_emp in enumerate(employee_obj_list):
                one_row_dict = defaultdict(str)
                one_row_dict["index"] = str(index + 1)  # 序号
                one_row_dict["name"] = one_emp.name  # 姓名
                one_row_dict["create_time"] = get_strftime(one_emp.create_time,
                                                           "%Y-%m-%d %X") if one_emp.create_time else "--"
                one_row_dict["modified"] = get_strftime(one_emp.modified, "%Y-%m-%d %X") if one_emp.modified else "--"
                one_row_dict["sex"] = one_emp.get_sex_display()  # 性别
                one_row_dict[
                    "identity_card_number"] = one_emp.identity_card_number  # 身份证号
                if one_emp.project_name:
                    one_row_dict[
                        "project_name"] = one_emp.project_name.full_name  # 项目名称
                else:
                    one_row_dict["project_name"] = "--"  # 项目名称
                one_row_dict["attribution_dept"] = one_emp.project_name.department.name  # 服务部门
                try:
                    one_row_dict["recruitment_attache"] = one_emp.recruitment_attache.first_name  # 招聘人员
                except:
                    one_row_dict["recruitment_attache"] = "--"  # 招聘人员
                one_row_dict["phone_number"] = one_emp.phone_number  # 联系电话
                one_row_dict["start_work_date"] = get_strftime(one_emp.start_work_date,
                                                               "%Y-%m-%d") if one_emp.start_work_date else ''  # 开始工作日
                one_row_dict["end_work_date"] = get_strftime(one_emp.end_work_date,
                                                             "%Y-%m-%d") if one_emp.end_work_date else ''  # 结束工作日
                one_row_dict["work_days"] = one_emp.work_days  # 工作天数
                one_row_dict["hours"] = one_emp.hours  # 小时数
                one_row_dict["amount_of_payment"] = one_emp.amount_of_payment  # 发放金额
                try:
                    one_row_dict["release_user"] = one_emp.release_user.first_name  # 发放人
                except:
                    one_row_dict["release_user"] = "--"  # 发放人
                one_row_dict["release_time"] = get_strftime(one_emp.release_time,
                                                            "%Y-%m-%d") if one_emp.release_time else ''  # 发放时间
                one_row_dict["remark1"] = one_emp.remark1  # 备注1

                rows_list.append(one_row_dict.copy())

        if rows_list:
            name = "emp"
            param = dict(sheetname=name, head_title_list=head_list, field_name_list=field_list,
                         data_obj_list=rows_list, filename=name, path="export_employee")

            export_excel = ExportExcel(**param)
            if employee_type == "employee":
                export_excel.sheetname = "Employee"
                export_excel.filename = "Employee"
            elif employee_type == "temporary":
                export_excel.sheetname = "Temporary"
                export_excel.filename = "Temporary"

            filepath, file_name = export_excel.export()

    except:
        traceback.print_exc()
    finally:
        return filepath, file_name


@class_view_decorator(login_required)
@class_view_decorator(permission_required('employee_info.export_employee', raise_exception=True))
class EmployeeExportView(View):
    """导出员工信息"""

    def get(self, request, *args, **kwargs):

        employee_type = self.request.GET.get("employee_type", "")
        try:
            # 员工查询
            status = self.request.GET.get("status", "")  # 目前状态
            project_name = self.request.GET.get("project_name", "")  # 项目名称
            dept_name = self.request.GET.get("dept_name", "")  # 服务部门
            principal = self.request.GET.get("principal", "")  # 项目负责人
            name = self.request.GET.get("name", "")  # 姓名
            identity_card_number = self.request.GET.get("identity_card_number", "")  # 身份证号
            person_type = int(self.request.GET.get("person_type", 0))  # 人员属性
            contract_type = self.request.GET.get("contract_type", "")  # 合同属性

            # 临时员工查询
            phone_number = self.request.GET.get("phone_number", "")  # 联系方式
            recruitment_attache = self.request.GET.get("recruitment_attache", "")  # 招聘人员
            st_release_time = self.request.GET.get("st_release_time", "")  # 发放起始时间
            et_release_time = self.request.GET.get("et_release_time", "")  # 发放终止日期
            self.start_time = self.request.GET.get("start_time", "")  # 创建起始时间
            self.end_time = self.request.GET.get("end_time", "")  # 创建终止时间

            if self.start_time and self.end_time:
                self.start_time += " 00:00:01"
                self.end_time += " 23:59:59"
                self.start_time = date_formater(self.start_time, "%Y/%m/%d %X")
                self.end_time = date_formater(self.end_time, "%Y/%m/%d %X")

            # try:
            # 	user_position = self.request.user.position.name  # 用户岗位
            # except:
            # 	user_position = "--"
            # position_list = [u"客服专员", u"客服主管", u"外包主管", u"客服经理"]
            # if user_position in position_list:  # 登录用户在客服部，只能查看所在部门员工信息
            # 	dept_name = self.request.user.attribution_dept

            search_condition = {
                "status": status,
                "project_name__full_name__icontains": project_name,
                "project_name__principal__first_name__icontains": principal,
                "name__icontains": name,
                "identity_card_number__icontains": identity_card_number,
                "person_type": person_type,
                "contract_type": contract_type,
                "phone_number": phone_number,
                "recruitment_attache__first_name__icontains": recruitment_attache,
                "release_time__gte": st_release_time,
                "release_time__lte": et_release_time,
                "create_time__gte": self.start_time,
                "create_time__lte": self.end_time
            }
            if dept_name:
                search_condition.update({"project_name__department__name__in": dept_name.split(",")})
            else:
                if not self.request.user.is_superuser:
                    managements = map(int, self.request.user.remark2.split(",")) if self.request.user.remark2 else []
                    search_condition.update({"project_name__department__id__in": managements})

            # 普通管理员只查询自己负责项目的员工信息
            if not self.request.user.is_superuser and not self.request.user.dept_head:
                search_condition.update({"project_name__principal": self.request.user})

            kwargs = get_kwargs(search_condition)
            if employee_type == "employee":  # 查看员工信息
                kwargs.update({"is_temporary": False})
            elif employee_type == "temporary":  # 查看临时工信息
                kwargs.update({"is_temporary": True})
            employee_obj_list = Employee.objects.filter(**kwargs)

            filepath, file_name = write_excel(employee_type, employee_obj_list)

            if filepath and file_name:
                # 页面下载导出文件
                response = download_file(filepath, file_name, False)
                return response
            else:
                # 导出只有表头信息的空文件
                if employee_type == "employee":
                    return redirect(reverse('download', args=("employee_info",)))
                elif employee_type == "temporary":
                    return redirect(reverse('download', args=("temporary_info",)))
        except:
            traceback.print_exc()


def write_employee_file(employee_type, employee_obj_list, filepath):
    try:
        head_list = list()
        if employee_type == "employee":
            head_list = employee_head_list
        elif employee_type == "temporary":
            head_list = temporary_head_list
        head_str = "\t".join(head_list)
        with open(filepath, "w") as f:  # 格式化字符串还能这么用！
            f.write(head_str)
            f.write("\n")
        # 组装导出数据
        if employee_obj_list.exists():
            if employee_type == "employee":
                with open(filepath, "a+") as f:
                    for index, one_emp in enumerate(employee_obj_list):
                        tmp_one = list()
                        tmp_one.append(str(index + 1))
                        tmp_one.append(one_emp.name if one_emp.name else "--")  # 姓名
                        tmp_one.append(
                            one_emp.project_name.department.name if one_emp.project_name and one_emp.project_name.department else "--")  # 服务部门
                        tmp_one.append(
                            one_emp.identity_card_number if one_emp.identity_card_number else "--")  # 身份证号
                        tmp_one.append(one_emp.get_status_display() if one_emp.status else "--")  # 目前状态
                        tmp_one.append(one_emp.project_name.full_name if one_emp.project_name else "--")  # 项目名称
                        tmp_one.append(one_emp.salary_card_number if one_emp.salary_card_number else "--")  # 银行卡号
                        tmp_one.append(one_emp.bank_account if one_emp.bank_account else "--")  # 开户银行
                        tmp_one.append(one_emp.bank_address if one_emp.bank_address else "--")  # 开户地
                        tmp_one.append(one_emp.job_dept if one_emp.job_dept else "--")  # 部门
                        tmp_one.append(one_emp.position if one_emp.position else "--")  # 职务
                        tmp_one.append(one_emp.get_sex_display() if one_emp.sex else "--")  # 性别
                        tmp_one.append(one_emp.get_nation_display() if one_emp.nation else "--")  # 民族
                        tmp_one.append(one_emp.get_education_display() if one_emp.education else "--")  # 学历
                        tmp_one.append(one_emp.birthday.strftime("%Y-%m-%d") if one_emp.birthday else '--')  # 出生年月
                        tmp_one.append(str(one_emp.age) if one_emp.age else "--")  # 年龄
                        tmp_one.append(one_emp.register_address if one_emp.register_address else "--")  # 户口所在地
                        tmp_one.append(one_emp.register_postcode if one_emp.register_postcode else "--")  # 户口邮编
                        tmp_one.append(
                            one_emp.get_register_type_display() if one_emp.register_type else "--")  # 户口性质
                        tmp_one.append(one_emp.work_address if one_emp.work_address else "--")  # 工作地
                        tmp_one.append(one_emp.insured_place if one_emp.insured_place else "--")  # 社保地
                        tmp_one.append(one_emp.person_type.name if one_emp.person_type else "--")  # 人员属性
                        tmp_one.append(
                            one_emp.get_contract_type_display() if one_emp.contract_type else "--")  # 合同属性
                        tmp_one.append(one_emp.contract_subject.name if one_emp.contract_subject else "--")  # 合同主体
                        tmp_one.append(one_emp.entry_date.strftime("%Y-%m-%d") if one_emp.entry_date else '--')  # 入职日期
                        tmp_one.append(
                            one_emp.call_out_time.strftime("%Y-%m-%d") if one_emp.call_out_time else '--')  # 调出时间
                        tmp_one.append(one_emp.into_time.strftime("%Y-%m-%d") if one_emp.into_time else '--')  # 转入时间
                        tmp_one.append(one_emp.social_insurance_increase_date.strftime(
                            "%Y-%m-%d") if one_emp.social_insurance_increase_date else '--')  # 社保增员日期
                        tmp_one.append(
                            one_emp.social_security_payment_card if one_emp.social_security_payment_card else "--")
                        tmp_one.append(one_emp.use_bank if one_emp.use_bank else "--")
                        tmp_one.append(one_emp.business_insurance_increase_date.strftime(
                            "%Y-%m-%d") if one_emp.business_insurance_increase_date else '--')  # 商保增员日期
                        tmp_one.append(one_emp.provident_fund_increase_date.strftime(
                            "%Y-%m-%d") if one_emp.provident_fund_increase_date else '--')  # 公积金增员日期
                        tmp_one.append(one_emp.contract_begin_date.strftime(
                            "%Y-%m-%d") if one_emp.contract_begin_date else '--')  # 合同开始日期
                        tmp_one.append(str(one_emp.probation_period) if one_emp.probation_period else "--")  # 试用期限
                        tmp_one.append(str(one_emp.contract_period) if one_emp.contract_period else "--")  # 合同期限
                        tmp_one.append(one_emp.probation_end_date.strftime(
                            "%Y-%m-%d") if one_emp.probation_end_date else '--')  # 试用到期日期
                        tmp_one.append(one_emp.contract_end_date.strftime(
                            "%Y-%m-%d") if one_emp.contract_end_date else '--')  # 合同到期日期
                        tmp_one.append(
                            str(one_emp.contract_renew_times) if one_emp.contract_renew_times else "--")  # 合同续签次数
                        tmp_one.append(
                            one_emp.departure_date.strftime("%Y-%m-%d") if one_emp.departure_date else '--')  # 离职日期
                        tmp_one.append(
                            one_emp.get_departure_procedure_display() if one_emp.departure_procedure else "--")  # 离职手续
                        tmp_one.append(one_emp.departure_cause if one_emp.departure_cause else "--")  # 离职原因
                        tmp_one.append(one_emp.social_insurance_reduce_date.strftime(
                            "%Y-%m-%d") if one_emp.social_insurance_reduce_date else '--')  # 社保减员日期
                        tmp_one.append(one_emp.business_insurance_reduce_date.strftime(
                            "%Y-%m-%d") if one_emp.business_insurance_reduce_date else '--')  # 商保减员日期
                        tmp_one.append(one_emp.provident_fund_reduce_date.strftime(
                            "%Y-%m-%d") if one_emp.provident_fund_reduce_date else '--')  # 公积金减员日期
                        tmp_one.append(one_emp.phone_number if one_emp.phone_number else "--")  # 联系电话
                        tmp_one.append(one_emp.contact_person if one_emp.contact_person else "--")  # 紧急联系人
                        tmp_one.append(
                            one_emp.contact_relationship if one_emp.contact_relationship else "--")  # 与联系人关系
                        tmp_one.append(
                            one_emp.contact_person_phone if one_emp.contact_person_phone else "--")  # 紧急联系人电话
                        tmp_one.append(
                            one_emp.get_recruitment_channel_display() if one_emp.recruitment_channel else "--")  # 招聘渠道
                        try:
                            tmp_one.append(one_emp.recruitment_attache.first_name)  # 招聘人员
                        except:
                            tmp_one.append("--")  # 招聘人员
                        try:
                            tmp_one.append(one_emp.project_name.customer_service_staff.first_name)  # 客户专员
                        except:
                            tmp_one.append("--")
                        try:
                            tmp_one.append(one_emp.project_name.customer_service_charge.first_name)  # 客服主管
                        except:
                            tmp_one.append("--")
                        try:
                            tmp_one.append(one_emp.project_name.outsource_director.first_name)  # 外包主管
                        except:
                            tmp_one.append("--")
                        try:
                            tmp_one.append(one_emp.project_name.customer_service_director.first_name)  # 客服经理
                        except:
                            tmp_one.append("--")
                        try:
                            tmp_one.append(one_emp.project_name.other_responsible_person.first_name)  # 其他负责人
                        except:
                            tmp_one.append("--")
                        tmp_one.append(
                            one_emp.create_time.strftime("%Y-%m-%d %X") if one_emp.create_time else "--")  # 创建时间
                        tmp_one.append(
                            one_emp.modified.strftime("%Y-%m-%d %X") if one_emp.create_time else "--")  # 修改时间
                        f.write("\t".join(tmp_one))
                        f.write("\n")

            elif employee_type == "temporary":
                with open(filepath, "a+") as f:
                    for index, one_emp in enumerate(employee_obj_list):
                        tmp_one = list()
                        tmp_one.append(str(index + 1))
                        tmp_one.append(one_emp.name if one_emp.name else "--")  # 姓名
                        tmp_one.append(one_emp.create_time.strftime("%Y-%m-%d %X") if one_emp.create_time else "--")
                        tmp_one.append(one_emp.get_sex_display() if one_emp.sex else "--")  # 性别
                        tmp_one.append(
                            one_emp.identity_card_number if one_emp.identity_card_number else "--")  # 身份证号
                        tmp_one.append(one_emp.project_name.full_name if one_emp.project_name else "--")  # 项目名称
                        tmp_one.append(
                            one_emp.project_name.department.name if one_emp.project_name and one_emp.project_name.department else "--")  # 服务部门
                        tmp_one.append(
                            one_emp.recruitment_attache.first_name if one_emp.recruitment_attache else "--")  # 招聘人员
                        tmp_one.append(one_emp.phone_number if one_emp.phone_number else "--")  # 联系电话
                        tmp_one.append(one_emp.start_work_date.strftime(
                            "%Y-%m-%d") if one_emp.start_work_date else '--')  # 开始工作日
                        tmp_one.append(
                            one_emp.end_work_date.strftime("%Y-%m-%d") if one_emp.end_work_date else '--')  # 结束工作日
                        tmp_one.append(str(one_emp.work_days) if one_emp.work_days else "--")  # 工作天数
                        tmp_one.append(str(one_emp.hours) if one_emp.hours else "--")  # 小时数
                        tmp_one.append(
                            str(one_emp.amount_of_payment) if one_emp.amount_of_payment else "--")  # 发放金额
                        tmp_one.append(one_emp.release_user.first_name if one_emp.release_user else "--")  # 发放人
                        tmp_one.append(
                            one_emp.release_time.strftime("%Y-%m-%d") if one_emp.release_time else '--')  # 发放时间
                        tmp_one.append(one_emp.remark1 if one_emp.remark1 else "--")  # 备注1
                        f.write("\t".join(tmp_one))
                        f.write("\n")
        # 上传百度云
        # 判断文件是否存在
        if os.path.exists(filepath):
            # os.system("bypy mkdir ExportEmployee")
            os.system("bypy upload %s ExportEmployee -v" % filepath)
    except:
        traceback.print_exc()

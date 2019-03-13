# coding=utf-8
from django import template
import traceback
import datetime
from modules.project_manage.models import Project
from django.contrib.auth.models import User
from modules.employee_management.employee_info.models import Employee
from django.utils import timezone

register = template.Library()


@register.filter
def get_recruitment_attache(employee_dict):
    """获取招聘人员信息
    :param employee_dict:在员工信息表中，根据招聘人员和项目信息去重信息列表
    :return:招聘人员姓名
    """
    recruitment_attache = ""
    try:
        user_id = employee_dict.get("recruitment_attache", "")
        user_obj = User.objects.filter(id=user_id)
        if user_obj.exists():
            recruitment_attache = user_obj[0].first_name
    except:
        traceback.print_exc()
    finally:
        return recruitment_attache


@register.filter
def get_project_name(employee_dict):
    """获取项目名称
    :param employee_dict:在员工信息表中，根据招聘人员和项目信息去重信息列表
    :return:项目名称
    """
    project_name = ""
    try:
        project_id = employee_dict.get("project_name", "")
        project_obj = Project.objects.filter(id=project_id)
        if project_obj.exists():
            project_name = project_obj[0].full_name
    except:
        traceback.print_exc()
    finally:
        return project_name


@register.filter
def project_emp_count(employee_dict):
    """招聘人数
    :param employee_dict:在员工信息表中，根据招聘人员和项目信息去重信息列表
    :return:
    """
    emp_count = 0
    try:
        user_id = employee_dict.get("recruitment_attache", "")
        project_id = employee_dict.get("project_name", "")
        emp_count = Employee.objects.filter(recruitment_attache_id=user_id, project_name__id=project_id).count()
    except:
        traceback.print_exc()
    finally:
        return emp_count


# 在职天数
@register.filter
def work_days(employee_object):
    try:
        entry_date = employee_object.entry_date  # 入职日期
        departure_date = employee_object.departure_date  # 离职日期
        start_work_date = employee_object.start_work_date  # 开始工作日
        end_work_date = employee_object.end_work_date  # 结束工作日

        if employee_object.is_temporary:
            if start_work_date and end_work_date:  # 入职+离职+1
                return (end_work_date - start_work_date).days + 1
            elif start_work_date and not end_work_date:  # 入职
                now_date = datetime.date.today()
                return (now_date - start_work_date).days + 1
            else:
                return 0
        else:
            if entry_date and departure_date:  # 入职+离职+1
                return (departure_date - entry_date).days + 1
            elif entry_date and not departure_date:  # 入职
                now_date = datetime.date.today()
                return (now_date - entry_date).days + 1
            else:
                return 0
    except:
        traceback.print_exc()
        return 0


# 计算单价
@register.filter
def unit_price(employee_object):
    """
    :param employee_object:
    :return:
    """
    unit_prices = 0
    try:
        if employee_object.project_name:
            unit_prices = employee_object.project_name.get_unit_price(str(timezone.now().month))
    except:
        traceback.print_exc()
    finally:
        return unit_prices


# 计算招聘提成
@register.filter
def recruitment_commission(employee_object, type_str):
    result = 0
    try:
        work_days_num = work_days(employee_object)  # 工作天数
        if employee_object.is_temporary and type_str == "temporary":  # 临时工
            unit_orice = unit_price(employee_object)
            result = work_days_num * unit_orice

        if not employee_object.is_temporary and type_str == "employee":
            if work_days_num >= 25:
                unit_orice = unit_price(employee_object)
                result = work_days_num * unit_orice
    except:
        traceback.print_exc()
    finally:
        return result


# 计算招聘提成
@register.filter
def grand_total_recruitment_commission(employee_dict, type_str):
    all_recruitment_commission = 0
    try:
        user_id = employee_dict.get("recruitment_attache", "")
        project_id = employee_dict.get("project_name", "")
        emp_objs = Employee.objects.filter(recruitment_attache_id=user_id, project_name__id=project_id)
        if str(type_str) == "temporary":  # 临时工
            for one_emp in emp_objs:
                all_recruitment_commission += recruitment_commission(one_emp, "temporary")

        if str(type_str) == "employee":
            for one_emp in emp_objs:
                all_recruitment_commission += recruitment_commission(one_emp, "employee")
    except:
        traceback.print_exc()
    finally:
        return all_recruitment_commission


@register.filter
def grand_total_work_days(employee_dict):
    """累计在职天数
    :param employee_dict:
    :return:
    """
    all_work_days = 0
    try:
        user_id = employee_dict.get("recruitment_attache", "")
        project_id = employee_dict.get("project_name", "")
        emp_objs = Employee.objects.filter(recruitment_attache_id=user_id, project_name__id=project_id)
        for one_emp in emp_objs:
            all_work_days += work_days(one_emp)
    except:
        traceback.print_exc()
    finally:
        return all_work_days

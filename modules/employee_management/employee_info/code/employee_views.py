# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView

from config.conf_core import PAGINATE
from modules.employee_management.employee_info.models import *
from modules.share_module.formater import *
from modules.share_module.permissionMixin import class_view_decorator
from modules.share_module.utils import get_kwargs


@class_view_decorator(login_required)
class EmployeeList(ListView):
    context_object_name = "emplyee_list"
    template_name = "employee_list.html"
    allow_empty = True
    paginate_by = PAGINATE

    def get_queryset(self):
        try:
            self.employee_type = self.kwargs.get("employee_type", "")

            # 权限校验
            perm = self.request.user.has_perm('employee_info.browse_%s' % self.employee_type)
            if not perm:
                raise PermissionDenied

            # 查询条件
            self.status = self.request.GET.get("status", "")  # 目前状态
            # if not self.request.user.is_superuser and self.request.user.has_perm('employee_info.leave_employee'):
            #     self.status = "2"
            self.project_name = self.request.GET.get("project_name", "")  # 项目名称
            self.dept_name = self.request.GET.get("dept_name", "")  # 服务部门
            self.principal = self.request.GET.get("principal", "")  # 项目负责人
            self.name = self.request.GET.get("name", "")  # 姓名
            self.identity_card_number = self.request.GET.get("identity_card_number", "")  # 身份证号
            self.person_type = int(self.request.GET.get("person_type", 0))  # 人员属性
            self.contract_type = self.request.GET.get("contract_type", "")  # 合同属性

            self.phone_number = self.request.GET.get("phone_number", "")  # 联系方式
            self.recruitment_attache = self.request.GET.get("recruitment_attache", "")  # 招聘人员
            self.st_release_time = self.request.GET.get("st_release_time", "")  # 发放起始时间
            self.et_release_time = self.request.GET.get("et_release_time", "")  # 发放终止日期
            self.start_time_str = self.request.GET.get("start_time", "")  # 创建起始时间
            self.end_time_str = self.request.GET.get("end_time", "")  # 创建终止时间
            self.start_time = self.start_time_str
            self.end_time = self.end_time_str

            if self.start_time and self.end_time:
                self.start_time += " 00:00:01"
                self.end_time += " 23:59:59"
                self.start_time = date_formater(self.start_time, "%Y/%m/%d %X")
                self.end_time = date_formater(self.end_time, "%Y/%m/%d %X")

            # 判断是否是客服部,是，只显示当前用户所属部门下信息
            self.customer_service = 0
            # try:
            #     user_position = self.request.user.position.name  # 用户岗位
            # except:
            #     user_position = ""
            # position_list = [u"客服专员", u"客服主管", u"外包主管", u"客服经理"]
            # if user_position in position_list:  # 登录用户在客服部，只能查看所在员工项目信息
            #     self.dept_name = self.request.user.attribution_dept
            #     self.customer_service = 1

            search_condition = {
                "status": self.status,
                "project_name__full_name__icontains": self.project_name,
                "project_name__principal__first_name__icontains": self.principal,
                "name__icontains": self.name,
                "identity_card_number__icontains": self.identity_card_number,
                "person_type": self.person_type,
                "contract_type": self.contract_type,
                "phone_number": self.phone_number,
                "recruitment_attache__first_name__icontains": self.recruitment_attache,
                "release_time__gte": self.st_release_time,
                "release_time__lte": self.et_release_time,
                "create_time__gte": self.start_time,
                "create_time__lte": self.end_time
            }
            if self.dept_name:
                search_condition.update({"project_name__department__name__in": self.dept_name.split(",")})
            else:
                if not self.request.user.is_superuser:
                    managements = map(int, self.request.user.remark2.split(",")) if self.request.user.remark2 else []
                    search_condition.update({"project_name__department__id__in": managements})

            # 普通管理员只查询自己负责项目的员工信息
            if not self.request.user.is_superuser and not self.request.user.dept_head:
                search_condition.update({"project_name__principal": self.request.user})

            kwargs = get_kwargs(search_condition)

            if self.employee_type == "employee":  # 查看员工信息
                kwargs.update({"is_temporary": False})

            elif self.employee_type == "temporary":  # 查看临时工信息
                kwargs.update({"is_temporary": True})

            return_emps = Employee.objects.filter(**kwargs)

            # # 当目前状态为离职，将所有离职人员一并显示
            # if self.status == "2":
            # 	leav_emps = Employee.objects.filter(status="2")
            # 	return_emps = return_emps | leav_emps

            return return_emps
        except:
            traceback.print_exc()

    def get_context_data(self, **kwargs):
        context = super(EmployeeList, self).get_context_data(**kwargs)
        context["status"] = self.status
        context["list_status"] = IS_WORK
        context["project_name"] = self.project_name
        context["dept_name"] = self.dept_name
        context["principal"] = self.principal
        context["name"] = self.name
        context["identity_card_number"] = self.identity_card_number
        context["person_type"] = self.person_type
        context["person_type_list"] = ContractType.objects.all()
        context["contract_type"] = self.contract_type
        context["list_contract_type"] = CONTRACT_CHOICES
        context["customer_service"] = self.customer_service
        context["phone_number"] = self.phone_number
        context["recruitment_attache"] = self.recruitment_attache
        context["st_release_time"] = self.st_release_time
        context["start_time"] = self.start_time_str
        context["end_time"] = self.end_time_str
        context["et_release_time"] = self.et_release_time
        context["employee_type"] = self.employee_type
        return context

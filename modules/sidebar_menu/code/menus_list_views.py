# encoding=utf-8
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import View

from modules.contract_manage.models import ContractPreviewCode
from modules.dict_table.models import *
from modules.finance.arrival_and_billing.models import ArrivalAndBilling
from modules.finance.loans_and_write_offs.models import LoansAndWriteOffs
from modules.finance.social_security_audit.models import SocialSecurityAudit
from modules.organizational_structure.departments.models import Department
from modules.organizational_structure.profiles.models import Profile
from modules.share_module.permissionMixin import class_view_decorator
from modules.system.models import DataBackup, SystemConfig

menu_list = [
    {
        "permissions": "admin_account.browse_index",
        "show": True,
        "text": "我的主页",
        "icon": "menu-icon fa fa-tachometer",
        "url": reverse('home_page:index', args=())
    },

    {
        "permissions": "admin_account.browse_mysite",
        "show": True,
        "text": "我的地盘",
        "icon": "menu-icon fa fa-user",
        "url": "",
        "menus": [
            {
                "permissions": "admin_account.browse_personal",
                "show": True,
                "text": "我的个人信息",
                "icon": "",
                "url": reverse('mysite:personal', args=())
            },
            {
                "permissions": '',
                "show": False,
                "text": "我的邮箱",
                "icon": "",
                "url": reverse('mysite:emails', args=())
            },
        ]
    },

    {
        "permissions": "admin_account.browse_organizational",
        "show": True,
        "text": "组织架构",
        "icon": "menu-icon fa fa-sitemap",
        "url": "",
        "menus": [
            {
                "permissions": "admin_account.browse_structure",
                "show": False,
                "text": "组织架构图",
                "icon": "",
                "url": reverse('organizational_structure:structure', args=())
            },
            {
                "permissions": "departments.browse_department",
                "show": True,
                "text": "部门信息",
                "icon": "",
                "url": Department.get_absolute_url()
            },
            {
                "permissions": "admin_account.browse_user",
                "show": True,
                "text": "管理人员",
                "icon": "",
                "url": Profile.get_absolute_url()
            }
        ]
    },

    {
        "permissions": "admin_account.browse_project_manage",
        "show": True,
        "text": "项目管理",
        "icon": "menu-icon fa fa-briefcase",
        "url": "",
        "menus": [
            {
                "permissions": "project_manage.browse_basic_info",
                "show": True,
                "text": "项目基础信息",
                "icon": "",
                "url": "/projectmanage/project/basic_info"
            },

            {
                "permissions": "project_manage.browse_social_security_info",
                "show": True,
                "text": "项目福利信息",
                "icon": "",
                "url": "/projectmanage/project/social_security_info"
            },

            {
                "permissions": "project_manage.browse_settle_accounts_info",
                "show": True,
                "text": "项目结算信息",
                "icon": "",
                "url": "/projectmanage/project/settle_accounts_info"
            },

            {
                "permissions": "project_manage.browse_billing_info",
                "show": True,
                "text": "项目开票信息",
                "icon": "",
                "url": "/projectmanage/project/billing_info"
            },

            {
                "permissions": "project_manage.browse_sales_info",
                "show": True,
                "text": "项目销售信息",
                "icon": "",
                "url": "/projectmanage/project/sales_info"
            },

            {
                "permissions": "project_manage.browse_recruitment_unit",
                "show": True,
                "text": "项目招聘单价",
                "icon": "",
                "url": "/projectmanage/project/recruitment_unit"
            }
        ]
    },

    {
        "permissions": "admin_account.browse_employee_manage",
        "show": True,
        "text": "员工管理",
        "icon": "menu-icon fa fa-users",
        "url": "",
        "menus": [
            {
                "permissions": "employee_info.browse_employee",
                "show": True,
                "text": "员工信息",
                "icon": "",
                "url": "/employeemanage/employee/list"
            },
            {
                "permissions": "employee_info.browse_archive",
                "show": True,
                "text": "员工档案信息",
                "icon": "",
                "url": "/archive/list"
            },
            {
                "permissions": "employee_info.browse_temporary",
                "show": True,
                "text": "临时工信息",
                "icon": "",
                "url": "/employeemanage/temporary/list"
            }
        ]
    },

    {
        "permissions": "admin_account.browse_socialsecurity",
        "show": True,
        "text": "社保福利",
        "icon": "menu-icon fa fa-coffee",
        "menus": [
            {
                "permissions": "increase_info.browse_increase",
                "show": True,
                "text": "增员信息",
                "icon": "",
                "url": "/increase/list"
            },
            {
                "permissions": "reduction_info.browse_reduction",
                "show": True,
                "text": "减员信息",
                "icon": "",
                "url": "/reduction/list"
            },
            {
                "permissions": "social_security_detail.browse_social_security_detail",
                "show": True,
                "text": "社保明细",
                "icon": "",
                "url": "/social_security_detail/list"
            }
        ]
    },

    {
        "permissions": "settlement_pay.browse_payroll",
        "show": True,
        "text": "结算发薪",
        "icon": "menu-icon fa fa-gift",
        "url": "/payroll/list"
    },

    {
        "permissions": "admin_account.browse_recruitment",
        "show": True,
        "text": "招聘管理",
        "icon": "menu-icon fa fa-filter",
        "url": "/recruitment/list",
        "menus": [
            {
                "permissions": "admin_account.browse_month_entry_job_details",
                "show": True,
                "text": "当月入职招聘明细",
                "icon": "",
                "url": "/recruitment/month_entry_job_details"
            },
            {
                "permissions": "admin_account.browse_individual_job",
                "show": True,
                "text": "个人招聘",
                "icon": "",
                "url": "/recruitment/individual_job"
            },
            {
                "permissions": "admin_account.browse_job_statistic",
                "show": True,
                "text": "招聘统计",
                "icon": "",
                "url": "/recruitment/job_statistic"
            }
        ]
    },

    {
        "permissions": "admin_account.browse_approval",
        "show": True,
        "text": "审批流程",
        "icon": "menu-icon glyphicon glyphicon-retweet",
        "url": "",
        "menus": [
            {
                "permissions": "admin_account.browse_apply_info_template",
                "show": True,
                "text": "申请信息模板",
                "icon": "",
                "url": "/approval/"
            },
            {
                "permissions": "admin_account.browse_approval_pending",
                "show": True,
                "text": "待审批信息",
                "icon": "",
                "url": "/approval/pending"
            }
        ]
    },

    {
        "permissions": "expense_manage.browse_expense",
        "show": True,
        "text": "费用管理",
        "icon": "menu-icon glyphicon glyphicon-usd",
        "url": "/expense/list"
    },

    {
        "permissions": "admin_account.browse_payroll_manage",
        "show": True,
        "text": "薪资管理",
        "icon": "menu-icon fa fa-money",
        "url": "",
        "menus": [
            {
                "permissions": "payroll_detail.browse_payrolldetail",
                "show": True,
                "text": "薪资明细",
                "icon": "",
                "url": "/payroll_manage/detail/list"
            },
            {
                "permissions": "payroll_gather.browse_payrollgather",
                "show": True,
                "text": "薪资汇总",
                "icon": "",
                "url": "/payroll_manage/gather/list"
            }
        ]
    },

    {
        "permissions": "admin_account.browse_qualityassurance_manage",
        "show": True,
        "text": "人事操作质量",
        "icon": "menu-icon fa fa-check-square-o",
        "url": "",
        "menus": [
            {
                "permissions": "personnel_operation.browse_qualityassurance",
                "show": True,
                "text": "个人操作质量",
                "icon": "",
                "url": "/personnel/list"
            },
            {
                "permissions": "admin_account.browse_qualityassurance_gather",
                "show": True,
                "text": "操作质量汇总",
                "icon": "",
                "url": "/personnel/gather"
            }
        ]
    },

    {
        "permissions": "admin_account.browse_finance",
        "show": True,
        "text": "财务管理",
        "icon": "menu-icon fa fa-pencil-square-o",
        "menus": [
            {
                "permissions": "social_security_audit.browse_socialsecurityaudit",
                "show": True,
                "text": "社保审核",
                "icon": "",
                "url": SocialSecurityAudit.get_absolute_url()
            },
            {
                "permissions": "arrival_and_billing.browse_arrivalandbilling",
                "show": True,
                "text": "到账与开票",
                "icon": "",
                "url": ArrivalAndBilling.get_absolute_url()
            },
            {
                "permissions": "loans_and_write_offs.browse_loansandwriteoffs",
                "show": True,
                "text": "借款与销账",
                "icon": "",
                "url": LoansAndWriteOffs.get_absolute_url()
            }
        ]
    },

    {
        "permissions": "admin_account.browse_contract",
        "show": True,
        "text": "合同管理",
        "icon": "menu-icon fa fa-file-text-o",
        "menus": [
            {
                "permissions": "contract_manage.browse_contractsend",
                "show": True,
                "text": "派遣",
                "icon": "",
                "url": ContractPreviewCode.get_absolute_url()
            },

            {
                "permissions": "contract_manage.browse_contractoutsourc",
                "show": True,
                "text": "外包",
                "icon": "",
                "url": ContractPreviewCode.get_absolute_url()
            },

            {
                "permissions": "contract_manage.browse_contractintern",
                "show": True,
                "text": "实习生",
                "icon": "",
                "url": ContractPreviewCode.get_absolute_url()
            },

            {
                "permissions": "contract_manage.browse_contractservice",
                "show": True,
                "text": "劳务",
                "icon": "",
                "url": ContractPreviewCode.get_absolute_url()
            },

            {
                "permissions": "contract_manage.browse_contracthourly",
                "show": True,
                "text": "小时工",
                "icon": "",
                "url": ContractPreviewCode.get_absolute_url()
            },

            {
                "permissions": "contract_manage.browse_contractpreviewcode",
                "show": True,
                "text": "合同预览",
                "icon": "",
                "url": ContractPreviewCode.get_absolute_url()
            }
        ]
    },

    {
        "permissions": "admin_account.browse_system",
        "show": True,
        "text": "系统相关",
        "icon": "menu-icon fa fa-cogs",
        "url": "",
        "menus": [
            {
                "permissions": "admin_account.browse_admin",
                "show": True,
                "text": "权限管理",
                "icon": "",
                "url": "/admin"
            },
            {
                "permissions": "system.browse_systemconfig",
                "show": True,
                "text": "系统设置",
                "icon": "",
                "url": SystemConfig.get_absolute_url()
            },
            {
                "permissions": "system.data_backup",
                "show": True,
                "text": "数据备份",
                "icon": "",
                "url": DataBackup.get_absolute_url()
            }
        ]
    },

    {
        "permissions": "admin_account.browse_dict",
        "show": True,
        "text": "字典表",
        "icon": "menu-icon fa fa-book",
        "url": "",
        "menus": [
            {
                "permissions": "dict_table.browse_companysubject",
                "show": True,
                "text": "公司主体",
                "icon": "",
                "url": CompanySubject.get_absolute_url()
            },
            {
                "permissions": "dict_table.browse_contracttype",
                "show": True,
                "text": "合同类型",
                "icon": "",
                "url": ContractType.get_absolute_url()
            },
            {
                "permissions": "dict_table.browse_projecttype",
                "show": True,
                "text": "项目类型",
                "icon": "",
                "url": ProjectType.get_absolute_url()
            },
            {
                "permissions": "dict_table.browse_progressstate",
                "show": True,
                "text": "项目目前状态",
                "icon": "",
                "url": ProgressState.get_absolute_url()
            },
            {
                "permissions": "dict_table.browse_salestype",
                "show": True,
                "text": "销售类型",
                "icon": "",
                "url": SalesType.get_absolute_url()
            },
            {
                "permissions": "dict_table.browse_socialsecuritytype",
                "show": True,
                "text": "社保险种",
                "icon": "",
                "url": SocialSecurityType.get_absolute_url()
            },
            {
                "permissions": "dict_table.browse_socialsecurityaccounttype",
                "show": True,
                "text": "社保账户类型",
                "icon": "",
                "url": SocialSecurityAccountType.get_absolute_url()
            },
            {
                "permissions": "dict_table.browse_businessinsurancecompany",
                "show": True,
                "text": "商保公司",
                "icon": "",
                "url": BusinessInsuranceCompany.get_absolute_url()
            },
            {
                "permissions": "dict_table.browse_cycle",
                "show": True,
                "text": "时间周期",
                "icon": "",
                "url": Cycle.get_absolute_url()
            },
            {
                "permissions": "dict_table.browse_wagegranttype",
                "show": True,
                "text": "工资发放方式",
                "icon": "",
                "url": WageGrantType.get_absolute_url()
            },
            {
                "permissions": "dict_table.browse_invoicetype",
                "show": True,
                "text": "发票类型",
                "icon": "",
                "url": InvoiceType.get_absolute_url()
            },
            {
                "permissions": "dict_table.browse_position",
                "show": True,
                "text": "岗位类型",
                "icon": "",
                "url": Position.get_absolute_url()
            },
            {
                "permissions": "dict_table.browse_archivetype",
                "show": True,
                "text": "档案类型",
                "icon": "",
                "url": ArchiveType.get_absolute_url()
            },
            {
                "permissions": "dict_table.browse_expensetype",
                "show": True,
                "text": "费用类型",
                "icon": "",
                "url": ExpenseType.get_absolute_url()
            },
            {
                "permissions": "dict_table.browse_improvestatus",
                "show": True,
                "text": "改善状态",
                "icon": "",
                "url": ImproveStatus.get_absolute_url()
            },
            {
                "permissions": "dict_table.browse_leavetype",
                "show": True,
                "text": "请假类型",
                "icon": "",
                "url": LeaveType.get_absolute_url()
            },
            {
                "permissions": "dict_table.browse_subject",
                "show": True,
                "text": "科目",
                "icon": "",
                "url": Subject.get_absolute_url()
            },
            {
                "permissions": "dict_table.browse_management_rights",
                "show": True,
                "text": "管理权",
                "icon": "",
                "url": ManagementRights.get_absolute_url()
            }
        ]
    }
]


@class_view_decorator(login_required)
class SidebarMenusList(View):
    """
    菜单
    """

    def get(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        data = self.get_menu_list()
        result = json.dumps({"data": data})
        return HttpResponse(result, content_type="application/json")

    def get_menu_list(self):
        """
        :return:
        """
        try:
            if not self.request.user.is_superuser:
                for one_menu in menu_list:
                    if not self.request.user.has_perm(one_menu["permissions"]):
                        one_menu["show"] = False
                        continue
                    else:
                        if one_menu.has_key("menus"):
                            sum_sub_menus = len(one_menu["menus"])
                            sum_false = 0
                            for sub in one_menu["menus"]:
                                if not self.request.user.has_perm(sub.get("permissions")):
                                    sub["show"] = False
                                    sum_false += 1
                            if sum_false == sum_sub_menus:
                                one_menu["show"] = False
        except:
            traceback.print_exc()
        finally:
            return menu_list

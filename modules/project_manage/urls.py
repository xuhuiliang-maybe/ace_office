# coding=utf-8
from django.conf.urls import url

from modules.project_manage.code import projects_views, del_project_info, add_project_info, edit_project_info, \
	load_project_views, export_project_views
from modules.project_manage.models import Project

urlpatterns = [
    # 项目基础信息
    url(r'^project/(?P<project_info_type>\w+)$', projects_views.ProjectsList.as_view(), name="project_list"),
    # 项目信息
    url(r'^project_add$', add_project_info.ProjectsCreate.as_view(), name="project-add"),  # 新增
    url(r'^project/(?P<pk>[0-9]+)/edit$', edit_project_info.ProjectUpdate.as_view(), {"model_name": Project},
        name="project_edit"),  # 编辑
    url(r'^project/(?P<pk>[0-9]+)/delete$', del_project_info.ProjectsDelete.as_view(), {"model_name": Project},
        name="project_delete"),  # 删除
    # 批量删除
    url(r'^projects/batchdelete$', del_project_info.ProjectsBatchDelete.as_view(), name="project_batch_delete"),
    url(r'^load$', load_project_views.LoadProjectView.as_view(), name="project_load"),  # 导入
    url(r'^export$', export_project_views.ProjectExportView.as_view(), name="project_export"),

    # 项目福利信息-编辑
    url(r'^project/(?P<pk>[0-9]+)/edit_social_security_info$',
        edit_project_info.ProjectSocialSecurityInfoUpdate.as_view(), {"model_name": Project},
        name="edit_project_social_security"),

    # 项目结算信息-编辑
    url(r'^project/(?P<pk>[0-9]+)/edit_settle_accounts_info$',
        edit_project_info.ProjectSettleAccountsInfoUpdate.as_view(),
        {"model_name": Project}, name="edit_project_settle_accounts"),

    # 项目开票信息-编辑
    url(r'^project/(?P<pk>[0-9]+)/edit_billing_info$', edit_project_info.ProjectBillingInfoUpdate.as_view(),
        {"model_name": Project}, name="edit_project_billing"),

    # 项目销售信息-编辑
    url(r'^project/(?P<pk>[0-9]+)/edit_sales_info$', edit_project_info.ProjectSalesInfoUpdate.as_view(),
        {"model_name": Project}, name="edit_project_sales"),

    # 项目招聘单价-编辑
    url(r'^project/(?P<pk>[0-9]+)/edit_recruitment_unit$', edit_project_info.ProjectRecruitmentUnitUpdate.as_view(),
        {"model_name": Project}, name="edit_project_recruitment_unit"),
]

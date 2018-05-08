# coding=utf-8
from django.conf.urls import url

from modules.recruitment_manage.code import individual_job
from modules.recruitment_manage.code import job_statistic
from modules.recruitment_manage.code import month_entry_job_details

# 招聘管理
urlpatterns = [
	# 当月入职招聘明细
	url(r'^month_entry_job_details$', month_entry_job_details.MonthEntryJobDetailsListView.as_view()),

	url(r'^individual_job$', individual_job.IndividualJobListView.as_view()),  # 个人招聘相关

	# 招聘统计
	url(r'^job_statistic$', job_statistic.JobStatisticListView.as_view()),
	# 导出招聘统计
	url(r'^job_statistic/export$', job_statistic.JobStatisticExportView.as_view(), name="job_statistic_export"),
]

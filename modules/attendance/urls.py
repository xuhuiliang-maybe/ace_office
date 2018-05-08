# coding=utf-8
from django.conf.urls import url

from modules.attendance.code import profiles_att_views, workers_att_views

# 考勤
urlpatterns = [
	url(r'profiles_att$', profiles_att_views.ProfileAttendanceListView.as_view()),  # 人员考勤
	url(r'workers_att$', workers_att_views.WorkerAttendanceListView.as_view()),  # 务工人员考勤
]

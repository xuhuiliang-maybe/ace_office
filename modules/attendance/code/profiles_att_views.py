# coding=utf-8
from django.views.generic import ListView


class ProfileAttendanceListView(ListView):
	context_object_name = "profile_att_list"
	template_name = "profiles_attendance.html"

	# allow_empty = True
	# paginate_by = 10

	def get_queryset(self):
		pass

	def post(self, request):
		pass

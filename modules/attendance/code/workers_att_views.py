# coding=utf-8
from django.views.generic import ListView


class WorkerAttendanceListView(ListView):
	context_object_name = "worker_att_list"
	template_name = "workers_attendance.html"

	# allow_empty = True
	# paginate_by = 30

	def get_queryset(self):
		pass

	def post(self, request):
		pass

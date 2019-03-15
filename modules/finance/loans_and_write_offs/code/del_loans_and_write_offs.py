# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import DeleteView

from modules.finance.loans_and_write_offs.models import LoansAndWriteOffs
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('loans_and_writeoffs.delete_loansandwriteoffs', raise_exception=True))
class LoansAndWriteOffsDelete(SuccessMessageMixin, DeleteView):
    model = LoansAndWriteOffs
    template_name = "base/confirm_delete.html"
    success_message = u"%(remark)s 删除创建"

    def get_success_url(self):
        url = self.model.get_absolute_url()
        referrer = self.request.POST.get("referrer", "")
        if referrer:
            url = referrer
        return url

    def get_context_data(self, **kwargs):
        context = super(LoansAndWriteOffsDelete, self).get_context_data(**kwargs)
        referrer = self.request.META.get('HTTP_REFERER', "")
        context["referrer"] = referrer
        return context

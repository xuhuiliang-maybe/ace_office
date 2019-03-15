# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView

from modules.finance.loans_and_write_offs.models import LoansAndWriteOffs
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('loans_and_write_offs.add_loansandwriteoffs', raise_exception=True))
class LoansAndWriteOffsCreate(SuccessMessageMixin, CreateView):
    model = LoansAndWriteOffs
    template_name = "base/document_edit.html"
    fields = ["remark"]
    success_message = u"%(remark)s 成功创建"

    def get_success_url(self):
        self.url = self.model.get_absolute_url()
        referrer = self.request.POST.get("referrer", "")
        # if referrer:
        # 	self.url = referrer
        return self.url

    def get_context_data(self, **kwargs):
        context = super(LoansAndWriteOffsCreate, self).get_context_data(**kwargs)
        context["form_content"] = u"新增借款与销账"
        referrer = self.request.META.get('HTTP_REFERER', "")
        context["referrer"] = referrer
        return context

    # 表单处理
    def form_valid(self, form):
        return super(LoansAndWriteOffsCreate, self).form_valid(form)

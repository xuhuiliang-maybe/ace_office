# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView

from modules.finance.loans_and_write_offs.models import LoansAndWriteOffs
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('loans_and_write_offs.change_loansandwriteoffs', raise_exception=True))
# @class_view_decorator(check_principal)  # 校验是否负责该项目
class LoansAndWriteOffsUpdate(SuccessMessageMixin, UpdateView):
    model = LoansAndWriteOffs
    template_name = "loans_and_write_offs_edit.html"
    success_message = u"%(remark)s 成功修改"
    fields = ["amount_write_offs", "write_offs_date", "remark"]

    def get_success_url(self):
        url = self.model.get_absolute_url()
        referrer = self.request.POST.get("referrer", "")
        if referrer:
            url = referrer
        return url

    # 增加返回参数
    def get_context_data(self, **kwargs):
        context = super(LoansAndWriteOffsUpdate, self).get_context_data(**kwargs)
        context["form_content"] = u"修改借款与销账"
        referrer = self.request.META.get('HTTP_REFERER', "")
        context["referrer"] = referrer
        return context

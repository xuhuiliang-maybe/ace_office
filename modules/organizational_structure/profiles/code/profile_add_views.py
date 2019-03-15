# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView

from modules.organizational_structure.profiles.models import Profile
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('auth.add_user', raise_exception=True))
class ProfileCreate(SuccessMessageMixin, CreateView):
    model = User
    template_name = "base/document_edit.html"
    fields = ["username", "first_name", "password", "attribution_dept", "remark2"]
    success_message = u"%(username)s 成功创建"

    def get_success_url(self):
        self.url = Profile.get_absolute_url()
        referrer = self.request.POST.get("referrer", "")
        # if referrer:
        # 	self.url = referrer
        _addanother = self.request.POST.get("_addanother", "")
        if _addanother:
            self.url = reverse('organizational_structure:profile:profile_add')
        return self.url

    def get_context_data(self, **kwargs):
        context = super(ProfileCreate, self).get_context_data(**kwargs)
        context["form_content"] = u"新增管理人员"
        referrer = self.request.META.get('HTTP_REFERER', "")
        context["referrer"] = referrer
        return context

    # 对新增用户密码做加密处理
    def form_valid(self, form):
        form.instance.password = make_password(form.instance.password)
        return super(ProfileCreate, self).form_valid(form)

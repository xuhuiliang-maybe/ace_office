# encoding=utf-8
import json
import traceback

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import View

from modules.share_module.permissionMixin import class_view_decorator


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
        menu_list = list()
        try:
            from modules.sidebar_menu.code.menus import menu_list
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

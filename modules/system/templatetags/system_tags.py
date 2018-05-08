# coding=utf-8
import os
import traceback

from django import template

from modules.share_module.get_path import get_media_sub_path

register = template.Library()


@register.filter
def check_db_backup(file_name):
    try:
        bak_dir = get_media_sub_path("mysql_backup/")
        bak_dir_db_name = bak_dir + file_name
        if os.path.exists(bak_dir_db_name):
            return r'<i class="green ace-icon fa fa-check-circle bigger-130"></i>'
        return r'<i class="red ace-icon fa fa-times-circle bigger-130"></i>'
    except:
        traceback.print_exc()
        return u""


@register.filter
def backup_db_status(status_str):
    try:
        if status_str == "1":
            return "<span class='label arrowed-right arrowed-in'>备份</span>"
        elif status_str == "2":
            return "<span class='label label-success arrowed-in arrowed-in-right'>已还原</span>"
        else:
            return ""
    except:
        traceback.print_exc()
        return ""

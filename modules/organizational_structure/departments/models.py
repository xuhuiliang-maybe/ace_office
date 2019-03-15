# coding=utf-8
import traceback

from django.core.cache import cache
from django.db import models

from modules.dict_table.models import ManagementRights

DEPTVERSION = 1

APPORTION_TYPE = (
    ("1", u"个人分摊"),
    ("2", u"部门分摊"),
    ("3", u"公司分摊"),
)
TYPE_DICT = {
    # "1": '<i class="ace-icon fa fa-paper-plane red"></i> ',
    # "2": '<i class="ace-icon fa fa-paper-plane green"></i> ',
    # "3": '<i class="ace-icon fa fa-paper-plane"></i> ',
    "1": u"个人分摊",
    "2": u"部门分摊",
    "3": u"公司分摊",
}


class Department(models.Model):
    """部门信息 """

    name = models.CharField(u"部门名称", max_length=50, unique=True)
    parent_dept = models.PositiveIntegerField(u"上级部门", blank=False, default=1, db_index=True)
    apportion_type = models.CharField(u"分摊类型", max_length=1, choices=APPORTION_TYPE, default='1')
    management_rights = models.ForeignKey(ManagementRights, verbose_name="管理权", null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"部门信息"
        index_together = ["name"]  # 索引字段组合
        permissions = (
            ("browse_department", u"浏览 部门信息"),
        )

    def update_dept_cache(self):
        """更新部门信息缓存
        :return:
        """
        global DEPTVERSION
        cache.delete("dept_tree_%s" % DEPTVERSION)  # 删部门树缓存
        cache.delete("department_%s_%s" % (self.id, DEPTVERSION))  # 删对应部门缓存
        DEPTVERSION += 1

    @staticmethod
    def get_dept_by_name(name):
        try:
            return Department.objects.get(name=name)
        except:
            traceback.print_exc()
            return ""

    @staticmethod
    def get_dept_by_id(dept_id):
        """
        :param dept_id:
        :return:
        """
        global DEPTVERSION
        try:
            if not dept_id:
                return None

            department = cache.get("dept_%s_%s" % (dept_id, DEPTVERSION))
            if department:
                return department

            try:
                department = Department.objects.get(id=dept_id)
            except:
                department = None

            if department:
                cache.set("department_%s_%s" % (dept_id, DEPTVERSION), department)
            return department
        except:
            traceback.print_exc()

    def get_children(self):
        return Department.objects.filter(parent_dept=self.id)

    @staticmethod
    def get_apportion_type(apportion_type):
        return TYPE_DICT.get(apportion_type, "")

    def all_children(self, start=[]):
        try:
            for d in self.get_children():
                if d not in start:
                    start.append(d)
                    d.all_children(start)
        except:
            traceback.print_exc()
        return start

    def save(self):
        global DEPTVERSION
        try:
            parent_dept = self.get_dept_by_id(self.parent_dept)  # 上级部门总数

            if parent_dept and parent_dept != self:
                # 上级部门存在，上级部门不是自己本身
                self.update_dept_cache()
                models.Model.save(self)
            elif self.parent_dept == 0:
                default_dept = Department.objects.filter(parent_dept=0)
                if not default_dept.exists():
                    # 保存默认部门
                    self.update_dept_cache()
                    models.Model.save(self)
            else:
                raise Exception("Default department already exists.")
        except:
            traceback.print_exc()

    def delete(self):
        self.update_dept_cache()  # 更新缓存
        super(Department, self).delete()

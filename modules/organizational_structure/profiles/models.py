# coding=utf-8
import traceback

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

from modules.dict_table.models import Position
from modules.organizational_structure.departments.models import Department


class ProfileBase(type):  # 对于传统类，他们的元类都是types.ClassType
    def __new__(cls, name, bases, attrs):  # 带参数的构造器，__new__一般用于设置不变数据类型的子类
        module = attrs.pop('__module__')
        parents = [b for b in bases if isinstance(b, ProfileBase)]
        if parents:
            fields = []
            for obj_name, obj in attrs.items():
                if isinstance(obj, models.Field): fields.append(obj_name)
                User.add_to_class(obj_name, obj)
            UserAdmin.fieldsets = list(UserAdmin.fieldsets)
            UserAdmin.fieldsets.append((name, {'fields': fields}))
        return super(ProfileBase, cls).__new__(cls, name, bases, attrs)


class ProfileUser(object):
    __metaclass__ = ProfileBase  # 类属性


GENDER_CHOICES = (
    ('M', u'男'),
    ('F', u'女'),
)


class Profile(ProfileUser):
    """管理员扩展信息"""

    company = models.CharField(u"公司名称", max_length=256, blank=True)
    one_level_dept = models.CharField(u"一级部门", max_length=100, blank=True)
    attribution_dept = models.CharField(u"部门", max_length=100, blank=True)  # 二级部门
    gender = models.CharField(u"性别", max_length=2, choices=GENDER_CHOICES, blank=True)
    dept_head = models.BooleanField(u"是否部门负责人", default=False, blank=True)
    higher_up = models.CharField(u"直线上级", max_length=100, blank=True)
    position = models.ForeignKey(Position, verbose_name=u"岗位", null=True, blank=True)
    mobile_phone = models.CharField(u"手机号", max_length=11, blank=True)
    telephone = models.CharField(u"座机号", max_length=12, blank=True)
    authorize_leave = models.PositiveIntegerField(u"可审批请假天数", default=0, blank=True)
    authorize_loan = models.PositiveIntegerField(u"可审批借款金额", default=0, blank=True)
    authorize_wage = models.PositiveIntegerField(u"可审批涨薪金额", default=0, blank=True)
    photo = models.ImageField(u"头像", upload_to='user_photo', default='/static/avatars/avatar2.png', blank=True)
    address = models.CharField(u"办公通讯地址", max_length=256, blank=True)
    remark1 = models.CharField(u"户籍地址", max_length=256, blank=True)
    remark2 = models.CharField(u"授权管理部门", max_length=256, blank=True)
    remark3 = models.CharField(u"备注3", max_length=256, blank=True)
    remark4 = models.CharField(u"备注4", max_length=256, blank=True)
    remark5 = models.CharField(u"备注5", max_length=256, blank=True)

    USERNAME_FIELD = 'username'
    FIRST_NAME_FIELD = 'first_name'

    class Meta:
        verbose_name = u"用户信息"
        ordering = ['-id']

    def get_username(self):
        return getattr(self, self.FIRST_NAME_FIELD)

    @staticmethod
    def get_user_by_username_or_first_name(user_str):
        try:
            if user_str:
                user_obj = User.objects.filter(Q(first_name=user_str) | Q(username=user_str))
                if user_obj.exists():
                    return user_obj.first()
            return None
        except:
            traceback.print_exc()

# class ProfileManageDepartment(models.Model):
#     """用户授权管理部门 """
#     user = models.ForeignKey(User, verbose_name=u"用户")
#     department = models.ForeignKey(Department, verbose_name=u"授权部门")
#
#     def __str__(self):
#         return self.user, self.department
#
#     class Meta:
#         verbose_name = u"用户授权管理部门"
#         verbose_name_plural = verbose_name
#         unique_together = (("user", "department"),)

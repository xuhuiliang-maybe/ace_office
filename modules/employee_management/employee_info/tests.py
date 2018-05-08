# coding=utf-8
from django.test import TestCase
from modules.employee_info.models import Employee
from django.contrib.auth.models import User
from modules.organizational_structure.departments.models import Department

"""
用户信息单元测试
项目下运行：python manage.py test modules.employee_info
"""


# Create your tests here.

#测试部门过滤
dept_ids= u'1,'
dept_ids = [int(i) for i in dept_ids[:-1].split(',')]
dept_list = Department.objects.filter(id__in=dept_ids)
print dept_list[0].name
# user_obj_list = Employee.objects.filter(attribution_dept__in=dept_list[0].name)
user_obj_list = Employee.objects.filter(attribution_dept__icontains='北京')
# user_obj_list = Employee.objects.filter(name__icontains=name)
print user_obj_list


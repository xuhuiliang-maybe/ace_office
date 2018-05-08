# coding=utf-8
from django.conf.urls import url

from modules.expense_manage.code import expense_views, expense_add_views, expense_edit_views, expense_delete
from modules.expense_manage.models import Expense

# 费用管理相关
urlpatterns = [
	url(r'^list$', expense_views.ExpenseListView.as_view(), name="expense_list"),  # 费用管理
	url(r'^expense_add$', expense_add_views.ExpenseCreate.as_view(), name="expense_add"),  # 新增
	url(r'^expense_(?P<pk>[0-9]+)/edit$', expense_edit_views.ExpenseUpdate.as_view(), {"model_name": Expense},
	    name="expense_edit"),  # 编辑
	url(r'^expense_(?P<pk>[0-9]+)/delete$', expense_delete.ExpenseDelete.as_view(), {"model_name": Expense},
	    name="expense_delete"),  # 删除

]

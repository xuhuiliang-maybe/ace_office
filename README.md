# ace_office
## 目录说明：
* ace_office：总路由，项目settings
* config：网站配置参数（数据库，缓存）
* doc：文档目录（前端模板文件，google浏览器打开才会显示图标）
* media：
    info_template：导入信息模板，提供给用户下载参考
    tmp：临时文件，可存放测试文件和导出数据文件
    user_photo：用户头像
* modules：包含所有模块（app）
    * 'modules.admin_account' 用户权限
    * 'modules.home_page' 我的主页
    * 'modules.mysite' 我的地盘
    * 'modules.organizational_structure' 组织架构
    * 'modules.organizational_structure.departments' 部门信息
    * 'modules.organizational_structure.profiles' 管理员信息
    * 'modules.organizational_structure.structures' 组织结构图
    * 'modules.project_manage' 项目管理
    * 'modules.employee_info' 员工信息
    * 'modules.social_security' 社保福利
    * 'modules.settlement_pay' 结算发薪
    * 'modules.recruitment_manage' 招聘管理
    * 'modules.approval_process' 审批流程
    * 'modules.approval_process.leave' 审批流程，申请请假
    * 'modules.approval_process.loan' 审批流程，申请借款
    * 'modules.approval_process.wage' 审批流程，申请涨薪
    * 'modules.expense_manage' 费用管理
    * 'modules.personnel_operation' 人事操作质量
    * 'modules.system' 系统管理
    * 'modules.share_module' 公用模块
    * 'modules.attendance' 考勤,暂缓开通
    * 'modules.calendards' 日历，暂缓开通


* static：网站模板用css，js静态文件
* templates：总模板目录

## 部署说明：
* 确认工具是否安装
```
pip
setuptools
```
* 项目根路径下执行
```
pip install -r requirements.txt
uwsgi -x /var/www/html/ace_office/ace_office/django.xml &
```
* 定时任务
```
* 0 */3 * * /usr/local/nginx/logs/aa_nginx_access_log.sh
0 */6 * * * /var/www/html/backmysql.sh
0 2 * * * /var/www/html/ace_office/export.sh >> /tmp/export_emp.log
```

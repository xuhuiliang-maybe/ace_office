# coding=utf-8
import xlrd
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect
from django.views.generic import View

from modules.dict_table.models import *
from modules.organizational_structure.departments.models import Department
from modules.organizational_structure.profiles.models import Profile
from modules.project_manage.models import Project
from modules.share_module.formater import *
from modules.share_module.get_path import *
from modules.share_module.load_info import LoadInfoUploadForm
from modules.share_module.permissionMixin import class_view_decorator


@class_view_decorator(login_required)
@class_view_decorator(permission_required('project_manage.add_project', raise_exception=True))
class LoadProjectView(View):
    def post(self, request, *args, **kwargs):
        try:
            upload_form = LoadInfoUploadForm(request.POST, request.FILES)
            if upload_form.is_valid():
                upload_file_obj = upload_form.cleaned_data['load_info']  # 上传文件对象
                upload_file_name = upload_file_obj.name
                upload_file_path = os.path.join(get_media_sub_path("tmp"), upload_file_name)

                # 将上传文件暂存tmp目录
                data = ""
                for chunk in upload_file_obj.chunks():
                    data += chunk
                f = file(upload_file_path, "wb")
                f.write(data)
                f.close()

                # 执行导入数据库
                return self.load_data(upload_file_path)

            messages.warning(self.request, u"无文件上传！")
            return redirect(reverse('project_manage:project_list', args=("basic_info",)))
        except:
            traceback.print_exc()
            messages.warning(self.request, u"导入异常！")
            return redirect(reverse('project_manage:project_list', args=("basic_info",)))

    def get_principal(self, row_str):
        """导入项目信息，筛选项目负责人信息
        :param row_str:
        :return:
        """
        user_obj = None
        try:
            customer_service_staff = Profile.get_user_by_username_or_first_name(row_str[13])  # 客服专员
            customer_service_charge = Profile.get_user_by_username_or_first_name(row_str[14])  # 客服主管
            outsource_director = Profile.get_user_by_username_or_first_name(row_str[15])  # 外包主管
            customer_service_director = Profile.get_user_by_username_or_first_name(row_str[16])  # 客服经理
            other_responsible_person = Profile.get_user_by_username_or_first_name(row_str[17])  # 其他负责人
            if customer_service_staff:
                user_obj = customer_service_staff
            elif customer_service_charge:
                user_obj = customer_service_charge
            elif outsource_director:
                user_obj = outsource_director
            elif customer_service_director:
                user_obj = customer_service_director
            elif other_responsible_person:
                user_obj = other_responsible_person
        except:
            traceback.print_exc()
        return user_obj

    def load_data(self, filepath):
        """执行导入
        :param filepath:导入文件路径
        :return:total："total": 总行数, "import": 成功导入数, "repeat": 已存在未导入数
        """
        try:
            # 读取模板
            data = xlrd.open_workbook(filepath)
            table = data.sheets()[0]  # 通过索引顺序获取,工作表
            nrows = table.nrows  # 行数
            # ncols = table.ncols  # 列数

            # 组装数据
            # colnames = table.row_values(0)  # 表头数据
            import_num = 0  # 导入数
            repeat_num = 0  # 重复导入
            no_project_num = 0  # 缺少项目编号

            total = nrows - 1
            messages_warning = ""
            for rowindex in xrange(1, nrows):  # 默认略过标题行,从第一行开始
                row = table.row_values(rowindex)
                if row:
                    try:
                        project_number = str(get_excel_int(row[0]))
                        if not project_number:
                            no_project_num += 1
                            continue

                        info_dict = dict(
                            number=project_number,
                            short_name=row[1],  # 项目简称
                            full_name=row[2],  # 项目名称
                            principal=self.get_principal(row),  # 项目负责人
                            department=Department.get_dept_by_name(row[4]),  # 负责部门

                            # 项目基础信息
                            customer=row[5],  # 客户名称
                            business_city=row[6],  # 业务城市
                            company_subject=CompanySubject.get_dict_item_by_name(row[7]),
                            # 公司主体
                            contract_type=ContractType.get_dict_item_by_name(row[8]),
                            # 合同类别
                            project_type=ProjectType.get_dict_item_by_name(row[9]),  # 项目类别
                            start_date=get_excel_date(row[10]),  # 起始日期
                            end_date=get_excel_date(row[11]),  # 终止日期
                            progress_state=ProgressState.get_dict_item_by_name(row[12]),
                            # 目前状态
                            customer_service_staff=Profile.get_user_by_username_or_first_name(
                                row[13]),  # 客服专员
                            customer_service_charge=Profile.get_user_by_username_or_first_name(
                                row[14]),  # 客服主管
                            outsource_director=Profile.get_user_by_username_or_first_name(
                                row[15]),
                            # 外包主管
                            customer_service_director=Profile.get_user_by_username_or_first_name(
                                row[16]),  # 客服经理
                            other_responsible_person=Profile.get_user_by_username_or_first_name(
                                row[17]),  # 其他负责人

                            # 社保福利
                            insured_place=row[18],  # 参保地
                            # social_security_type=SocialSecurityType.get_dict_item_by_name(row[19]),  # 社保险种，多选
                            social_security_account_type=SocialSecurityAccountType.get_dict_item_by_name(
                                row[20]),  # 社保账户类型
                            social_security_account_name=row[21],  # 社保账户名称
                            social_security_node_require=row[22],  # 社保节点要求
                            social_security_settlement_cycle=row[23],  # 社保结算周期
                            # business_insurance_company=BusinessInsuranceCompany.get_dict_item_by_name(row[24]),  # 商保公司，多选
                            business_insurance_settlement_cycle=Cycle.get_dict_item_by_name(
                                row[25]),  # 商保结算周期
                            business_insurance_standard=row[26],  # 商保收取标准
                            business_insurance_payment=row[27],  # 商保赔付额度
                            business_insurance_node_require=row[28],  # 商保节点要求
                            accumulation_fund_place_province=row[29],  # 公积金地点
                            proportion=row[30],  # 比例
                            radix=row[31],  # 基数

                            # 结算信息
                            service_standard=row[32],  # 服务费标准
                            service_cost_node_require=row[33],  # 服务费节点要求
                            residual_premium_cycle=Cycle.get_dict_item_by_name(row[34]),
                            # 残保金收取周期
                            residual_premium_place=row[35],  # 残保金收取地
                            settlement_report_day=row[36],  # 提供结算表时间
                            cost_arrival_day=row[37],  # 费用到账时间
                            wage_grant_day=row[38],  # 工资发放时间
                            wage_grant_type=WageGrantType.get_dict_item_by_name(row[39]),
                            # 工资发放方式
                            settlement_person=row[40],  # 结算对接人及联系方式
                            abnormal_settlement=row[41],  # 异常结算情况
                            wage_service_cost_settlement_cycle=row[42],  # 工资服务费结算周期
                            other_project=row[43],  # 其他需要我司代收代付项目

                            # 开票信息
                            invoice_type=InvoiceType.get_dict_item_by_name(row[44]),  # 发票类型
                            invoice_title=row[45],  # 发票抬头
                            invoice_mode=row[46],  # 开票方式
                            special_subject=row[47],  # 专票科目
                            special_cost=row[48],  # 专票费用内容
                            special_desc=row[49],  # 专票说明
                            general_subject=row[50],  # 普票科目
                            general_cost=row[51],  # 普票费用内容
                            general_desc=row[52],  # 普票说明
                            invoice_receiver=row[53],  # 发票接收人
                            invoice_phone=row[54],  # 电话
                            invoice_mail=row[55],  # 地址
                            fast_mail_desc=row[56],  # 快递说明
                            invoice_open_date=row[57],  # 发票开据时间
                            is_general_taxpayer=true_false_unformat_new(row[58]),  # 是否一般纳税人
                            taxpayer_identifier=row[59],  # 纳税人识别号
                            address=row[60],  # 地址
                            phone=row[61],  # 电话
                            bank=row[62],  # 开户行
                            account_number=row[63],  # 账号

                            # 销售信息
                            salesman=Profile.get_user_by_username_or_first_name(row[64]),
                            # 销售人员
                            sales_type=SalesType.get_dict_item_by_name(row[65]),  # 销售类型
                            dispatch_commission=get_excel_float(row[66]),  # 派遣提成标准
                            remark1=row[67],
                            outsourc_commission=get_excel_float(row[68]),  # 外包提成标准
                            remark2=row[69],
                            proxy_personnel_commission=get_excel_float(row[70]),  # 代理人事提成标准
                            remark3=row[71],
                            proxy_recruitment_commission=get_excel_float(row[72]),  # 代理招聘提成标准
                            remark4=row[73],
                            hourly_commission=get_excel_float(row[74]),  # 小时工提成标准
                            remark5=row[75],

                            # 招聘单价
                            recruit_difficulty=row[76],  # 招聘难度系数
                            jan=row[77],  # 1月
                            feb=row[78],  # 2月
                            mar=row[79],  # 3月
                            apr=row[80],  # 4月
                            may=row[81],  # 5月
                            jun=row[82],  # 6月
                            jul=row[83],  # 7月
                            aug=row[84],  # 8月
                            sep=row[85],  # 9 月
                            oct=row[86],  # 10月
                            nov=row[87],  # 11月
                            dec=row[88],  # 12月
                        )
                        # 信息已存在，没有创建新的，对已有数据做更新
                        project_obj = Project.objects.filter(full_name=row[2])
                        if project_obj.exists():
                            repeat_num += 1  # 重复导入数
                            project_obj.update(**info_dict)
                            continue

                        Project.objects.create(**info_dict)
                        import_num += 1
                    except:
                        messages_warning += str(rowindex) + ","
                        traceback.print_exc()

            os.remove(filepath)
            if messages_warning:
                messages.warning(self.request, messages_warning + u"行数据格式错误！")

            msg = u"导入成功，记录总数：%s条，" % total
            msg += u"新增：%s条，" % import_num
            msg += u"更新：%s条，" % repeat_num
            if no_project_num: msg += u"无项目编号(忽略)：%s条，" % no_project_num
            messages.success(self.request, msg)

            return redirect(reverse('project_manage:project_list', args=("basic_info",)))
        except:
            traceback.print_exc()
            messages.warning(self.request, u"导入异常！")
            return redirect(reverse('project_manage:project_list', args=("basic_info",)))

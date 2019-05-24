# coding=utf-8

from django import forms
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelChoiceField, TypedChoiceField
from django.utils import timezone

from modules.dict_table.models import *
from modules.dict_table.models import ArchiveType
from modules.project_manage.models import Project

GENDER_CHOICES = (
    ('M', u'男'),
    ('F', u'女'),
)

EDUCATION_CHOICES = (
    ('1', u'初中及以下'),
    ('2', u'高中及中专'),
    ('3', u'大专'),
    ('4', u'本科'),
    ('5', u'研究生及以上'),
)
REGISTERTYPE_CHOICES = (
    ('1', u'本地城镇'),
    ('2', u'本地农业'),
    ('3', u'外地城镇'),
    ('4', u'外地农业'),
)
CONTRACT_CHOICES = (
    ('1', u'实习'),
    ('2', u'临时'),
    ('3', u'劳务'),
    ('4', u'派遣'),
    ('5', u'外包'),
    ('6', u'代理'),
)

RECRUITMENTCHANNEL_CHOICES = (
    ('1', u'员工推荐'),
    ('2', u'传单'),
    ('3', u'职介'),
    ('4', u'招聘会'),
    ('5', u'主动求职'),
    ('6', u'网络'),
    ('7', u'熟人介绍'),
    ('8', u'其他'),
)

DIMISSION_PROCEDURE_CHOICES = (
    ('1', u'未办'),
    ('2', u'已办'),
    ('3', u'不全（员工手册未交）'),
    ('4', u'不全（员工手册已交）'),
)

NATION_CHOICES = (
    ('1', u'汉族'),
    ('2', u'蒙古族'),
    ('3', u'回族'),
    ('4', u'藏族'),
    ('5', u'维吾尔族'),
    ('6', u'苗族'),
    ('7', u'彝族'),
    ('8', u'壮族'),
    ('9', u'布依族'),
    ('10', u'朝鲜族'),
    ('11', u'满族'),
    ('12', u'侗族'),
    ('13', u'瑶族'),
    ('14', u'白族'),
    ('15', u'土家族'),
    ('16', u'哈尼族'),
    ('17', u'哈萨克族'),
    ('18', u'傣族'),
    ('19', u'黎族'),
    ('20', u'傈僳族'),
    ('21', u'佤族'),
    ('22', u'畲族'),
    ('23', u'高山族'),
    ('24', u'拉祜族'),
    ('25', u'水族'),
    ('26', u'东乡族'),
    ('27', u'纳西族'),
    ('28', u'景颇族'),
    ('29', u'柯尔克孜族'),
    ('30', u'土族'),
    ('31', u'达斡尔族'),
    ('32', u'仫佬族'),
    ('33', u'羌族'),
    ('34', u'布朗族'),
    ('35', u'撒拉族'),
    ('36', u'毛南族'),
    ('37', u'仡佬族'),
    ('38', u'锡伯族'),
    ('39', u'阿昌族'),
    ('40', u'普米族'),
    ('41', u'塔吉克族'),
    ('42', u'怒族'),
    ('43', u'乌孜别克族'),
    ('44', u'俄罗斯族'),
    ('45', u'鄂温克族'),
    ('46', u'德昂族'),
    ('47', u'保安族'),
    ('48', u'裕固族'),
    ('49', u'京族'),
    ('50', u'塔塔尔族'),
    ('51', u'独龙族'),
    ('52', u'鄂伦春族'),
    ('53', u'赫哲族'),
    ('54', u'门巴族'),
    ('55', u'珞巴族'),
    ('56', u'基诺族'),
)

IS_WORK = (
    ('1', u'在职'),
    ('2', u'离职'),
    ('3', u'调出'),
)


class Employee(models.Model):
    """员工信息 """

    # 员工信息与临时工信息，公用字段
    name = models.CharField(u"姓名", max_length=100, db_index=True)
    sex = models.CharField(u"性别", max_length=2, choices=GENDER_CHOICES, blank=True, help_text=u"选填，可由身份证号计算")
    identity_card_number = models.CharField(u"身份证号", max_length=18, db_index=True)
    project_name = models.ForeignKey(Project, verbose_name=u"项目名称", blank=True, null=True, on_delete=models.SET_NULL,
                                     related_name="employees", db_index=True)
    recruitment_attache = models.ForeignKey(User, blank=True, null=True, verbose_name=u"招聘人员",
                                            on_delete=models.SET_NULL,
                                            related_name="user_recruitment_attache")
    is_temporary = models.BooleanField(u"是否临时工", default=False, blank=True)  # 页面不做选择，后台赋值，默认不是临时工
    phone_number = models.CharField(u"联系电话", max_length=100, blank=True)

    # 员工信息字段
    status = models.CharField(u"目前状态", max_length=100, choices=IS_WORK, default="1", db_index=True)
    salary_card_number = models.CharField(u"银行卡号", max_length=100, blank=True)
    job_dept = models.CharField(u"部门", max_length=100, blank=True)
    bank_account = models.CharField(u"开户银行", max_length=100, blank=True)
    position = models.CharField(u"职务", max_length=100, blank=True)
    nation = models.CharField(u"民族", max_length=10, choices=NATION_CHOICES, blank=True)
    education = models.CharField(u"学历", max_length=10, choices=EDUCATION_CHOICES, blank=True)
    birthday = models.DateField(u"出生年月", blank=True, null=True)
    age = models.PositiveIntegerField(u"员工年龄", blank=True, default=0, help_text=u"选填，可由身份证号计算")
    register_address = models.TextField(u"户口所在地", blank=True)
    register_postcode = models.CharField(u"户口邮编", max_length=20, blank=True)
    register_type = models.CharField(u"户口性质", max_length=20, choices=REGISTERTYPE_CHOICES, blank=True)
    work_address = models.CharField(u"工作地", max_length=256, blank=True)
    insured_place = models.CharField(u"社保地", max_length=256, blank=True)
    person_type = models.ForeignKey(ContractType, blank=True, null=True, on_delete=models.SET_NULL,
                                    verbose_name=u"人员属性", db_index=True)
    contract_type = models.CharField(u"合同属性", max_length=10, choices=CONTRACT_CHOICES, blank=True, db_index=True)
    contract_subject = models.ForeignKey(CompanySubject, blank=True, null=True, on_delete=models.SET_NULL,
                                         verbose_name=u"合同主体")
    entry_date = models.DateField(u"入职日期", default=timezone.now, null=True, blank=True)
    call_out_time = models.DateField(verbose_name=u'调出时间', blank=True, null=True)
    into_time = models.DateField(verbose_name=u'转入时间', blank=True, null=True)
    social_insurance_increase_date = models.DateField(u"#DIV/0!01+", blank=True, null=True)
    social_security_payment_card = models.CharField(u"社保支付卡", max_length=255, blank=True, null=True)
    use_bank = models.CharField(u"开户银行", max_length=255, blank=True, null=True)
    business_insurance_increase_date = models.DateField(u"#DIV/0!02+", blank=True, null=True)
    provident_fund_increase_date = models.DateField(u"公积金增员日期", blank=True, null=True)
    contract_begin_date = models.DateField(u"合同开始日期", blank=True, null=True)
    probation_period = models.PositiveIntegerField(u"试用期限（月）", blank=True, null=True)
    contract_period = models.PositiveIntegerField(u"合同期限（月）", blank=True, null=True)
    probation_end_date = models.DateField(u"试用到期日期", blank=True, null=True)
    contract_end_date = models.DateField(u"合同到期日期", blank=True, null=True)
    contract_renew_times = models.PositiveIntegerField(u"合同续签次数", blank=True, null=True)
    departure_date = models.DateField(u"离职日期", blank=True, null=True)
    departure_procedure = models.CharField(u"离职手续", max_length=10, choices=DIMISSION_PROCEDURE_CHOICES, blank=True)
    departure_cause = models.CharField(u"离职原因", max_length=200, blank=True)
    social_insurance_reduce_date = models.DateField(u"#DIV/0!01-", blank=True, null=True)
    business_insurance_reduce_date = models.DateField(u"#DIV/0!02-", blank=True, null=True)
    provident_fund_reduce_date = models.DateField(u"公积金减员日期", blank=True, null=True)
    contact_person = models.CharField(u"紧急联系人", max_length=100, blank=True)
    contact_relationship = models.CharField(u"与联系人关系", max_length=100, blank=True)
    contact_person_phone = models.CharField(u"紧急联系人电话", max_length=100, blank=True)
    recruitment_channel = models.CharField(u"招聘渠道", max_length=10, choices=RECRUITMENTCHANNEL_CHOICES, blank=True)

    # 临时工信息字段,temporary
    start_work_date = models.DateField(u"开始工作日", blank=True, null=True)
    end_work_date = models.DateField(u"结束工作日", blank=True, null=True)
    work_days = models.PositiveIntegerField(u"工作天数", blank=True, null=True)
    hours = models.PositiveIntegerField(u"小时数", blank=True, null=True)
    amount_of_payment = models.PositiveIntegerField(u"发放金额", blank=True, null=True)
    release_user = models.ForeignKey(User, blank=True, null=True, verbose_name=u"发放人", on_delete=models.SET_NULL,
                                     related_name="release_user")
    release_time = models.DateField(u"发放时间", blank=True, null=True)
    remark1 = models.CharField(u"备注1", max_length=256, blank=True)
    interviewer_information = models.TextField(u"面试人员信息", blank=True, null=True)

    # 预留字段
    remark2 = models.CharField(u"备注2", max_length=256, blank=True)
    remark3 = models.CharField(u"备注3", max_length=256, blank=True)
    remark4 = models.CharField(u"备注4", max_length=256, blank=True)
    remark5 = models.CharField(u"备注5", max_length=256, blank=True)
    create_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True, blank=True, null=True, db_index=True)
    modified = models.DateTimeField(verbose_name=u'修改时间', auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"员工信息"
        # unique_together = (("name", "identity_card_number"),)  # 不重复的字段组合
        ordering = ['-id']  # id倒叙
        index_together = ["project_name", "name", "identity_card_number", "person_type", "contract_type", "status",
                          "create_time"]
        permissions = (
            ("browse_employee", u"浏览 员工信息"),
            ("export_employee", u"导出 员工信息"),

            ("add_temporary", u"增加 临时工信息"),
            ("delete_temporary", u"删除 临时工信息"),
            ("browse_temporary", u"浏览 临时工信息"),
            ("change_temporary", u"修改 临时工信息"),
            ("export_temporary", u"导出 临时工信息"),
            ("download_all_employee", u"下载 全部员工"),
            ("leave_employee", u"查看-导出 离职员工"),
        )


# 自定义验证
class EmployeeForm(forms.ModelForm):
    # def clean(self):
    # 	cleaned_data = super(EmployeeForm, self).clean()
    # 	# 校验身份证号，有在职员工有相同身份证号，不能同时存在，阻止录入，有相同身份证已离职可录入
    # 	identity_card_number = self.cleaned_data['identity_card_number']
    # 	status = self.cleaned_data['status']
    # 	name = self.cleaned_data['name']
    # 	user_obj = Employee.objects.filter(identity_card_number=identity_card_number, status="1").exclude(name=name)
    # 	if user_obj.exists() and status == "1":
    # 		# 身份证相同并在职，不予录入
    # 		self.add_error('identity_card_number', u"相同身份证号并且在职的员工信息已经存在!")

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, ModelChoiceField) or isinstance(field, TypedChoiceField):
                field.widget.attrs.update({'class': 'select2'})

    class Meta:
        model = Employee
        fields = [
            "name", "sex", "identity_card_number", "project_name",
            "recruitment_attache", "status", "salary_card_number", "job_dept", "bank_account", "position",
            "nation", "education", "birthday", "age", "register_address", "register_postcode",
            "register_type", "work_address", "insured_place", "person_type", "contract_type",
            "contract_subject", "entry_date", "call_out_time", "into_time", "social_insurance_increase_date",
            "social_security_payment_card", "use_bank", "business_insurance_increase_date",
            "provident_fund_increase_date", "contract_begin_date", "probation_period",
            "contract_period", "probation_end_date", "contract_end_date", "contract_renew_times",
            "departure_date", "departure_procedure", "departure_cause",
            "social_insurance_reduce_date", "business_insurance_reduce_date",
            "provident_fund_reduce_date", "phone_number", "contact_person",
            "contact_relationship", "contact_person_phone", "recruitment_channel"
        ]


class TemporaryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TemporaryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, ModelChoiceField) or isinstance(field, TypedChoiceField):
                field.widget.attrs.update({'class': 'select2'})

    class Meta:
        model = Employee
        fields = [
            "name", "sex", "identity_card_number", "project_name",
            "recruitment_attache", "phone_number", "start_work_date", "end_work_date", "work_days", "hours",
            "amount_of_payment", "release_user", "release_time", "remark1",
        ]


ISSUE_STATUS = (
    ('1', u'是'),
    ('2', u'否'),
)


class Archive(models.Model):
    """ 员工管理-档案信息 """

    employee_id = models.ForeignKey(Employee, verbose_name=u"员工信息", related_name="archives", db_index=True)
    number = models.CharField(u"档案编号", max_length=100, blank=True, null=True)
    type = models.ForeignKey(ArchiveType, verbose_name=u"档案类型", blank=True, null=True)
    issue = models.CharField(u"是否发出", max_length=2, blank=True, choices=ISSUE_STATUS, default="2", db_index=True)
    receive = models.CharField(u"是否收到", max_length=2, blank=True, choices=ISSUE_STATUS, default="2", db_index=True)
    bank_copy = models.PositiveIntegerField(u"银行卡复印件", blank=True, null=True)
    id_copy = models.PositiveIntegerField(u"身份证复印件", blank=True, null=True)
    booklet_copy = models.PositiveIntegerField(u"户口本复印件", blank=True, null=True)
    photo = models.PositiveIntegerField(u"照片", blank=True, null=True)
    contract = models.PositiveIntegerField(u"合同", blank=True, null=True)
    resume = models.PositiveIntegerField(u"员工简历", blank=True, null=True)
    family_contract = models.PositiveIntegerField(u"计划生育合同", blank=True, null=True)
    entry_conditions = models.PositiveIntegerField(u"入职须知", blank=True, null=True)
    breach_book = models.PositiveIntegerField(u"违约责任书", blank=True, null=True)
    salary_confirmation = models.PositiveIntegerField(u"薪资确认单", blank=True, null=True)
    health_certificate = models.PositiveIntegerField(u"健康证明", blank=True, null=True)
    his_resignation = models.PositiveIntegerField(u"离职单", blank=True, null=True)
    labor_relations_prove = models.PositiveIntegerField(u"解除劳动关系证明", blank=True, null=True)
    register_letter = models.DateField(u"报到函发出时间", blank=True, null=True)
    relieve_letter = models.DateField(u"解除函发出时间", blank=True, null=True)
    remark1 = models.CharField(u"备注1", max_length=256, blank=True)
    remark2 = models.CharField(u"备注2", max_length=256, blank=True)
    remark3 = models.CharField(u"备注3", max_length=256, blank=True)
    remark4 = models.CharField(u"备注4", max_length=256, blank=True)
    remark5 = models.CharField(u"备注5", max_length=256, blank=True)

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = u"员工档案信息"
        ordering = ['-id']  # id倒叙
        index_together = ["employee_id", "issue", "receive"]
        permissions = (
            ("browse_archive", u"浏览 员工档案信息"),
        )


@receiver(post_save, sender=Employee)  # 信号的名字，发送者
def add_employee_event(sender, instance, **kwargs):  # 回调函数，收到信号后的操作
    """增加员工信息同时增加档案信息
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    from modules.social_security.increase_info.models import Increase
    from modules.social_security.reduction_info.models import Reduction
    try:
        is_temporary = instance.is_temporary
        if not is_temporary:  # 判断是否临时工，否，增加档案信息
            Archive.objects.get_or_create(employee_id=instance)  # 增加档案信息

            social_insurance_increase_date = instance.social_insurance_increase_date  # 社保增员日期
            if social_insurance_increase_date:
                Increase.objects.get_or_create(emplyid=instance)  # 如果有增员时间，增加增员信息

            social_insurance_reduce_date = instance.social_insurance_reduce_date  # 社保减员日期
            if social_insurance_reduce_date:
                Reduction.objects.get_or_create(emplyid=instance)  # 如果有减员时间，增加减员信息
    except:
        traceback.print_exc()

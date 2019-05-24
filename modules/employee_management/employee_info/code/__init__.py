# coding=utf-8
employee_head_list = [u"序号", u'姓名（必填）', u'服务部门', u'身份证号（必填）', u'目前状态(在职/离职)', u'项目名称（必填）', u'银行卡号', u'开户银行',
                      u'部门', u'职务', u'性别(男/女)', u'民族', u'学历', u'出生年月(2016-01-01)', u'员工年龄', u'户口所在地',
                      u'户口邮编', u'户口性质', u'工作地', u'社保地', u'人员属性', u'合同属性', u'合同主体',
                      u'入职日期(2016-01-01)', u'调出时间(2016-01-01)', u'转入时间(2016-01-01)', u'#DIV/0!01+', u"社保支付卡",
                      u"开户银行", u'#DIV/0!02+',
                      u'公积金增员日期(2016-01-01)', u'合同开始日期(2016-01-01)', u'试用期限', u'合同期限', u'试用到期日期(2016-01-01)',
                      u'合同到期日期(2016-01-01)', u'合同续签次数', u'离职日期(2016-01-01)', u'离职手续', u'离职原因',
                      u'#DIV/0!01-', u'#DIV/0!02-', u'公积金减员日期(2016-01-01)', u'联系电话', u'紧急联系人',
                      u'与联系人关系', u'紧急联系人电话', u'招聘渠道', u'招聘人员', u'客服专员', u'客服主管',
                      u'外包主管', u'客服经理', u'其他负责人', u"面试人员信息", u"创建时间", u"修改时间"]
employee_field_list = ["index", "name", "attribution_dept", "identity_card_number", "status", "project_name",
                       "salary_card_number", "bank_account", "job_dept", "position", "sex", "nation",
                       "education",
                       "birthday", "age", "register_address", "register_postcode", "register_type",
                       "work_address", "insured_place", "person_type", "contract_type",
                       "contract_subject",
                       "entry_date", "call_out_time", "into_time", "social_insurance_increase_date",
                       "social_security_payment_card",
                       "use_bank",
                       "business_insurance_increase_date", "provident_fund_increase_date",
                       "contract_begin_date",
                       "probation_period", "contract_period", "probation_end_date", "contract_end_date",
                       "contract_renew_times", "departure_date", "departure_procedure",
                       "departure_cause",
                       "social_insurance_reduce_date", "business_insurance_reduce_date",
                       "provident_fund_reduce_date", "phone_number", "contact_person",
                       "contact_relationship",
                       "contact_person_phone", "recruitment_channel", "recruitment_attache",
                       "customer_service_staff", "customer_service_charge", "outsource_director",
                       "customer_service_director", "other_responsible_person", "interviewer_information",
                       "create_time", "modified"]

temporary_head_list = [u"序号", u"姓名", u"性别", u"身份证号", u"项目名称", u"服务部门", u"招聘人员", u"联系电话", u"开始工作日",
                       u"结束工作日", u"工作天数", u"小时数", u"发放金额", u"发放人", u"发放时间", u"备注1", u"创建时间", u"修改时间"]
temporary_field_list = ["index", "name", "sex", "identity_card_number", "project_name", "attribution_dept",
                        "recruitment_attache", "phone_number", "start_work_date",
                        "end_work_date", "work_days", "hours", "amount_of_payment", "release_user",
                        "release_time", "remark1", "create_time", "modified"]

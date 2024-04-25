{
  'name': 'Jorels Api Connection by Grupo Quanam Colombia',
  'version': '1.0',
  'description': 'This module connect the Jorels Api to Payroll_Quanamco Module',
  'summary': '',
  'author': 'Grupo Quanam Colombia SAS',
  'website': 'https://grupoquanam.com.co',
  'license': 'LGPL-3',
  'category': 'Jores, Api',
  'depends': [
    'payroll_quanamco',
    'payroll',
    'account',
    'mail',
  ],
  'data': [
    # Security
    'security/ir.model.access.csv',
    'report/hr_payslip_edi_report.xml',
    'views/action_menus.xml',
    'views/edi_gen_views.xml',
    'views/hr_contract_views.xml',
    'views/hr_payslip_edi_views.xml',
    'views/hr_payslip_views.xml',
    'views/hr_salary_rule_views.xml',
    'views/res_config_settings_views.xml',
  ],
  # 'demo': [
  #   ''
  # ],
  'auto_install': False,
  'application': False,
  'assets': {
    
  }
}
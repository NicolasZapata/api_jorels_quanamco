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
    'account',
    'mail',
  ],
  'data': [
    # Security
    'security/ir.model.access.csv',
  ],
  # 'demo': [
  #   ''
  # ],
  'auto_install': False,
  'application': False,
  'assets': {
    
  }
}
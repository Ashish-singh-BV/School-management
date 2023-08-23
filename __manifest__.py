{
    'name': 'School Management',
    'version': '1.0',
    'sequence' : -99,
    'description': """
        This Module help you to Manage your school data with
        proper manner and all requirment is here for school related work
        """,
    'category': 'Apps',
    'author': 'Ashish',
    'license' : 'LGPL-3',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/email_temp.xml',
        'wizard/del_stu_rec.xml',
        'views/stu_regi_view.xml',
        'views/cron_stu_regi.xml',
        'views/teacher_view.xml',
        'views/res_config_settings_views.xml',
        'reports/student_report.xml',
        'reports/report.xml',
        'views/views_menu.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'images': [
        'static/description/icon.png',
        # 'static/description/potrait.png'
        ],
    'application': True,
    'demo': True,
}

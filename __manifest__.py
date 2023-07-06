{
    'name': 'School Management',
    'version': '1.0',
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
        'views/stu_regi_view.xml',
        'views/teacher_view.xml',
        'views/views_menu.xml',
        'data/demo_data.xml'
    ],
    'application': True,
    'demo': True,
}

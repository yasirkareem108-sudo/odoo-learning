{
    'name': 'Library Management',
    'version': '1.0',
    'category': 'Library',
    'summary': 'Manage books, students, and borrowing in a library system',
    'author': 'Yasir Kareem',
    'depends': ['base', 'web'],
    'data': [
        # 🔐 Security
        'security/library_security.xml',
        'security/ir.model.access.csv',

        # 🧩 Wizard (load first)
        'wizard/return_book_wizard_view.xml',
         'wizard/library_books_report_wizard.xml',
        # 📊 Views
        'views/book_views.xml',
        'views/borrow_views.xml',
        'views/library_menu.xml',
        'views/student_views.xml',
        'views/book_kanban.xml',
        'views/res_config_settings_views.xml',

        # 📝 Reports
        'report/library_book_report_template.xml',
        #'report/library_borrow_report.xml',

        # 📦 Demo Data
         'data/cron.xml',
        'data/demo_data.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'library_management/static/src/js/library.js',
            'library_management/static/src/xml/library.xml',
        ],
    },
    'application': True,
    'installable': True,
}

{
    'name' : "App One",
    'author': "Awadh M Bin Wahlan", 
    'category': '',
    'version' : '17.0.0.1.0',
    'depends': ['base', 'sale', 'account', 'mail'],

    "data": [
        "security/students_security.xml",
        "security/ir.model.access.csv",
        "data/sequence.xml",
        "views/base_menue.xml",
        "views/students_views.xml",
        "views/students_history_views.xml",
        "views/country_views.xml",
        "views/Subject_views.xml",
        "views/sale_views.xml",
        "views/account_move_views.xml",    
        "wizard/change_state_wizard_views.xml",
        "reports/students_report.xml",        
    ],   
    "assets": {
        'web.assets_backend': [
            'app_one/static/src/css/style.css',
            'app_one/static/src/components/listView/css/listView.css',
            'app_one/static/src/components/listView/js/listView.js',
            'app_one/static/src/components/listView/xml/listView.xml',
            ],
        'web.report_assets_common' : ['app_one/static/src/css/font.css']
    } ,
    'application': True,     
}

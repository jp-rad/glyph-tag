{
    'name': "joo_mjrengo",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    # fonts, css, js
    'assets': {
        'web.assets_backend': [
            'joo_mjrengo/static/src/fonts/ipamjm.ttf',
            'joo_mjrengo/static/src/fonts/DWPIMincho.ttf',
            'joo_mjrengo/static/src/fonts/DWPIexMincho.ttf',

            'joo_mjrengo/static/src/css/fonts.css',
            'joo_mjrengo/static/src/js/font_loader.js',
        ],
    }

}


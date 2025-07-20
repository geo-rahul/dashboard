# -*- coding: utf-8 -*-
{
    'name': 'Dynamic Dashboard Builder',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Visual dashboard builder for any Odoo model',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        # 'views/dashboard_dashboard_views.xml',
        'views/dashboard_client_action.xml',
        'views/dashboard_item_views.xml',
    ],
    'assets': {
        'web.assets_backend': [

            # Library
            'dynamic_dashboard_builder/static/lib/js/gridstack-all.js',
            'dynamic_dashboard_builder/static/lib/css/gridstack.min.css',

            'dynamic_dashboard_builder/static/src/js/dashboard_app.js',
            'dynamic_dashboard_builder/static/src/js/dashboard_item_wizard.js',
            'dynamic_dashboard_builder/static/src/xml/dashboard_templates.xml',
            'dynamic_dashboard_builder/static/src/xml/dashboard_item_wizard_template.xml',
            'dynamic_dashboard_builder/static/src/xml/dashboard_modal.xml',
            'dynamic_dashboard_builder/static/src/css/dashboard.css',
            'dynamic_dashboard_builder/static/src/css/dashboard_item.css',
        ],
    },
    'installable': True,
    'application': True,
}

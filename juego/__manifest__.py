# -*- coding: utf-8 -*-
{
    'name': "Juego",

    'summary': """
        Módulo para SGE 2021/2022 IES Lluis Simarro
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Pascual Rodríguez",
    'website': "http://www.pascualgorrita.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Videogame',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],
    'depends': ['base_import'],
    

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
        'demo/npcs.xml',
        'demo/bunkers.xml',
    ],

    'qweb': [
        "static/src/xml/button_template.xml",
    ],
}

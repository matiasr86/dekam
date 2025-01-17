# -*- coding: utf-8 -*-
{
    'name': "Dekam",

    'summary': """
        Aplicación para gestion de cotizaciones y despieces de proyectos""",

    'description': """
        Dekam permite cotizar un proyecto conociendo al detalle costos y rentabilidad. Tambien 
        permite obtener rapidamente el despiece del proyecto.
    """,

    'author': "Matias Marinelli",
    'website': "https://www.devcode73.com.ar",
    'icon_image': ['static/description/icon.png'],
    'installable': True,
    'application': True,  # Indica que es una aplicación

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/dekam_workforce.xml',
        'views/dekam_background.xml',
        'views/dekam_box.xml',
        'views/dekam_line.xml',
        'views/dekam_url.xml',
        'views/dekam_material.xml',
        'views/dekam_cut.xml',
        'views/dekam_edge.xml',
        'views/dekam_accessory.xml',
        'views/dekam_module.xml',
        'views/dekam_door.xml',
        'views/menu.xml',
    ],
}

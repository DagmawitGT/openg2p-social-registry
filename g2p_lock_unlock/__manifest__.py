# Part of OpenG2P Social Registry. See LICENSE file for full copyright and licensing details.
{
    "name": "OpenG2P Lock Unlock",
    "category": "G2P",
    "version": "17.0.1.0.0",
    "sequence": 1,
    "author": "OpenG2P",
    "website": "https://openg2p.org",
    "license": "Other OSI approved licence",
    "depends": [
        "base",
        "g2p_registry_group",
        "g2p_registry_individual",
        "g2p_registry_membership",
    ],
    "external_dependencies": {},
    "data": [
        'security/registry_groups.xml',
        'security/ir.model.access.csv',
        'views/no_of_edit_views.xml',
        'views/request_views.xml',
         "wizard/request_wiz_view.xml",
         "views/edit_request.xml",
         # "data/edit_request_mail_template.xml",
         # "data/activity.xml",
        'views/g2p_lock_social_registry.xml',
    ],
     "assets": {"web.assets_backend": [
    # 'g2p_lock_unlock/static/src/js/g2p_profile_lock.js'
    ]},
    "demo": [],
    "images": [],
    "application": True,
    "installable": True,
    "auto_install": False,
}

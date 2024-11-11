# Part of OpenG2P Registry. See LICENSE file for full copyright and licensing details.
{
    "name": "OpenG2P Social Registry: Dashboard",
    "category": "G2P",
    "version": "17.0.0.0.0",
    "sequence": 1,
    "author": "OpenG2P",
    "website": "https://openg2p.org",
    "license": "LGPL-3",
    "depends": ["g2p_social_registry"],
    "external_dependencies": {},
    "data": ["data/cron_job.xml", "views/menu.xml"],
    "assets": {
        "web.assets_backend": [
            "https://cdn.jsdelivr.net/npm/chart.js",
            "g2p_social_registry_dashboard/static/src/js/dashboard.js",
            "g2p_social_registry_dashboard/static/src/xml/dashboard.xml",
            "g2p_social_registry_dashboard/static/src/scss/dashboard.scss",
        ],
    },
    "demo": [],
    "images": [],
    "application": True,
    "installable": True,
    "auto_install": False,
    "post_init_hook": "init_materialized_view",
    "uninstall_hook": "drop_materialized_view",
}

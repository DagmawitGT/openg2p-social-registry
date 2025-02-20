{
    "name": "Leaflet Map View",
    "version": "17.0.0.0.0",
    "website": "https://openg2p.org",
    "category": "Hidden",
    "license": "LGPL-3",
    "installable": True,
    "depends": ["base", "web", "g2p_registry_individual"],
    "data": [
        "security/ir.model.access.csv",
        "views/osm_config.xml",
        "views/show_on_map.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "leaflet_map/static/src/*",
        ]
    },
    "author": "OpenG2P",
}

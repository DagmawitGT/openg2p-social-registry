{
    "name": "Leaflet Map View",
    "version": "17.0.0.0.0",
    "author": "OpenG2P",
    "website": "https://openg2p.org",
    "license": "LGPL-3",
    "category": "Hidden",
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
}

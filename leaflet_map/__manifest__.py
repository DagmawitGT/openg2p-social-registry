{
    "name": "Leaflet Map View",
    "description": "Leaflet Map View",
    "version": "1.0",
    "category": "Hidden",
    "installable": True,
    "depends": ["base", "web","g2p_registry_individual"],
    'data': [
        'security/ir.model.access.csv',
        'views/osm_config.xml',
        'views/show_on_map.xml',

    ],
    "assets": {
        "web.assets_backend": [
            "leaflet_map/static/src/*",
        ]
    },
}
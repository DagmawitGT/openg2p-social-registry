/** @odoo-module */

import { Component, onWillStart, useRef, onMounted } from "@odoo/owl";
import { loadJS, loadCSS } from "@web/core/assets";

export class LeafletMapRenderer extends Component {
    static template = "leaflet_map.MapRenderer";
    static props = {
        polygonCoords: { type: Array, optional: true, default: [] },
    };

    setup() {
        this.root = useRef("map");
        this.config = {
            tile_server_url: "https://tile.openstreetmap.org/{z}/{x}/{y}.png", // Default fallback
        };

        // Fetch only the tile server URL from Odoo config
        onWillStart(async () => {
            try {
                const response = await fetch("/osm/config/get", {
                    method: "GET",
                    headers: { "Content-Type": "application/json" },
                });

                if (response.ok) {
                    const data = await response.json();
                    this.config.tile_server_url = data.tile_server_url || this.config.tile_server_url;
                } else {
                    console.warn("Failed to fetch tile server URL, using default.");
                }

                // ✅ Ensure Leaflet JS & CSS are loaded from local static files
                await loadCSS("/leaflet_map/static/lib/leaflet/leaflet.css");
                await loadJS("/leaflet_map/static/lib/leaflet/leaflet.js");
            } catch (error) {
                console.error("Error loading OSM config:", error);
            }
        });

        onMounted(() => {
            if (!this.root.el) return;

            // ✅ Check if Leaflet (L) is loaded before using it
            if (typeof L === "undefined") {
                console.error("Leaflet JS is not loaded.");
                return;
            }

            this.map = L.map(this.root.el).setView([9.145, 40.489], 12);

            // Use the tile server from Odoo config
            L.tileLayer(this.config.tile_server_url, {
                maxZoom: 19,
                attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
            }).addTo(this.map);

            // Add polygon if coordinates exist
//            if (this.props.polygonCoords?.length) {
//                L.polygon(this.props.polygonCoords).addTo(this.map);
//            } else {
//                console.warn("No polygon coordinates received.");
//            }
        });
    }
}

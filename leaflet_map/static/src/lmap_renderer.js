/* eslint-disable  */
/** @odoo-module */

import {Component, onWillStart, useRef, onMounted} from "@odoo/owl";
import {loadJS, loadCSS} from "@web/core/assets";

export class LeafletMapRenderer extends Component {
    static template = "leaflet_map.MapRenderer";
    static props = {
        polygonCoords: {type: Array, optional: true, default: []},
        partnerLatitude: {type: Number, optional: true},
        partnerLongitude: {type: Number, optional: true},
    };

    setup() {
        console.log("Renderer Props:", this.props);
        this.root = useRef("map");
        this.config = {
            tile_server_url: "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        };

        onWillStart(async () => {
            try {
                const response = await fetch("/osm/config/get", {
                    method: "GET",
                    headers: {"Content-Type": "application/json"},
                });

                if (response.ok) {
                    const data = await response.json();
                    this.config.tile_server_url = data.tile_server_url || this.config.tile_server_url;
                } else {
                    console.warn("Failed to fetch tile server URL, using default.");
                }

                await loadCSS("/leaflet_map/static/lib/leaflet/leaflet.css");
                await loadJS("/leaflet_map/static/lib/leaflet/leaflet.js");
            } catch (error) {
                console.error("Error loading OSM config:", error);
            }
        });

        onMounted(() => {
            if (!this.root.el) return;

            if (typeof L === "undefined") {
                console.error("Leaflet JS is not loaded.");
                return;
            }

            let mapCenter = [9.145, 40.489]; // Default center
            let zoomLevel = 12;

            if (this.props.partnerLatitude !== null && this.props.partnerLongitude !== null) {
                mapCenter = [this.props.partnerLatitude, this.props.partnerLongitude];
            }

            this.map = L.map(this.root.el).setView(mapCenter, zoomLevel);

            L.tileLayer(this.config.tile_server_url, {
                maxZoom: 19,
                attribution: "&copy; OpenStreetMap contributors",
            }).addTo(this.map);

            // ✅ Add Polygon and Automatically Adjust Zoom
            if (this.props.polygonCoords?.length) {
                const polygon = L.polygon(this.props.polygonCoords).addTo(this.map);
                this.map.fitBounds(polygon.getBounds()); // Auto zoom to fit polygon
            } else {
                console.warn("No polygon coordinates received.");
            }

            // ✅ Add Marker for Partner Location
            if (this.props.partnerLatitude !== null && this.props.partnerLongitude !== null) {
                L.marker([this.props.partnerLatitude, this.props.partnerLongitude])
                    .addTo(this.map)
                    .bindPopup("Data Collection Point")
                    .openPopup();
            }
        });
    }
}

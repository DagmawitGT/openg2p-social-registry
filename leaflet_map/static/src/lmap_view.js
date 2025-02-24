/* eslint-disable  */
/** @odoo-module */

import {LeafletMapController} from "./lmap_controller";
import {registry} from "@web/core/registry";

const leafletMapView = {
    type: "lmap",
    display_name: "Leaflet Map",
    icon: "fa fa-map-marker",
    multiRecord: true,
    Controller: LeafletMapController,
};

registry.category("views").add("lmap", leafletMapView);

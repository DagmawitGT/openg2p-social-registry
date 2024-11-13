/** @odoo-module */

import {Component} from "@odoo/owl";

export class KpiComponent extends Component {}

KpiComponent.template = "g2p_social_registry_dashboard.KpiTemplate";

KpiComponent.props = {
    title: {type: String, optional: true},
    data: {type: [String, Number], optional: true},
    size: {type: String, optional: true},
};

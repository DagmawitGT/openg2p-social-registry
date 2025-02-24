from odoo import fields, models


class MapView(models.Model):
    _name = "map.view"
    _description = "Map View"

    partner_id = fields.Many2one("res.partner")


class ResPartnerMap(models.Model):
    _inherit = "res.partner"

    map_view_ids = fields.One2many("map.view", "partner_id", string="Map View")

    def show_map(self):
        self.ensure_one()

        action = {
            "type": "ir.actions.act_window",
            "name": "Partner Map",
            "res_model": "map.view",
            "view_mode": "lmap",
            "view_id": self.env.ref("leaflet_map.action_g2p_partner_map_view").id,
            "target": "new",
            "context": {
                "partner_latitiude": self.partner_latitude,
                "partner_longitude": self.partner_longitude,
            },
        }
        return action

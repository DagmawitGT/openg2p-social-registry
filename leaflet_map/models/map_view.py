from odoo import fields, models


class MapView(models.Model):
    _name = "map.view"
    _description = "Map View"

    partner_id = fields.Many2one("res.partner")


class ResPartnerMap(models.Model):
    _inherit = "res.partner"

    map_view_ids = fields.One2many("map.view", "partner_id", string="Map View")

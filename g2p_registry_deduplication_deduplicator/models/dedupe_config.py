import os

from odoo import api, fields, models


class G2PDedupeConfigField(models.Model):
    _name = "g2p.registry.deduplication.deduplicator.config.field"
    _description = "Deduplicator Config Field"

    name = fields.Char(required=True)
    fuzziness = fields.Char()
    weightage = fields.Float()
    exact = fields.Boolean()

    dedupe_config_id = fields.Many2one(
        "g2p.registry.deduplication.deduplicator.config", ondelete="cascade", required=True
    )


class G2PDedupeConfig(models.Model):
    _name = "g2p.registry.deduplication.deduplicator.config"
    _description = "Deduplicator Config"

    name = fields.Char(required=True)

    config_name = fields.Char(required=True, default="default")

    dedupe_service_base_url = fields.Char(
        default=os.getenv(
            "DEDUPLICATOR_SERVICE_BASE_URL", "http://socialregistry-deduplicator-openg2p-deduplicator"
        )
    )

    config_index_name = fields.Char(default="res_partner")
    config_fields = fields.One2many(
        "g2p.registry.deduplication.deduplicator.config.field", "dedupe_config_id"
    )
    config_score_threshold = fields.Float()

    active = fields.Boolean(required=True)

    _sql_constraints = [
        ("unique_config_name", "unique (config_name)", "Dedupe Config with same config name already exists !")
    ]

    @api.model
    def get_configured_deduplicator(self):
        dedupe_config_id = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("g2p_registry_deduplication_deduplicator.deduplicator_config_id", None)
        )
        return self.browse(int(dedupe_config_id)) if dedupe_config_id else None

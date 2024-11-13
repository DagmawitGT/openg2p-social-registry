# Part of OpenG2P. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class ResPartnerDashboard(models.Model):
    _inherit = "res.partner"

    @api.model
    def get_dashboard_data(self):
        """Fetch data from materialized view and prepare it for charts."""
        company_id = self.env.company.id

        query = """
            SELECT total_registrants, gender_spec, age_distribution
            FROM g2p_sr_dashboard_data
            WHERE company_id = %s
        """
        self.env.cr.execute(query, (company_id,))
        result = self.env.cr.fetchone()

        total_registrants, gender_spec, age_distribution = result

        return {
            "total_individuals": total_registrants.get("total_individuals", 0),
            "total_groups": total_registrants.get("total_groups", 0),
            "gender_distribution": gender_spec,
            "age_distribution": {
                "Below 18": age_distribution.get("below_18", 0),
                "18 to 30": age_distribution.get("18_to_30", 0),
                "31 to 40": age_distribution.get("31_to_40", 0),
                "41 to 50": age_distribution.get("41_to_50", 0),
                "Above 50": age_distribution.get("above_50", 0),
            },
        }

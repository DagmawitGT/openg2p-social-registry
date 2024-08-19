from odoo import api, exceptions, fields, models, _


class ResPartner(models.Model):
    _inherit = "res.partner"




    def button_open_profile(self):
        self.write({'edit_state': 'open'})

        self.edit_count = self.edit_count - 1


    # def write(self, vals):
    #     no_of_edits = self.env['no.of.edits'].search([])
    #     for record in self:
    #         if record.edit_count >= no_of_edits.edit_amount - 1:
    #             vals['edit_state'] = 'locked'
    #         vals['edit_count'] = record.edit_count + 1
    #     return super(ResPartner, self).write(vals)




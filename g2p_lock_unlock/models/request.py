from odoo import models,fields,api

class Request(models.TransientModel):
    _name = 'request'
    _description = 'Request'


    reason = fields.Text(string="Reason Description", required=True)
    record_id = fields.Many2one('res.partner', string='Record ID', required=True)
    requester_id = fields.Many2one('res.users', string='Requester', required=True)
    status = fields.Selection([('newSuggestion', 'New Suggestion'), ('updated', 'Updated')], string='Status', default = 'newSuggestion' )
    type = fields.Selection([('suggestion', 'Suggestion'), ('edit', 'Edit Access Request')], string='Type')
    seen = fields.Boolean(string='Seen', default=False)


    @api.model
    def create(self, vals):
        # Automatically reset seen status on new requests
        vals['status'] = 'newSuggestion'
        vals['seen'] = False
        return super(Request, self).create(vals)
    

    def update_request(self, vals):
        
        if self.status == 'newSuggestion':
            self.status = 'updated'
        return self.write(vals)

    def accept_request(self):
        
        self.record_id.edit_state = "open"
        # self.record_id.write({'edit_state': 'open'})
        self.status = 'accepted'

    def reject_request(self):
        self.record_id.edit_state = "locked"
        self.status = 'rejected'



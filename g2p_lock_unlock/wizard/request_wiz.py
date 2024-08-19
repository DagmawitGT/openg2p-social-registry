from odoo import models, fields

import logging
_logger = logging.getLogger(__name__)



class RequestWizard(models.TransientModel):
    _name = 'request.wiz'
    _inherit = ['mail.thread.main.attachment', 'mail.activity.mixin']
    _description = 'Request Wizard'


    reason = fields.Text(string="Reason Description", required=True)
    record_ids = fields.Many2many('res.partner', string='Records to be Edited')
    def send_request(self):
        activity_type = self.env.ref('mail.mail_activity_data_todo').id  # Get the activity type (e.g., To Do)
        for record in self.record_ids:
            enumerators =  record.create_uid
            print(enumerators.id)
            self.env['mail.activity'].create({
                'res_model_id': self.env['ir.model']._get_id('request.wiz'),
                'res_id': record.id,
                'activity_type_id': activity_type,
                'summary': 'Follow up on this record',
                'user_id': enumerators.id,  # Assign to the current user
                'date_deadline': fields.Date.today(),
            })


            # Save the data to the regular model
            self.env['request'].create({
                'reason': self.reason,
                'record_id': record.id,
                'requester_id': self.env.user.id,
                "status": 'pending',
                'type': 'edit'
            })
        
        return True
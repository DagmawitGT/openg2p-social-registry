from odoo import api, exceptions, fields, models, _
import json
import ast
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    # _inherit = ['mail.thread', 'mail.activity.mixin']

    approval_status = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='draft', string="Approval Status", track_visibility='onchange')

    edit_state = fields.Selection(selection=[('open', 'Open'),
                                             ('locked', 'Locked')], default="open")

    edit_count = fields.Integer(string='Edit Count', default=0)

    def _filter_json_compatible(self, vals):
        """
        Filters out fields with non-JSON-serializable data.
        """

        filtered_vals = {}
        for key, value in vals.items():
            field = self._fields.get(key)
            if field and isinstance(field, fields.Binary):
                # Skip binary fields
                continue

            try:
                # Attempt to serialize the value to JSON to check if it's compatible
                json.dumps(value)
                filtered_vals[key] = value
            except (TypeError, ValueError):
                # Log the exclusion for debugging purposes (optional)
                self.env.cr.rollback()  # Rollback to avoid partial updates in transactions
                self.message_post(body=f"Field '{key}' was excluded from change request due to non-JSON serializability.")

        return filtered_vals

    def write(self, vals):
        no_of_edits = self.env['no.of.edits'].search([])
        json_compatible_vals = self._filter_json_compatible(vals)
        user = self.env.user

        for record in self:
            print(record.edit_count)
            print(no_of_edits.edit_amount)
            if record.edit_count >= no_of_edits.edit_amount - 1:
                vals['edit_state'] = 'locked'
            vals['edit_count'] = record.edit_count + 1

        if self.env.context.get('bypass_write') or record.edit_state != 'locked' or user.has_group('g2p_lock_unlock.registry_super_admin'):
            # Allow write operations if the bypass context is set
            return super(ResPartner, self).write(vals)
        else:
            # Create a change request for each record that is being updated
            for partner in self:
                self.env['res.partner.change.request'].create({
                    'partner_id': partner.id,
                    'new_values': json_compatible_vals,
                    'state': 'pending',
                })
            # Return a meaningful value; for example, the count of records 'affected'
            return len(self)


        # def write(self, vals):
        #     no_of_edits = self.env['no.of.edits'].search([])
        #     for record in self:
        #         if record.edit_count >= no_of_edits.edit_amount - 1:
        #             vals['edit_state'] = 'locked'
        #         vals['edit_count'] = record.edit_count + 1
        #     return super(ResPartner, self).write(vals)

    # def write(self, vals):
    #     print("new update")
    #     # Create a new change request
    #     change_request_vals = {
    #         'partner_id': self.id,
    #         'new_values': vals,
    #         'state': 'pending',
    #     }
    #     self.env['res.partner.change.request'].create(change_request_vals)
    #
    #     # Set the approval status to pending
    #     vals.update({'approval_status': 'pending'})
    #
    #
    #     return super(ResPartner, self).write(vals)


class ResPartnerChangeRequest(models.Model):
    _name = 'res.partner.change.request'
    _description = 'Res Partner Change Request'

    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    # new_values = fields.Text(string="New Values", required=True)
    requested_by = fields.Many2one('res.users', string="Requested By", default=lambda self: self.env.user)
    new_values = fields.Json(string="New Values", required=True)
    new_values_display = fields.Char(string="New Values (Preview)", compute='_compute_new_values_display')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='pending', string="Status")

    def _compute_new_values_display(self):
        for record in self:
            try:
                # Convert JSON to a pretty-printed string for display
                record.new_values_display = json.dumps(record.new_values, indent=2)
            except Exception as e:
                record.new_values_display = "Error displaying JSON"

    def approve_changes(self):
        record = self.env['res.partner'].browse(self.partner_id)
        print(record)
        for request in self:
            try:
                # Safely parse the new_values string to a dictionary
                new_vals = request.new_values
                if isinstance(new_vals, dict):
                    # Apply the new values directly using the super method
                    request.partner_id.with_context(bypass_write=True).sudo().write(new_vals)
                    # Mark the request as approved
                    request.state = 'approved'
                    # Log the applied changes for debugging
                    request.partner_id.message_post(body=f"Changes approved and applied: {new_vals}")
                else:
                    raise ValueError("Parsed new_values is not a dictionary")
            except Exception as e:
                # Handle any exceptions and log them for debugging
                request.state = 'rejected'
                request.partner_id.message_post(body=f"Failed to apply changes: {str(e)}")
                # Optionally, raise the exception if you want to handle it at a higher level
                raise

    def reject_changes(self):
        for request in self:
            request.state = 'rejected'
            request.partner_id.approval_status = 'rejected'

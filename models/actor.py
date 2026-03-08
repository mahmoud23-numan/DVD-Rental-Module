from odoo import api, fields, models

class DvdRentalActor(models.Model):
    _name = 'dvd_rental.actor'
    _description = 'DVD Rental Actor'
    _inherit = ['mail.thread','mail.activity.mixin']
    _order = 'display_name'

    display_name = fields.Char(string='Display Name',compute='_compute_display_name',store=True)

    first_name = fields.Char(string='First Name',tracking=True)
    last_name = fields.Char(string='Last Name',tracking=True)

    film_ids  = fields.Many2many('dvd_rental.film',string='Films',tracking=True)

    @api.depends('first_name', 'last_name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.first_name or ''} - {record.last_name or ''}"
from odoo import api, fields, models

class DvdRentalCity(models.Model):
    _name = 'dvd_rental.city'
    _description = 'DVD Rental City'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'state_id'

    country_id = fields.Many2one('dvd_rental.country',string='Country',tracking=True)
    res_country_id = fields.Many2one(
        'res.country',
        related='country_id.country_id',
        store=True
    )

    state_id = fields.Many2one(
        'res.country.state',
        string='State',
        domain="[('country_id', '=', res_country_id)]",tracking=True
    )


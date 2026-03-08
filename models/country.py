from odoo import api, fields, models

class DvdRentalCountry(models.Model):
    _name = 'dvd_rental.country'
    _description = 'Country'
    _rec_name = 'country_id'
    _inherit = ['mail.thread','mail.activity.mixin']

    country_id = fields.Many2one('res.country', string='Country',tracking=True)
from odoo import fields, models,api

class DvdRentalAddress(models.Model):
    _name = 'dvd_rental.address'
    _description = 'DVD Rental Address'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'address'
    address = fields.Char(string='Address1',tracking=True)
    address2 = fields.Char(string='Address2',tracking=True)
    city_id = fields.Many2one('dvd_rental.city',string='City',tracking=True)
    postal_code = fields.Char(string='Postcode',size=5,tracking=True)
    phone = fields.Char(string='Phone',size=11,tracking=True)

    _sql_constraints = [
        ('phone_unique','UNIQUE (phone)','Phone must be unique'),
    ]

    @api.constrains('phone')
    def _check_phone(self):
        if self.phone:
            if not self.phone.isdigit():
                raise ValueError('Phone must be an integer')
            if len(self.phone) < 11 or len(self.phone) > 11:
                raise ValueError('Phone must be  11 digits')


    @api.constrains('postal_code')
    def _check_postal(self):
        if self.postal_code:
            if len(self.postal_code) < 5 or len(self.postal_code) > 5:
                raise ValueError('Postcode must be  5 digits')


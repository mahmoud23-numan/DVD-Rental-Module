from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError


class DvdRentalSpecialFeature(models.Model):
    _name = 'dvd_rental.special_feature'
    _description = 'DVD Rental Special Feature'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string='Feature Name',required=True)

    _sql_constraints = [
        ('unique_name','UNIQUE (name)','Name must be unique'),
    ]

    @api.constrains('name')
    def _check_name(self):
        if self.name is None:
            raise ValidationError('Special Feature Name cannot be empty')
        if self.name.isdigit():
            raise ValidationError('Special Feature Name cannot contain digits')
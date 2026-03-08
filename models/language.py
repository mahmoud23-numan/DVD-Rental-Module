from odoo import fields,models,api
from odoo.exceptions import ValidationError


class DvdRentalLanguage(models.Model):
    _name = 'dvd_rental.language'
    _description = 'DVD Rental Language'
    _rec_name = 'name'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(string='Language Name',required=True,tracking=True)

    _sql_constraints = [
        ('language_name_unique', 'UNIQUE (name)','Name must be unique'),
    ]

    @api.constrains('name')
    def _check_name(self):
        if self.name is None:
            raise ValidationError('Name IS Required')
        if self.name.isdigit():
            raise ValidationError('Name IS Not Contain A Digit Number')
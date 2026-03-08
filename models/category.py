from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class DvdRentalCategory(models.Model):
    _name = 'dvd_rental.category'
    _description = 'DVD Rental Category'
    _rec_name = 'name'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(string='Name',tracking=True)
    film_ids = fields.Many2many('dvd_rental.film',string='Films',readonly=True)

    _sql_constraints = [
        ('unique_name','UNIQUE (name)','Name must be unique.')
    ]

    @api.constrains('name')
    def _check_name(self):
        if self.name is None:
            raise ValidationError('Name cannot be empty.')
        if self.name.isdigit():
            raise ValidationError('Name cannot contain digits.')
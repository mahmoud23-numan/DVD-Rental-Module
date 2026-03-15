import re

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class DvdRentalStaff(models.Model):
    _name = 'dvd_rental.staff'
    _description = 'DVD Rental Staff'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'first_name'

    first_name = fields.Char(string='First Name',tracking=True)
    last_name = fields.Char(string='Last Name',tracking=True)
    address_id = fields.Many2one('dvd_rental.address',string='Address',tracking=True)
    email = fields.Char(string='Email',tracking=True)
    active = fields.Boolean(default=True,tracking=True)
    active_bool = fields.Boolean(default=True,tracking=True)
    user_id = fields.Many2one('res.users',string='User',tracking=True,readonly=True)
    picture = fields.Binary(string='Picture')
    store_id = fields.Many2one('dvd_rental.store', string='Store',tracking=True)

    _sql_constraints = [
        ('email_unique', 'UNIQUE (email)', 'Email address must be unique'),
    ]

    @api.constrains('email')
    def _check_email(self):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if self.email and not re.match(email_regex, self.email):
            raise ValidationError('Email address is not valid')


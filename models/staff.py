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
    payment_count = fields.Integer(string='Payment Count',compute='_compute_payment_count')
    _sql_constraints = [
        ('email_unique', 'UNIQUE (email)', 'Email address must be unique'),
    ]

    def _compute_payment_count(self):
        for record in self:
            count = self.env['dvd_rental.payment'].search_count([('staff_id','=',record.id)])
            record.payment_count = count

    def git_all_payment(self):
        action = self.env['ir.actions.act_window']._for_xml_id('dvd_rental.payment_view_menu_action')
        action['domain']=[('staff_id','=',self.id)]
        return action

    @api.constrains('email')
    def _check_email(self):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if self.email and not re.match(email_regex, self.email):
            raise ValidationError('Email address is not valid')


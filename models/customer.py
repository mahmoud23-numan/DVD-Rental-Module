import re

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class DvdRentalCustomer(models.Model):
    _name = 'dvd_rental.customer'
    _description = 'DVD Rental Customer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'display_name'

    display_name = fields.Char(string='Display Name',store=True,compute='_compute_display_name')
    first_name = fields.Char(string='First Name',tracking=True)
    last_name = fields.Char(string='Last Name',tracking=True)
    email = fields.Char(string='Email',tracking=True)
    active_bool = fields.Boolean(default=True,tracking=True)
    user_id = fields.Many2one('res.users', string='Related User',readonly=True)
    active = fields.Boolean(default=True,tracking=True)
    address_id = fields.Many2one('dvd_rental.address', string='Address',tracking=True)
    store_id = fields.Many2one('dvd_rental.store', string='Store',tracking=True)
    rental_count = fields.Integer(string='Rental Count',compute='_compute_count_rental')
    _sql_constraints = [
        ('email_unique','UNIQUE (email)','Email address must be unique'),
    ]

    def _compute_count_rental(self):
        for record in self:
            count = self.env['dvd_rental.rental'].search_count([('customer_id','=',record.id)])
            record.rental_count = count

    def get_all_rentals(self):
        action = self.env['ir.actions.act_window']._for_xml_id('dvd_rental.rental_view_menu_action')
        action['domain'] = [('customer_id', '=', self.id)]
        return action

    @api.depends('first_name', 'last_name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.first_name or ''} - {record.last_name or ''}"

    @api.constrains('email')
    def _check_email(self):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if self.email and not re.match(email_regex, self.email):
            raise ValidationError('Email address is not valid')


from odoo import api, fields, models

class DvdRentalStore(models.Model):
    _name = 'dvd_rental.store'
    _description = 'DVD Rental Store'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'title'

    title = fields.Char(string='Title',required=True,tracking=True)
    address_id = fields.Many2one('dvd_rental.address', string='Address',tracking=True)
    manager_staff_id = fields.Many2one('dvd_rental.staff', string='Manager',tracking=True)
    staff_member = fields.One2many('dvd_rental.staff','store_id',string='Staff'
                                   ,tracking=True)
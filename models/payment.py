from odoo import api, fields, models, tools

class DvdRentalPayment(models.Model):
    _name = 'dvd_rental.payment'
    _description = 'DVD Rental Payment'
    _inherit = ['mail.thread','mail.activity.mixin']

    customer_id = fields.Many2one('dvd_rental.customer', string='Customer',tracking=True)
    staff_id = fields.Many2one('dvd_rental.staff', string='Staff',tracking=True)
    rental_id = fields.Many2one('dvd_rental.rental', string='Rental',tracking=True)
    amount = fields.Float(string='Amount',tracking=True,digits=(4,3))
    payment_date = fields.Date(string='Payment Date',tracking=True,default=fields.Date.today())


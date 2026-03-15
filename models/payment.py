from email.policy import default

from odoo import api, fields, models, tools
from odoo.exceptions import UserError


class DvdRentalPayment(models.Model):
    _name = 'dvd_rental.payment'
    _description = 'DVD Rental Payment'
    _inherit = ['mail.thread','mail.activity.mixin']

    customer_id = fields.Many2one('dvd_rental.customer', string='Customer',tracking=True)
    staff_id = fields.Many2one('dvd_rental.staff', string='Staff',tracking=True)
    rental_id = fields.Many2one('dvd_rental.rental', string='Rental',tracking=True)
    amount = fields.Monetary(string='Amount',currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.ref('base.USD'))

    payment_date = fields.Date(string='Payment Date',tracking=True,default=fields.Date.context_today)


    @api.model
    def create(self, vals):
        if not self.env.context.get('is_from_wizard'):
            raise UserError("You cannot create a payment manually; you must use the Payment Wizard.")

        return super(DvdRentalPayment,self).create(vals)

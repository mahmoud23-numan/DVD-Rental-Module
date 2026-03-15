from odoo import api, fields, models
from odoo.exceptions import UserError


class CreatePaymentWizard(models.TransientModel):
    _name = 'wizard.create_payment_wizard'

    customer_id = fields.Many2one('dvd_rental.customer', string='Customer')
    staff_id = fields.Many2one('dvd_rental.staff', string='Staff')
    rental_id = fields.Many2one('dvd_rental.rental', string='Rental')
    amount = fields.Monetary(string='Amount', store=True, currency_field="currency_id")
    currency_id = fields.Many2one('res.currency',
                                  default=lambda self: self.env.ref('base.USD'))
    payment_date = fields.Date(string='Payment Date', default=fields.Date.context_today)

    @api.model
    def default_get(self, fields_list):
        res = super(CreatePaymentWizard, self).default_get(fields_list)
        rental_id = self.env.context.get('active_id')
        if rental_id:
            rental = self.env['dvd_rental.rental'].browse(rental_id)
            res.update({
                'rental_id' : rental.id,
                'customer_id' : rental.customer_id.id,
                'staff_id' : rental.staff_id.id,
                'amount' : rental.amount,
            })

        return res

    def action_confirm_payment(self):
        self.env['dvd_rental.payment'].with_context(is_from_wizard=True).create({
            'customer_id':self.customer_id.id,
            'staff_id':self.staff_id.id,
            'amount':self.amount,
            'rental_id':self.rental_id.id,
            'payment_date':self.payment_date,
        })
        if self.rental_id:
            self.rental_id.write({
                'state':'borrowed',
            })
            self.rental_id.inventory_id.film_id.write({
                'state':'borrowed',
            })
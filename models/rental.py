from odoo import api , fields,models,tools

class DvdRentalRental(models.Model):
    _name = 'dvd_rental.rental'
    _description = 'DVD Rental Rental'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'display_name'

    display_name = fields.Char(string='Display Name',compute='_compute_display_name')
    rental_date = fields.Date(string='Date of Rental',tracking=True,default=fields.Date.today())
    inventory_id = fields.Many2one('dvd_rental.inventory',string='Inventory',tracking=True)
    customer_id = fields.Many2one('dvd_rental.customer',string='Customer',tracking=True)
    return_date = fields.Date(string='Date of Return',tracking=True)
    staff_id = fields.Many2one('dvd_rental.staff',string='Staff',tracking=True)

    @api.depends('inventory_id','customer_id')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.inventory_id.display_name or ''} + {record.customer_id.display_name or ''}"
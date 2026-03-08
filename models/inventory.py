from odoo import api,fields,models

class DvdRentalInventory(models.Model):
    _name = 'dvd_rental.inventory'
    _description = 'DVD Rental Inventory'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'display_name'

    display_name = fields.Char(string='Display Name',store=True,compute='_compute_display_name')
    film_id = fields.Many2one('dvd_rental.film',string='Film',tracking=True)
    store_id = fields.Many2one('dvd_rental.store',string='Store',tracking=True)

    @api.depends('film_id','store_id')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.film_id.title or ''} - {record.store_id.title or ''}"
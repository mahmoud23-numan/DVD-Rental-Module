from odoo import api, fields, models

class DvdRentalActor(models.Model):
    _name = 'dvd_rental.actor'
    _description = 'DVD Rental Actor'
    _inherit = ['mail.thread','mail.activity.mixin']
    _order = 'display_name'

    display_name = fields.Char(string='Display Name',compute='_compute_display_name',store=True)

    first_name = fields.Char(string='First Name',tracking=True)
    last_name = fields.Char(string='Last Name',tracking=True)

    film_ids  = fields.Many2many('dvd_rental.film',string='Films',tracking=True)
    film_count = fields.Integer(string='Film Count',compute='_compute_film_count')

    def _compute_film_count(self):
        for record in self:
            count = self.env['dvd_rental.film'].search_count([('actor_ids','=',record.id)])
            record.film_count = count

    def git_all_film(self):
        action=self.env['ir.actions.act_window']._for_xml_id('dvd_rental.film_view_menu_action')
        action['domain'] = [('actor_ids','=',self.ids)]
        return action

    @api.depends('first_name', 'last_name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.first_name or ''} - {record.last_name or ''}"
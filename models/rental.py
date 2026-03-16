from odoo import api , fields,models,tools
from odoo.exceptions import ValidationError, UserError


class DvdRentalRental(models.Model):
    _name = 'dvd_rental.rental'
    _description = 'DVD Rental Rental'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'display_name'
    _order = 'state asc'

    display_name = fields.Char(string='Display Name',compute='_compute_display_name')
    rental_date = fields.Date(string='Date of Rental',tracking=True,default=fields.Date.today())
    inventory_id = fields.Many2one('dvd_rental.inventory',string='Inventory Film'
                                   ,tracking=True,domain=[('film_id.state','=','available')])
    customer_id = fields.Many2one('dvd_rental.customer',string='Customer',tracking=True)
    return_date = fields.Date(string='Date of Return',tracking=True)
    staff_id = fields.Many2one('dvd_rental.staff',string='Staff',tracking=True)
    state = fields.Selection([
        ('draft','Draft'),
        ('borrowed','Borrowed'),
        ('returned','Returned'),
        ('overdue','Overdue'),
    ],string='Status',default='draft',tracking=True)
    number_of_days_rental= fields.Integer(string='Number of Days Rental',
                                          compute='_compute_number_of_days_rental',store=True)

    amount = fields.Monetary(string='Amount',store=True,currency_field="currency_id"
                             ,compute='_compute_amount_rental')
    currency_id = fields.Many2one('res.currency',
                                  default=lambda self: self.env.ref('base.USD'))
    _sql_constraints = [
        ('check_days','CHECK(amount >= 0)','Days Can Not In Past'),
    ]

    def action_print_payment_receipt(self):
        self.ensure_one()
        payment = self.env['dvd_rental.payment'].search([('rental_id','=',self.id)], limit=1)
        if not payment:
            raise UserError("No payment record exists for this rental.")

        return self.env.ref('dvd_rental.payment_report_action').report_action(payment)

    def check_date_of_rental(self):
        today = fields.Date.today()
        overdue_rentals= self.search([
            ('state','=','borrowed'),
            ('return_date','<',today),
        ])
        for record in overdue_rentals:
            record.write({'state': 'overdue'})


    @api.model
    def create(self, vals):
        inventory_id = vals.get('inventory_id')
        if inventory_id:
            inventory_record = self.env['dvd_rental.inventory'].browse(inventory_id)
            if inventory_record.film_id.state == 'borrowed':
                raise UserError("Sorry, this movie is currently on loan and cannot be rented.")
        return super(DvdRentalRental, self).create(vals)

    def write(self,vals):
        for record in self:
            if record.state != 'draft' and not ('state' in vals and len(vals) == 1):
                raise UserError("You cannot edit a record in a non-Draft state.")
        return super(DvdRentalRental,self).write(vals)

    @api.constrains('number_of_days_rental')
    def check_number_of_days_rental(self):
        if self.number_of_days_rental :
            if self.number_of_days_rental > self.inventory_id.film_id.rental_duration:
                raise ValidationError(f'The Film Cannot Be Rented For More Than {self.inventory_id.film_id.rental_duration} Days')


    @api.depends('inventory_id')
    def _compute_amount_rental(self):
        for record in self:
            if record.inventory_id:
                record.amount = (record.inventory_id.film_id.replacement_cost *
                                 record.number_of_days_rental)
            else:
                record.amount = 0.0


    @api.depends('rental_date','return_date')
    def _compute_number_of_days_rental(self):
        for record in self:
            if record.rental_date and record.return_date:
                delta = record.return_date - record.rental_date
                record.number_of_days_rental = delta.days
            else:
                record.number_of_days_rental = 0


    def action_returned(self):
        self.state = 'returned'
        self.inventory_id.film_id.write(
            {'state':'available'}
        )

    @api.depends('inventory_id','customer_id')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.inventory_id.display_name or ''} + {record.customer_id.display_name or ''}"


    def unlink(self):
        for record in self:
            if record.inventory_id.film_id.state == 'borrowed':
                raise UserError("You cannot delete the rental history because the current film is still in 'borrowed' status.")

        return super(DvdRentalRental, self).unlink()



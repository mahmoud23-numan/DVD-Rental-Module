from odoo import api, fields, models
from odoo.exceptions import ValidationError


class DVDRentalFilm(models.Model):
    _name = 'dvd_rental.film'
    _description = 'DVD Rental Film'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'title'

    title = fields.Char(string='Title',size=30,tracking=True)
    description = fields.Char(string='Description',size=200,tracking=True)
    release_year = fields.Date(string='Release Year',tracking=True)
    language_id = fields.Many2one('dvd_rental.language',string='Language',tracking=True)
    rental_duration = fields.Integer(string='Rental Duration',size=1,tracking=True)
    rental_rate = fields.Integer(string='Rental Rate',tracking=True)
    length = fields.Integer(string='Length',size=3,tracking=True)
    replacement_cost = fields.Float(string='Replacement Cost',tracking=True)
    rating = fields.Selection([
        ('g', 'G'),
        ('pg', 'PG'),
        ('pg-13', 'PG-13'),
        ('r', 'R'),
        ('nc-17', 'NC-17'),
    ], string='Rating', default='g',tracking=True)
    special_feature_ids = fields.Many2many('dvd_rental.special_feature',string='Special Feature',tracking=True)
    fulltext = fields.Text(string='Full Text',tracking=True)
    category_ids = fields.Many2many('dvd_rental.category',string='Categories',tracking=True)
    actor_ids = fields.Many2many('dvd_rental.actor',string='Actors',tracking=True)


    _sql_constraints = [
        ('check_rental_rate','CHECK (rental_rate >= 1 OR rental_rate <= 5)','Rate Must Between 1 and 5'),
        ('check_rental_duration','CHECK (rental_rate >= 1 OR rental_rate <= 7)','Rental Duration Must Between 1 and 7'),
    ]

    @api.constrains('rental_rate')
    def _check_rental_rate(self):
        if self.rental_rate < 1 or self.rental_rate > 5:
            raise ValidationError("Rental Rate must be between 1 and 5")

    @api.constrains('rental_duration')
    def _check_rental_duration(self):
        if self.rental_duration < 1 or self.rental_duration > 7:
            raise ValidationError("Rental Duration must be between 1 and 7")

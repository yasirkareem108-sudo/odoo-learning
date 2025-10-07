from odoo import api, fields, models
from odoo.exceptions import ValidationError

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(string="Title", required=True)
    author = fields.Char(string="Author")
    isbn = fields.Char(string="ISBN")
    copies_total = fields.Integer(string="Total Copies", default=1, required=True)
    copies_available = fields.Integer(string="Available Copies", default=1, required=True)

    # ✅ New image field
    image = fields.Image(string="Book Image")

    @api.constrains('copies_available', 'copies_total')
    def _check_copies(self):
        for rec in self:
            if rec.copies_available > rec.copies_total:
                raise ValidationError("Available copies cannot exceed total copies.")

from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import date


class LibraryBorrow(models.Model):
    _name = 'library.borrow'
    _description = 'Library Borrow Record'

    student_id = fields.Many2one(
        'res.partner',
        string="Student",
        domain=[('is_student', '=', True)],
        required=True
    )
    book_id = fields.Many2one(
        'library.book',
        string="Book",
        required=True
    )
    borrow_date = fields.Date(string="Borrow Date", default=fields.Date.today)
    return_date = fields.Date(string="Return Date")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('lost', 'Lost'),
        ('returned', 'Returned'),
    ], string="Status", default='draft')

    penalty = fields.Float(string="Penalty", default=0.0)
    lost_book = fields.Boolean(string="Book Lost", default=False)

    # -------------------------
    # Header Button Actions
    # -------------------------
    def action_set_available(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError("Only draft records can be made available.")
            rec.state = 'available'

    def action_set_borrowed(self):
        today = date.today()
        for rec in self:
            # ✅ Membership check
            if rec.student_id.membership_end and rec.student_id.membership_end < today:
                raise UserError("Student membership expired! Cannot borrow books.")
            if rec.state != 'available':
                raise UserError("Only available books can be borrowed.")
            if rec.book_id.copies_available <= 0:
                raise UserError("No copies available for this book.")
            rec.book_id.copies_available -= 1
            rec.state = 'borrowed'
            rec.borrow_date = fields.Date.today()

    def action_set_lost(self):
        for rec in self:
            if rec.state != 'borrowed':
                raise UserError("Only borrowed books can be marked as lost.")
            rec.lost_book = True
            rec.state = 'lost'

    # -------------------------
    # Return Button
    # -------------------------
    def action_set_returned(self):
        for rec in self:
            if rec.state != 'borrowed':
                raise UserError("Only borrowed books can be returned.")
            rec.state = 'returned'
            rec.return_date = fields.Date.today()
            rec.book_id.copies_available += 1

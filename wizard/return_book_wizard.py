from odoo import models, fields
from odoo.exceptions import UserError

class LibraryReturnWizard(models.TransientModel):
    _name = 'library.return.wizard'
    _description = 'Library Return Wizard'

    borrow_id = fields.Many2one(
        'library.borrow',
        string="Borrow Record",
        required=True,
        domain="[('state','=', 'borrowed')]"
    )
    return_date = fields.Date(
        string="Return Date",
        required=True,
        default=fields.Date.today
    )

    def action_confirm(self):
        """Mark the borrow as returned and update available copies"""
        if not self.borrow_id:
            raise UserError("Please select a borrow record.")
        if self.borrow_id.state == 'returned':
            raise UserError("This book has already been returned.")

        self.borrow_id.state = 'returned'
        self.borrow_id.return_date = self.return_date
        self.borrow_id.book_id.copies_available += 1

        return {'type': 'ir.actions.act_window_close'}

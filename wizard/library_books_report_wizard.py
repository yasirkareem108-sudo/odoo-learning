from odoo import models, fields
from odoo.exceptions import UserError

class LibraryBooksReportWizard(models.TransientModel):
    _name = 'library.books.report.wizard'
    _description = 'Library Books Report Wizard'

    book_id = fields.Many2one(
        'library.book',
        string="Select Book",
        required=True,
        domain="[('copies_total','>',0)]"
    )

    def action_generate_pdf(self):
        """Generate PDF report of all students who borrowed the selected book"""
        if not self.book_id:
            raise UserError("Please select a book.")

        # Collect all borrow records for this book
        borrow_records = self.env['library.borrow'].search([
            ('book_id', '=', self.book_id.id)
        ])

        students_info = []
        for rec in borrow_records:
            students_info.append({
                'name': rec.student_id.name,
                'email': rec.student_id.email,
                'phone': rec.student_id.phone,
                'borrow_date': rec.borrow_date.strftime('%Y-%m-%d') if rec.borrow_date else '',
                'return_date': rec.return_date.strftime('%Y-%m-%d') if rec.return_date else '',
                'state': rec.state,
                'book_name': self.book_id.name,
            })

        # 🔹 Get library name from General Settings
        library_name = self.env['ir.config_parameter'].sudo().get_param(
            'library_management.library_name', default="Library"
        )

        # Pass students_info + library_name
        return self.env.ref('library_management.library_books_report_action').report_action(
            self,
            data={
                'students_info': students_info,
                'library_name': library_name
            }
        )

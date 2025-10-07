from odoo import models

class LibraryBooksReport(models.AbstractModel):
    _name = 'report.library_management.library_book_report_template'
    _description = 'Library Books Report'

    def _get_report_values(self, docids, data=None):
        # ✅ Fetch Library Name from Settings (with fallback)
        library_name = (
            self.env['ir.config_parameter']
            .sudo()
            .get_param('library_management.library_name', 'Allama Iqbal Library')
        )

        # ✅ Get student info from wizard data
        students_info = data.get('students_info') if data else []

        # ✅ Return values to QWeb
        return {
            'doc_ids': docids,
            'doc_model': 'library.books.report.wizard',
            'students_info': students_info,
            'library_name': library_name,
        }

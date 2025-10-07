from odoo import fields, models, api
from datetime import date

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_student = fields.Boolean(string="Is Student")
    borrowed_books_ids = fields.One2many(
        'library.borrow',
        'student_id',
        string="Borrowed Books"
    )

    # 🔹 Membership fields
    membership_type = fields.Selection([
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('vip', 'VIP'),
    ], string="Membership Type")

    membership_start = fields.Date(string="Membership Start Date")
    membership_end = fields.Date(string="Membership End Date")
    membership_fee = fields.Float(string="Membership Fee")

    # 🔹 Status field (manual + scheduler dono control karenge)
    membership_status = fields.Selection(
        [
            ('active', 'Active'),
            ('expired', 'Expired'),
            ('none', 'No Membership'),
        ],
        string="Membership Status",
        default="none"
    )

    # 🔘 Manual buttons ke liye
    def action_activate_membership(self):
        for rec in self:
            rec.membership_status = "active"

    def action_expire_membership(self):
        for rec in self:
            rec.membership_status = "expired"

    # 🔁 Scheduler ke liye method
    def _cron_update_membership_status(self):
        today = date.today()
        students = self.search([('is_student', '=', True)])
        for rec in students:
            if rec.membership_start and rec.membership_end:
                if rec.membership_end < today:
                    rec.membership_status = "expired"
                elif rec.membership_start <= today <= rec.membership_end:
                    rec.membership_status = "active"
                else:
                    rec.membership_status = "none"
            else:
                rec.membership_status = "none"

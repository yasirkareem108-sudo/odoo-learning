from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    library_name = fields.Char(
        string="Library Name",
        config_parameter='library_management.library_name'
    )


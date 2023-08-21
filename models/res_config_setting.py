from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    
    cancel_admission = fields.Integer(string='Cancel Admission',config_parameter = "school_managment.cancel_admission")
    setting_name = fields.Char(string='Teacher Name', default='ssss')
    setting_class = fields.Integer(string='Assign class to teacher')
    setting_div = fields.Selection(selection=[('A', 'A'), ('B', 'B')])
    setting_stream = fields.Selection(
        selection=[('Science', 'Science'), ('Commerce', 'Commerce'), ('Art', 'Art')])
    setting_bool = fields.Boolean(string= 'action_chek')
    setting_seq = fields.Boolean(string='Genrating seq.')
    stu_rec = fields.Many2one('student.registration')
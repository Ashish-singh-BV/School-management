from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SchoolTeacher(models.Model):
    _name = 'school.teachers'
    _description = 'all teacher data'
    _rec_name = 'teacher_name'

    teacher_name = fields.Char(string='Teacher Name')
    asign_class = fields.Integer(string='Assign class to teacher')
    respect_div = fields.Selection(selection=[('A', 'A'), ('B', 'B')])
    assign_stream = fields.Selection(
        selection=[('Science', 'Science'), ('Commerce', 'Commerce'), ('Art', 'Art')])

    #  constrains for stream field

    @api.constrains('asign_class', 'assign_stream')
    def _check_stream_required(self):
        if ((self.asign_class in [11, 12]) and not self.assign_stream):
            raise ValidationError("Stream field is required for class 12.")

    @api.model
    def create(self, vals):
        all_teacher = self.env['school.teachers'].search([('asign_class', '=', vals['asign_class']), 
            ('respect_div', '=', vals['respect_div']), ('assign_stream', '=', vals['assign_stream'])]) or 0
        if all_teacher:
            raise ValidationError(f"This class already assign to '{all_teacher.teacher_name}'")
        return super(SchoolTeacher , self).create(vals)

from odoo import models, fields, api
# from odoo.exceptions import ValidationError


class DeleteStudent(models.Model):
    _name = 'delete.student'
    _description = 'deleted student record'
    # _rec_name = 'teacher_name'
    
    deleted_student_record = fields.Many2one('student.registration',string="Student Name")
    
    
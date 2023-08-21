from odoo import models, fields, api
# from odoo.exceptions import ValidationError


class DeleteStudent(models.Model):
    _name = 'delete.student'
    _description = 'deleted student record'
    # _rec_name = 'teacher_name'
    
    deleted_student_record = fields.Many2one('student.registration',string="Student Name")
    
    
    
    def cancel(self):
        student_id = self.deleted_student_record.id
        # print(student_id,"gdfshahfhsjfgl")
        student_record = self.env['student.registration'].browse(student_id)
        return { 
            'type' : 'ir.actions.act_window',
            
        }
        # student_record.unlink()
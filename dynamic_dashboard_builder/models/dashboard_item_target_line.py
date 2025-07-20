
from odoo import models, fields, api

class DashboardItemTargetLine(models.Model):
    _name = 'dashboard.item.target.line'
    _description = 'Dashboard Target Line'

    item_id = fields.Many2one('dashboard.item', required=True, ondelete='cascade')
    date = fields.Date(string="Target Date")
    value = fields.Float(string="Target Value")
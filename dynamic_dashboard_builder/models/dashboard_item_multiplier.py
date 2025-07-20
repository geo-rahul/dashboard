
from odoo import fields, models

class DashboardItemMultiplier(models.Model):
    _name = 'dashboard.item.multiplier'
    _description = 'Dashboard Field Multiplier'

    item_id = fields.Many2one('dashboard.item', required=True, ondelete='cascade')
    field_id = fields.Many2one('ir.model.fields', string="Field", required=True, ondelete='cascade')
    multiplier = fields.Float(string="Multiplier", required=True, default=1.0)
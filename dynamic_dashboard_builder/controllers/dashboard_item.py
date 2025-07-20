# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request

class DashboardItemController(http.Controller):

    @http.route('/dashboard/item/defaults', type='json', auth='user')
    def defaults(self, dashboard_id, item_id=False):
        Item = request.env['dashboard.item'].sudo()
        if item_id:
            item = Item.browse(item_id)
            vals = {
                'id':                     item.id,
                'name':                   item.name,
                'dashboardId':            item.dashboard_id.id,
                'modelId':                item.model_id.id,
                'companyId':              item.company_id.id,
                'itemType':               item.item_type,
                'sequence':               item.sequence,
                'description':            item.description,
                'helpText':               item.help_text,
                'measureFieldIds':        item.measure_field_ids.ids,
                'secondaryMeasureIds':    item.secondary_measure_ids.ids,
                'dataAggregation':        item.data_aggregation,
                'groupByFieldId':         item.group_by_field_id.id,
                'groupByDateUnit':        item.group_by_date_unit,
                'subGroupByFieldId':      item.sub_group_by_field_id.id,
                'sortFieldId':            item.sort_field_id.id,
                'sortOrder':              item.sort_order,
                'limitEnabled':           item.limit_enabled,
                'limitValue':             item.limit_value,
                'domain':                 item.domain or '[]',
                'dateFieldId':            item.date_field_id.id,
                'defaultDateRange':       item.default_date_range,
                'numberFormat':           item.number_format,
                'valueFormat':            item.value_format,
                'decimalPlaces':          item.decimal_places,
                'isStacked':              item.is_stacked,
                'colorPalette':           item.color_palette,
                'valueSuffix':            item.value_suffix,
                'labelPosition':          item.label_position,
                'icon':                   item.icon,
                'showLegend':             item.show_legend,
                'showValuesOnChart':      item.show_values_on_chart,
                'useMultiplier':          item.use_multiplier,
                'multiplierLineIds':      item.multiplier_line_ids.ids,
                'enableTarget':           item.enable_target,
                'targetValue':            item.target_value,
                'targetType':             item.target_type,
                'targetLineIds':          item.target_line_ids.ids,
                'actionModel':            item.action_model,
                'actionDomain':           item.action_domain,
                'positionX':              item.position_x,
                'positionY':              item.position_y,
                'width':                  item.width,
                'height':                 item.height,
                'refreshInterval':        item.refresh_interval,
                'isGlobalItem':           item.is_global_item,
                'secondaryModelId':       item.secondary_model_id.id,
                'secondaryMeasureFieldId': item.secondary_measure_field_id.id,
                'secondaryAggregationType':item.secondary_aggregation_type,
                'secondaryDomain':        item.secondary_domain,
                'secondaryDateFieldId':   item.secondary_date_field_id.id,
                'secondaryDateRange':     item.secondary_date_range,
                'isCumulative':           item.is_cumulative,
                'cumulativeMeasureFieldIds': item.cumulative_measure_field_ids.ids,
                'lineMeasureFieldIds':    item.line_measure_field_ids.ids,
                'semiCircleMode':         item.semi_circle_mode,
                'stackedChart':           item.stacked_chart,
                'recordLimitEnabled':     item.record_limit_enabled,
                'recordLimit':            item.record_limit,
                'iconClass':              item.icon_class,
                'iconColor':              item.icon_color,
                'backgroundColor':        item.background_color,
                'fontColor':              item.font_color,
                'layoutMode':             item.layout_mode,
                'theme':                  item.theme,
                'dateFilterSelection':    item.date_filter_selection,
                'dateFrom':               item.date_from and item.date_from.strftime('%Y-%m-%d %H:%M:%S'),
                'dateTo':                 item.date_to   and item.date_to.strftime('%Y-%m-%d %H:%M:%S'),
                'enableCustomUnit':       item.enable_custom_unit,
                'customUnitLabel':        item.custom_unit_label,
                'currencyId':             item.currency_id.id,
                'numberFormatStyle':      item.number_format_style,
                'actionWindowId':         item.action_window_id.id,
                'clientActionId':         item.client_action_id.id,
                'enableRecordClick':      item.enable_record_click,
                'paginationLimit':        item.pagination_limit,
                'domainOverride':         item.domain_override,
            }
        else:
            vals = {
                'id':                     False,
                'name':                   '',
                'dashboardId':            dashboard_id,
                'modelId':                False,
                'companyId':              request.env.company.id,
                'itemType':               'kpi',
                'sequence':               10,
                'description':            '',
                'helpText':               '',
                'measureFieldIds':        [],
                'secondaryMeasureIds':    [],
                'dataAggregation':        'count',
                'groupByFieldId':         False,
                'groupByDateUnit':        False,
                'subGroupByFieldId':      False,
                'sortFieldId':            False,
                'sortOrder':              'desc',
                'limitEnabled':           False,
                'limitValue':             10,
                'domain':                 '[]',
                'dateFieldId':            False,
                'defaultDateRange':       False,
                'numberFormat':           'english',
                'valueFormat':            'decimal',
                'decimalPlaces':          2,
                'isStacked':              False,
                'colorPalette':           'default',
                'valueSuffix':            '',
                'labelPosition':          'top',
                'icon':                   '',
                'showLegend':             True,
                'showValuesOnChart':      False,
                'useMultiplier':          False,
                'multiplierLineIds':      [],
                'enableTarget':           False,
                'targetValue':            0.0,
                'targetType':             'line',
                'targetLineIds':          [],
                'actionModel':            '',
                'actionDomain':           '',
                'positionX':              0,
                'positionY':              0,
                'width':                  4,
                'height':                 2,
                'refreshInterval':        0,
                'isGlobalItem':           False,
                'secondaryModelId':       False,
                'secondaryMeasureFieldId':False,
                'secondaryAggregationType':'sum',
                'secondaryDomain':        '',
                'secondaryDateFieldId':   False,
                'secondaryDateRange':     False,
                'isCumulative':           False,
                'cumulativeMeasureFieldIds': [],
                'lineMeasureFieldIds':    [],
                'semiCircleMode':         False,
                'stackedChart':           False,
                'recordLimitEnabled':     False,
                'recordLimit':            10,
                'iconClass':              '',
                'iconColor':              '#ffffff',
                'backgroundColor':        '#ffffff',
                'fontColor':              '#000000',
                'layoutMode':             'layout1',
                'theme':                  'white',
                'dateFilterSelection':    False,
                'dateFrom':               False,
                'dateTo':                 False,
                'enableCustomUnit':       False,
                'customUnitLabel':        '',
                'currencyId':             False,
                'numberFormatStyle':      'english',
                'actionWindowId':         False,
                'clientActionId':         False,
                'enableRecordClick':      False,
                'paginationLimit':        20,
                'domainOverride':         '',
            }
        return vals

    @http.route('/dashboard/item/save', type='json', auth='user')
    def save(self, values):
        Item = request.env['dashboard.item'].sudo()
        data = {
            'dashboard_id':        values['dashboardId'],
            'name':                values['name'],
            'model_id':            values['modelId'],
            'company_id':          values.get('companyId') or False,
            'item_type':           values['itemType'],
            'sequence':            values['sequence'],
            'description':         values['description'],
            'help_text':           values['helpText'],
            'measure_field_ids':   [(6, 0, values.get('measureFieldIds', []))],
            'secondary_measure_ids':[(6,0,values.get('secondaryMeasureIds',[]))],
            'data_aggregation':    values['dataAggregation'],
            'group_by_field_id':   values.get('groupByFieldId'),
            'group_by_date_unit':  values.get('groupByDateUnit'),
            'sub_group_by_field_id': values.get('subGroupByFieldId'),
            'sort_field_id':       values.get('sortFieldId'),
            'sort_order':          values['sortOrder'],
            'limit_enabled':       values['limitEnabled'],
            'limit_value':         values['limitValue'],
            'domain':              values['domain'],
            'date_field_id':       values.get('dateFieldId'),
            'default_date_range':  values.get('defaultDateRange'),
            'number_format':       values['numberFormat'],
            'value_format':        values['valueFormat'],
            'decimal_places':      values['decimalPlaces'],
            'is_stacked':          values['isStacked'],
            'color_palette':       values['colorPalette'],
            'value_suffix':        values['valueSuffix'],
            'label_position':      values['labelPosition'],
            'icon':                values['icon'],
            'show_legend':         values['showLegend'],
            'show_values_on_chart':values['showValuesOnChart'],
            'use_multiplier':      values['useMultiplier'],
            'multiplier_line_ids': [(6,0,values.get('multiplierLineIds',[]))],
            'enable_target':       values['enableTarget'],
            'target_value':        values['targetValue'],
            'target_type':         values['targetType'],
            'target_line_ids':     [(6,0,values.get('targetLineIds',[]))],
            'action_model':        values['actionModel'],
            'action_domain':       values['actionDomain'],
            'position_x':          values['positionX'],
            'position_y':          values['positionY'],
            'width':               values['width'],
            'height':              values['height'],
            'refresh_interval':    values['refreshInterval'],
            'is_global_item':      values['isGlobalItem'],
            'secondary_model_id':  values.get('secondaryModelId'),
            'secondary_measure_field_id': values.get('secondaryMeasureFieldId'),
            'secondary_aggregation_type': values['secondaryAggregationType'],
            'secondary_domain':    values['secondaryDomain'],
            'secondary_date_field_id': values.get('secondaryDateFieldId'),
            'secondary_date_range':values['secondaryDateRange'],
            'is_cumulative':       values['isCumulative'],
            'cumulative_measure_field_ids': [(6,0,values.get('cumulativeMeasureFieldIds',[]))],
            'line_measure_field_ids': [(6,0,values.get('lineMeasureFieldIds',[]))],
            'semi_circle_mode':    values['semiCircleMode'],
            'stacked_chart':       values['stackedChart'],
            'record_limit_enabled':values['recordLimitEnabled'],
            'record_limit':        values['recordLimit'],
            'icon_class':          values['iconClass'],
            'icon_color':          values['iconColor'],
            'background_color':    values['backgroundColor'],
            'font_color':          values['fontColor'],
            'layout_mode':         values['layoutMode'],
            'theme':               values['theme'],
            'date_filter_selection': values.get('dateFilterSelection'),
            'date_from':           values.get('dateFrom'),
            'date_to':             values.get('dateTo'),
            'enable_custom_unit':  values['enableCustomUnit'],
            'custom_unit_label':   values['customUnitLabel'],
            'currency_id':         values.get('currencyId'),
            'number_format_style': values['numberFormatStyle'],
            'action_window_id':    values.get('actionWindowId'),
            'client_action_id':    values.get('clientActionId'),
            'enable_record_click': values['enableRecordClick'],
            'pagination_limit':    values['paginationLimit'],
            'domain_override':     values['domainOverride'],
        }
        if values.get('id'):
            item = Item.browse(values['id'])
            item.write(data)
        else:
            item = Item.create(data)
        return {'id': item.id}

    @http.route('/dashboard/item/companies', type='json', auth='user')
    def get_companies(self):
        return [{'id': c.id, 'name': c.name} for c in request.env['res.company'].sudo().search([])]

    @http.route('/dashboard/item/models', type='json', auth='user')
    def get_models(self, search=''):
        domain = [
            ('access_ids', '!=', False),
            ('transient', '=', False),
            ('model', 'not ilike', 'base_import%'),
            ('model', 'not ilike', 'ir.%'),
            ('model', 'not ilike', 'web_editor.%'),
            ('model', 'not ilike', 'web_tour.%'),
            ('model', '!=', 'mail.thread'),
            ('model', 'not ilike', 'dash%')
        ]
        if search:
            domain += ['|', ('name', 'ilike', search), ('model', 'ilike', search)]
        models = request.env['ir.model'].sudo().search(domain)
        return [
            {'id': m.id, 'name': m.name, 'model': m.model, 'field_count': len(m.field_id)}
            for m in models
        ]

    @http.route('/dashboard/item/aggregation/fields', type='json', auth='user')
    def get_agrregation_fields(self, model_id):
        print('model_id',model_id)
        fields = request.env['ir.model.fields'].sudo().search([('model_id', '=', model_id),('name','!=','id'), ('store','=',True), ('ttype','=','monetary')])
        return [
            {'id': f.id, 'name': f.display_name}
            for f in fields
        ]

    @http.route('/dashboard/item/date_fields', type='json', auth='user')
    def get_date_fields_by_model_id(self, model_id):
        model = request.env['ir.model'].browse(model_id)
        if not model.exists():
            return []
        date_fields = request.env['ir.model.fields'].sudo().search([('model_id', '=', model_id),('name','!=','id'), ('store','=',True), ('ttype','in', ['date', 'datetime'])])
        return [
            {'id': f.id, 'name': f.display_name}
            for f in date_fields
        ]

    @http.route('/dashboard/item/groupby/fields', type='json', auth='user')
    def get_groupby_fields(self, model_id):
        print('model_id', model_id)
        fields = request.env['ir.model.fields'].sudo().search(
            [('model_id', '=', model_id), ('name', '!=', 'id'),('name', '!=', 'sequence'), ('store', '=', True), ('ttype', '!=', 'binary'), ('ttype', '!=', 'many2many'), ('ttype', '!=', 'one2many')])
        return [
            {'id': f.id, 'name': f.display_name}
            for f in fields
        ]
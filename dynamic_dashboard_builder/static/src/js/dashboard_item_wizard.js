/** @odoo-module **/
import { Component, onWillStart, useState, xml } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { debounce } from "@web/core/utils/timing";
import { SelectMenu } from "@web/core/select_menu/select_menu";
import { DomainSelectorDialog } from "@web/core/domain_selector_dialog/domain_selector_dialog";



export class DashboardItemWizard extends Component {
  DEFAULT_ICONS = [
    'fa-home', 'fa-star', 'fa-car', 'fa-calendar', 'fa-bar-chart',
    'fa-line-chart', 'fa-cogs', 'fa-user', 'fa-book', 'fa-bell',
  ];
  static components = { 
    SelectMenu
  };
  static template = "dynamic_dashboard_builder.DashboardItemWizard";
  static props = {
    dashboardId: { type: Number },
//    itemId:      { type: [Number, Boolean], optional: true },
//    onSave:      { type: Function },  // called when user clicks Save & Close
    close:      { type: Function },  // called when user clicks × or Discard
//    action: { type: Object },
  };

  setup() {
    this.state = useState({
      loading:                 true,
      id:                      this.props.itemId || false,
      name:                    '',
      dashboardId:             this.props.dashboardId,
      dataSource:              'odoo',
      models:                  [],             // all available models (populate via RPC)
      selectedModelId:         null,
      selectedModelName:       '',
      companyIds:              [],             // all available companies (populate via RPC)
      companyId:               false,
      itemType:                'kpi',
      sequence:                10,
      description:             '',
      helpText:                '',
      measureFieldIds:         [],
      secondaryMeasureIds:     [],
      dataAggregation:         'count',
      dataAggregationFieldId:  false,
      aggregationFieldOptions: [],
      groupByFieldOptions:     [],
      groupByFieldId:          false,
      groupByDateUnit:         false,
      subGroupByFieldId:       false,
      sortFieldId:             false,
      sortOrder:               'desc',
      limitEnabled:            false,
      limitValue:              10,
      domain:                  '[]',
      dateFieldOptions:        [],
      dateFieldId:             false,
      defaultDateRange:        'l_none',
      numberFormat:            'english',
      showUnit:                false,
      unitType:                'currency',
      charUnit:                 '',
      itemTheme:                'white',
      backgroundColor:          '#ffffff',
      bgAlpha:                  100,
      fontColor:                '#000000',
      fontAlpha:                100,
      valueFormat:             'decimal',
      decimalPlaces:           2,
      isStacked:               false,
      colorPalette:            'default',
      valueSuffix:             '',
      labelPosition:           'top',
      icon:                    '',
      showIconModal:           false,
      displayedIcons:          [...this.DEFAULT_ICONS],
      showLegend:              true,
      showValuesOnChart:       false,
      useMultiplier:           false,
      multiplierLineIds:       [],
      enableTarget:            false,
      targetValue:             0.0,
      targetType:              'line',
      targetLineIds:           [],
      actionModel:             '',
      actionDomain:            '',
      positionX:               0,
      positionY:               0,
      width:                   4,
      height:                  2,
      refreshInterval:         0,
      isGlobalItem:            false,
      secondaryModelId:        false,
      secondaryMeasureFieldId: false,
      secondaryAggregationType:'sum',
      secondaryDomain:         '',
      secondaryDateFieldId:    false,
      secondaryDateRange:      false,
      isCumulative:            false,
      cumulativeMeasureFieldIds: [],
      lineMeasureFieldIds:     [],
      semiCircleMode:          false,
      stackedChart:            false,
      recordLimitEnabled:      false,
      recordLimit:             10,
      iconClass:               '',
      iconColor:               '#ffffff',
      backgroundColor:         '#ffffff',
      fontColor:               '#000000',
      layoutMode:              'layout1',
      theme:                   'white',
      dateFilterSelection:     false,
      dateFrom:                '',
      dateTo:                  '',
      enableCustomUnit:        false,
      customUnitLabel:         '',
      currencyId:              false,
      numberFormatStyle:       'english',
      actionWindowId:          false,
      clientActionId:          false,
      enableRecordClick:       false,
      paginationLimit:         20,
      domainOverride:          '',
      activeTab:               'data',
      itemType:                'kpi',
      dashboardId:             this.props.currentDashboardId,
    });
    this.typeOptions = [
    ['kpi',      'Tile',          'th-large'],
    ['bar',      'Bar',           'bar-chart'],
    ['hbar',     'H. Bar',        'bars'],
    ['line',     'Line',          'line-chart'],
    ['area',     'Area',          'area-chart'],
    ['pie',      'Pie',           'pie-chart'],
    ['doughnut', 'Doughnut',      'dot-circle-o'],
    ['polar',    'Polar',         'circle-o-notch'],
    ['radar',    'Radar',         'circle'],
    ['radial',   'Radial',        'circle-thin'],
    ['flower',   'Flower',        'flower'],
    ['funnel',   'Funnel',        'filter'],
    ['bullet',   'Bullet',        'bullseye'],
    ['list',     'List',          'list'],
    ['map',      'Map',           'map-marker'],
  ];
  this.tabs = [
    { id: 'data',    label: 'Data' },
    { id: 'display', label: 'Display' },
    { id: 'actions', label: 'Actions' },
    { id: 'config',  label: 'Advanced Config' },
    { id: 'desc',    label: 'Item Description' },
  ];
  this.dataAggregationOptions = [
    { value: 'count', label: 'Count' },
    { value: 'sum', label: 'Sum' },
    { value: 'avg', label: 'Average' },
  ];
  this.sortOrderOptions = [
    { value: 'asc', label: 'Ascending' },
    { value: 'desc', label: 'Descending' },
  ];
  this.numberFormatOptions = [
    { value: 'english', label: 'English' },
    { value: 'indian', label: 'Indian' },
    { value: 'exact', label: 'Exact' },
  ];
  this.unitTypeOptions = [
    { value: 'currency', label: 'Currency' },
    { value: 'custom', label: 'Custom' },
  ];
  this.themeColors = [
    { value: 'white', color: '#ffffff' },
    { value: 'blue', color: '#007bff' },
    { value: 'red', color: '#dc3545' },
    { value: 'orange', color: '#fd7e14' },
    { value: 'green', color: '#28a745' },
  ];
  this.ICON_LIST = [
    'fa fa-bar-chart',
    'fa fa-pie-chart',
    'fa fa-line-chart',
    'fa fa-table',
    'fa fa-bolt',
    'fa fa-heartbeat',
    'fa fa-users',
    'fa fa-cogs',
    'fa fa-check-circle',
    'fa fa-tachometer',
  ];
  this.dateRangeOptions = [
      { label: 'None', value: 'l_none' },
      { label: 'Today', value: 'l_day' },
      { label: 'This Week', value: 't_week' },
      { label: 'This Month', value: 't_month' },
      { label: 'This Quarter', value: 't_quarter' },
      { label: 'This Year', value: 't_year' },
      { label: 'Week to Date', value: 'td_week' },
      { label: 'Month to Date', value: 'td_month' },
      { label: 'Quarter to Date', value: 'td_quarter' },
      { label: 'Year to Date', value: 'td_year' },
      { label: 'Next Day', value: 'n_day' },
      { label: 'Next Week', value: 'n_week' },
      { label: 'Next Month', value: 'n_month' },
      { label: 'Next Quarter', value: 'n_quarter' },
      { label: 'Next Year', value: 'n_year' },
      { label: 'Last Day', value: 'ls_day' },
      { label: 'Last Week', value: 'ls_week' },
      { label: 'Last Month', value: 'ls_month' },
      { label: 'Last Quarter', value: 'ls_quarter' },
      { label: 'Last Year', value: 'ls_year' },
      { label: 'Last 7 days', value: 'l_week' },
      { label: 'Last 30 days', value: 'l_month' },
      { label: 'Last 90 days', value: 'l_quarter' },
      { label: 'Last 365 days', value: 'l_year' },
      { label: 'Past Till Now', value: 'ls_past_until_now' },
      { label: 'Past Excluding Today', value: 'ls_pastwithout_now' },
      { label: 'Future Starting Now', value: 'n_future_starting_now' },
      { label: 'Future Starting Tomorrow', value: 'n_futurestarting_tomorrow' },
      { label: 'Custom Filter', value: 'l_custom' },
    ];
    this.actionService = useService("action");
    this.dialogService = useService("dialog");
    const orm = useService("orm");  // For fetching fields, if needed
    onWillStart(async () => {
      await this._loadDefaults();  // your existing code
      await this._loadModels();
      await this._loadCompanies();
      this.fullIconSet = await this.fetchFontAwesomeIcons();
    });
    this.onModelSelect = this.onModelSelect.bind(this);
    this.onCompanySelect = this.onCompanySelect.bind(this);
    this.onSelectDataAggregation = this.onSelectDataAggregation.bind(this);
    this.openDomainDialog = this.openDomainDialog.bind(this);
  }

  async _loadCompanies() {
    const companies = await rpc('/dashboard/item/companies');
    console.log(companies);
    this.state.companyIds = companies.map(c => ({
      value: c.id,
      label: c.name,
    }));
  }

  async _loadModels() {
    const models = await rpc('/dashboard/item/models');
    console.log(models);
    this.state.models = models.map(model => ({
      value: model.id,
      label: model.name || model.model || 'Unnamed Model',
      model: model.model,
    }));
  }catch (error) {
    console.error("Failed to load models:", error);
    this.state.models = [];
  }

  async _loadGroupByFields() {
    console.log('🔍 Debug - Loading group by fields for model:', this.state.selectedModelId);
    const fields = await rpc('/dashboard/item/groupby/fields',{
      model_id: this.state.selectedModelId
      });
    console.log(fields);
    this.state.groupByFieldOptions = fields.map(field => ({
      value: field.id,
      label: field.name,
    }));
    console.log('🔍 Debug - Aggregation fields loaded:', this.state.groupByFieldOptions);
  }

  async _loadAgregation() {
    console.log('🔍 Debug - Loading aggregation fields for model:', this.state.selectedModelId);
    const fields = await rpc('/dashboard/item/aggregation/fields',{
      model_id: this.state.selectedModelId
      });
    console.log(fields);
    this.state.aggregationFieldOptions = fields.map(field => ({
      value: field.id,
      label: field.name,
    }));
    console.log('🔍 Debug - Aggregation fields loaded:', this.state.aggregationFieldOptions);
  }

  async _loadDateFieldOptionsByModelId() {
    if (!this.state.selectedModelId) return;

    try {
      const result = await rpc('/dashboard/item/date_fields', {
        model_id: this.state.selectedModelId,
      });
      this.state.dateFieldOptions = result.map(field => ({
          value: field.id,
          label: field.name
      }));
    } catch (error) {
      console.error('Failed to fetch date fields by model ID:', error);
    }
  }

  async onModelSelect(value) {
    console.log('Model selected:', value);
    this.state.selectedModelId = parseInt(value);

    const selectedModel = this.state.models.find(m => m.value === parseInt(value));
    console.log('selectedModel', selectedModel);

    if (selectedModel && selectedModel.model) {
      this.state.selectedModelName = selectedModel.model;
      console.log('selectedModelName set to:', this.state.selectedModelName);
    } else {
      console.warn('Could not set selectedModelName – field missing or model not found');
    }

    await this._loadAgregation();
    await this._loadDateFieldOptionsByModelId();
    await this._loadGroupByFields();
  }
  async openDomainDialog() {
    console.log('Selected models',this.state.selectedModelName);
    if (!this.state.selectedModelName) {
        return alert("Please select a model first");
    }

    const result = await this.dialogService.add(DomainSelectorDialog, {
        title: "Set Domain Filter",
        resModel: this.state.selectedModelName,  // e.g. 'sale.order'
        domain: this.state.domain ? this.state.domain : [],
        onConfirm: (newDomain) => {
            this.state.domain = newDomain;
        },
    });
  }

  onCompanySelect(value) {
    console.log('Company selected:', value);
    this.state.companyId = value;
  }
  async onSelectDataAggregation(value) {
      console.log('Data Aggregation selected:', value);
      this.state.dataAggregation = value;
      await this._loadAgregation();
  }

  onSelectMeasures = (values) => {
    // values is expected to be an array of selected field IDs
    console.log('Selected Measure Fields:', values);
    this.state.measureFieldIds = values;
    console.log('Measure Field IDs:', this.state.measureFieldIds);
  }

  get DEFAULT_ICONS() {
    return [
      'fa-home', 'fa-star', 'fa-car', 'fa-calendar', 'fa-bar-chart',
      'fa-line-chart', 'fa-cogs', 'fa-user', 'fa-book', 'fa-bell',
    ];
  }

  async fetchFontAwesomeIcons() {
    console.log('Fetching FontAwesome icons...');
    return [
      'fa-home', 'fa-user', 'fa-users', 'fa-cog', 'fa-cogs', 'fa-wrench', 'fa-gear', 'fa-briefcase', 'fa-suitcase', 'fa-building',
      'fa-industry', 'fa-database', 'fa-chart-bar', 'fa-bar-chart', 'fa-line-chart', 'fa-area-chart', 'fa-pie-chart', 'fa-tasks', 'fa-check', 'fa-times',
      'fa-search', 'fa-filter', 'fa-sort', 'fa-sort-asc', 'fa-sort-desc', 'fa-dashboard', 'fa-envelope', 'fa-inbox', 'fa-paper-plane', 'fa-comment',
      'fa-comments', 'fa-phone', 'fa-mobile', 'fa-globe', 'fa-map', 'fa-map-marker', 'fa-location-arrow', 'fa-calendar', 'fa-clock-o', 'fa-bell',
      'fa-bolt', 'fa-heart', 'fa-star', 'fa-flag', 'fa-folder', 'fa-folder-open', 'fa-file', 'fa-file-text', 'fa-file-excel-o', 'fa-file-pdf-o',
      'fa-file-image-o', 'fa-save', 'fa-download', 'fa-upload', 'fa-share', 'fa-share-alt', 'fa-link', 'fa-chain', 'fa-external-link', 'fa-trash',
      'fa-archive', 'fa-edit', 'fa-pencil', 'fa-pencil-square-o', 'fa-plus', 'fa-minus', 'fa-times-circle', 'fa-check-circle', 'fa-info-circle', 'fa-question-circle',
      'fa-exclamation-circle', 'fa-warning', 'fa-lightbulb-o', 'fa-lock', 'fa-unlock', 'fa-key', 'fa-shield', 'fa-user-plus', 'fa-user-times', 'fa-sign-in',
      'fa-sign-out', 'fa-eye', 'fa-eye-slash', 'fa-bars', 'fa-ellipsis-h', 'fa-ellipsis-v', 'fa-chevron-up', 'fa-chevron-down', 'fa-chevron-left', 'fa-chevron-right',
      'fa-angle-up', 'fa-angle-down', 'fa-angle-left', 'fa-angle-right', 'fa-arrows', 'fa-arrows-alt', 'fa-expand', 'fa-compress', 'fa-refresh', 'fa-repeat', 'fa-undo'
    ];
  }

  onSearchIcon() {
    const query = this.state.iconSearch.trim().toLowerCase();
    if (!query) return;

    const match = this.fullIconSet.find(icon => icon.includes(query));
    if (match && !this.state.displayedIcons.includes(match)) {
      this.state.displayedIcons.push(match);
    }
  }


  openIconPicker() {
    // You can show a modal or dropdown here
    // For testing, simulate icon select:
    this.state.icon = 'fa fa-bar-chart';
  }
  selectIcon = (icon) => {
    this.state.icon = icon;
    this.state.showIconModal = false;
  }
  clearIcon() {
    this.state.icon = '';
  }


  onLimitValueChange = (ev) => {
    this.state.limitValue = parseInt(ev.target.value || 0);
  }

  onSelectLineMeasures = (values) => {
    console.log('Selected Line Measure Fields:', values);
    this.state.secondaryMeasureIds = values;
    console.log('Line Measure Field IDs:', this.state.secondaryMeasureIds);
  }

  //TODO: Helper function to convert hex to rgba will be used to set the background color of the item when saving the item
  getRgbaString(hex, alpha) {
    const r = parseInt(hex.substring(1, 3), 16);
    const g = parseInt(hex.substring(3, 5), 16);
    const b = parseInt(hex.substring(5, 7), 16);
    return `rgba(${r}, ${g}, ${b}, ${alpha / 100})`;
  }

  async _loadDefaults() {
    const defs = await rpc('/dashboard/item/defaults', {
      dashboard_id: this.props.dashboardId,
      item_id:      this.state.id,
    });
    Object.assign(this.state, defs);
    this.state.loading = false;
  }

  async saveAndClose() {
    const values = { ...this.state };
    const res = await rpc('/dashboard/item/save', { values });
    this.props.onClose();
  }

//  // Called by your “×” and “Discard” buttons
  closeWizard = () => {
    this.props.close();
  };

  setItemType = (type) => {
    this.state.itemType = type;
  };
  activateTab = (tabId) => {
      this.state.activeTab = tabId;
    }

}

DashboardItemWizard.template = "dynamic_dashboard_builder.DashboardItemWizard";
registry.category('actions').add('dynamic_dashboard_builder.DashboardItemWizardAction', DashboardItemWizard);
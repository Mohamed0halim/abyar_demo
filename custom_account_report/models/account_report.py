# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import ast
import copy
import datetime
import io
import json
import logging
import markupsafe
from collections import defaultdict
from math import copysign, inf
import js2py

import lxml.html
from babel.dates import get_quarter_names
from dateutil.relativedelta import relativedelta
from markupsafe import Markup

from odoo import models, fields, api, _
from odoo.addons.web.controllers.main import clean_action
from odoo.exceptions import RedirectWarning
from odoo.osv import expression
from odoo.tools import config, date_utils, get_lang
from odoo.tools.misc import formatLang, format_date
from odoo.tools.misc import xlsxwriter
from odoo.http import request

_logger = logging.getLogger(__name__)


class AccountReport(models.AbstractModel):
    _inherit = 'account.report'
    _description = 'Account Report'

    def _get_reports_buttons(self, options):
        return [
            {'name': _('PDF'), 'sequence': 1, 'action': 'print_pdf', 'file_export_type': _('PDF')},
            {'name': _('XLSX'), 'sequence': 2, 'action': 'print_xlsx', 'file_export_type': _('XLSX')},
            {'name': _('Print'), 'sequence': 3, 'action': 'print_only', 'file_export_type': _('print_only')},
            {'name': _('Save'), 'sequence': 10, 'action': 'open_report_export_wizard'},
        ]

    def print_only(self, options):
        # import pyautogui
        # import time
        #
        # # Wait for 5 seconds before executing the next line
        # time.sleep(5)
        #
        # # Press and hold 'ctrl' key
        # pyautogui.keyDown('ctrl')
        #
        # # Press 'p' key
        # pyautogui.press('p')
        #
        # # Release 'ctrl' key
        # pyautogui.keyUp('ctrl')

        js = """
        odoo.define('custom_account_report.OrderReceipt', function(require){
    "use strict";
    var models = require('point_of_sale.models');
//    models.load_fields('product.template', 'product_grade_id');
    var _super_orderline = models.Orderline.prototype;
      window.print();
        });
        """
        add = js2py.eval_js(js)
        # print(add(1, 2))
        print('test')

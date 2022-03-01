# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import _
import random
#from odoo.exceptions import ValidationError, Warning
#import secrets
import logging
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from odoo import http
import base64
import re


from odoo.tools import image

_logger = logging.getLogger(__name__)


class banner_juego_controller(http.Controller):
    @http.route('/juego/banner', auth='user', type='json')
    def banner(self):
        return {
            'html': """
                <div  class="juego_banner" 
                style="height: 280px; background-size:100%; background-image: url(../static/src/img/banner.jpg)">
                <p>BANNER</p>
                </div> """
        }


# -*- coding: utf-8 -*-
import werkzeug
import logging
import odoo
import odoo.exceptions
import werkzeug.exceptions
import traceback
import json
from odoo.tools import ustr, consteq, frozendict, pycompat, unique, date_utils
from odoo.http import JsonRequest, AuthenticationError, SessionExpiredException, ustr, request, serialize_exception, Response

_logger = logging.getLogger(__name__)

# def _handle_exception(self, exception):
#     """Called within an except block to allow converting exceptions
#        to arbitrary responses. Anything returned (except None) will
#        be used as response."""
#     config_parameter = request.env['ir.config_parameter'].sudo()
#     title_name = config_parameter.get_param('odoo_tittle_name', 'Dreamwarez')
#     try:
#         return super(JsonRequest, self)._handle_exception(exception)
#     except Exception:
#         if not isinstance(exception, SessionExpiredException):
#             if exception.args and exception.args[0] == "bus.Bus not available in test mode":
#                 _logger.info(exception)
#             elif isinstance(exception, (odoo.exceptions.UserError,
#                                         werkzeug.exceptions.NotFound)):
#                 _logger.warning(exception)
#             else:
#                 _logger.exception("Exception during JSON request handling.")
#         error = {
#             'code': 200,
#             'message': title_name + " Server Error",
#             'data': serialize_exception(exception),
#         }
#         if isinstance(exception, werkzeug.exceptions.NotFound):
#             error['http_status'] = 404
#             error['code'] = 404
#             error['message'] = "404: Not Found"
#         if isinstance(exception, AuthenticationError):
#             error['code'] = 100
#             error['message'] = title_name + " Session Invalid"
#         if isinstance(exception, SessionExpiredException):
#             error['code'] = 100
#             error['message'] = title_name + " Session Expired"
#         return self._json_response(error=error)

# setattr(JsonRequest, '_handle_exception', _handle_exception)

def _json_response(self, result=None, error=None):
    config_parameter = request.env['ir.config_parameter'].sudo()
    title_name = config_parameter.get_param('odoo_tittle_name', 'Dreamwarez')
    response = {
        'jsonrpc': '2.0',
        'id': self.jsonrequest.get('id')
        }
    if error is not None:
        error['message'] = error['message'].replace("Odoo", title_name)
        response['error'] = error
    if result is not None:
        response['result'] = result

    mime = 'application/json'
    body = json.dumps(response, default=date_utils.json_default)

    return Response(
        body, status=error and error.pop('http_status', 200) or 200,
        headers=[('Content-Type', mime), ('Content-Length', len(body))]
    )

setattr(JsonRequest,'_json_response',_json_response) #overwrite the method

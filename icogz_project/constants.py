import json

from django.http import HttpResponse


response_master = {
    'success': '',
    'code': '',
    'data': '',
    'message': '',
}


def send_response(error_code, data, success, message, errors=[]):
    fronted_response = response_master
    fronted_response['success'] = success
    fronted_response['code'] = error_code
    fronted_response['data'] = data
    fronted_response['message'] = message
    fronted_response['errors'] = errors
    return HttpResponse(json.dumps(fronted_response, sort_keys=True, default=str),
                        content_type="application/json", status=error_code)



def exception_response(error_code, data, success, message, error_message):
    exception_response = response_master
    exception_response['success'] = success
    exception_response['code'] = error_code
    exception_response['data'] = data
    exception_response['message'] = message
    exception_response['errors'] = []
    return HttpResponse(json.dumps(exception_response, sort_keys=True, default=str),
                        content_type="application/json", status=error_code)
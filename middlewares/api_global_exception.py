from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from django.conf import settings
import traceback
import json
import datetime

def get_response(exc,meta_data):
    if isinstance(exc,APIException):
        return Response(data={"detail":str(exc),"timestamp":int(datetime.datetime.timestamp(datetime.datetime.now())),"meta_data":meta_data},status=exc.status_code)
    return Response(data={"detail":str(exc),"timestamp":int(datetime.datetime.timestamp(datetime.datetime.now())),"meta_data":meta_data},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def error_log(exc,context):
    view = context.get('view')
    request = context.get('request')

    client_ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if client_ip:
        client_ip = client_ip.split(',')[0].strip()
    else:
        client_ip = request.META.get('REMOTE_ADDR')
    
    log_data = {
        "user_id": request.token_payload.get('user_id'),
        "user_type": request.token_payload.get('role'),
        "error_message": str(exc),
        "request_method": request.method if request else None,
        "request_headers": dict(request.headers) if request else None,
        "request_parameters": dict(request.query_params) if request else None,
        "request_body": request.data if request else None,
        "client_ip": client_ip,
        "stack_trace": traceback.format_tb(exc.__traceback__) if hasattr(exc, '__traceback__') else None,
        "exception_type": type(exc).__name__,
        "view_name": view.__class__.__name__ if view else None,
        "response_status_code": exc.get_codes() if isinstance(exc, APIException) else 500,
        "environment": 'development' if settings.DEBUG else 'production',
        "error_location": None,
    }
    if view:
        module_name = view.__class__.__module__
        class_name = view.__class__.__name__

        if hasattr(view, '__name__'):
            function_name = view.__name__
            log_data["error_location"] = f"{module_name}.{function_name}"
        else:
            log_data["error_location"] = f"{module_name}.{class_name}"

    print("Error => ",json.dumps(log_data))
    return log_data

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data['status_code'] = response.status_code
    if exc:
        log_data=error_log(exc,context)
        return get_response(exc,log_data)
    return response
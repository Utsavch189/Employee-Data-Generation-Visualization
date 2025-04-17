from django.shortcuts import redirect
from django.http import JsonResponse

def login_required(redirect_url:str,json_response:bool=False,role:str=None,follow_path_include=False):
    def _inner(func):
        def _wrapped_view(*args, **kwargs):
            access_token = args[1].COOKIES.get('access_token')
            refresh_token = args[1].COOKIES.get('refresh_token')
            incoming_role=args[1].token_payload.get("role")
            requested_path = args[1].META.get('PATH_INFO')
            if (not (access_token and refresh_token)) or args[1].logout:
                args[1].logout=True
                response=None
                if not json_response:
                    if follow_path_include:
                        _redirect_url = redirect_url+f"?follow-path={requested_path}"
                        response=redirect(_redirect_url)
                    else:
                        response=redirect(redirect_url)
                else:
                    response=JsonResponse({"message":"unauthorized!","status":401,"redirect_url":redirect_url},status=401)
                if role and role!=incoming_role:
                    if not json_response:
                        if follow_path_include:
                            _redirect_url = redirect_url+f"?follow-path={requested_path}"
                            response=redirect(_redirect_url)
                        else:
                            response=redirect(redirect_url)
                    else:
                        response=JsonResponse({"message":"unauthorized!","status":401,"redirect_url":redirect_url},status=401)
                return response
            return func(*args, **kwargs)
        return _wrapped_view
    return _inner
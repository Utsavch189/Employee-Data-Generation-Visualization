from utils.jwt_manager import JwtManager 
import json
import os
from dotenv import load_dotenv

load_dotenv()

class JwtCookieAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process request
        access_token = request.COOKIES.get('access_token',None)
        refresh_token = request.COOKIES.get('refresh_token',None)
        jwt_builder = JwtManager()
        setattr(request,'need_refresh',False)
        setattr(request,'logout',False)
        setattr(request,'token_payload',{})

        if access_token:
            payload = jwt_builder.decode(access_token)
            if payload:
                request.token_payload = {
                    "sub":payload.get("sub"),
                    "user_id":payload.get("user_id"),
                    "role":payload.get("role"),
                    "email":payload.get("email")
                }
            else:
                if refresh_token:
                    payload = jwt_builder.decode(refresh_token)
                    if payload:
                        request.token_payload = {
                            "sub":payload.get("sub"),
                            "user_id":payload.get("user_id"),
                            "role":payload.get("role"),
                            "email":payload.get("email")
                        }
                        setattr(request,'need_refresh',True)
                    else:
                        setattr(request,'logout',True)
 
        # Process response
        response = self.get_response(request)

        if request.need_refresh:
            if type(request.token_payload)==str:
                new_tokens = jwt_builder.get_token(payload=json.loads(request.token_payload))
            elif type(request.token_payload)==dict:
                new_tokens = jwt_builder.get_token(payload=request.token_payload)
                
            response.set_cookie(key='access_token', value=new_tokens['access_token'],max_age=60*int(os.getenv("REFRESH_TOKEN_EXPIRY")))
            response.set_cookie(key='refresh_token', value=new_tokens['refresh_token'],max_age=60*int(os.getenv("REFRESH_TOKEN_EXPIRY")))
            return response

        if request.logout:
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response
        
        return response
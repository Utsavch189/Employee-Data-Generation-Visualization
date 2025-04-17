from rest_framework.views import APIView 
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from utils.api_exceptions import NotExists,GenericException
from app.models import  AdminUser
from utils.jwt_manager import JwtManager
from dotenv import load_dotenv
import os

load_dotenv()

class LoginView(APIView):

    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            raise GenericException(detail="provide email and password!")
        
        admin_user = AdminUser.objects.get(email=email)

        if not admin_user:
            raise GenericException(detail="wrong crendentials!")
        
        h_password = admin_user.password

        if not check_password(password,h_password):
            raise GenericException(detail="wrong crendentials!")
        
        tokens = JwtManager().get_token({
            "sub": admin_user.email,
            "name": admin_user.first_name+" "+admin_user.last_name
        })

        res = Response({
            "detail":"logged in!",
            "jwt_tokens":tokens
        })

        res.set_cookie(key='access_token', value=tokens.get('access_token'),max_age=60*int(os.getenv("REFRESH_TOKEN_EXPIRY")))
        res.set_cookie(key='refresh_token', value=tokens.get('refresh_token'),max_age=60*int(os.getenv("REFRESH_TOKEN_EXPIRY")))
        return res

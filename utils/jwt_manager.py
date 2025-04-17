import jwt
from datetime import datetime,timedelta
from dotenv import load_dotenv
import os

load_dotenv()

class JwtManager:

    def __init__(self) -> None:
        self.jwt_secret:str=os.getenv('SECRET')
        self.jwt_algos:str=os.getenv('ALGORITHM')
        self.access_token_exp:int=int(os.getenv("ACCESS_TOKEN_EXPIRY")) # in minutes
        self.refresh_token_exp:int=int(os.getenv("REFRESH_TOKEN_EXPIRY")) # in minutes
    
    def get_token(self,payload:dict)->dict:
        try:
            tokens={
                "access_token":jwt.encode(payload={**{"iat":int(datetime.timestamp(datetime.now())),"exp":int(datetime.timestamp(datetime.now()+timedelta(minutes=self.access_token_exp))),"iss":os.getenv('OWNER')},**payload},key=self.jwt_secret,algorithm=self.jwt_algos),
                "refresh_token":jwt.encode(payload={**{"iat":int(datetime.timestamp(datetime.now())),"exp":int(datetime.timestamp(datetime.now()+timedelta(minutes=self.refresh_token_exp))),"iss":os.getenv('OWNER')},**payload},key=self.jwt_secret,algorithm=self.jwt_algos),
            }
            return tokens
        except Exception as e:
            print(str(e))
            return {}

    def decode(self,token:str) -> dict:
        try:
            return jwt.decode(token,self.jwt_secret,algorithms=[self.jwt_algos])
        except Exception as e:
            return False
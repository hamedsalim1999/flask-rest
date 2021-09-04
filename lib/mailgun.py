from flask.wrappers import Response
from requests import post
from typing import List
from decouple import config
from flask import request , url_for

class MailGunException(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)
class MailGun:
 
    ADDRES=config('ADDRES')
    FROM_TITLE=config('FROM_TITLE')
    FROM_EMAIL =config('FROM_EMAIL')
    PRIVATE_API=config('PRIVATE_API_KEY')    
    @classmethod 
    def send_email(cls,email:List[str],subject:str,text:str,html:str) -> Response:
        
        return post(
        f"https://api.mailgun.net/v3/{cls.ADDRES}/messages",
        auth=("api", cls.PRIVATE_API),
        data={
            "from": f"{cls.FROM_TITLE}<{cls.FROM_EMAIL}>",
            "to":email,
            "subject": subject,
            "text":text,
            "html":html
              },
        )
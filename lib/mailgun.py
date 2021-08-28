from flask.wrappers import Response
from requests import post
from typing import List
from decouple import config
from flask import request , url_for
class MailGun:
    def __init__(self):
        self.ADDRES=config('ADDRES')
        self.FROM_TITLE=config('FROM_TITLE')
        self.FROM_EMAIL =config('FROM_EMAIL')
        self.PRIVATE_API=config('PRIVATE_API_KEY')    
        
    def send_email(self,email:List[str],subject:str,text:str,html:str) -> Response:
        
        return post(
        f"https://api.mailgun.net/v3/{self.ADDRES}/messages",
        auth=("api", self.PRIVATE_API),
        data={
            "from": f"{self.FROM_TITLE}<{self.FROM_EMAIL}>",
            "to":email,
            "subject": subject,
            "text":text,
            "html":html
              },
        )
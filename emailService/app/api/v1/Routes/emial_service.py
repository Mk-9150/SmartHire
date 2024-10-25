from typing import Annotated , Union , Literal , Any
from typing_extensions import Self
from fastapi import Depends , HTTPException , status,APIRouter,Query
from app.model.data_model import Account
from app.core.app_settings import settings
from app.crud.emailCrud import generate_password_reset_token , generate_reset_password_email

from app.crud.emailCrud import send_email , generate_new_account_email

router=APIRouter()

@router.post("/newaccount/user")
def Generate_New_Account(data:Account):
    """
    Create new user.
    """
    if settings.EmailEnabled :
        email_data = generate_new_account_email(
            email_to=data.email, username=data.username,
        )
        send_email(
            email_to=data.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
    return status.HTTP_200_OK



@router.post("/password/recovery")
def PasswordRecovery(email:str=Query(alias="email")):
    
    password_reset_token = generate_password_reset_token(email=email)
    
    email_data = generate_reset_password_email(
        email_to=email, email=email, token=password_reset_token
    )
    send_email(
        email_to=email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return "Password recovery email sent"




    
    
    
    ...
    
    
    












    
    
     

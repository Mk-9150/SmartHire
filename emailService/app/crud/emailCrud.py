import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from fastapi import HTTPException, status, Security

import emails  # type: ignore
from jinja2 import Template
from app.core.app_settings import settings
from jose import JWTError, jwt


@dataclass
class EmailData:
    html_content: str
    subject: str

def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
    # template_str = (
    #     Path(__file__).parent / "email-templates" / "build" / template_name
    # ).read_text()
    
    template_str = (
        Path(__file__).parent / ".." / "email-templates" / "build" / template_name
    ).read_text()
    # template_str = template_path.read_text()
    
    # print(template_str)
    
    
    
    html_content = Template(template_str).render(context)
    # print(html_content)
 
    return html_content


def send_email(*,email_to: str,subject: str = "",html_content: str = "") -> None:
    assert settings.EmailEnabled, "no provided configuration for email variables"
    message = emails.Message(
        subject=subject,
        html=html_content,
        mail_from=(settings.EMAIL_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}

    if settings.SMTP_TLS:
        smtp_options["tls"] = True

    elif settings.SMTP_SSL:
        smtp_options["ssl"] = True

    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER

    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    # print("smtp_options", smtp_options)
    response = message.send(to=email_to, smtp=smtp_options)
    logging.info(f"send email result: {response}")



def generate_new_account_email(
    email_to: str, username: str
) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    html_content = render_email_template(
        template_name="new_account.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "description":settings.WELCOME_MSG,
            # "password": password,
            "email": email_to,
            "link": settings.server_host,
        },
    )
    return EmailData(html_content=html_content, subject=subject)



def generate_password_reset_token(*,email:str):
    ...
    
    timedlta=timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    
    now=datetime.utcnow()
    print(now)
    expiresDelta=now+timedlta
    print(expiresDelta)
    
    exp=expiresDelta.timestamp()
    print(exp)
    
    encodedJwt= jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encodedJwt
    
    
    
def generate_reset_password_email(email_to: str, email: str, token: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    link = f"{settings.server_host}/reset-password?token={token}"
    html_content = render_email_template(
        template_name="reset_password.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )
    return EmailData(html_content=html_content, subject=subject)
    
   

# @router.post("/reset-password/")
# def reset_password(session: SessionDep, body: NewPassword) -> Message:
#     """
#     Reset password
#     """
#     email = verify_password_reset_token(token=body.token)
#     if not email:
#         raise HTTPException(status_code=400, detail="Invalid token")
#     user = crud.get_user_by_email(session=session, email=email)
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this email does not exist in the system.",
#         )
#     elif not user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     hashed_password = get_password_hash(password=body.new_password)
#     user.hashed_password = hashed_password
#     session.add(user)
#     session.commit()
#     return Message(message="Password updated successfully")   
   
    


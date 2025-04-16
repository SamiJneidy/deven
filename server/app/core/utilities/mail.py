from fastapi_mail import FastMail, MessageSchema
from pydantic import EmailStr
from ..config.mail_settings import connection_config

fastmail = FastMail(connection_config)

async def send_email(to: list[EmailStr], subject: str, body: str, subtype: str = "plain") -> None:
    message = MessageSchema(
        subject=subject, body=body, recipients=to, subtype=subtype
    )
    await fastmail.send_message(message)
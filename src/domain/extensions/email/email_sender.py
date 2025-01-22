from src.infrastructure.config.config import (
    PROJECT_NAME, MAIL_FROM, MAIL_SERVER, MAIL_PORT, 
    MAIL_USERNAME, MAIL_PASSWORD,
    REGISTERED_HTML, UPDATE_PASSWORD_HTML
)

from aiosmtplib import SMTP
from email.mime.text import MIMEText
from jinja2 import Template


registered = Template(REGISTERED_HTML, enable_async=True)
update_password = Template(UPDATE_PASSWORD_HTML, enable_async=True)


class EmailSender:
    """
    Class that is responsible for sending emails with smtp lib.
    """
    client = SMTP(
        hostname=MAIL_SERVER, 
        port=MAIL_PORT, 
        use_tls=True, 
        validate_certs=False, 
        username=MAIL_USERNAME, 
        password=MAIL_PASSWORD
    )

    @staticmethod  
    async def send_registered(email: str, password: str) -> None:
        """
        Create a message with registration
        :param email: email address
        :param password: password
        """
        registered_html = await registered.render_async(password=password)

        await EmailSender.__send(
            email, f"Вы добавлены на платформу {PROJECT_NAME}", registered_html    
        )

    @staticmethod
    async def send_update_password(email: str, password_link: str) -> None:
        """
        Create a message for a password update and send it
        :param email: email address
        :param password_link: link to password
        """
        update_password_html = await update_password.render_async(
            link=password_link
        )

        await EmailSender.__send(
            email, "Ссылка для изменения пароля", update_password_html
        )
    
    @staticmethod
    async def __send(email: str, subject: str, html_template) -> None:
        """
        Creates a message with template and sends it to email.
        :param email: Email address
        :param subject: Subject
        :param html_template: HTML template for a message
        """
        msg = MIMEText(html_template, "html")
        msg["Subject"] = subject
        msg["From"] = f"{PROJECT_NAME} <{MAIL_FROM}>"
        msg["To"] = email

        async with EmailSender.client as c:
            await c.send_message(msg)

"""  """

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

class EmailSenderError(Exception):
    """ Exceptions associeted with the process of send a email. """

class EmailAttachFilesError(EmailSenderError):...


class SmtplibSender:
    def execute(
        self,
        sender: str, 
        password: str, 
        recipients: list[str], 
        subject: str, 
        body: str, 
        files: list[str] = None,
        smtp: str = "smtp.gmail.com"
    ) -> None:
        """
        Sends email with attachments to multiple recipients.
        
        Args:
            sender (str): Sender email.
            password (str): Sender password.
            recipients (list[str]): List with recipients emails.
            subject (str): Subject of message.
            body (str): Body of message.
            files (list[str]): List with paths of files to send.
        """
        try:
            msg = MIMEMultipart()
            self._configure_email(msg, sender, recipients, subject)
            self._add_body(msg, body)
            self._attach_files(msg, files)
            self._send_email(msg, sender, password, recipients, smtp)
        except (EmailSenderError, Exception) as e:
            raise
    
    def _configure_email(
        self, 
        msg: MIMEMultipart, 
        sender: str, 
        recipients: list[str], 
        subject: str
    ) -> None:
        msg['From'] = sender
        msg['To'] = ', '.join(recipients) # Recivers list separeted by commas
        msg['Subject'] = subject
    
    def _add_body(self, msg: MIMEMultipart, body: str) -> None:
        msg.attach(MIMEText(body, 'plain')) # E-mail body
    
    def _attach_files(self, msg: MIMEMultipart, files: list[str]) -> None:
        if not files:
            return
        
        for file in files:
            try:
                with open(file, "rb") as anexo:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(anexo.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename="{os.path.basename(file)}"'
                )
                msg.attach(part)
            except FileNotFoundError as e:
                raise EmailAttachFilesError(f"Erro: Arquivo {file} não encontrado. -> {e}")
            except Exception as e:
                print(f"Erro inesperado ao associar o arquivo: {file} -> {e}")
    
    def _send_email(
            self, 
            msg: MIMEMultipart,
            sender: str,
            password: str,
            recipients: list[str],
            smtp: str
        ) -> None:
        try:
            server = smtplib.SMTP(smtp, 587)
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, recipients, msg.as_string())
            server.quit()
            print("E-mail enviado com sucesso!")
        except smtplib.SMTPResponseException as e:
            raise EmailSenderError(f"Erro na bibliotec smartpli durante o envio do email. {e}")
        except Exception as e:
            raise

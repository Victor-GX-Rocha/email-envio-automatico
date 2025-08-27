import re
from src.core.log import log
from src.infra.db.repo import EmailRepository
from src.infra.db.repo.email import EmailRecord
from src.infra.db.repo.models import ResponseCode
from .senders import SmtplibSender, EmailSenderError

class EmailRecordValidation:
    def validate(self, line: EmailRecord) -> bool:
        """ 
        Validates if the line has all data necessary to send a valid email. 
        Args:
            line (EmailRecord): Record of a line from table email.
        """
        
        errors: dict = {}
        self.validate_empty_columns(line, errors)
        self.validate_invalid_columns(line, errors)
        
        if errors:
            raise EmailSenderError(errors)
    
    def validate_empty_columns(self, line: EmailRecord, errors: dict) -> None:
        """ Validate that essential columns are filled in. """
        empty_columns: list[str] = [
            col for col in [
                    line.shipping.recipient_email, 
                    line.shipping.sender_email, 
                    line.shipping.sender_password
                ] if not col
            ]
        if not empty_columns:
            return
        errors.update({"Coluna(s) obrigatória(s) vazias": empty_columns})
    
    def validate_invalid_columns(self, line: EmailRecord, errors: dict) -> None:
        """ Validate that essencial columns are in the correct format. """
        invalid_emails: list[str] = []
        
        for email in line.shipping.recipient_email:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                invalid_emails.append(email)
        
        if invalid_emails:
            errors.update({"Emails em formato inválido": invalid_emails})

class EmailSenderApp:
    def __init__(self):
        self.repo = EmailRepository()
        self.sender = SmtplibSender()
        self.validator = EmailRecordValidation()
    
    def execute(self) -> None:
        pending_lines: list[EmailRecord] = self.repo.get.pending_operations()
        
        if not pending_lines:
            return
        
        for line in pending_lines:
            self.send_email(line)
    
    def send_email(self, line: EmailRecord) -> None:
        """ 
        Send a email based on table email lines. 
        Args:
            line (EmailRecord): Record of a line from table email.
        """
        try:
            self.validator.validate(line)
            
            self.sender.execute(
                sender=line.shipping.sender_email,
                password=line.shipping.sender_password,
                recipients=line.shipping.recipient_email,
                subject=line.content.subject,
                body=line.content.message,
                files=line.content.attachments,
                smtp=line.shipping.sender_smtp
            )
            self.repo.update.log_success(line.id)
        except EmailSenderError as e:
            log.dev.exception(f"Erro ao enviar e-mail: {str(e)}")
        except Exception as e:
            log.dev.exception(f"Erro inesperado ao enviar e-mail: {str(e)}")
            self.repo.update.log_error(line.id, ResponseCode.PROGRAM_ERROR, f"Falha inesperada durante o envio de email {e}")


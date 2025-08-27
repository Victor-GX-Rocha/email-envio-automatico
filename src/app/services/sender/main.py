
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import re

from src.infra.db.repo import EmailRepository
from src.infra.db.repo.email import EmailRecord
from src.infra.db.repo.models import ResponseCode

from src.core.log import log


class EmailSender:
    def __init__(self):
        self.repo = EmailRepository()
    
    def execute(self) -> None:
        pending_lines: list[EmailRecord] = self.repo.get.pending_operations()
        
        if not pending_lines:
            return
        
        for line in pending_lines:
            self.send_email(line)
    
    def send_email(self, line: EmailRecord) -> None:
        """  """
        try:
            self.enviar_email(
                remetente=line.shipping_details.sender_email,
                senha=line.shipping_details.sender_password,
                destinatarios=line.shipping_details.recipient_email.strip(),
                assunto=line.content.subject,
                corpo=line.content.message,
                arquivos=line.content.attachments
            )
            self.repo.update.log_success(line.id)
        except Exception as e:
            log.dev.exception(f"Erro ao enviar e-mail: {str(e)}")
            self.repo.update.log_error(line.id, ResponseCode.PROGRAM_ERROR, f"Falha inesperada durante o envio de email {e}")
    
    def enviar_email(
        self,
        remetente: str, 
        senha: str, 
        destinatarios: str, 
        assunto: str, 
        corpo: str, 
        arquivos: str =None
    ) -> None:
        """ Envia e-mail com anexos para múltiplos destinatários. """
        
        # Configurar mensagem
        destinatarios = re.split(r'[;,]', destinatarios)
        # to = re.split(r'[,;]', destinatarios)
        print(f"destinatários {destinatarios}")
        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = ', '.join(destinatarios) # Lista de destinatários separados por vírgula
        msg['Subject'] = assunto
        
        # Corpo do e-mail
        msg.attach(MIMEText(corpo, 'plain'))
        
        # Anexar arquivos
        if arquivos:
            arquivos = re.split(r'[,;]', arquivos)
            print(f"arquivos: {arquivos}")
            for arquivo in arquivos:
                try:
                    with open(arquivo, "rb") as anexo:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(anexo.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename="{os.path.basename(arquivo)}"'
                    )
                    msg.attach(part)
                except FileNotFoundError:
                    print(f"Erro: Arquivo {arquivo} não encontrado.")
        
        # Enviar e-mail
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)  # Alterar para seu servidor SMTP
            server.starttls()
            server.login(remetente, senha)
            server.sendmail(remetente, destinatarios, msg.as_string())
            server.quit()
            print("E-mail enviado com sucesso!")
        except Exception as e:
            log.dev.exception(f"Erro ao enviar e-mail: {str(e)}")
            raise

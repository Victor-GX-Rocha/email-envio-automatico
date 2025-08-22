
import time

from .core import log
from .config import AppConfigManager
# from .app import App

config = AppConfigManager()
database_config = config.load_database_config()

class MainLoop:
    def turn_on(self):
        """ Turns on the loop and keeps it active as long as the STILL_ON variable in the .env file is active. """
        
        try:
            
            log.user.info("Iniciando o bot...")
            # last_deactivated_run: float = 0
            
            while True:
                
                app_config = config.load_app_config()
                
                if not app_config.still_on:
                    log.user.info('Arquivo .env: Comando desligar.')
                    break
                
                # current_time = time.time()
                
                # Regular operations
                # App.email_sender.execute()
                
                time.sleep(app_config.timer)
            
        except KeyboardInterrupt as k:
            log.user.info(f"Programa desligado manualmente pelo usuário {k}")
        except Exception as e:
            log.dev.exception(f"Exceção inesperada durante a execução do loop principal: {e}")
    
    def turn_off(self) -> None:
        """ Turn off the loop. """
        try:
            log.user.info('Desligando o bot...\n\n')
        except Exception as e:
            log.dev.exception(f"Exceção inesperada durante a desativação do loop principal: {e}")

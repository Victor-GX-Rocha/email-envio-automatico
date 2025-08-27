"""  """

from .services import EmailSender

class App:
    email_sender = EmailSender()

__version__: str = "v.0.0.1"
__all__: list = [
    "__version__",
    "App"
]

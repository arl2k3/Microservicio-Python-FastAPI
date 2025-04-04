import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "API de Eventos y Calendario"
    PROJECT_VERSION : str = "1.0.0"
    PROJECT_DESCRIPTION: str = "API para gestionar eventos y enviar notificaciones"
    PROJECT_API_VERSION: str = "1.0.0"

    SMTP_SERVER: str = os.getenv("SMTP_SERVER")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")

settings = Settings()
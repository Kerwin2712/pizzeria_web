# config.py
import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Dict, Any
import flet as ft
from urllib.parse import quote_plus # Importa quote_plus para escapar la contraseña

# Carga las variables de entorno del archivo .env
load_dotenv()

class Config:
    """
    Clase de configuración para la aplicación de la pizzería.
    Carga los ajustes desde variables de entorno o usa valores por defecto.
    """
    # Configuración general de la aplicación
    APP_NAME: str = os.getenv("APP_NAME", "La Mejor Pizzería")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-pizzeria-dev") # Clave secreta para uso en desarrollo

    # Configuración de la base de datos PostgreSQL
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "pizzeria_db") # Nombre de tu base de datos de pizzería
    DB_USER: str = os.getenv("DB_USER", "pizzeria_user") # Usuario de la base de datos
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "") # Contraseña de la base de datos

    # Construye la URL completa de la base de datos para SQLAlchemy
    @property
    def DATABASE_URL(self) -> str:
        """Retorna la URL de conexión de la base de datos."""
        # Escapa la contraseña para asegurar que los caracteres especiales se manejen correctamente
        # en la URL de conexión.
        encoded_password = quote_plus(self.DB_PASSWORD)
        return f"postgresql://{self.DB_USER}:{encoded_password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Configuración de la aplicación Flet
    FLET_PORT: int = int(os.getenv("FLET_PORT", "8500"))
    
    @property
    def FLET_VIEW(self) -> ft.AppView:
        """
        Retorna la vista de Flet basada en la variable de entorno FLET_VIEW.
        Soporta "WEB_BROWSER", "FLET_APP", "FLET_APP_WEB".
        """
        view_mapping = {
            "WEB_BROWSER": ft.AppView.WEB_BROWSER,
            "FLET_APP": ft.AppView.FLET_APP,
            "FLET_APP_WEB": ft.AppView.FLET_APP_WEB
        }
        # Usa .get() para proporcionar un valor por defecto seguro
        return view_mapping.get(os.getenv("FLET_VIEW", "WEB_BROWSER"), ft.AppView.WEB_BROWSER)

    # Configuración de autenticación (ejemplo)
    SESSION_TIMEOUT: int = int(os.getenv("SESSION_TIMEOUT", "3600"))  # 1 hora en segundos

    # Rutas de la aplicación (ejemplo, puedes ajustarlas según tu estructura)
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    TEMPLATES_DIR: Path = BASE_DIR / "templates"
    STATIC_DIR: Path = BASE_DIR / "static"

    # Configuración de logging (ejemplo)
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "pizzeria.log")

    @classmethod
    def get_database_config(cls) -> Dict[str, Any]:
        """
        Retorna la configuración de la base de datos como un diccionario.
        Útil para frameworks o librerías que esperan esta estructura.
        """
        return {
            "host": cls.DB_HOST,
            "port": cls.DB_PORT,
            "database": cls.DB_NAME,
            "user": cls.DB_USER,
            "password": cls.DB_PASSWORD
        }

# Instancia de configuración para importar fácilmente en otras partes de la aplicación
settings = Config()

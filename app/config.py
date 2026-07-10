import os
from pathlib import Path

class Settings:
    """
    Configuración centralizada de NexusBI.
    Utiliza pathlib para garantizar compatibilidad multiplataforma (Windows/Linux/Mac).
    """
    
    # Determina el directorio raíz del proyecto (2 niveles arriba de este archivo)
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    
    # Entorno (desarrollo o producción)
    APP_ENV: str = os.getenv("APP_ENV", "dev")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")
    
    # Servidor
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8050))
    
    # Rutas de Datos (Absolutas)
    DATA_DIR: Path = BASE_DIR / "data"
    UPLOAD_DIR: Path = DATA_DIR / "uploads"
    MODEL_DIR: Path = DATA_DIR / "models"
    CACHE_DIR: Path = DATA_DIR / "cache"
    DB_FILE: Path = DATA_DIR / "nexusbi.db"

    @classmethod
    def initialize(cls):
        """
        Crea los directorios necesarios si no existen.
        Se debe llamar una vez al arrancar la aplicación.
        """
        dirs_to_create = [
            cls.UPLOAD_DIR,
            cls.MODEL_DIR,
            cls.CACHE_DIR
        ]
        for directory in dirs_to_create:
            directory.mkdir(parents=True, exist_ok=True)
            
        if cls.DEBUG:
            print(f"🚀 NexusBI Iniciado en modo: {cls.APP_ENV.upper()}")
            print(f"📁 Directorio de Datos: {cls.DATA_DIR}")

# Instancia global de configuración
settings = Settings()
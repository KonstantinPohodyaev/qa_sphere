'''
Конфигурация приложения
'''
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    '''Настройки приложения'''
    
    PROJECT_NAME: str = 'Pipeline Management Platform'
    VERSION: str = '1.0.0'
    DESCRIPTION: str = 'Платформа запуска и мониторинга бизнес-пайплайнов'
    API_V1_STR: str = '/api/v1'
    
    # База данных PostgreSQL
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = 'omd_user'
    POSTGRES_PASSWORD: str = 'omd_password'
    POSTGRES_DB: str = 'omd_db'
    
    @property
    def DATABASE_URL(self) -> str:
        '''Формирование URL для подключения к PostgreSQL'''
        return f'postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ['http://localhost:3000', 'http://localhost:8000']
    
    # JWT (если будет использоваться)
    SECRET_KEY: str = 'your-secret-key-change-in-production'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = '.env'
        case_sensitive = True


settings = Settings()

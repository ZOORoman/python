from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    
    @property
    def DATABESE_URL_asyncpg(self):
        
    @property
    def DATABESE_URL_psycopg(self):
        
    model_config = SettingsConfigDict(env_file=".env")
        
settings = Settings()
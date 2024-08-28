from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

global APP_PATH
# Take fixed file path, and not the relative file path
APP_PATH = os.path.dirname(os.path.realpath(__file__))

# ENVIRONMENT = "LOCAL"
# ENVIRONMENT = "SIT"
ENVIRONMENT = "PROD"

if ENVIRONMENT != "PROD":
    env_prefix = f"{ENVIRONMENT}_"
else:
    env_prefix = f""


class Settings(BaseSettings):
    PROJECT_NAME: str = "OCR System"
    API_PREFIX: str = ""
    
    MONGODB_USERNAME: str = "ocr"
    MONGODB_PASSWORD: str = "ocr"
    MONGODB_URL: str = "localhost:27018"
    MONGODB_DATABASE: str = "ocr-system"

    KAFKA_INTERNAL: str = "localhost:9092"
    KAFKA_USERNAME: str = "admin"
    KAFKA_PASSWORD: str = "admin"
    KAFKA_TOPIC: str = "test"
    KAFKA_CONSUMER_GROUP: str = "consumer-group"
    KAFKA_NOTI_TOPIC: str = ""
    KAFKA_PASSIVE_TOPIC: str = ""
    KAFKA_PASSIVE_RETRIED_TOPIC: str = ""

    SECRET_KEY: str = ""
    ALGORITHM: str = ""

    model_config = SettingsConfigDict(
        env_prefix=env_prefix,
        env_file=".env",
        extra="ignore",
    )

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        uri = "mongodb://{}:{}@{}/{}?authSource={}&retryWrites=true&w=majority".format(
            self.MONGODB_USERNAME,
            self.MONGODB_PASSWORD,
            self.MONGODB_URL,
            self.MONGODB_DATABASE,
            self.MONGODB_DATABASE
        )
        return uri

settings = Settings()
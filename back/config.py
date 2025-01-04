import os
import loguru
import dotenv
from langchain_ollama import ChatOllama


class Config:
    _instance = None

    def __init__(self):
        self.NEEDED_VARS = [
            "API_URL",
            "APP_MODEL",
            "DB_NAME"
        ]


        self.DEBUG = None
        self.API_URL = None
        self.APP_MODEL = None
        self.DB_NAME = None

        self.llm = None

    @classmethod
    def load(cls):
        if cls._instance is None:
            dotenv.load_dotenv()

            cls._instance = cls()
            cls._instance.DEBUG = os.getenv("DEBUG")
            cls._instance.API_URL = os.getenv("API_URL")

            cls._instance.APP_MODEL = os.getenv("APP_MODEL")
            cls._instance.DB_NAME = os.getenv("DB_NAME")

            cls._instance.validate()
            cls._instance.load_llm()
        return cls._instance

    def validate(self):
        missing_vars = [var for var in self.NEEDED_VARS if not getattr(self, var)]
        if missing_vars:
            loguru.logger.error(f"Missing environment variables: {missing_vars}")
            exit(0)

    def load_llm(self):
        self.llm = ChatOllama(
                    model = self.APP_MODEL,
                    temperature = 0.8,
                    num_predict = 256,
                )


config = Config.load()

def get_config():
    return config

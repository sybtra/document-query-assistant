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
            "DB_NAME",
            "MODEL_BASE_URL"
        ]


        self.DEBUG = None
        self.API_URL = None
        self.APP_MODEL = None
        self.DB_NAME = None
        self.MODEL_BASE_URL = None

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
            cls._instance.MODEL_BASE_URL = os.getenv("MODEL_BASE_URL")

            cls._instance.validate()
            cls._instance.load_llm()
        return cls._instance

    def validate(self):
        missing_vars = [var for var in self.NEEDED_VARS if not getattr(self, var)]
        if missing_vars:
            loguru.logger.error(f"Missing environment variables: {missing_vars}")
            exit(0)

    def load_llm(self):
        system_prompt = """You are an expert AI assistant specialized in understanding and answering questions based on provided context. Follow these guidelines:

                        1. CONTEXT ANALYSIS:
                        - Carefully analyze all provided context
                        - Focus on relevant information
                        - Identify key concepts and relationships

                        2. ANSWER FORMULATION:
                        - Be precise and factual
                        - Only use information from the provided context
                        - If context is insufficient, acknowledge limitations
                        - Structure complex answers for clarity

                        3. RESPONSE STYLE:
                        - Be concise but comprehensive
                        - Use clear, professional language
                        - Include relevant quotes when appropriate
                        - Maintain a helpful and informative tone

                        4. ACCURACY:
                        - Verify claims against context
                        - Avoid speculation beyond provided information
                        - Acknowledge when information is unclear or missing
                        - Correct any inconsistencies found in questions

                        5. SOURCE HANDLING:
                        - Reference specific parts of context when relevant
                        - Distinguish between different sources if multiple are provided
                        - Maintain context relevance throughout the response

                        Remember: Always ground your responses in the provided context and maintain high accuracy standards."""
        self.llm = ChatOllama(
                    model = self.APP_MODEL,
                    base_url=self.MODEL_BASE_URL,
                    system=system_prompt,
                    temperature=float(os.getenv("MODEL_TEMPERATURE", 0.3)),
                    num_predict=int(os.getenv("MODEL_NUM_PREDICT", 2048)),
                    options={
                        "num_ctx": int(os.getenv("MODEL_NUM_CTX", 4096)),
                        "top_k": int(os.getenv("MODEL_TOP_K", 30)),
                        "top_p": float(os.getenv("MODEL_TOP_P", 0.9)),
                        "repeat_penalty": 1.2,  # avoid repetition
                        "seed": 42        # for reproductibility
                    }
                )


config = Config.load()

def get_config():
    return config

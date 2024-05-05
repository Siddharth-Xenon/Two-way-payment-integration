import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the default .env file


class DatabaseConfig:
    DB_USERNAME: str = os.getenv("DB_USERNAME", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "8493")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_NAME: str = os.getenv("DB_NAME", "payments")
    DB_PORT: str = os.getenv("DB_PORT", "5432")


class StripeConfig:
    STRIPE_API_KEY: str = os.getenv("STRIPE_API_KEY")
    STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET")

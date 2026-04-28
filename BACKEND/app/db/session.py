from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from dotenv import load_dotenv
import os

ENV_PATH = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=ENV_PATH)
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_pg = os.getenv("POSTGRES_DB")
db_host = os.getenv("PG_HOST")

DATABASE_URL = f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:5432/{db_pg}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# if __name__ == '__main__':
#     from sqlalchemy import text

#     try:
#         with engine.connect() as connection:
#             result = connection.execute(text("SELECT 1"))
#             print("✅ Conexão com o banco funcionando!", result.scalar())
#     except Exception as e:
#         print("❌ Erro ao conectar no banco:", e)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Creamos la URL de conexión para SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./notes.db"

# Creamos el engine de SQLAlchemy
# El argumento check_same_thread es necesario para SQLite específicamente
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Creamos la SessionLocal que usaremos para hacer queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# clase base para nuestros modelos
Base = declarative_base()

# función para obtener la sesión local
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
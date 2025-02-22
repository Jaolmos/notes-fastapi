import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, get_db
from main import app

# Configuramos la base de datos en memoria para testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Creamos el engine para la base de datos de testing
engine = create_engine(
   SQLALCHEMY_DATABASE_URL,
   connect_args={"check_same_thread": False},
   poolclass=StaticPool,
)

# Creamos la sesión de testing
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db():
   """Fixture que proporciona una base de datos de prueba"""
   Base.metadata.create_all(bind=engine)
   try:
       db = TestingSessionLocal()
       yield db
   finally:
       db.close()
       Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
   """Fixture que proporciona un cliente de prueba"""
   def override_get_db():
       try:
           yield test_db
       finally:
           test_db.close()
   
   app.dependency_overrides[get_db] = override_get_db
   yield TestClient(app)
   app.dependency_overrides.clear()
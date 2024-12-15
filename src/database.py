from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de la base de datos SQLite
DATABASE_URL = "sqlite:///task.db"

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, echo=True)

# Crear una clase sessionmaker para gestionar las sesiones
Session = sessionmaker(bind=engine)

# Crear una base para los modelos
Base = declarative_base()

# Crear la sesión
session = Session()


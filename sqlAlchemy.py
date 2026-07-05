from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi import FastAPI, Depends

# Create the FastAPI application
app = FastAPI()

# Database connection URL (SQLite database named test.db)
DATABASE_URL = "sqlite:///./test.db"

# Create a connection (engine) to the database
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed only for SQLite to allow multiple threads
)

# Creates new database sessions whenever required
sessionLocal = sessionmaker(bind=engine)

# Base class that all database models (tables) will inherit from
Base = declarative_base()


# Define a table named "todos"
class Todo(Base):
    __tablename__ = "todos"  # Name of the table in the database

    # Define table columns
    id = Column(Integer, primary_key=True, index=True)  # Unique ID
    title = Column(String)                              # Task title
    completed = Column(String)                          # Completion status


# Create the table in the database if it doesn't already exist
Base.metadata.create_all(bind=engine)


# Dependency function to provide a database session
def get_db():
    db = sessionLocal()          # Open a database session
    try:
        yield db                 # Give the session to the API
    finally:
        db.close()               # Always close the session after use


# Home endpoint
@app.get("/")
def home(db: Session = Depends(get_db)):
    # FastAPI automatically calls get_db() and injects the session into 'db'
    return {
        "message": "DB connected fine"
    }
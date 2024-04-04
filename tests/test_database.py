from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, InvalidRequestError
from app.config import EnvironmentVariables
from app.database import SessionLocal, get_db

def test_database_connection():
	try:
		engine = create_engine(EnvironmentVariables().DATABASE_URL)
		connection = engine.connect()
	except OperationalError:
		self.fail("Database connection failed!")
	else:
		connection.close()

def test_session_creation():
	try:
		session = SessionLocal()
	except OperationalError:
		self.fail("Session creation failed!")
	else:
		session.close()

def test_get_db():
    try:
        db = next(get_db())
        assert db
    except OperationalError:
        self.fail("Database connection failed!")
    except InvalidRequestError:
        self.fail("Session creation failed!")
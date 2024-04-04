import pytest
from app.database import SessionLocal
from app.schemas.user import UserCreate, User as UserSchema, UserType
from app.models.user import User
from unittest.mock import Mock, patch
from app.crud import user as user_crud

mock_user = Mock(spec=UserSchema, **{
	'id': "1",
	'email': "test@example.com",
	'first_name': "Test",
	'last_name': "User",
	'type': UserType.admin,
})

mock_user_db = Mock(spec=User, **{
	'id': mock_user.id,
	'email': mock_user.email,
	'first_name': mock_user.first_name,
	'last_name': mock_user.last_name,
	'type': mock_user.type.value,
	'password_hash': "$2b$12$t6lklpVWbH2G4q8v.wa50OT7ddh4m5oREa3MyWEAyW6xLwmSuV9mi"
})

def test_create_user():
	session = SessionLocal()
	new_user = UserCreate(
		email="test@example.com",
		first_name="Test",
		last_name="User",
		password="password",
		type=UserType.admin
	)
	with patch.object(session, 'add'), patch.object(session, 'commit'), patch.object(session, 'refresh', side_effect=lambda x: setattr(x, 'id', '1')):
		result = user_crud.create_user(session, new_user)
	assert result.email == "test@example.com"
	assert result.id == "1"

def test_get_all_users():
	session = SessionLocal()
	mock_query = Mock()
	mock_query.all.return_value = [mock_user]
	with patch.object(session, 'query', return_value=mock_query):
		result = user_crud.get_all_users(session)
	assert len(result) == 1

def test_get_user_by_id():
	session = SessionLocal()
	mock_query = Mock()
	mock_query.filter.return_value = mock_query
	mock_query.first.return_value = mock_user
	with patch.object(session, 'query', return_value=mock_query):
		result = user_crud.get_user_by_id(session, "1")
	assert result.id == "1"

def test_update_user():
	session = SessionLocal()
	mock_query = Mock()
	mock_query.filter.return_value = mock_query
	mock_query.first.return_value = mock_user_db
	update_user = mock_user
	update_user.email = "test2@example.com"
	with patch.object(session, 'query', return_value=Mock(first=Mock(return_value=mock_user_db))), patch.object(session, 'commit'), patch.object(session, 'refresh'):
		result = user_crud.update_user(session, update_user.id, update_user)
	assert result.email == "test2@example.com"
	
def test_delete_user():
    session = SessionLocal()
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = mock_user_db
    with patch.object(session, 'query', return_value=mock_query), patch.object(session, 'commit'), patch.object(session, 'delete') as mock_delete:
        user_crud.delete_user(session, mock_user_db.id)
        mock_delete.assert_called_once_with(mock_user_db)

def test_authenticate_user():
	session = SessionLocal()
	mock_query = Mock()
	mock_query.filter.return_value = mock_query
	mock_query.first.return_value = mock_user_db
	with patch.object(session, 'query', return_value=mock_query):
		result = user_crud.authenticate_user(session, mock_user_db.email, 'password')
	assert isinstance(result, User)

def test_fail_to_authenticate_user():
	session = SessionLocal()
	mock_query = Mock()
	mock_query.filter.return_value = mock_query
	mock_query.first.return_value = mock_user_db
	with patch.object(session, 'query', return_value=mock_query):
		result = user_crud.authenticate_user(session, mock_user_db.email, 'wrong_password')
	assert result == False

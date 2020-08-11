import pytest
import bcrypt
import json

from app                    import create_app
from sqlalchemy             import create_engine, text
from datetime               import date, datetime, timedelta

from configs.test_config    import local_test_config
from setup_test_data        import setup_test_data


def json_default(value): 
    if isinstance(value, datetime): 
        return value.strptime('%Y-%m-%d') 
    raise TypeError('not JSON serializable')


database = create_engine(local_test_config['DB_URL'], encoding='utf-8', max_overflow = 0)

@pytest.fixture
def api():
    app = create_app(local_test_config)
    app.config['TEST'] = True
    api = app.test_client()

    return api

def setup_function():
    setup_test_data(database)

def teardown_function():
    database.execute(text('SET FOREIGN_KEY_CHECKS=0'))
    database.execute(text('TRUNCATE users'))
    database.execute(text('SET FOREIGN_KEY_CHECKS=1'))


## ------------------------ test 용 functions ------------------------

## 테스트를 위한 로그인
def get_access_token(api):
    resp = api.post(
        '/user-management/auth/login',
        data = json.dumps({
            'user_email' : 'test_email',
            'user_pw' : 'test_password'
        }),
        content_type = 'application/json'
    )

    resp_json = json.loads(resp.data.decode('utf-8'))
    access_token = resp_json['access_token']

    return access_token


## 유저 패스워드 호출
def get_user_pw(user_id):
    row = database.execute(text('''
        SELECT hashed_pw
        FROM users
        WHERE id = :user_id
    '''),{
        'user_id' : user_id
    }).fetchone()

    return {
        'hashed_pw': row['hashed_pw']
    } if row else None



## ------------------------ B01 ------------------------

def test_user_login(api):
    resp = api.post(
        '/user-management/auth/login',
        data = json.dumps({
            'user_email' : 'test_email',
            'user_pw' : 'test_password'
        }),
        content_type = 'application/json'
    )

    assert b"access_token" in resp.data


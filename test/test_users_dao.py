import pytest
import bcrypt
import json

from app                    import create_app
from sqlalchemy             import create_engine, text

from configs.test_config    import local_test_config
from setup_test_data        import setup_test_data


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



## -----------------------------


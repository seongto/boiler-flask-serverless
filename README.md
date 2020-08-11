# boiler-flask-serverless

## clone 후 만들어야 할 것들

- configs 폴더를 생성한 후 config.js 와 test_config.py 를 생성한다.
  
  config.js : 프로덕션 혹은 개발 서버를 배포할 때 서버리스 환경 변수(DB정보 등) 전달을 위한 파일. 아래는 샘플코드
  ```
  const dev_db = {
      host: 'host',
      user: 'root',
      password: 'password',
      port: 3306,
      database: 'db_name',
  }

  const prod_db = {
      host: 'host',
      user: 'root',
      password: 'password',
      port: 3306,
      database: 'db_name',
  }

  module.exports.DATABASE_CONFIG = (serverless) => ({
      dev: {
          DB_URL: `mysql+mysqlconnector://${dev_db['user']}:${dev_db['password']}@${dev_db['host']}:${dev_db['port']}/${dev_db['database']}?charset=utf8`,
          JWT_SECRET_KEY_A: 'key_a',
          JWT_SECRET_KEY_B: 'key_b'
      },

      prod: {
          DB_URL: `mysql+mysqlconnector://${prod_db['user']}:${prod_db['password']}@${prod_db['host']}:${prod_db['port']}/${prod_db['database']}?charset=utf8`,
          JWT_SECRET_KEY_A: 'key_a',
          JWT_SECRET_KEY_B: 'key_b'
      }
  });
  ```
  
  test_config.py : 로컬 테스트 용 로컬 디비 경로 전달용 파일. 아래는 샘플코드
  ```
  local_test_db = {
      "user": "user",
      "password": "password",
      "host": "localhost",
      "port": 3306,
      "database": "db_name_test",
  }

  local_test_config = {
      "DB_URL": f"mysql+mysqlconnector://{local_test_db['user']}:{local_test_db['password']}@{local_test_db['host']}:{local_test_db['port']}/{local_test_db['database']}?charset=utf8",
      "JWT_SECRET_KEY_A": "keyA",
      "JWT_SECRET_KEY_B": "keyB",
  }
  ```
  
  

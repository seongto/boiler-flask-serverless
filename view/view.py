import jwt
import re
import inspect

from flask          import request, jsonify, current_app, Response, g
from flask.json     import JSONEncoder
from functools      import wraps
from sqlalchemy     import text
from datetime       import datetime, timedelta

from assets         import request_data_check


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):         # pylint: disable=E0202
        if isinstance(obj, set):
            return list(obj)

        return JSONEncoder.default(self, obj)



## ---------------------- Decorators ------------------------------

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try: 
            access_token = request.headers.get('Authorization')

            if access_token is not None :
                try :
                    payload = jwt.decode(access_token, current_app.config['JWT_SECRET_KEY_A'], algorithms=['HS256'])
                except jwt.InvalidTokenError :
                    payload = None
                
                if payload is None :
                    raise Exception('payload is None')
                
                admin_id     = payload['auth_id']
                g.admin_id   = admin_id

            else:
                raise Exception('access_token is missing!')

        except Exception as e :
            print(f"PROBLEM / view / {inspect.currentframe().f_code.co_name} : ", e)
            return Response(status=401)

        return f(*args, **kwargs)
    return decorated_function

## -------------------- API ----------------------------

def create_endpoints(app, services):
    auth_service = services.auth_service
    sample_service = services.sample_service


    ## API doc No.
    @app.route('/user-management/auth/login', methods=['POST'])
    def user_login():
        try:
            credential = request.json
            check_result = request_data_check(credential, {
                'user_email': (str, False), 
                'user_pw': (str, False)
            })
            assert check_result.error == None, check_result.data

            authorized = auth_service.user_login_auth(credential)
            assert authorized.error == None, authorized.data
            
            token = auth_service.generate_access_token_user(authorized.data.id)
            assert token.error == None, token.data
            
            data = {
                'user_name': authorized.data.user_name,
                'access_token': token.data
            }

        except AssertionError as e:
            print(f"PROBLEM / view / {inspect.currentframe().f_code.co_name} : ", e)
            return jsonify({"comment": e.args[0].msg}), e.args[0].status

        except Exception as e:
            print(f"PROBLEM / view / {inspect.currentframe().f_code.co_name} : ", e)
            return jsonify({"comment": "Internal Server Error"}), 500

        else:
            return jsonify(data), 200





    ## ----------------- samples -------------------

    ## GET Sample
    @app.route('/sampleget', methods=['GET'])
    @admin_login_required
    def sample_get():
        try:
            result = sample_service.service_sample_get()
            assert result.error == None, result.data

        except AssertionError as e:
            print(f"PROBLEM / view / {inspect.currentframe().f_code.co_name} : ", e)
            return jsonify({"comment": e.args[0].msg}), e.args[0].status

        except Exception as e:
            print(f"PROBLEM / view / {inspect.currentframe().f_code.co_name} : ", e)
            return jsonify({"comment": "Internal Server Error"}), 500

        else:
            return jsonify({"sample" : result.data}), 200

    
    ## POST sample
    @app.route('/samplepost', methods=['POST'])
    @admin_login_required
    def create_brand_story():
        try:
            session = current_app.Session()
            credential = request.json
            check_result = request_data_check(credential, {
                "param1" : (str, False),
                "param2" : (str, False)
            })
            assert check_result.error == None, check_result.data

            result = sample_service.sample_service_post(credential, session)
            assert result.error == None, result.data

        except AssertionError as e:
            session.rollback()
            print(f"PROBLEM / view / {inspect.currentframe().f_code.co_name} : ", e)
            return jsonify({"comment": e.args[0].msg}), e.args[0].status
                
        except Exception as e:
            session.rollback()
            print(f"PROBLEM / view / {inspect.currentframe().f_code.co_name} : ", e)
            return jsonify({"comment": "Internal Server Error"}), 500

        else:
            session.commit()
            return jsonify({"sample" : result.data}), 200

        finally:
            session.close()

    ## ping test
    @app.route('/ping', methods=['GET'])
    def ping_test():
        return 'ping success', 200

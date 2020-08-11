import re
import jwt
import bcrypt
import string
import inspect

from datetime               import datetime, timedelta
from flask                  import g, current_app

from assets                 import Resp, ErrorData


class AuthService:
    def __init__(self, models, config):
        self.models = models
        self.config = config


    ## ------- 내부 메소드 : 외부 호출없이 내부에서만 호출하는 메소드 -------

    def objs_to_dic(self, arr, params=None):
        result = []

        if not params:
            for item in arr :
                result.append(item.export_dict())
        else:
            for item in arr :
                result.append(item.export_dict(params))
        
        return result



    ## ------------------ login ------------------- 

    def user_login_auth(self, credential, session=None):        
        try :
            email = credential["user_email"]
            password = credential["user_pw"]

            user_credential = self.models.users_dao.get_user_by_email(email)
            assert user_credential, ErrorData('no email data', '서버에 유저 정보가 없거나 잘못된 암호입니다.', 400)

            check_pw = bcrypt.checkpw( 
                password.encode("UTF-8"), 
                user_credential.hashed_pw.encode("UTF-8")
            )
            assert check_pw, ErrorData('incorrect password', '서버에 유저 정보가 없거나 잘못된 암호입니다.', 400)
        
        except AssertionError as e:
            print(f"PROBLEM / service / {inspect.currentframe().f_code.co_name} : ", e)
            return Resp(e, e.args[0])

        except Exception as e:
            print(f"PROBLEM / service / {inspect.currentframe().f_code.co_name} : ", e)
            return Resp(e, ErrorData(f'{inspect.currentframe().f_code.co_name} service failed', f'{inspect.currentframe().f_code.co_name} service failed', 500))

        else: 
            return Resp( None, user_credential )


    def generate_access_token_user(self, user_id, session=None):
        try: 
            payload = {
                "auth_id": user_id,
                "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
            }

            token = jwt.encode(payload, self.config["JWT_SECRET_KEY_A"], "HS256")
            assert token, ErrorData('generating access token failed', 'generating access token failed', 500)

        except AssertionError as e:
            print(f"PROBLEM / service / {inspect.currentframe().f_code.co_name} : ", e)
            return Resp(e, e.args[0])

        except Exception as e:
            print(f"PROBLEM / service / {inspect.currentframe().f_code.co_name} : ", e)
            return Resp(e, ErrorData(f'{inspect.currentframe().f_code.co_name} service failed', f'{inspect.currentframe().f_code.co_name} service failed', 500))

        else:
            return Resp( None, token.decode("UTF-8"))

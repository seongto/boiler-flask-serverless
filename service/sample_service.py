import re
import jwt
import bcrypt
import string
import inspect

from datetime               import datetime, timedelta
from flask                  import g, current_app

from assets                 import Resp, ErrorData


class SampleService:
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


    ## ------- samples ------------

    def sample_service_get(self, session=None):
        try:
            result = self.models.samples_dao.samples_dao_get()
            assert result, ErrorData('exp', 'msg', 500)

        except AssertionError as e:
            print(f"PROBLEM / service / {inspect.currentframe().f_code.co_name} : ", e)
            return Resp(e, e.args[0])

        except Exception as e:
            print(f"PROBLEM / service / {inspect.currentframe().f_code.co_name} : ", e)
            return Resp(e, ErrorData(f'{inspect.currentframe().f_code.co_name} service failed', f'{inspect.currentframe().f_code.co_name} service failed', 500))

        else:
            return Resp(None, result)

    
    def sample_service_post(self, credential, session):
        try:
            result = self.models.samples_dao.samples_dao_post(session)
            assert result, ErrorData('exp', 'msg', 500)

        except AssertionError as e:
            print(f"PROBLEM / service / {inspect.currentframe().f_code.co_name} : ", e)
            return Resp(e, e.args[0])

        except Exception as e:
            print(f"PROBLEM / service / {inspect.currentframe().f_code.co_name} : ", e)
            return Resp(e, ErrorData(f'{inspect.currentframe().f_code.co_name} service failed', f'{inspect.currentframe().f_code.co_name} service failed', 500))

        else:
            return Resp(None, result)

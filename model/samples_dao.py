import re
import inspect

from sqlalchemy     import text, exc
from flask          import current_app
from dataclasses    import dataclass

from .super_model   import SuperModel


@dataclass(order=True)
class Sample(SuperModel) :
    id:int = None
    sample:str = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    

class SamplesDao :
    def __init__(self, database):
        self.db = database


    def samples_dao_get(self, session=None):
        try:
            sample = 'sample'
            
            return sample

        except Exception as e:
            print(f"PROBLEM / model / {inspect.currentframe().f_code.co_name} : ", e)
            return None


    def samples_dao_post(self, session):
        try:
            sample = 'sample'
            
            return sample

        except Exception as e:
            print(f"PROBLEM / model / {inspect.currentframe().f_code.co_name} : ", e)
            return None

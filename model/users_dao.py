import re
import inspect

from sqlalchemy     import text, exc
from flask          import current_app
from dataclasses    import dataclass

from .super_model   import SuperModel


@dataclass(order=True)
class User(SuperModel) :
    id:int = None
    name:str = None
    hashed_pw:str = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    

class UsersDao :
    def __init__(self, database):
        self.db = database

    def get_user_by_email(self, input_email, session=None):
        try:
            if session :
                this_db = session
            else :
                this_db = self.db
                
            row = this_db.execute(text('''
                SELECT 
                    id,
                    name,
                    hashed_pw
                FROM users
                WHERE email = :email
                AND is_deleted = false
            '''), {'email': input_email}).fetchone()

            return User(
                id = row['id'],
                user_name = row['name'],
                hashed_pw = row['hashed_pw']
            ) if row else None

        except Exception as e:
            print(f"PROBLEM / model / {inspect.currentframe().f_code.co_name} : ", e)
            return None


    def get_dao_sample(self, session=None):
        try:
            sample = 'sample'
            
            return sample

        except Exception as e:
            print(f"PROBLEM / model / {inspect.currentframe().f_code.co_name} : ", e)
            return None

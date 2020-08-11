from datetime       import datetime, timedelta
from .namedtuples   import Resp, ErrorData


def request_data_check(data, keyTypes):
    try: 
        for item in keyTypes:
            if keyTypes[item][0] == datetime:
                data[item] = datetime.strptime(data[item], "%Y-%m-%d %H:%M:%S")

            if data[item] :
                assert keyTypes[item][0] == type(data[item]), item
            else :
                ## keyTypes[item][1] = nullable ( True 일 경우에만 null 허용.) 
                if keyTypes[item][1] == False :
                    assert keyTypes[item][0] == type(data[item]), item

    except AssertionError as e:
        return Resp(e, ErrorData(f'value type Error, {e.args[0]} key', f'{e.args[0]} 키의 value 타입이 잘못되었습니다.', 400))
    except ValueError as e:
        return Resp(e, ErrorData(f'value type Error, {e.args[0]} key', f'{e.args[0]} 키의 value 타입이 잘못되었습니다.', 400))
    except KeyError as e:
        return Resp(e, ErrorData(f'request has no key, {e.args[0]}', f'{e.args[0]} 키를 찾을 수 없습니다.', 400))
    except Exception as e:
        return Resp(e, ErrorData(e.args[0], 'data check error', 500))
    else:
        return Resp(None, data)
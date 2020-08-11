from collections    import namedtuple

## AssertionError 시에 상세한 에러 데이터를 담을수 있는 namedtuple.
## exp : 추후 error logging을 위한 실제 에러 기록
## msg : 프론트로 보내줄 response error message 
## status : error시 프론트로 보낼 HTTP status code
ErrorData = namedtuple('ErrorData', 'exp, msg, status')

## 상위 레이어에서 데이터 검사를 위한 데이터 전송포맷 namedtuple
## error : error 가 없을 경우 None, 그 외엔 assert 검사에서 AssertionError 발생
## data : error 시엔 ErrorData가 포함되며, 정상작동 시엔 데이터 전달
Resp = namedtuple('Resp', 'error, data' )
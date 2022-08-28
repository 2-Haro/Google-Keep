from flask import Blueprint, g, abort
from flask_restx import Api
from .user import ns as UserNamespace
from .memo import ns as MemoNamespace
from .label import ns as LabelNamespace
from functools import wraps

def check_session(func): # 12. 세션 기반 인증 흐름 구현: 로그인 여부에 따라 api 페이지 접근 가능 여부를 판단하는 함수 -> func 함수를 받아서
  @wraps(func) # 12. 세션 기반 인증 흐름 구현: 데코레이터 패턴으로 만든 파이썬 함수를 API를 init할 때 정의해주면 로그인되어 있지 않을 때 api 페이지에 접근할 수 없도록 하는 기능을 restx가 지원한다
  def __wrapper(*args, **kwargs): # 12. 세션 기반 인증 흐름 구현: 위치 인자, 키워드 인자를 받는다
    if not g.user: # 12. 세션 기반 인증 흐름 구현: 로그인되어 있지 않다면
      abort(401) # 12. 세션 기반 인증 흐름 구현: 인증되지 않은 유저이므로 api 페이지에 접근 불가(401: Unauthorized)
    return func(*args, **kwargs) # 12. 세션 기반 인증 흐름 구현: func 함수 실행
  return __wrapper # 12. 세션 기반 인증 흐름 구현: func 함수를 실행한 함수 return
  
blueprint = Blueprint( # 8. API 문서 자동화: Blueprint init
  'api',
  __name__,
  url_prefix='/api' # 8. API 문서 자동화: prefix로 api를 가지게 되는데, 여기에 namespace가 추가되기 때문에 user, memo, label 엔드포인트에 기본적으로 api가 붙고 그 하위에 정의한 namespace(users, memos, labels)가 붙는다
  )

api = Api( # 8. API 문서 자동화: API(restx) init
  blueprint, # 8. API 문서 자동화: blueprint
  title='Google Keep API', # 8. API 문서 자동화: API 문서 제목
  version='1.0', # 8. API 문서 자동화: API 문서 버전
  doc='/docs', # 8. API 문서 자동화: API 문서 경로(http://127.0.0.1:5000/api/docs)
  decorators=[check_session], # 12. 세션 기반 인증 흐름 구현: 데코레이터 패턴으로 만든 파이썬 함수 정의
  description='Welcome to my API docs' # 8. API 문서 자동화: API 문서 설명
)

api.add_namespace(UserNamespace) # 8. API 문서 자동화: Blueprint에 Namespace(User) 추가
api.add_namespace(MemoNamespace) # 13. 메모 기본 기능 구현: Blueprint에 Namespace(Memo) 추가
api.add_namespace(LabelNamespace) # 16. 라벨 기본 기능 구현: Blueprint에 Namespace(Lable) 추가
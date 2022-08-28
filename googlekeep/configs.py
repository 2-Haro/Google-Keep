import os # 11. 유닛 테스트와 TDD: os 모듈 import
BASE_PATH = os.path.dirname(os.path.abspath(__file__)) # 11. 유닛 테스트와 TDD: 현재 파이썬 파일이 가지는 절대경로의 디렉토리명

class Config(object): # 10. Flask Configs: Class로 config 관리
  '''Flask Config'''
  SECRET_KEY = 'secretkey' # 2. CSRF 방어: CSRF 토큰 자체가 암호화되어 있기 때문에 특정 key(SECRET_KEY)가 정의되어 있어야 한다 -> Flask CSRF Token이 정상적으로 만들어진다
  SESSION_COOKIE_NAME = 'googlekeep' # 5. 로그인 기능 구현: session cookie 이름을 googlekeep으로 설정
  SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/googlekeep?charset=utf8' # 6. 데이터베이스: SQLALCHEMY_DATABASE_URI 설정
  SQLALCHEMY_TRACK_MODIFICATIONS = False # 6. 데이터베이스: SQLAlchemy의 이벤트를 처리하는 옵션 -> 추가적인 메모리를 필요로 하기 때문에 꺼둔다
  SWAGGER_UI_DOC_EXPANSION = 'list' # 8. API 문서 자동화: API 조회시 펼침 상태로 UI 노출
  USER_STATIC_BASE_DIR = 'user_images' # 15. 메모 기능 업그레이드: 이미지 보관 장소 -> 공통적으로 사용 (static 폴더 하위의 user_images 폴더)

  def __init__(self): # 18. Dockerizing: config.py가 initialize 될 때 오류가 발생하면 항상 재시동
    db_env = os.environ.get('SQLALCHEMY_DATABASE_URI') # 18. Dockerizing: .env 파일에서 정의한 URI가 docker-compose 파일의 환경변수로 정의되고, Python Application에서 환경변수로 전달(환경변수 가져오기)
    if db_env: # 18. Dockerizing: db_env(환경변수)가 정의가 되어 있다면
      self.SQLALCHEMY_DATABASE_URI = db_env # 18. Dockerizing: SQLALCHEMY_DATABASE_URI를 .env 파일에서 init된 값으로 치환(환경변수로 정의된 env로 반영)

class DevelopmentConfig(Config): # 10. Flask Configs: Development 환경(Config 상속)
  '''Flask Config for Dev'''
  DEBUG = True # 1. 템플릿 엔진 기초: 디버그 모드(개발 환경)
  SEND_FILE_MAX_AGE_DEFAULT = 1 # 1. 템플릿 엔진 기초: 디버깅 모드에서 캐시 제거(1초로 설정)
  # TODO: 프론트 호출시 처리
  WTF_CSRF_ENABLED = False # 8. API 문서 자동화: 400 error(CSRF token is missing) -> POST Method를 보낼 때 CSRF 토큰을 함께 씌워서 보내줬는데, 현재 문서에서는 이러한 작업을 하지 않았기 때문에 오류 발생 -> 개발 환경이기 때문에 이를 무시하도록 하는 코드(호출을 할 때 CSRF 토큰이 없어도 검증처리를 하지 않곘다는 의미)

class TestingConfig(DevelopmentConfig): # 11. 유닛 테스트와 TDD: Testing 환경(개발 환경 상속)
  __test__ = False # 11. 유닛 테스트와 TDD: 'test'로 시작하지만, Testcase를 타지 않도록 설정
  TESTING = True # 11. 유닛 테스트와 TDD: Testing 환경
  SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_PATH, "sqlite_test.db")}' # 11. 유닛 테스트와 TDD: configs.py와 동일한 경로에 sqlite_test.db 파일명을 가지는 DB 생성

class ProductionConfig(Config): # 10. Flask Configs: Production 환경(개발 환경 상속)
  pass
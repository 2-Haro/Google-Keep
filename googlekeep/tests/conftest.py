# 11. 유닛 테스트와 TDD: conftest.py -> 테스트에서 모듈(디렉토리)별로 fixture(pytest.fixture)를 관리하도록 하는 역할 -> 디렉토리 내에서 fixture를 공통적으로 사용할 수 있도록 공유해주는 역할  
import sys
sys.path.append('.') # 11. 유닛 테스트와 TDD: googlekeep에 있는 모듈을 가져오기 위해 사용(특정한 디렉토리에 있는 모듈을 불러와서 사용하고 싶을 때 sys.path.append() 사용)

from googlekeep.configs import TestingConfig # 11. 유닛 테스트와 TDD: TestingConfig import
from googlekeep import create_app, db # 11. 유닛 테스트와 TDD: create_app 함수, db import
from googlekeep.models.user import User as UserModel # 11. 유닛 테스트와 TDD: User 모델 import
from googlekeep.models.memo import Memo as MemoModel
import pytest # 11. 유닛 테스트와 TDD: pytest import
import os, shutil

@pytest.fixture(scope='session') # 11. 유닛 테스트와 TDD: Testcase 내에서 공통적으로 사용할 수 있는 자원으로 설정(user_data)
def user_data(): # 11. 유닛 테스트와 TDD: Test를 위한 더미 유저 데이터
  yield dict(
    user_id='tester',
    user_name='tester',
    password='tester'
  )

@pytest.fixture(scope='session') # 13. 메모 기본 기능 구현: Testcase 내에서 공통적으로 사용할 수 있는 자원으로 설정(user_data)
def memo_data(): # 13. 메모 기본 기능 구현: Test를 위한 더미 메모 데이터
  yield dict( # 13. 메모 기본 기능 구현: nullable하지 않은 데이터인 제목과 내용을 넣어주고, user_id는 현재 식별 불가능하므로 아래 app 함수에서 추가
    title='title',
    content='content'
  )

@pytest.fixture(scope='session') # 11. 유닛 테스트와 TDD: Testcase 내에서 공통적으로 사용할 수 있는 자원 Testcase 내에서 공통적으로 사용할 수 있는 자원으로 설정(app) # 12. 세션 기반 인증 흐름 구현: scope='session' -> 전역적으로 fixture 관리 -> 세션에서 fixture 공유(fixture가 test session 동안 1회 생성)
def app(user_data, memo_data): # 11. 유닛 테스트와 TDD: client 세분화를 위한 app 함수 # 11. 유닛 테스트와 TDD: user_data: 상위에서 만든 fixture
  app = create_app(TestingConfig()) # 11. 유닛 테스트와 TDD: __init__.py에 있는 create_app 함수를 사용해서 Testing 환경으로 app을 만든다
  with app.app_context(): # 11. 유닛 테스트와 TDD: DB 데이터 컨트롤
    db.drop_all() # 11. 유닛 테스트와 TDD: DB 초기화
    db.create_all() # 11. 유닛 테스트와 TDD: DB 생성 -> flask db upgrade 처럼 동작
    user = UserModel(**user_data) # 11. 유닛 테스트와 TDD: 더미 유저 데이터를 UserModel에 넣어서 user에 할당
    db.session.add(user) # 13. 메모 기본 기능 구현: DB에 더미 유저 데이터 추가
    db.session.flush() # 13. 메모 기본 기능 구현: flush -> 트랜잭션을 DB로 전송(커밋 X) -> user.id를 받아오기 위해 실행
    memo_data['user_id'] = user.id # 13. 메모 기본 기능 구현: user가 생성된 이후에 user의 id를 받아서 메모의 user_id로 설정
    db.session.add(MemoModel(**memo_data)) # 13. 메모 기본 기능 구현: 더미 메모 데이터를 MemoModel에 넣어서 DB에 추가
    db.session.commit() # 11. 유닛 테스트와 TDD: DB commit
    yield app # 11. 유닛 테스트와 TDD: return 대신 yield 사용 -> 작업을 나눠서 관리 가능
    # 12. 세션 기반 인증 흐름 구현: 불필요 DB 정리 및 삭제
    # /static/user_images/tester(==user_id)
    path = os.path.join( # 15. 메모 기능 업그레이드: Testcase(이미지 추가, 업데이트) 작성 후, Testcase가 끝나면 user_images 폴더 내에 Testcase로 생성되는 이미지 삭제 위한 경로
      app.static_folder, # 15. 메모 기능 업그레이드: static 폴더
      app.config['USER_STATIC_BASE_DIR'], # 15. 메모 기능 업그레이드: user_images 폴더
      user_data['user_id'] # 15. 메모 기능 업그레이드: Testcase user_id인 tester 폴더 -> static/user_images내에 user_id 별로 폴더 분류(static/user_images/tester)
    )
    # 15. 메모 기능 업그레이드: shutil 모듈 -> 파일 및 디렉토리 작업을 수행하는데 기본적인 모듈로써 파일 및 디렉토리에 대해서 복사, 이동, 삭제 등에 관한 기능 제공
    shutil.rmtree(path, True) # 15. 메모 기능 업그레이드: shutil.rmtree() -> 지정된 폴더와 하위 디렉토리 폴더, 파일을 전부 삭제 # 디렉토리가 없어도 에러가 발생하지 않도록 True 처리
    db.drop_all() # 12. 세션 기반 인증 흐름 구현: DB 초기화
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace( # 12. 세션 기반 인증 흐름 구현: DB 경로
      'sqlite:///', # 12. 세션 기반 인증 흐름 구현: sqlite:///를
      '' # 12. 세션 기반 인증 흐름 구현: 빈문자로 replace -> configs.py의 TestingConfig에 있는 {os.path.join(BASE_PATH, "sqlite_test.db")} 경로(DB 경로)
   )
    if os.path.isfile(db_path): # 12. 세션 기반 인증 흐름 구현: db_path(DB 경로)에 파일이 있으면
      os.remove(db_path) # 12. 세션 기반 인증 흐름 구현: 해당 파일 삭제

@pytest.fixture(scope='session') # 11. 유닛 테스트와 TDD: Testcase 내에서 공통적으로 사용할 수 있는 자원 Testcase 내에서 공통적으로 사용할 수 있는 자원으로 설정(client)
def client(app, user_data): # 11. 유닛 테스트와 TDD: client 함수 생성(인자로 app과 user_data)
  with app.test_client() as client: # 11. 유닛 테스트와 TDD: with 절을 사용해서 app.test_client를 client로 호출
    # 12. 세션 기반 인증 흐름 구현: 세션 입혀주기
    with client.session_transaction() as session: # 12. 세션 기반 인증 흐름 구현: API 실행을 위해서 로그인 상태여야 하는 문제점 해결 # 요청이 실행되기 전에 세션 수정, 접근 가능 -> 트랜잭션의 끝에서 해당 세션 저장
      session['user_id'] = user_data.get('user_id') # 12. 세션 기반 인증 흐름 구현: # Set a user_id without going through the login route # user_id = tester # session에 user_id만 넣어주면 g.user에 정의(auth_route -> before_app_request())
    yield client # 11. 유닛 테스트와 TDD: 여러 Testcase에서 client를 함수 인자로 받아서 그대로 사용 가능
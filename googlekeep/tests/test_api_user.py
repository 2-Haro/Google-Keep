def test_get_users(client): # 11. 유닛 테스트와 TDD: 복수 유저 조회에 대한 Testcase
  r = client.get( # 11. 유닛 테스트와 TDD: GET Method
    '/api/users',  # 11. 유닛 테스트와 TDD: 엔드포인트 -> /api/users (모든 유저)
    follow_redirects = True # 11. 유닛 테스트와 TDD: 페이지가 다른 페이지로 리디렉션 되었을 때 그 페이지를 따라가고, 해당 페이지의 response 값을 가져온다
  )
  assert r.status_code == 200 # 11. 유닛 테스트와 TDD: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(200: OK)
  assert len(r.json) == 1 # 11. 유닛 테스트와 TDD: response의 길이 = 1 -> conftest.py에서 유저 모델 더미 데이터를 1개 넣었기 때문

def test_get_user(client, user_data): # 11. 유닛 테스트와 TDD: 단일 유저 조회에 대한 Testcase(user_data(더미 데이터)를 가져와서 넣은 데이터와 일치하는지 확인)
  r = client.get( # 11. 유닛 테스트와 TDD: GET Method
  '/api/users/1',  # 11. 유닛 테스트와 TDD: 엔드포인트 -> /api/users/1 (미리 생성된 첫번째 유저)
  follow_redirects = True # 11. 유닛 테스트와 TDD: 페이지가 다른 페이지로 리디렉션 되었을 때 그 페이지를 따라가고, 해당 페이지의 response 값을 가져온다
  )
  assert r.status_code == 200 # 11. 유닛 테스트와 TDD: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(200: OK)
  assert r.json.get('user_id') == user_data.get('user_id') # 11. 유닛 테스트와 TDD: user_id가 더미 데이터의 user_id와 같아야 한다
  assert r.json.get('user_name') == user_data.get('user_name') # 11. 유닛 테스트와 TDD: user_name이 더미 데이터의 user_name과 같아야 한다

def test_post_user(client, user_data):  # 11. 유닛 테스트와 TDD: 유저 생성에 대한 Testcase(POST Method를 통해 유저를 생성할 때도 더미 데이터 이용)
  r = client.post( # 11. 유닛 테스트와 TDD: POST Method
    '/api/users', # 11. 유닛 테스트와 TDD: 엔드포인트 -> /api/users (모든 유저)
    data = user_data # 11. 유닛 테스트와 TDD: data를 user_data(더미 데이터)로 설정
  )
  assert r.status_code == 409 # 11. 유닛 테스트와 TDD: 의도적으로 409 에러(Conflict) 발생 -> user_id는 unique해야 하므로 이미 DB에 존재하는 user_id(더미 데이터의 user_id인 tester)를 그대로 가져와서 생성하려고 하면 409 에러 발생
  new_user_data = user_data.copy() # 11. 유닛 테스트와 TDD: new_user_data에 user_data(더미 데이터) 복사
  new_user_data['user_id'] = 'tester2' # 11. 유닛 테스트와 TDD: new_user_data의 user_id를 tester2로 설정(user_name은 unique하지 않아도 되기 때문에 상관 X)

  r = client.post( # 11. 유닛 테스트와 TDD: POST Method
    '/api/users', # 11. 유닛 테스트와 TDD: 엔드포인트 -> /api/users (모든 유저)
    data = new_user_data # 11. 유닛 테스트와 TDD: data를 new_user_data(user_id = tester2)로 설정
  )
  assert r.status_code == 201 # 11. 유닛 테스트와 TDD: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(201: Created)
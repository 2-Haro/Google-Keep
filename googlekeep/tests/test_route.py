def test_auth(client): # 11. 유닛 테스트와 TDD: /auth로 시작하는 엔드포인트들에 대한 Testcase(로그인, 회원가입, 로그아웃 페이지)
  r = client.get( # 11. 유닛 테스트와 TDD: GET Method
    '/auth/register', # 11. 유닛 테스트와 TDD: 엔드포인트 -> /auth/register(회원가입 페이지)
    follow_redirects=True # 11. 유닛 테스트와 TDD: 페이지가 다른 페이지로 리디렉션 되었을 때 그 페이지를 따라가고, 해당 페이지의 response 값을 가져온다
  )
  assert r.status_code == 200 # 11. 유닛 테스트와 TDD: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(200: OK)

  r = client.get( # 11. 유닛 테스트와 TDD: GET Method
    '/auth/login', # 11. 유닛 테스트와 TDD: 엔드포인트 -> /auth/login(로그인 페이지)
    follow_redirects=True # 11. 유닛 테스트와 TDD: 페이지가 다른 페이지로 리디렉션 되었을 때 그 페이지를 따라가고, 해당 페이지의 response 값을 가져온다
  )
  assert r.status_code == 200 # 11. 유닛 테스트와 TDD: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(200: OK)

  r = client.get( # 11. 유닛 테스트와 TDD: GET Method
    '/auth', # 11. 유닛 테스트와 TDD: 엔드포인트 -> /auth
    follow_redirects=True # 11. 유닛 테스트와 TDD: 페이지가 다른 페이지로 리디렉션 되었을 때 그 페이지를 따라가고, 해당 페이지의 response 값을 가져온다
  )
  assert r.status_code == 200 # 11. 유닛 테스트와 TDD: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(200: OK)

  r = client.get( # 11. 유닛 테스트와 TDD: GET Method
    '/auth/logout', # 11. 유닛 테스트와 TDD: 엔드포인트 -> /auth/logout(로그아웃 페이지)
    follow_redirects=True # 11. 유닛 테스트와 TDD: 페이지가 다른 페이지로 리디렉션 되었을 때 그 페이지를 따라가고, 해당 페이지의 response 값을 가져온다
  )
  assert r.status_code == 200 # 11. 유닛 테스트와 TDD: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(200: OK)

def test_base(client): # 11. 유닛 테스트와 TDD: /로 시작하는 엔드포인트들에 대한 Testcase(인덱스 페이지)
  r = client.get( # 11. 유닛 테스트와 TDD: GET Method
    '/',  # 11. 유닛 테스트와 TDD: 엔드포인트 -> /
    follow_redirects=True # 11. 유닛 테스트와 TDD: 페이지가 다른 페이지로 리디렉션 되었을 때 그 페이지를 따라가고, 해당 페이지의 response 값을 가져온다
  )
  assert r.status_code == 200 # 11. 유닛 테스트와 TDD: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(200: OK)
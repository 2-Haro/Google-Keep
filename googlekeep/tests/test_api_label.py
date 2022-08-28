def test_get_labels(client): # 16. 라벨 기본 기능 구현: 라벨 조회에 대한 Testcase
  r = client.get( # 16. 라벨 기본 기능 구현: GET Method
      '/api/labels', # 16. 라벨 기본 기능 구현: 엔드포인트 -> /api/labels
      follow_redirects=True # 16. 라벨 기본 기능 구현: 페이지가 다른 페이지로 리디렉션 되었을 때 그 페이지를 따라가고, 해당 페이지의 response 값을 가져온다
  )
  assert r.status_code == 200 # 16. 라벨 기본 기능 구현: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(200: OK)
  assert r.json == [] # 16. 라벨 기본 기능 구현: 라벨 모델 데이터베이스에는 데이터가 들어있지 않기 때문에 비어있어야 한다

def test_post_label(client): # 16. 라벨 기본 기능 구현: 라벨 생성에 대한 Testcase
  label = { # 16. 라벨 기본 기능 구현: 라벨 더미 데이터 생성
      'content': 'label' # 16. 라벨 기본 기능 구현: content를 label로 설정
    }
  r = client.post( # 16. 라벨 기본 기능 구현: POST Method
    '/api/labels', # 16. 라벨 기본 기능 구현: 엔드포인트 -> /api/labels
    data=label # 16. 라벨 기본 기능 구현: data를 label(더미 데이터)로 설정
  )
  assert r.status_code == 201 # 16. 라벨 기본 기능 구현: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(201: Created)
  assert r.json.get('content') == label['content'] # 16. 라벨 기본 기능 구현: content가 더미 데이터의 content와 같아야 한다 

def test_delete_label(client): # 16. 라벨 기본 기능 구현: 라벨 삭제에 대한 Testcase
  r = client.delete( # 16. 라벨 기본 기능 구현: DELETE Method
    '/api/labels/1', # 16. 라벨 기본 기능 구현: 엔드포인트 -> /api/labels/1 (POST Method에서 더미 데이터로 생성한 라벨의 id가 1이기 때문에)
  )
  assert r.status_code == 204 # 16. 라벨 기본 기능 구현: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(204: No Content)
  r = client.get( # 16. 라벨 기본 기능 구현: GET Method
    '/api/labels', # 16. 라벨 기본 기능 구현: 엔드포인트 -> /api/labels
    follow_redirects=True # 16. 라벨 기본 기능 구현: 페이지가 다른 페이지로 리디렉션 되었을 때 그 페이지를 따라가고, 해당 페이지의 response 값을 가져온다
  )
  assert r.status_code == 200 # 16. 라벨 기본 기능 구현: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(200: OK)
  assert r.json == [] # 16. 라벨 기본 기능 구현: 라벨 모델 데이터베이스에서 POST Method로 생성한 더미 데이터를 DELETE Method로 삭제했기 때문에 데이터가 들어있지 않으므로 비어있어야 한다
from io import BytesIO # 15. 메모 기능 업그레이드: 더미 이미지 생성을 위한 모듈 -> 객체 내에 저장된 bytes 정보를 불러와 이미지로 읽어준다

def test_get_memo(client, memo_data): # 13. 메모 기본 기능 구현: 메모 단수 조회에 대한 Testcase
  r = client.get( # 13. 메모 기본 기능 구현: GET Method
    '/api/memos/1', # 13. 메모 기본 기능 구현: 엔드포인트 -> /api/memos/1 (미리 생성된 첫번째 메모)
    follow_redirects = True # 13. 메모 기본 기능 구현: 페이지가 다른 페이지로 리디렉션 되었을 때 그 페이지를 따라가고, 해당 페이지의 response 값을 가져온다
  )
  assert r.status_code == 200 # 13. 메모 기본 기능 구현: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(200: OK)
  assert r.json['title'] == memo_data['title'] # 13. 메모 기본 기능 구현: 메모의 title이 memo_data(더미 데이터)의 title과 같아야 한다

def test_get_memos(client): # 13. 메모 기본 기능 구현: 메모 복수 조회에 대한 Testcase
  r = client.get( # 13. 메모 기본 기능 구현: GET Method
    '/api/memos', # 13. 메모 기본 기능 구현: 엔드포인트 -> /api/memos (모든 메모)
    follow_redirects = True # 13. 메모 기본 기능 구현: 페이지가 다른 페이지로 리디렉션 되었을 때 그 페이지를 따라가고, 해당 페이지의 response 값을 가져온다
  )
  assert r.status_code == 200 # 13. 메모 기본 기능 구현: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(200: OK)
  assert len(r.json) == 1 # 13. 메모 기본 기능 구현: response의 길이 = 1 -> conftest.py에서 메모 모델 더미 데이터를 1개 넣었기 때문

def test_post_memo(client, memo_data): # 13. 메모 기본 기능 구현: 메모 생성에 대한 Testcase(POST Method를 통해 메모를 생성할 때도 더미 데이터 이용)
  r = client.post( # 13. 메모 기본 기능 구현: POST Method
    '/api/memos', # 13. 메모 기본 기능 구현: 엔드포인트 -> /api/memos (모든 메모)
    data = memo_data # 13. 메모 기본 기능 구현: data를 memo_data(더미 데이터)로 설정
  )
  assert r.status_code == 201 # 13. 메모 기본 기능 구현: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(201: Created)
  r = client.get( # 13. 메모 기본 기능 구현: GET Method(새로운 메모가 생성(POST)되었는지 확인)
    '/api/memos', # 13. 메모 기본 기능 구현: 엔드포인트 -> /api/memos (모든 메모)
    follow_redirects = True # 13. 메모 기본 기능 구현: 페이지가 다른 페이지로 리디렉션 되었을 때 그 페이지를 따라가고, 해당 페이지의 response 값을 가져온다
  )
  assert r.status_code == 200 # 13. 메모 기본 기능 구현: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(200: OK)
  assert len(r.json) == 2 # 13. 메모 기본 기능 구현: response의 길이 = 2 -> conftest.py에서 메모 모델 더미 데이터 1개, POST Method로 메모 모델 더미 데이터 1개, 총 2개를 넣었기 때문

def test_put_memo(client): # 13. 메모 기본 기능 구현: 메모 수정(업데이트)에 대한 Testcase
  new_data = { # 13. 메모 기본 기능 구현: 새로운 더미 데이터 생성
    'title': 'new_title', # 13. 메모 기본 기능 구현: title은 new_title로 설정
    'content': 'new_content' # 13. 메모 기본 기능 구현: content는 new_content로 설정
  }
  r = client.put( # 13. 메모 기본 기능 구현: PUT Method
    '/api/memos/1', # 13. 메모 기본 기능 구현: 엔드포인트 -> /api/memos/1 (생성된 첫번째 메모)
    data = new_data # 13. 메모 기본 기능 구현: data를 new_data(더미 데이터)로 설정
  )
  assert r.status_code == 200 # 13. 메모 기본 기능 구현: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(200: OK)
  assert r.json['title'] == new_data['title'] # 13. 메모 기본 기능 구현: 수정된 메모의 title이 new_data(더미 데이터)의 title과 같이야 한다
  assert r.json['content'] == new_data['content'] # 13. 메모 기본 기능 구현: 수정된 메모의 content가 new_data(더미 데이터)의 content와 같이야 한다

def test_delete_memo(client): # 13. 메모 기본 기능 구현: 메모 삭제에 대한 Testcase
  r = client.delete( # 13. 메모 기본 기능 구현: Delete Method
    '/api/memos/1' # 13. 메모 기본 기능 구현: 엔드포인트 -> /api/memos/1 (생성된 첫번째 메모)
  )
  assert r.status_code == 204 # 13. 메모 기본 기능 구현: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(204: No Content)
  r = client.get( # 13. 메모 기본 기능 구현: GET Method
    '/api/memos', # 13. 메모 기본 기능 구현: 엔드포인트 -> /api/memos (모든 메모)
    follow_redirects = True # 13. 메모 기본 기능 구현: 페이지가 다른 페이지로 리디렉션 되었을 때 그 페이지를 따라가고, 해당 페이지의 response 값을 가져온다
  )
  assert r.status_code == 200 # 13. 메모 기본 기능 구현: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(200: OK)
  assert len(r.json) == 1 # 13. 메모 기본 기능 구현: response의 길이 = 1 -> conftest.py에서 메모 모델 더미 데이터 1개, POST Method로 메모 모델 더미 데이터 1개, 총 2개를 넣었지만, 1개를 삭제했기 때문

def test_post_memo_with_img(client, memo_data): # 15. 메모 기능 업그레이드: 메모 이미지 생성에 대한 Testcase
  data = memo_data.copy() # 15. 메모 기능 업그레이드: 얕은 복사(동일한 메모리 주소 참조)
  data['linked_image'] = ( # 15. 메모 기능 업그레이드: data에 linked_image 필드 추가 예상 -> 추후 개발
    BytesIO(b'dummy'), # 15. 메모 기능 업그레이드: 더미 데이터
    'test.jpg' # 15. 메모 기능 업그레이드: 더미 데이터 이미지 이름
  )
  r = client.post( # 15. 메모 기능 업그레이드: POST Method
    '/api/memos', # 15. 메모 기능 업그레이드: 엔드포인트 -> /api/memos (모든 메모)
    data = data # 15. 메모 기능 업그레이드: data를 data(memo_data에 linked_image 필드가 추가된 더미 데이터)로 설정
  )
  assert r.status_code == 201 # 15. 메모 기능 업그레이드: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(201: Created)
  assert r.json.get('linked_image') is not None # 15. 메모 기능 업그레이드: linked_image 필드가 비어있지 않아야 한다 -> apis/memo.py에서 Marshalling 할 때 skip_none=True로 해줬기 때문에 만약 linked_image에 데이터가 들어가지 않았다면 None 반환

def test_put_memo_with_img(client, memo_data): # 15. 메모 기능 업그레이드: 메모 이미지 수정(업데이트)에 대한 Testcase
  r = client.post( # 15. 메모 기능 업그레이드: POST Method -> 업데이트를 검증하는 Testcase이므로 response(POST) 받은 데이터를 PUT하는 방식으로 Test 검증
    '/api/memos', # 15. 메모 기능 업그레이드: 엔드포인트 -> /api/memos (모든 메모)
    data = memo_data # 15. 메모 기능 업그레이드: data를 memo_data로 설정
  )
  assert r.status_code == 201 # 15. 메모 기능 업그레이드: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(201: Created)
  memo_id = r.json['id'] # 15. 메모 기능 업그레이드: memo_id를 생성(POST)된 메모의 id로 설정
  data = { # 15. 메모 기능 업그레이드: PUT할 메모 data 생성
    'linked_image':( # 15. 메모 기능 업그레이드: linked_image 필드 추가
      BytesIO(b'dummy'), # 15. 메모 기능 업그레이드: 더미 데이터
      'test.jpg' # 15. 메모 기능 업그레이드: 더미 데이터 이미지 이름
    )
   }
  r = client.put( # 15. 메모 기능 업그레이드: PUT Method
    f'/api/memos/{memo_id}', # 15. 메모 기능 업그레이드: 엔드포인트 -> /api/memos/{memo_id}
    data = data # 15. 메모 기능 업그레이드: data를 data(수정할 더미 데이터)로 설정
  )
  assert r.status_code == 200 # 15. 메모 기능 업그레이드: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(200: OK)
  assert r.json.get('linked_image') is not None # 15. 메모 기능 업그레이드: linked_image 필드가 비어있지 않아야 한다 -> apis/memo.py에서 Marshalling 할 때 skip_none=True로 해줬기 때문에 만약 linked_image에 데이터가 들어가지 않았다면 None 반환

def test_delete_memo_img(client, memo_data): # 15. 메모 기능 업그레이드: 메모 이미지 삭제에 대한 Testcase
  data = memo_data.copy() # 15. 메모 기능 업그레이드: 얕은 복사(동일한 메모리 주소 참조)
  data['linked_image'] = ( # 15. 메모 기능 업그레이드: data에 linked_image 필드 추가 예상 -> 추후 개발
    BytesIO(b'dummy'), # 15. 메모 기능 업그레이드: 더미 데이터
    'test.jpg' # 15. 메모 기능 업그레이드: 더미 데이터 이미지 이름
  )
  r = client.post( # 15. 메모 기능 업그레이드: POST Method -> 삭제를 검증하는 Testcase이므로 response(POST) 받은 데이터를 DELETE하는 방식으로 Test 검증
    '/api/memos', # 15. 메모 기능 업그레이드: 엔드포인트 -> /api/memos (모든 메모)
    data = data # 15. 메모 기능 업그레이드: data를 data(memo_data에 linked_image 필드가 추가된 더미 데이터)로 설정
  )
  assert r.status_code == 201 # 15. 메모 기능 업그레이드: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(201: Created)
  assert r.json.get('linked_image') is not None # 15. 메모 기능 업그레이드: linked_image 필드가 비어있지 않아야 한다 -> apis/memo.py에서 Marshalling 할 때 skip_none=True로 해줬기 때문에 만약 linked_image에 데이터가 들어가지 않았다면 None 반환
  memo_id = r.json['id'] # 15. 메모 기능 업그레이드: memo_id를 생성(POST)된 메모의 id로 설정

  r = client.delete( # 15. 메모 기능 업그레이드: DELETE Method(메모 이미지 삭제)
    f'/api/memos/{memo_id}/image' # 15. 메모 기능 업그레이드: 엔드포인트 -> /api/memos/{memo_id}/image -> 이미지를 삭제하는 새로운 엔드포인트 필요
  )
  assert r.status_code == 204 # 15. 메모 기능 업그레이드: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(204: No Content)
  
  r = client.get( # 15. 메모 기능 업그레이드: GET Method
    f'/api/memos/{memo_id}', # 15. 메모 기능 업그레이드: 엔드포인트 -> /api/memos/{memo_id}
    follow_redirects = True # 15. 메모 기능 업그레이드: 페이지가 다른 페이지로 리디렉션 되었을 때 그 페이지를 따라가고, 해당 페이지의 response 값을 가져온다
  )
  assert r.json.get('linked_image') is None # 15. 메모 기능 업그레이드: linked_image 필드가 비어있어야 한다 -> 메모 이미지를 삭제했기 때문

def test_put_memo_status_is_deleted(client):
  r = client.get( # 15. 메모 기능 업그레이드: GET Method
    '/api/memos?is_deleted=false', # 15. 메모 기능 업그레이드: 엔드포인트 -> /api/memos?is_deleted=false # 필드를 추가하면서 조회할 때 쿼리스트링으로 엔드포인트에 데이터를 넘겨주어야 한다 -> is_deleted 값이 False인 항목 조회
    follow_redirects = True # 15. 메모 기능 업그레이드: 페이지가 다른 페이지로 리디렉션 되었을 때 그 페이지를 따라가고, 해당 페이지의 response 값을 가져온다
  )
  assert r.status_code == 200 # 15. 메모 기능 업그레이드: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(200: OK)
  assert r.json[0].get('is_deleted') == False # 15. 메모 기능 업그레이드: 첫번째 데이터의 is_deleted 값이 False여야 한다

  r = client.put( # 15. 메모 기능 업그레이드: PUT Method
    f'/api/memos/{r.json[0]["id"]}', # 15. 메모 기능 업그레이드: 엔드포인트 -> /api/memos/{r.json[0]["id"]} (위에서 조회한 항목의 id값을 받아와서 엔드포인트에서 사용)
    data = { # 15. 메모 기능 업그레이드: PUT할 메모 데이터 생성
      'is_deleted': True # 15. 메모 기능 업그레이드: 조화한 항목의 is_deleted 값을 True로 변경
    }
  )
  assert r.status_code == 200 # 15. 메모 기능 업그레이드: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(200: OK)
  assert r.json.get('is_deleted') == True # 15. 메모 기능 업그레이드: is_deleted 값이 True여야 한다

def test_post_memo_status_is_deleted(client, memo_data):
  data = memo_data.copy() # 15. 메모 기능 업그레이드: 얕은 복사(동일한 메모리 주소 참조)
  data['is_deleted'] = True # 15. 메모 기능 업그레이드: data의 is_deleted 값을 True로 설정
  r = client.post( # 15. 메모 기능 업그레이드: POST Method
    '/api/memos', # 15. 메모 기능 업그레이드: 엔드포인트 -> /api/memos (모든 메모)
    data = data # 15. 메모 기능 업그레이드: data를 data(memo_data에 is_deleted 필드가 True로 추가된 더미 데이터)로 설정
  )
  assert r.status_code == 201 # 15. 메모 기능 업그레이드: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(201: Created)
  assert r.json.get('is_deleted') == True # 15. 메모 기능 업그레이드: is_deleted 값이 True여야 한다

def test_get_memo_status_is_deleted(client):
  r = client.get( # 15. 메모 기능 업그레이드: GET Method 
    '/api/memos?is_deleted=true', # 15. 메모 기능 업그레이드: 엔드포인트 -> /api/memos?is_deleted=true (위의 POST Method에서 is_deleted가 True인 데이터를 넣어줬으므로 데이터가 존재한다)
    follow_redirects=True # 15. 메모 기능 업그레이드: 페이지가 다른 페이지로 리디렉션 되었을 때 그 페이지를 따라가고, 해당 페이지의 response 값을 가져온다
  ) 
  assert r.status_code == 200 # 15. 메모 기능 업그레이드: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(200: OK)
  assert len(r.json) >= 1 # 15. 메모 기능 업그레이드: response의 길이 >= 1 (위의 POST Method에서 데이터를 넣어줬기 때문)
  assert r.json[0].get('is_deleted') == True # 15. 메모 기능 업그레이드: 첫번째 데이터의 is_deleted 값이 True여야 한다

def test_post_memo_with_labels(client, memo_data): # 17. 메모 라벨링 기능 업데이트: 라벨이 있는 메모 생성에 대한 Testcase
  data = memo_data.copy() # 17. 메모 라벨링 기능 업데이트: 얕은 복사(동일한 메모리 주소 참조) 
  data['labels'] = 'test,' # 17. 메모 라벨링 기능 업데이트: 더미 데이터의 labels를 test,로 설정(콤마스트링으로 받는다)
  r = client.post( # 17. 메모 라벨링 기능 업데이트: POST Method
    '/api/memos', # 17. 메모 라벨링 기능 업데이트: 엔드포인트 -> /api/memos
    data=data # 17. 메모 라벨링 기능 업데이트: data를 data(memo_data에 labels 필드가 test,로 추가된 더미 데이터)로 설정
  )
  assert r.status_code == 201 # 17. 메모 라벨링 기능 업데이트: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(201: Created) 
  assert len(r.json.get('labels', [])) == 1 # 17. 메모 라벨링 기능 업데이트: 생성된 데이터의 labels를 받아온 값(없으면 빈 배열)의 길이 = 1 (더미 데이터로 test, 라벨을 넣었기 때문에 길이가 1)
  assert r.json.get('labels', [])[0]['content'] == 'test' # 17. 메모 라벨링 기능 업데이트: 생성된 데이터의 labels를 받아온 값(없으면 빈 배열)의 첫번째 항목의 content값이 test여야 한다

def test_put_memo_with_labels(client, memo_data): # 17. 메모 라벨링 기능 업데이트: 라벨이 있는 메모 수정에 대한 Testcase
  r = client.post( # 17. 메모 라벨링 기능 업데이트: POST Method
    '/api/memos', # 17. 메모 라벨링 기능 업데이트: 엔드포인트 -> /api/memos
    data=memo_data # 17. 메모 라벨링 기능 업데이트: data를 memo_data(더미 데이터)로 설정
  )
  assert r.status_code == 201 # 17. 메모 라벨링 기능 업데이트: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(201: Created) 
  assert len(r.json.get('labels', [])) == 0 # 17. 메모 라벨링 기능 업데이트: 생성된 데이터의 labels를 받아온 값(없으면 빈 배열)의 길이 = 0 (더미 데이터에 라벨이 없기 때문에 길이가 0)

  r = client.put( # 17. 메모 라벨링 기능 업데이트: PUT Method
    f'/api/memos/{r.json["id"]}', # 17. 메모 라벨링 기능 업데이트: 엔드포인트 -> /api/memos/{r.json["id"]}
    data={ # 17. 메모 라벨링 기능 업데이트: data의
      'labels': 'test,' # 17. 메모 라벨링 기능 업데이트: labels를 test로 설정
    }
  )
  assert r.status_code == 200 # 17. 메모 라벨링 기능 업데이트: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(200: OK)
  assert len(r.json.get('labels', [])) == 1 # 17. 메모 라벨링 기능 업데이트: 생성된 데이터의 labels를 받아온 값(없으면 빈 배열)의 길이 = 1 (더미 데이터로 test, 라벨을 넣었기 때문에 길이가 1)
  assert r.json.get('labels', [])[0]['content'] == 'test' # 17. 메모 라벨링 기능 업데이트: 생성된 데이터의 labels를 받아온 값(없으면 빈 배열)의 첫번째 항목의 content값이 test여야 한다

def test_get_memo_with_labels(client): # 17. 메모 라벨링 기능 업데이트: 라벨이 있는 메모 조회에 대한 Testcase
  r = client.get( # 17. 메모 라벨링 기능 업데이트: GET Method
    '/api/memos?label=1', # 17. 메모 라벨링 기능 업데이트: 엔드포인트 -> /api/memos?label=1 (라벨 번호가 1번인 항목들)
    follow_redirects=True # 17. 메모 라벨링 기능 업데이트: 페이지가 다른 페이지로 리디렉션 되었을 때 그 페이지를 따라가고, 해당 페이지의 response 값을 가져온다
  )
  assert r.status_code == 200 # 17. 메모 라벨링 기능 업데이트: 조건이 True임을 검증하기 위해 assert 사용 -> True가 아닐 때 예외 발생(200: OK)
  assert len(r.json) >= 1 # 17. 메모 라벨링 기능 업데이트: response의 길이 >= 1 (위의 POST Method에서 데이터를 넣어줬기 때문)
  assert r.json[0]['labels'][0]['content'] == 'test' # 17. 메모 라벨링 기능 업데이트: 첫번째 메모의 labels의 첫번째 항목의 content가 test여야 한다
from googlekeep.models.memo import Memo as MemoModel
from googlekeep.models.user import User as UserModel
from googlekeep.models.label import Label as LabelModel
from flask_restx import Namespace, fields, Resource, reqparse, inputs
from flask import g, current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import os
import shutil

ns = Namespace( # 13. 메모 기본 기능 구현: Namespace init
  'memos', # 13. 메모 기본 기능 구현: URL에 붙는 이름
  description='메모 관련 API' # 13. 메모 기본 기능 구현: 설명
)

# 17. 메모 라벨링 기능 업데이트: Response Mapping -> Marshalling: 설계한 Model의 값에 맞는 field들에만 해당되는 데이터들이 자동으로 mapping 되어서 프론트에 노출
label = ns.model('Label', {
  'id': fields.Integer(required=True, description='라벨 고유 번호'), # 17. 메모 라벨링 기능 업데이트: id -> 정수, 필수 요소, 라벨 고유 번호
  'content': fields.String(required=True, description='라벨 내용') # 17. 메모 라벨링 기능 업데이트: content -> 문자열, 필수 요소, 라벨 내용
})

# 13. 메모 기본 기능 구현: Response Mapping -> Marshalling: 설계한 Model의 값에 맞는 field들에만 해당되는 데이터들이 자동으로 mapping 되어서 프론트에 노출
memo = ns.model('Memo', {
  'id': fields.Integer(required=True, description='메모 고유 번호'), # 13. 메모 기본 기능 구현: id -> 정수, 필수 요소, 메모 고유 번호
  'user_id': fields.Integer(required=True, description='유저 고유 번호'), # 13. 메모 기본 기능 구현: user_id -> 정수, 필수 요소, 유저 고유 번호(유저 Table의 id(기본키))
  'title': fields.String(required=True, description='메모 제목'), # 13. 메모 기본 기능 구현: title -> 문자열, 필수 요소, 메모 제목
  'content': fields.String(required=True, description='메모 내용'), # 13. 메모 기본 기능 구현: content -> 문자열, 필수 요소, 메모 내용
  'linked_image': fields.String(required=False, description='메모 이미지 경로'), # 15. 메모 기능 업그레이드: linked_image -> 문자열(linked_image 필드에는 파일 데이터가 넘어오지만 이미지가 위치하는 상대 경로 데이터가 들어가기 때문에 Marshalling 하는 내용인 String으로 정의), 필수 요소 X
  'is_deleted': fields.Boolean(description='메모 삭제 상태'), # 15. 메모 기능 업그레이드: is_deleted -> Boolean, 메모 삭제 상태
  'labels': fields.List(fields.Nested(label), description='연결된 라벨'), # 17. 메모 라벨링 기능 업데이트: labels -> List, 중첩된 필드(label) 적용, 연결된 라벨
  'create_at': fields.DateTime(description='메모 작성 시간'), # 13. 메모 기본 기능 구현: created_at -> DateTime, 필수 요소 X, 메모 작성 시간
  'updated_at': fields.DateTime(description='메모 수정 시간') # 13. 메모 기본 기능 구현: updated_at -> DateTime, 필수 요소 X, 메모 수정 시간
})

parser = reqparse.RequestParser() # 13. 메모 기본 기능 구현: RequestParser init
# POST parser
parser.add_argument('title', required=True, help='메모 제목', location='form') # 13. 메모 기본 기능 구현: 받아올 정보 -> title
parser.add_argument('content', required=True, help='메모 내용', location='form') # 13. 메모 기본 기능 구현: 받아올 정보 -> content
parser.add_argument('linked_image', required=False, type=FileStorage, help='메모 이미지', location='files') # 15. 메모 기능 업그레이드: 받아올 정보 -> linked_image (put_parser에도 추가해줘야 하지만 put_parser가 parser를 copy하므로 parser에만 추가)
parser.add_argument('is_deleted', required=False, type=inputs.boolean, help='메모 삭제 상태', location='form') # 15. 메모 기능 업그레이드: 받아올 정보 -> is_deleted (put_parser에도 추가해줘야 하지만 put_parser가 parser를 copy하므로 parser에만 추가, get_parser에는 직접 추가)
parser.add_argument('labels', action='split', help='라벨 내용 콤마 스트링', location='form') # 17. 메모 라벨링 기능 업데이트: 받아올 정보 -> labels (action=split 속성을 통해 콤마 스트링으로 데이터가 들어왔을 때 parser.parse_args()를 하면 배열로 데이터를 반환할 수 있다) (put_parser에도 추가해줘야 하지만 put_parser가 parser를 copy하므로 parser에만 추가, get_parser에는 직접 추가)

# PUT parser(복사
put_parser = parser.copy() # 13. 메모 기본 기능 구현: .copy() -> parser inheritance
put_parser.replace_argument('title', required=False, help='메모 제목', location='form') # 13. 메모 기본 기능 구현: 수정할 정보 -> title
put_parser.replace_argument('content', required=False, help='메모 내용', location='form') # 13. 메모 기본 기능 구현: 수정할 정보 -> content

get_parser = reqparse.RequestParser() # GET parser
get_parser.add_argument('page', required=False, type=int, help='메모 페이지 번호', location='args') # 15. 메모 기능 업그레이드: 가져올 정보 -> page
get_parser.add_argument('needle', required=False, help='메모 검색어', location='args') # 15. 메모 기능 업그레이드: 가져올 정보 -> needle
get_parser.add_argument('is_deleted', required=False, type=inputs.boolean, help='메모 삭제 상태', location='args') # 15. 메모 기능 업그레이드: 받아올 정보 -> is_deleted (flask_restx에서 inputs를 import해서 Boolean 명시)
get_parser.add_argument('label', help='라벨 번호', location='args') # 17. 메모 라벨링 기능 업데이트: 받아올 정보 -> label (조회할 때는 특정 라벨만 받기 때문에 단수로 정의)

def allowed_file(filename): # 15. 메모 기능 업그레이드: Extension 설정(공식 문서 참조)
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'} # 15. 메모 기능 업그레이드: 이미지에 해당하는 값들만 받아온다

def randomword(length): # 15. 메모 기능 업그레이드: 동일한 파일 이름이 넘어오는 경우 대비
  import random, string
  letters = string.ascii_lowercase # 15. 메모 기능 업그레이드: 소문자들만 사용
  return ''.join(random.choice(letters) for i in range(length)) # 15. 메모 기능 업그레이드: length만큼 루프를 돌며 letter(문자열)안에 있는 문자를 random으로 choice해서 join을 통해 문자열(무작위)을 생성

def save_file(file): # 15. 메모 기능 업그레이드: 상대 경로, 절대 경로를 return하는 함수
  if file.filename == '': # 15. 메모 기능 업그레이드: Validation -> 파일이 존재하지 않는다면
    ns.abort(400) # 15. 메모 기능 업그레이드: 400 에러(400: Bad Request)
  if file and allowed_file(file.filename): # 15. 메모 기능 업그레이드: 파일이 존재하고, 파일 이름이 허용된 값인 경우
    filename = secure_filename(file.filename) # 15. 메모 기능 업그레이드: filename을 file의 filename(파일 이름)으로 설정 (secure_filname(): ../../test.jpg -> test.jpg & te st.jpg -> te_st.jpg)
    relative_path = os.path.join( # 15. 메모 기능 업그레이드: 상대 경로 -> current_app을 받아서 상대 경로를 만든다
      current_app.static_url_path[1:], # 15. 메모 기능 업그레이드: /static -> static
      current_app.config['USER_STATIC_BASE_DIR'], # 15. 메모 기능 업그레이드: static/user_images
      g.user.user_id, # 15. 메모 기능 업그레이드: static/user_images/{user_id}
      'memos', # 15. 메모 기능 업그레이드: static/user_images/{user_id}/memos
      randomword(5), # 15. 메모 기능 업그레이드: static/user_images/{user_id}/memos/asdfg
      filename # 15. 메모 기능 업그레이드: static/user_images/{user_id}/memos/asdfg/{filename}
    )
    upload_path = os.path.join( # 15. 메모 기능 업그레이드: 절대 경로
      current_app.root_path, # 15. 메모 기능 업그레이드: 루트 경로와
      relative_path # 15. 메모 기능 업그레이드: 상대 경로 join
    )
    os.makedirs( # 15. 메모 기능 업그레이드: 파일을 저장하기 위해 디렉토리 생성
      os.path.dirname(upload_path), # 15. 메모 기능 업그레이드: 업로드(절대) 경로로 디렉토리 생성
      exist_ok=True # 15. 메모 기능 업그레이드: 폴더가 이미 존재해도 에러 노출 X
    )
    file.save(upload_path) # 15. 메모 기능 업그레이드: 파일을 서버에 업로드
    return relative_path, upload_path # 15. 메모 기능 업그레이드: 상대 경로, 절대 경로 return
  else: # 15. 메모 기능 업그레이드: 파일이 존재하지 않거나, 파일 이름이 허용된 값이 아닐 경우
    ns.abort(400) # 15. 메모 기능 업그레이드: 400 에러(400: Bad Request)

# /api/memos
@ns.route('')
class MemoList(Resource): # 13. 메모 기본 기능 구현: 모든 메모의 정보 사용(복수)
  @ns.marshal_list_with(memo, skip_none=True) # 13. 메모 기본 기능 구현: Marshalling 정의(memo에 대한 marshalling, skip_none=True: 특정 field가 null이거나 데이터가 없을 경우에는 키 값을 만들지 않는다)
  @ns.expect(get_parser) # 15. 메모 기능 업그레이드: GET Method에서 GET parser 사용 명시
  def get(self): # 13. 메모 기본 기능 구현: GET Method
    '''메모 복수 조회'''
    args = get_parser.parse_args() # 15. 메모 기능 업그레이드: args에 GET한 데이터들 담기
    page = args['page'] # 15. 메모 기능 업그레이드: page를 GET한 page로 설정
    needle = args['needle'] # 15. 메모 기능 업그레이드: needle을 GET한 needle로 설정
    is_deleted = args['is_deleted'] # 15. 메모 기능 업그레이드: is_deleted를 GET한 is_deleted로 설정
    label = args['label'] # 17. 메모 라벨링 기능 업데이트: label을 GET한 label로 설정
    
    if is_deleted is None: # 15. 메모 기능 업그레이드: is_deleted 값이 없을 경우에는
      is_deleted = False # 15. 메모 기능 업그레이드: is_deleted 값을 False로 설정

    base_query = MemoModel.query.join( # 13. 메모 기본 기능 구현: join(inner join)을 통해서 MemoModel을
      UserModel, # 13. 메모 기본 기능 구현: UserModel과 연결
      UserModel.id == MemoModel.user_id # 13. 메모 기본 기능 구현: UserModel의 id(User Table의 id(기본키))와 MemoModel의 user_id(Memo Table의 user_id(외래키))가 같은 항목만 선택 -> 메모를 작성한 유저별로 분류
    ).filter( # 13. 메모 기본 기능 구현: filter 사용
      UserModel.id == g.user.id, # 13. 메모 기본 기능 구현: 로그인 되어 있는 유저의 메모 정보만 가지고 와야 하기 때문에 세션 내 유저의 id로 조회
      MemoModel.is_deleted == is_deleted # 15. 메모 기능 업그레이드: MemoModel의 is_deleted 값이 is_deleted와 동일한 값만 조회
    ).order_by( # 13. 메모 기본 기능 구현: order_by 사용(정렬 방법)
      MemoModel.created_at.desc() # 13. 메모 기본 기능 구현: 생성 시간이 최근인 메모부터 내림차순으로 정렬
    )

    if needle: # 15. 메모 기능 업그레이드: needle(검색어)이 존재하는 경우
      needle = f'%{needle}%' # 15. 메모 기능 업그레이드: like operator(SQL에서 특정 패턴의 텍스트를 찾아낼 때 사용)를 사용하기 위해 -> 공식 문서 참조
      base_query = base_query.filter( # 15. 메모 기능 업그레이드: # filter를 적용한 base_query 적용
        MemoModel.title.ilike(needle)|MemoModel.content.ilike(needle) # 15. 메모 기능 업그레이드: MemoModel의 title or content가 needle(검색어)과 일치하는 경우 base_query 수정 (ilike -> 대소문자 구별 X)
      )

    if label: # 17. 메모 라벨링 기능 업데이트: label이 존재하는 경우
      base_query = base_query.filter( # 17. 메모 라벨링 기능 업데이트: base_query를 base_query에 아래의 filter를 적용한 값으로 설정
        MemoModel.labels.any(LabelModel.id == label) # 17. 메모 라벨링 기능 업데이트: LabelModel의 id와 label을 비교한 값이 MemoModel이 가지고 있는 labels의 값과 하나라도 일치한다면 해당 label 번호에 맞는 데이터 검색
      )

    pages = base_query.paginate( # 15. 메모 기능 업그레이드: pagination 사용
      page=page, # 15. 메모 기능 업그레이드: page(현재 페이지 번호)를 page로 설정
      per_page=15 # 15. 메모 기능 업그레이드: per_page(현재 페이지에 display될 item 개수)를 15로 설정
    )
    return pages.items # 15. 메모 기능 업그레이드: pages의 items 반환(공식 문서 참조)

  @ns.marshal_list_with(memo, skip_none=True) # 13. 메모 기본 기능 구현: Marshalling 정의(memo에 대한 marshalling, skip_none=True: 특정 field가 null이거나 데이터가 없을 경우에는 키 값을 만들지 않는다)
  @ns.expect(parser) # 13. 메모 기본 기능 구현: POST Method에서 POST parser 이용 명시
  def post(self): # 13. 메모 기본 기능 구현: POST Method
    '''메모 생성'''
    args = parser.parse_args() # 13. 메모 기본 기능 구현: args에 POST할 데이터들 담기
    memo = MemoModel( # 13. 메모 기본 기능 구현: 메모 생성
      title=args['title'], # 13. 메모 기본 기능 구현: MemoModel의 title을 POST한 title로 설정
      content=args['content'], # 13. 메모 기본 기능 구현: MemoModel의 content를 POST한 content로 설정
      user_id=g.user.id # 13. 메모 기본 기능 구현: MemoModel의 user_id를 세션의 user_id로 설정
    )
    if args['is_deleted'] is not None: # 15. 메모 기능 업그레이드: is_deleted의 기본값이 False이기 때문에 is_deleted 값이 존재하는 경우
      memo.is_deleted = args['is_deleted'] # 15. 메모 기능 업그레이드: 해당 메모의 is_deleted 값에 POST한 is_deleted(False)로 설정
    file = args['linked_image'] # 15. 메모 기능 업그레이드: file을 POST한 linked_image로 설정
    if file: # 15. 메모 기능 업그레이드: file이 비어있지 않다면
      relative_path, _ = save_file(file) # 15. 메모 기능 업그레이드: 상대 경로 -> DB 적재 용도 # 업로드(절대) 경로 -> 파일 쓰기 용도 (사용 X)
      memo.linked_image = relative_path # 15. 메모 기능 업그레이드: 메모의 linked_image를 relative path(상대 경로)로 설정

    labels = args['labels'] # 17. 메모 라벨링 기능 업데이트: MemoModel의 labels를 POST한 labels로 설정
    if labels: # 17. 메모 라벨링 기능 업데이트: labels의 값이 존재하는 경우
      for cnt in labels: # 17. 메모 라벨링 기능 업데이트: labels 배열을 순회
        if cnt: # 17. 메모 라벨링 기능 업데이트: cnt(content)가 빈 문자열이 아닌 경우
          label = LabelModel.query.filter( # 17. 메모 라벨링 기능 업데이트: LabelModel을 filter를 통해서 -> 라벨의 존재 여부 확인
            LabelModel.content == cnt, # 17. 메모 라벨링 기능 업데이트: LabelModel의 content값과 cnt가 같은 항목만 선택
            LabelModel.user_id == g.user.id # 17. 메모 라벨링 기능 업데이트: LabelModel의 user_id(Label Table의 user_id(외래키))와 현재 세션의 user의 id와 같은 항목만 선택
          ).first() # 17. 메모 라벨링 기능 업데이트: 첫번째 항목 선택
          if not label: # 17. 메모 라벨링 기능 업데이트: 라벨이 존재하지 않는 경우
            label = LabelModel( # 17. 메모 라벨링 기능 업데이트: 라벨 생성
              content = cnt, # 17. 메모 라벨링 기능 업데이트: LabelModel의 content를 cnt로 설정
              user_id = g.user.id # 17. 메모 라벨링 기능 업데이트: LabelModel의 user_id를 현재 세션의 user의 id로 설정
            )
          memo.labels.append(label) # 17. 메모 라벨링 기능 업데이트: 메모(MemoModel)의 labels에 label을 append 한다(라벨이 존재하는 경우 append, 라벨이 존재하지 않는 경우 생성해서 append)
    g.db.add(memo) # 13. 메모 기본 기능 구현: DB에 메모 추가(세션)
    g.db.commit() # 13. 메모 기본 기능 구현: DB에 commit(세션)
    return memo, 201 # 13. 메모 기본 기능 구현: return memo, 생성에 성공했을 때 response code 201(201: created)

# /api/memos/id
@ns.route('/<int:id>')
@ns.param('id', '메모 고유 번호') # 13. 메모 기본 기능 구현: id에 대한 설명(메모 고유 번호)
class Memo(Resource): # 13. 메모 기본 기능 구현: 특정 id값을 가지는 메모 정보 사용(단수)
  @ns.marshal_list_with(memo, skip_none=True) # 13. 메모 기본 기능 구현: Marshalling 정의(memo에 대한 marshalling, skip_none=True: 특정 field가 null이거나 데이터가 없을 경우에는 키 값을 만들지 않는다)
  def get(self, id): # 13. 메모 기본 기능 구현: GET Method
    '''메모 단수 조회'''
    memo = MemoModel.query.get_or_404(id) # 13. 메모 기본 기능 구현: id값을 가진 메모 단수 조회, id에 해당하는 메모가 없다면 404 에러
    if g.user.id != memo.user_id: # 13. 메모 기본 기능 구현: 세션의 id값과 메모의 user_id값(메모를 작성한 유저의 id값)이 다른 경우
      ns.abort(403) # 13. 메모 기본 기능 구현: 403 에러 발생(403: Forbidden) -> 리소스는 존재하지만, 접근 권한이 없다
    return memo

  @ns.marshal_list_with(memo, skip_none=True) # 13. 메모 기본 기능 구현: Marshalling 정의(memo에 대한 marshalling, skip_none=True: 특정 field가 null이거나 데이터가 없을 경우에는 키 값을 만들지 않는다)
  @ns.expect(put_parser) # 13. 메모 기본 기능 구현: Put Method에서 Put parser 이용 명시
  def put(self, id): # 13. 메모 기본 기능 구현: PUT Method
    '''메모 업데이트'''
    args = put_parser.parse_args() # 13. 메모 기본 기능 구현: args에 PUT할 데이터들 담기
    memo = MemoModel.query.get_or_404(id) # 13. 메모 기본 기능 구현: id값을 가진 메모 단수 조회, id에 해당하는 메모가 없다면 404 에러
    if g.user.id != memo.user_id: # 13. 메모 기본 기능 구현: 세션의 id값과 메모의 user_id값(메모를 작성한 유저의 id값)이 다른 경우
      ns.abort(403) # 13. 메모 기본 기능 구현: 403 에러 발생(403: Forbidden) -> 리소스는 존재하지만, 접근 권한이 없다
    if args['title'] is not None: # 13. 메모 기본 기능 구현: PUT Method(수정)로 들어온 title값이 존재한다면
      memo.title = args['title'] # 13. 메모 기본 기능 구현: 메모의 title을 PUT한 title로 설정
    if args['content'] is not None: # 13. 메모 기본 기능 구현: PUT Method(수정)로 들어온 content값이 존재한다면
      memo.content = args['content'] # 13. 메모 기본 기능 구현: 메모의 content를 PUT한 content로 설정
    if args['is_deleted'] is not None: # 15. 메모 기능 업그레이드: is_deleted의 기본값이 False이기 때문에 is_deleted 값이 존재하는 경우
      memo.is_deleted = args['is_deleted'] # 15. 메모 기능 업그레이드: 해당 메모의 is_deleted 값에 POST한 is_deleted(False)로 설정]
    file = args['linked_image'] # 15. 메모 기능 업그레이드: file을 PUT한 linked_image로 설정
    if file: # 15. 메모 기능 업그레이드: file이 비어있지 않다면
      relative_path, upload_path = save_file(file) # 15. 메모 기능 업그레이드: 상대 경로 -> DB 적재 용도 # 업로드(절대) 경로 -> 파일 쓰기 용도
      if memo.linked_image: # 15. 메모 기능 업그레이드: 조회한 MemoModel에 이미 바인딩 된 이미지가 존재한다면 삭제 후 추가, 없으면 그냥 추가
        origin_path = os.path.join( # 15. 메모 기능 업그레이드: 바인딩 된 이미지의 업로드 경로(삭제하기 위해 생성)
          current_app.root_path, # 15. 메모 기능 업그레이드: 루트 경로와
          memo.linked_image # 15. 메모 기능 업그레이드: memo의 linked_image(경로) join
        )
        if origin_path != upload_path: # 15. 메모 기능 업그레이드: 바인딩 된 이미지의 업로드 경로와 새롭게 업로드 되는 이미지의 경로가 다른 경우
          if os.path.isfile(origin_path): # 15. 메모 기능 업그레이드: 바인딩 된 이미지 파일이 존재하는 경우
            shutil.rmtree(os.path.dirname(origin_path)) # 15. 메모 기능 업그레이드: 지정된 폴더(바인딩 된 이미지 파일의 폴더 경로)와 하위 파일을 전부 삭제
      memo.linked_image = relative_path # 15. 메모 기능 업그레이드: 상대 경로 업데이트
    labels = args['labels'] # 17. 메모 라벨링 기능 업데이트: MemoModel의 labels를 PUT한 labels로 설정
    if labels: # 17. 메모 라벨링 기능 업데이트: labels가 존재하는 경우
      memo.labels.clear() # 17. 메모 라벨링 기능 업데이트: 메모(MemoModel)에 연결된 라벨 삭제
      for cnt in labels: # 17. 메모 라벨링 기능 업데이트: labels 배열 순회
        if cnt: # 17. 메모 라벨링 기능 업데이트: cnt(content)가 빈 문자열이 아닌 경우
          label = LabelModel.query.filter( # 17. 메모 라벨링 기능 업데이트: LabelModel을 filter를 통해서 -> 라벨의 존재 여부 확인
            LabelModel.content == cnt, # 17. 메모 라벨링 기능 업데이트: LabelModel의 content값과 cnt가 같은 항목만 선택
            LabelModel.user_id == g.user.id # 17. 메모 라벨링 기능 업데이트: LabelModel의 user_id(Label Table의 user_id(외래키))와 현재 세션의 user의 id와 같은 항목만 선택
          ).first() # 17. 메모 라벨링 기능 업데이트: 첫번째 항목 선택
          if not label: # 17. 메모 라벨링 기능 업데이트: 라벨이 존재하지 않는 경우
            label = LabelModel( # 17. 메모 라벨링 기능 업데이트: 라벨 생성
              content = cnt, # 17. 메모 라벨링 기능 업데이트: LabelModel의 content를 cnt로 설정
              user_id = g.user.id# 17. 메모 라벨링 기능 업데이트: LabelModel의 user_id를 현재 세션의 user의 id로 설정
            )
          memo.labels.append(label) # 17. 메모 라벨링 기능 업데이트: 메모(MemoModel)의 labels에 label을 append 한다(라벨이 존재하는 경우 append, 라벨이 존재하지 않는 경우 생성해서 append)
    g.db.commit() # 13. 메모 기본 기능 구현: DB에 commit(세션)
    return memo
  
  def delete(self, id): # 13. 메모 기본 기능 구현: DELETE Method
    '''메모 삭제'''
    memo = MemoModel.query.get_or_404(id) # 13. 메모 기본 기능 구현: id값을 가진 메모 단수 조회, id에 해당하는 메모가 없다면 404 에러
    if g.user.id != memo.user_id: # 13. 메모 기본 기능 구현: 세션의 id값과 메모의 user_id값(메모를 작성한 유저의 id값)이 다른 경우
      ns.abort(403) # 13. 메모 기본 기능 구현: 403 에러 발생(403: Forbidden) -> 리소스는 존재하지만, 접근 권한이 없다
    g.db.delete(memo) # 13. 메모 기본 기능 구현: 세션의 id값과 메모의 user_id값(메모를 작성한 유저의 id값)이 같은 경우 DB에서 삭제(세션)
    g.db.commit() # 13. 메모 기본 기능 구현: DB에 commit(세션)
    return '', 204 # 13. 메모 기본 기능 구현: return None, 삭제에 성공했을 때 response code 204(204: No Content)

# /api/memos/id/image
@ns.route('/<int:id>/image')
@ns.param('id', '메모 고유 번호') # 15. 메모 기능 업그레이드: id에 대한 설명(메모 고유 번호)
class MemoImage(Resource): # 15. 메모 기능 업그레이드: 특정 id값을 가지는 메모 이미지 정보 사용(단수)
  def delete(self, id): # 15. 메모 기능 업그레이드: DELETE Method
    '''메모 이미지 삭제'''
    memo = MemoModel.query.get_or_404(id) # 15. 메모 기능 업그레이드: id값을 가진 메모 단수 조회, id에 해당하는 메모가 없다면 404 에러
    if g.user.id != memo.user_id: # 15. 메모 기능 업그레이드: 세션의 id값과 메모의 user_id값(메모를 작성한 유저의 id값)이 다른 경우
      ns.abort(403) # 15. 메모 기능 업그레이드: 403 에러 발생(403: Forbidden) -> 리소스는 존재하지만, 접근 권한이 없다
    if memo.linked_image: # 15. 메모 기능 업그레이드: 조회한 MemoModel에 이미 바인딩 된 이미지가 존재하는 경우
      origin_path = os.path.join( # 15. 메모 기능 업그레이드: 바인딩 된 이미지의 업로드 경로(삭제하기 위해 생성)
        current_app.root_path, # 15. 메모 기능 업그레이드: 루트 경로와
        memo.linked_image # 15. 메모 기능 업그레이드: memo의 linked_image(경로) join
      )
      if os.path.isfile(origin_path): # 15. 메모 기능 업그레이드: 업로드 된 경로에 파일이 존재하는 경우
        shutil.rmtree(os.path.dirname(origin_path)) # 15. 메모 기능 업그레이드: 지정된 폴더(바인딩 된 이미지 파일의 폴더 경로)와 하위 파일을 전부 삭제
      memo.linked_image = None # 15. 메모 기능 업그레이드: memo의 linked_image값 None 처리
      g.db.commit() # 15. 메모 기능 업그레이드: DB에 commit(세션)
      return '', 204 # 15. 메모 기능 업그레이드: return None, 삭제에 성공했을 때 response code 204(204: No Content)
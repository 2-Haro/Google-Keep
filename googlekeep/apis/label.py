from flask import g
from flask_restx import Namespace, fields, reqparse, Resource
from googlekeep.models.label import Label as LabelModel
from googlekeep.models.user import User as UserModel

ns = Namespace( # 16. 라벨 기본 기능 구현: Namespace init
  'labels', # 16. 라벨 기본 기능 구현: URL에 붙는 이름
  description='라벨 관련 API' # 16. 라벨 기본 기능 구현: 설명
)

# 16. 라벨 기본 기능 구현: Response Mapping -> Marshalling: 설계한 Model의 값에 맞는 field들에만 해당되는 데이터들이 자동으로 mapping 되어서 프론트에 노출
label = ns.model('Label', {
  'id': fields.Integer(required=True, description='라벨 고유 번호'), # 16. 라벨 기본 기능 구현: id -> 정수, 필수 요소, 라벨 고유 번호
  'user_id': fields.Integer(required=True, description='라벨 작성자 유저 고유 번호'), # 16. 라벨 기본 기능 구현: user_id -> 정수, 필수 요소, 라벨 작성자 유저 고유 번호
  'content': fields.String(required=True, description='라벨 내용'), # 16. 라벨 기본 기능 구현: content -> 문자열, 필수 요소, 라벨 내용
  'created_at': fields.DateTime(description='라벨 생성일') # 16. 라벨 기본 기능 구현: created_at -> DateTime, 라벨 생성일
})

parser = reqparse.RequestParser() # 16. 라벨 기본 기능 구현: RequestParser init
# POST parser
parser.add_argument('content', required=True, type=str, help='라벨 내용', location='form') # 16. 라벨 기본 기능 구현: 받아올 정보 -> content

# /api/labels
@ns.route('')
class LabelList(Resource): # 16. 라벨 기본 기능 구현: 모든 라벨의 정보 사용(복수)
  @ns.marshal_list_with(label, skip_none=True) # 16. 라벨 기본 기능 구현: Marshalling 정의(label에 대한 marshalling, skip_none=True: 특정 field가 null이거나 데이터가 없을 경우에는 키 값을 만들지 않는다)
  def get(self): # 16. 라벨 기본 기능 구현: GET Method
    '''라벨 복수 조회'''
    query = LabelModel.query.join( # 16. 라벨 기본 기능 구현: join(inner join)을 통해서 LabelModel을
      UserModel, # 16. 라벨 기본 기능 구현: UserModel과 연결
      UserModel.id == LabelModel.user_id # 16. 라벨 기본 기능 구현: UserModel의 id(User Table의 id(기본키))와 LabelModel의 user_id(Label Table의 user_id(외래키))가 같은 항목만 선택 -> 메모를 작성한 유저별로 분류
    ).filter( # 16. 라벨 기본 기능 구현: filter 사용
      UserModel.id == g.user.id # 16. 라벨 기본 기능 구현: 로그인 되어 있는 유저의 라벨 정보만 가지고 와야 하기 때문에 세션 내 유저의 id로 조회
    )
    return query.all() # 16. 라벨 기본 기능 구현: joim한 정보 모두 return
  
  @ns.marshal_list_with(label, skip_none=True) # 16. 라벨 기본 기능 구현: Marshalling 정의(label에 대한 marshalling, skip_none=True: 특정 field가 null이거나 데이터가 없을 경우에는 키 값을 만들지 않는다) 
  @ns.expect(parser) # 16. 라벨 기본 기능 구현: POST Method에서 (POST) parser 사용 명시
  def post(self): # 16. 라벨 기본 기능 구현: POST Method
    '''라벨 생성'''
    args = parser.parse_args() # 16. 라벨 기본 기능 구현: args에 POST할 데이터들 담기
    content = args['content'] # 16. 라벨 기본 기능 구현: LabelModel의 conten를 POST된 content로 설정
    label = LabelModel.query.join( # 16. 라벨 기본 기능 구현: join(inner join)을 통해서 LabelModel을
      UserModel, # 16. 라벨 기본 기능 구현: UserModel과 연결
      UserModel.id == LabelModel.user_id # 16. 라벨 기본 기능 구현: UserModel의 id(User Table의 id(기본키))와 LabelModel의 user_id(Label Table의 user_id(외래키))가 같은 항목만 선택 -> 메모를 작성한 유저별로 분류
    ).filter( # 16. 라벨 기본 기능 구현: filter 사용
      UserModel.id == g.user.id, # 16. 라벨 기본 기능 구현: 로그인 되어 있는 유저의 라벨 정보만 가지고 와야 하기 때문에 세션 내 유저의 id로 조회
      LabelModel.content == content # 16. 라벨 기본 기능 구현: 중복되는 데이터 체크
    ).first()
    if label: # 16. 라벨 기본 기능 구현: 중복되는 데이터가 존재하면 오류 발생
      ns.abort(409) # 16. 라벨 기본 기능 구현: 409 에러 발생(conflict)
    label = LabelModel( # 16. 라벨 기본 기능 구현: 라벨 생성
      content=content, # 16. 라벨 기본 기능 구현: content를 POST된 content로 설정
      user_id=g.user.id # 16. 라벨 기본 기능 구현: LabelModel의 user_id를 세션의 user_id로 설정
    )
    g.db.add(label) # 16. 라벨 기본 기능 구현: DB에 라벨 추가(세션)
    g.db.commit() # 16. 라벨 기본 기능 구현: DB에 commit(세션)
    return label, 201 # 16. 라벨 기본 기능 구현: return label, 생성에 성공했을 때 response code 201(201: created)

# /api/labels/id
@ns.route('/<int:id>') 
@ns.param('id', '라벨 고유 번호') # 16. 라벨 기본 기능 구현: id에 대한 설명(라벨 고유 번호) 
class Label(Resource): # 16. 라벨 기본 기능 구현: 특정 id값을 가지는 라벨 정보 사용(단수)
  def delete(self, id): # 16. 라벨 기본 기능 구현: DELETE Method
    '''라벨 삭제'''
    label = LabelModel.query.get_or_404(id) # 16. 라벨 기본 기능 구현: id값을 가진 라벨 단수 조회, id에 해당하는 라벨이 없다면 404 에러
    if label.user_id != g.user.id: # 16. 라벨 기본 기능 구현:  세션의 id값과 라벨의 user_id값(라벨을 작성한 유저의 id값)이 다른 경우
      ns.abort(403) # 16. 라벨 기본 기능 구현: 403 에러 발생(403: Forbidden) -> 리소스는 존재하지만, 접근 권한이 없다
    g.db.delete(label) # 16. 라벨 기본 기능 구현: 세션의 id값과 라벨의 user_id값(라벨을 작성한 유저의 id값)이 같은 경우 DB에서 삭제(세션)
    g.db.commit() # 16. 라벨 기본 기능 구현: DB에 commit(세션)
    return '', 204 # 16. 라벨 기본 기능 구현: return None, 삭제에 성공했을 때 response code 204(204: No Content)
from flask import g
from flask_restx import Namespace, Resource, fields, reqparse
from googlekeep.models.user import User as UserModel
from werkzeug import security

ns = Namespace( # 8. API 문서 자동화: Namespace init
  'users', # 8. API 문서 자동화: URL에 붙는 이름
  description='유저 관련 API' # 8. API 문서 자동화: 설명
)

# 8. API 문서 자동화: Response Mapping -> Marshalling: 설계한 Model의 값에 맞는 field들에만 해당되는 데이터들이 자동으로 mapping 되어서 프론트에 노출
user = ns.model('User', {
  'id': fields.Integer(required=True, description='유저 고유 번호'), # 8. API 문서 자동화: id -> 정수, 필수 요소, 유저 고유 번호
  'user_id': fields.String(required=True, description='유저 ID'), # 8. API 문서 자동화: user_id -> 문자열, 필수 요소, 유저 ID
  'user_name': fields.String(required=True, description='유저 이름'), # 8. API 문서 자동화: user_name -> 문자열, 필수 요소, 유저 이름
  'created_at': fields.DateTime(description='유저 생성 시간') # 9. DB 마이그레이션: created_at -> DateTime, 필수 요소 X, 유저 생성 시간
  # 8. API 문서 자동화: 'password' 작성 X -> 프론트에 노출 X
})

# TODO: 유저 삭제 API 생성

# 8. API 문서 자동화: reqparse -> API 호출을 할 때 특정 값을 넣어서 전달 받은 후에 데이터베이스에 넣어주는 일련의 과정 수행(넘어온 데이터 조회)
post_parser = reqparse.RequestParser() # 8. API 문서 자동화: RequestParser init
# 8. API 문서 자동화: POST parser
post_parser.add_argument('user_id', required=True, help='유저 고유 ID', location='form') # 8. API 문서 자동화: 받아올 정보 -> user_id
post_parser.add_argument('user_name', required=True, help='유저 이름', location='form') # 8. API 문서 자동화: 빋이올 정보 -> user_name
post_parser.add_argument('password', required=True, help='유저 패스워드', location='form') # 8. API 문서 자동화: 받아올 정보 -> password

# /api/users
@ns.route('')
@ns.response(409, 'User ID already exists') # 8. API 문서 자동화: 409 에러 시 메시지
# @ns.deprecated # 12. 세션 기반 인증 흐름 구현: 사용하지 않은 api 비활성화
class UserList(Resource): # 8. API 문서 자동화: 모든 유저의 정보 사용(복수)
  @ns.marshal_list_with(user, skip_none=True) # 8. API 문서 자동화: Marshalling 정의(user에 대한 marshalling, skip_none=True: 특정 field가 null이거나 데이터가 없을 경우에는 키 값을 만들지 않는다)
  def get(self): # 8. API 문서 자동화: GET Method
    '''유저 복수 조회'''
    data = UserModel.query.all() # 8. API 문서 자동화: 유저 복수 조회
    return data
  
  @ns.expect(post_parser) # 8. API 문서 자동화: POST Method에서 POST parser 이용 명시
  @ns.marshal_list_with(user, skip_none=True) # 8. API 문서 자동화: Marshalling 정의(user에 대한 marshalling, skip_none=True: 특정 field가 null이거나 데이터가 없을 경우에는 키 값을 만들지 않는다)
  def post(self): # 8. API 문서 자동화: POST Method
    '''유저 생성'''
    args = post_parser.parse_args() # 8. API 문서 자동화: args에 POST 할 데이터들 담기
    user_id = args['user_id'] # 8. API 문서 자동화: user_id를 args의 user_id(POST한 user_id)로 설정
    user = UserModel.find_one_by_user_id(user_id) # 8. API 문서 자동화: 유저 아이디 존재 여부 확인
    if user: # 8. API 문서 자동화: 유저가 이미 있는 경우
      ns.abort(409) # 8. API 문서 자동화: 409 에러 발생(abort: return과 마찬가지로 process 종료)
    user = UserModel( # 8. API 문서 자동화: 유저가 존재하지 않는 경우 유저 생성
      user_id = user_id, # 8. API 문서 자동화: UserModel의 user_id를 POST한 user_id로 설정
      user_name = args['user_name'], # 8. API 문서 자동화: UserModel의 user_name을 POST한 user_name으로 설정
      password = security.generate_password_hash(args['password']) # 8. API 문서 자동화: UserModel의 password를 POST한 password로 설정(werkzeug로 암호화)
    )
    g.db.add(user) # 8. API 문서 자동화: DB에 user 추가(세션)
    g.db.commit() # 8. API 문서 자동화: DB에 commit(세션)
    return user, 201 # 8. API 문서 자동화: return user, 생성에 성공했을 때 response code 201(created)

# /api/users/id
@ns.route('/<int:id>')
@ns.param('id', '유저 고유 번호') # 8. API 문서 자동화: id에 대한 설명(유저 고유 번호)
# @ns.deprecated # 12. 세션 기반 인증 흐름 구현: 사용하지 않은 api 비활성화
class User(Resource):  # 8. API 문서 자동화: 특정 id값을 가지는 유저 정보 사용(단수)
  @ns.marshal_list_with(user, skip_none=True) # 8. API 문서 자동화: Marshalling 정의(user에 대한 marshalling, skip_none=True: 특정 field가 null이거나 데이터가 없을 경우에는 키 값을 만들지 않는다)
  def get(self, id): # 8. API 문서 자동화: GET Method
    '''유저 단수 조회'''
    data = UserModel.query.get_or_404(id) # 8. API 문서 자동화: id값을 가진 유저 단수 조회, id에 해당하는 유저가 없다면 404 에러
    return data
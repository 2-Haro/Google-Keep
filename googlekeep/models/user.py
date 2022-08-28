from googlekeep import db # 6. 데이터베이스: db(SQLAlchemy) import
from sqlalchemy import func

class User(db.Model): # 6. 데이터베이스: User Class(Table) 생성
  id = db.Column(db.Integer, primary_key=True) # 6. 데이터베이스: id -> 정수, 기본키(auto_increment 자동 적용)
  user_id = db.Column(db.String(20), unique=True, nullable=False) # 6. 데이터베이스: user_id(유저 id) -> 문자열, 중복 X, NULL X
  user_name = db.Column(db.String(20), nullable=False) # 6. 데이터베이스: user_name(유저 이름) -> 문자열, NULL X
  password = db.Column(db.String(1000), nullable=False) # 6. 데이터베이스: password(비밀번호) -> 문자열, NULL X
  created_at = db.Column(db.DateTime(), server_default=func.now()) # 9. DB 마이그레이션: created_at(유저 생성 시간) -> DateTime, 기본값=현재 시간(데이터 생성 시간)
  # 9. DB 마이그레이션: server_default -> 빈 형태의 데이터들이 있을 경우에도 모두 func.now() 실행, default -> Migration을 하고 난 이후에 들어가는 데이터들에 한해서 func.now() 실행

  @classmethod # 7. 리팩토링: 클래스 메서드 사용
  def find_one_by_user_id(cls, user_id): # 7. 리팩토링: user_id를 찾는 함수
    return User.query.filter_by(user_id=user_id).first() # 7. 리팩토링: user_id를 찾는 쿼리
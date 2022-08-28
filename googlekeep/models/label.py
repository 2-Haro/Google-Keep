from googlekeep import db
from sqlalchemy import func

class Label(db.Model): # 16. 라벨 기본 기능 구현: Label Class(Table) 생성
  id = db.Column(db.Integer, primary_key=True) # 16. 라벨 기본 기능 구현: id(라벨 id) -> 정수, 기본키(auto_increment 자동 적용)
  content = db.Column(db.String(10), unique=True, nullable=False) # 16. 라벨 기본 기능 구현: content(내용) -> 문자열, 중복 X, NULL X
  created_at = db.Column(db.DateTime(), default=func.now()) # 16. 라벨 기본 기능 구현: created_at(라벨 생성 시간) -> DateTime, 기본값=현재 시간(데이터 생성 시간)
  user_id = db.Column( # 16. 라벨 기본 기능 구현: user_id(라벨 생성 유저 id) -> 정수, NULL X
    db.Integer,
    db.ForeignKey( # 16. 라벨 기본 기능 구현: 외래키
      'user.id', # 16. 라벨 기본 기능 구현: user table의 id와 관계 맺음
      ondelete='CASCADE' # 16. 라벨 기본 기능 구현: user table의 id가 삭제되면 동일하게 삭제
    ),
    nullable=False
  )
  __table_args__ = (
    db.UniqueConstraint( # 16. 라벨 기본 기능 구현: Unique Key(content와 user_id 이용) 생성(유저가 동일한 이름의 라벨 여러 개 생성 X, 유저 id가 다르면 동일한 이름의 라벨 생성 가능) -> 튜플
      "content", # 16. 라벨 기본 기능 구현: Field(Column) 값
      "user_id", # 16. 라벨 기본 기능 구현: Field(Column) 값
      name="uk_content_user_id"
    ),
  )
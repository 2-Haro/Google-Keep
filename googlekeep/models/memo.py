from googlekeep import db
from sqlalchemy import func

memos_labels = db.Table( # 17. 메모 라벨링 기능 업데이트: Association Table -> 양쪽의 외부 키를 attribute로 가진다 (두 개의 컬럼을 이용해서 DB에 기본키 생성)
  'memos_labels', # 17. 메모 라벨링 기능 업데이트: 테이블명 -> memos_labels
  db.Column('memo_id', db.Integer, db.ForeignKey('memo.id'), primary_key=True), # 17. 메모 라벨링 기능 업데이트: memo_id(메모 id) -> 정수, 외래키(memo table의 id와 관계 맺음), 기본키(auto_increment 자동 적용)
  db.Column('label_id', db.Integer, db.ForeignKey('label.id'), primary_key=True) # 17. 메모 라벨링 기능 업데이트: label_id(라벨 id) -> 정수, 외래키(label table의 id와 관계 맺음), 기본키(auto_increment 자동 적용)
)

class Memo(db.Model): # 13. 메모 기본 기능 구현: Memo Class(Table) 생성
  id = db.Column(db.Integer, primary_key=True) # 13. 메모 기본 기능 구현: id(메모 id) -> 정수, 기본키(auto_increment 자동 적용)
  title = db.Column(db.String(100), nullable=False) # 13. 메모 기본 기능 구현: title(제목) -> 문자열, NULL X
  content = db.Column(db.Text, nullable=False) # 13. 메모 기본 기능 구현: content(내용) -> Text(String 보다 긴 문자열 가능), NULL X
  linked_image = db.Column(db.String(200), nullable=True) # 15. 메모 기능 업그레이드: linked_image(이미지) -> 문자열, NULL 가능
  is_deleted = db.Column(db.Boolean(), nullable=False, default=False) # 15. 메모 기능 업그레이드: is_deleted(삭제 여부) -> Boolean, NULL X, 기본값=False
  created_at = db.Column(db.DateTime(), default=func.now()) # 13. 메모 기본 기능 구현: created_at(유저 생성 시간) -> DateTime, 기본값=현재 시간(데이터 생성 시간)
  updated_at = db.Column(db.DateTime(), default=func.now(), onupdate=func.now()) # 13. 메모 기본 기능 구현: updated_at(메모 업데이트 시간) -> DateTime, 기본값=현재 시간(데이터 생성 시간), 업데이트=현재 시간(데이터 업데이트 시간)
  user_id = db.Column( # 13. 메모 기본 기능 구현: user_id(메모 생성 유저 id) -> 정수, NULL X
    db.Integer,
    db.ForeignKey( # 13. 메모 기본 기능 구현: 외래키
      'user.id', # 13. 메모 기본 기능 구현: user table의 id와 관계 맺음
      ondelete="CASCADE" # 13. 메모 기본 기능 구현: user table의 id가 삭제되면 동일하게 삭제
    ),
    nullable=False
  )
  labels = db.relationship( # 17. 메모 라벨링 기능 업데이트: Memo Class는 labels라는 값을 가지는데, 
    'Label', # 17. 메모 라벨링 기능 업데이트: Label table과의 연관성을 가지고,
    secondary=memos_labels, # 17. 메모 라벨링 기능 업데이트: 다대다 관계(memos_labels)를 참조하며,
    backref=db.backref('memos') # 17. 메모 라벨링 기능 업데이트: Label 객체에서도 memos 객체에 접근하도록 처리(역참조)
    )
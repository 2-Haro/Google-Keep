from flask import Flask, g, render_template # Flask, g, render_template Import
from flask_wtf.csrf import CSRFProtect # 2. CSRF 방어: Flask WTF Import
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

csrf = CSRFProtect() # 2. CSRF 방어: Flask WTF init
db = SQLAlchemy() # 6. 데이터베이스: SQLAlchemy(ORM) init
migrate = Migrate() # 6. 데이터베이스: Migrate(데이터베이스 형상관리 툴) init

def create_app(config=None): # 0. 기초: create_app()을 자동으로 Flask가 실행시키고, __init__.py를 통해서 디렉토리가 모듈화됐기 때문에 googlekeep을 python 파일로 인식 # 10. Flask Configs: config을 받아서 None 처리
  app = Flask(__name__)

  '''Flask Configs'''
  from .configs import DevelopmentConfig, ProductionConfig
  if not config: # 10. Flask Configs: config가 None인 경우
    if app.config['DEBUG']: # 10. Flask Configs: app.config가 DEBUG인 경우(export FLASK_APP=googlekeep FLASK_ENV=development)
      config = DevelopmentConfig() # 10. Flask Configs: config을 DevelopmentConfig(개발 환경)으로 설정
    else: # 10. Flask Configs: app.config가 DEBUG가 아닌 경우(export FLASK_APP=googlekeep FLASK_ENV=production)
      config = ProductionConfig() # 10. Flask Configs: config을 ProductionConfig(배포 환경)으로 설정
    
  app.config.from_object(config) # 10. Flask Configs: config 실행을 위해서 from_object 사용해서 호출

  '''CSRF INIT'''
  csrf.init_app(app) # 2. CSRF 방어: CSRF init

  '''DB INIT'''
  db.init_app(app) # 6. 데이터베이스: DB init
  if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'): # 6. 데이터베이스: pytest를 사용할 때 사용할 sqlite에는 ALTER 쿼리를 사용할 수 없으므로 예외처리
    migrate.init_app(app, db, render_as_batch=True) # 6. 데이터베이스: Migrate init(sqlite) -> 새로운 테이블을 만들고 기존 데이터를 옮긴 후 기존 테이블을 지우는 batch 연산을 하도록 한다
  else:
    migrate.init_app(app, db) # 6. 데이터베이스: Migrate init(MySQL)

  '''RESTX INIT'''
  from googlekeep.apis import blueprint as api
  app.register_blueprint(api) # 8. API 문서 자동화: restx init -> Flask 앱에 api 페이지 연결
  # csrf.exempt(api) # 14. ajax CSRF 처리: api docs는 개발 환경에서만 사용 권장 -> production 환경에서 허용하고자 할 경우 사용

  '''Routes INIT'''
  from googlekeep.routes import base_route, auth_route
  app.register_blueprint(base_route.bp) # 3. 라우터 확장: Flask 앱에 index 페이지(base_route) 연결
  app.register_blueprint(auth_route.bp) # 3. 라우터 확장: Flask 앱에 auth 페이지(auth_route) 연결

  '''REQUSET HOOK'''
  @app.before_request # 7. 리팩토링: request 실행 전에 실행
  def before_request():
    g.db = db.session # 7. 리팩토링: request 실행 전에 db.session을 g 컨텍스트에 넣어준다(물려준다)
  
  @app.teardown_request # 7. 리팩토링: request가 끝날 때 실행
  def teardown_request(exception):
    if hasattr(g, 'db'): # 7. 리팩토링: g에 db라는 값이 설정되어 있다면(DB가 열려있다면)
      g.db.close() # 7. 리팩토링: request가 끝날 때 DB를 닫아준다

  @app.errorhandler(404) # 1. 템플릿 엔진 기초: 404 에러 Router 정의
  def page_404(error):
    return render_template('404.html'), 404 # 1. 템플릿 엔진 기초: 첫번째 인자: template 경로, 두번째 인자: 에러 코드

  return app
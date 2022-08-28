from flask import Blueprint, render_template, redirect, url_for, flash, session, request, g
from googlekeep.forms.auth_form import LoginForm, RegisterForm # 2. CSRF 방어: Router 정의
from googlekeep.models.user import User as UserModel # 6. 데이터베이스: 연결(flask db migrate 이용) -> flask DB가 인식
from werkzeug import security # 5. 로그인 기능 구현: import werkzeug

NAME = 'auth'

bp = Blueprint(NAME, __name__, url_prefix='/auth') # 3. 라우터 확장: Blueprint Init # 3. 라우터 확장: Blueprint 아래에 작성되는 route들은 모두 prefix(접두사)로 auth를 가지게 된다

@bp.before_app_request # 7. 리팩토링: before_request를 사용하면 해당 Blueprint(namespace)에 유입된 request 앞에서만 실행이 되지만, before_app_request를 사용하면 앱 전체에 전달된다(매 before_request 마다)
def before_app_request(): # 7. 리팩토링: 유저 세션 관리 -> g 컨텍스트로 빠르게 유저 모델에 접근
  g.user = None # 7. 리팩토링: 우선 g.user를 None 처리 한다
  user_id = session.get('user_id') # 7. 리팩토링: user_id를 현재 session의 user_id로 설정한다
  if (user_id): # 7. 리팩토링: user_id가 존재하는 경우(유저가 있는 경우)
    user = UserModel.find_one_by_user_id(user_id) # 7. 리팩토링: user.py에 있는 find_one_by_user_id를 사용해서 user에 user_id 저장
    if user: # 7. 리팩토링: user가 존재하는 경우(정확한 유저 정보가 들어가 있다고 간주)
      g.user = user # 7. 리팩토링: g.user를 user로 설정
    else: # 7. 리팩토링: user가 존재하지 않는 경우(잘못된 유저 정보가 들어가 있다고 간주)
      session.pop('user_id', None) # 7. 리팩토링: 세션에 저장되어 있는 user_id pop

@bp.route('/')
def index():
  return redirect(url_for(f'{NAME}.login')) # 3. 라우터 확장: index 페이지에 접근하더라도 login 페이지로 redirect

@bp.route('/login', methods=['GET', 'POST']) # 2. CSRF 방어: route -> /auth/login # Method -> GET, POST # 3. 라우터 확장: url_prefix가 auth이므로 경로에서 auth 생략 가능
def login():
  form = LoginForm() # 2. CSRF 방어: form 정의(Login Form)
  if form.validate_on_submit(): # 2. CSRF 방어: form(LoginForm)에 있는 함수인 validate_on_submit()을 사용해 POST Method인지(request.method == 'POST'), validator로 정의했던 내용들이 정상적으로 통과가 되는지 확인(전송된 form 데이터의 정합성 점검 -> POST, validate OK)
    user_id = form.data.get('user_id') # 유저 아이디 가져오기
    password = form.data.get('password') # 유저 패스워드 가져오기
    user = UserModel.find_one_by_user_id(user_id) # 7. 리팩토링: user.py에 있는 find_one_by_user_id를 사용해서 user에 user_id 저장
    if user: # 5. 로그인 기능 구현: DB에 유저가 존재하는 경우
      if not security.check_password_hash(user.password, password): # 5. 로그인 기능 구현: DB에 있는 user의 password와 입력한 password가 같은지 검사(암호화된 상태로)
        flash("Password is not valid.") # 에러 메시지 출력
      else:
        session['user_id'] = user_id # 5. 로그인 기능 구현: session(세션 컨텍스트)의 user_id를 입력한 user_id로 설정
        return redirect(url_for('base.index')) # 5. 로그인 기능 구현: index 페이지로 redirect(로그인 성공)
    else: # 5. 로그인 기능 구현: DB에 유저가 존재하지 않는 경우
      flash("User ID does not exist.") # 에러 메시지 출력
  else:
    flash_form_errors(form) # 4. 메시지 플래싱(에러)
  return render_template(f'{NAME}/login.html', form=form) # 2. CSRF 방어: render auth/login.html template, form은 RegisterForm # 좌항: html 내에서 사용할 변수 이름(login.html line 10), 우항: 변수의 값(LoginForm)

@bp.route('/register', methods=['GET', 'POST']) # 2. CSRF 방어: route -> /auth/register # Method -> GET, POST # 3. 라우터 확장: url_prefix가 auth이므로 경로에서 auth 생략 가능
def register():
  form = RegisterForm() # 2. CSRF 방어: form 정의(Register Form)
  if form.validate_on_submit(): # 2. CSRF 방어: form(RegisterForm)에 있는 함수인 validate_on_submit()을 사용해 POST Method인지(request.method == 'POST'), validator로 정의했던 내용들이 정상적으로 통과가 되는지 확인(전송된 form 데이터의 정합성 점검 -> POST, validate OK)
    user_id = form.data.get('user_id') # 유저 아이디 가져오기
    user_name = form.data.get('user_name') # 유저 이름 가져오기
    password = form.data.get('password') # 유저 패스워드 가져오기
    repassword = form.data.get('repassword') # 유저 재입력 패스워드 가져오기
    user = UserModel.find_one_by_user_id(user_id) # 7. 리팩토링: user.py에 있는 find_one_by_user_id를 사용해서 user에 user_id 저장
    if user: # 5. 로그인 기능 구현: DB에 유저가 존재하는 경우
      flash('User ID already exists.') # 에러 메시지 출력
      return redirect(request.path) # 5. 로그인 기능 구현: request.path(쿼리를 제외한 path 정보) -> /auth/register로 redirect
    else: # 5. 로그인 기능 구현: DB에 유저가 존재하지 않는 경우
      g.db.add( # 7. 리팩토링: DB에 유저 추가
        UserModel(
          user_id=user_id, # 5. 로그인 기능 구현: DB에 추가할 UserModel의 user_id를 user_id로 설정
          user_name=user_name, # 5. 로그인 기능 구현: DB에 추가할 UserModel의 user_name을 user_name으로 설정
          password=security.generate_password_hash(password) # 5. 로그인 기능 구현: DB에 추가할 UserModel의 password를 security.generate_password_hash()함수를 사용해서 암호회된 password로 설정
        )
      )
      g.db.commit() # 7. 리팩토링: DB 커밋 
      session['user_id'] = user_id # 5. 로그인 기능 구현: session(세션 컨텍스트)의 user_id를 입력한 user_id로 설정
      return redirect(url_for('base.index')) # 5. 로그인 기능 구현: index 페이지로 redirect(회원가입 성공)
  else:
    flash_form_errors(form) # 4. 메시지 플래싱(에러)
  return render_template(f'{NAME}/register.html', form=form) # 2. CSRF 방어: render auth/register.html template, form은 RegisterForm # 좌항: html 내에서 사용할 변수 이름(register.html line 9), 우항: 변수의 값(RegisterForm)

@bp.route('/logout') # 2. CSRF 방어: route -> /auth/logout # Method -> GET, POST
def logout():
  session.pop('user_id', None) # 5. 로그인 기능 구현: 세션에 저장되어 있는 user_id pop
  return redirect(url_for(f'{NAME}.login')) # 5. 로그인 기능 구현: 로그인 페이지로 redirect

def flash_form_errors(form): # 4. 메시지 플래싱: 에러 노출을 위한 함수
  for _, errors in form.errors.items(): # 4. 메시지 플래싱: form.errors에 에러 존재
    for e in errors:
      flash(e) # 4. 메시지 플래싱: flash -> 가장 빠르게 에러를 프론트에 노출시킬 수 있는 방법
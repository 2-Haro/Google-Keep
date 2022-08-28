from flask_wtf import FlaskForm # 2. CSRF 방어: FlaskForm Import(Flask WTF을 이용한 Form 만들기)
from wtforms import StringField, PasswordField # 2. CSRF 방어: 필요한 Field들 정의
from wtforms.validators import DataRequired, EqualTo # 2. CSRF 방어: DataRequired -> 필수 데이터, EqualTo -> 동일한 값인지 비교

class LoginForm(FlaskForm): # 2. CSRF 방어: 로그인 페이지 Form # FlaskForm 상속
  user_id = StringField('User Id', validators=[DataRequired()]) # 2. CSRF 방어: User Id Field # 프론트에 노출되는 라벨: User Id
  password = PasswordField('Password', validators=[DataRequired()]) # 2. CSRF 방어: User Password Field

class RegisterForm(LoginForm): # 2. CSRF 방어: 회원가입 페이지 Form # LoginForm 상속(중복되는 부분 감소)
  password = PasswordField( # 2. CSRF 방어: password 재정의
    'Password',
    validators=[DataRequired(), EqualTo( # 2. CSRF 방어: password 입력, repassword와 동일한 값인지 비교
      'repassword',
      message='Passwords must match.')]) # 2. CSRF 방어: 동일한 값이 아닐 경우 노출시키는 메시지
  repassword = PasswordField('Confirm Password', validators=[DataRequired()]) # 2. CSRF 방어: password 다시 입력
  user_name = StringField('User Name', validators=[DataRequired()]) # 2. CSRF 방어: User Name Field
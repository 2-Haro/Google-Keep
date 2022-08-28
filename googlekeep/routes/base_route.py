from flask import Blueprint, render_template, g, redirect, url_for

NAME = 'base'

bp = Blueprint(NAME, __name__) # 3. 라우터 확장: Blueprint Init

@bp.route('/') # 3. 라우터 확장: index 페이지 정의(base 경로)
def index():
  if not g.user: # 12. 세션 기반 인증 흐름 구현: 로그인되어 있지 않다면
    return redirect(url_for('auth.login')) # 12. 세션 기반 인증 흐름 구현: 로그인 페이지로 redirect
  return render_template('index.html') # 1. 템플릿 엔진 기초: render_template 함수는 기본적으로 프로젝트 폴더 내의 'templates'라는 이름의 폴더를 기본 경로로 설정한다 -> render index.html template
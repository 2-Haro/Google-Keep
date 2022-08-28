# 18. Dockerizing: FROM -> 어떤 이미지를 쓸 것인가?
# 18. Dockerizing: Docker hub에서 python 3.8 Image를 써서 Container를 띄워준다(Base Image)
FROM python:3.8

# root 권한
# 18. Dockerizing: RUN -> Command 실행
# 18. Dockerizing: 유저 추가, 패스워드 입력 필요 X, 홈 디렉토리 자동 생성
RUN adduser --disabled-password python

# 18. Dockerizing: USER -> 권한 전환
# 18. Dockerizing: 위에서 생성한 python 유저로 권한 전환 (root -> python)
USER python

# 18. Dockerizing: COPY -> 복사
# 18. Dockerizing: (python) 의존성 패키지 복사(requirements.txt -> Docker Image내의 tmp 경로의 requirements.txt로 복사)
COPY ./requirements.txt /tmp/requirements.txt

# 18. Dockerizing: (python) 의존성 패키지 설치
# 18. Dockerizing: python 유저로 설치, python 의존성 패키지들은 홈 디렉토리에 위치
RUN pip install --user -r /tmp/requirements.txt
# 18. Dockerizing: gunicorn 설치
RUN pip install --user gunicorn==20.1.0

# 18. Dockerizing: 프로젝트 복사(Owner와 Group을 python(유저)으로 바꾼다) -> 현재 위치에 있는 모든 파일을 Docker Image안의 www/googlekeep 경로로 복사한다
COPY --chown=python:python ./ /var/www/googlekeep

# 18. Dockerizing: WORKDIR -> 경로로 이동
# 18. Dockerizing: 복사한 프로젝트 경로로 이동
WORKDIR /var/www/googlekeep

# 18. Dockerizing: ENV -> 환경변수 설정
# 18. Dockerizing: 설치한 패키지 명령어를 사용하기 위해 환경변수 등록
ENV PATH="/home/python/.local/bin:${PATH}"

# 18. Dockerizing: entrypoint shell 실행 권한
RUN chmod +x ./etc/docker-entrypoint.sh

# 18. Dockerizing: EXPOSE -> 노출
# 18. Dockerizing: 8080 포트 노출
EXPOSE 8080

# 18. Dockerizing: CMD -> 해당 이미지를 컨테이너로 띄울 때 default로 실행할 커맨드나, ENTRYPOINT 명령문으로 지정된 커맨드에 default로 넘길 파라미터 지정할 때 사용
# 18. Dockerizing: gunicorn 실행(8080 포트 바인딩)
# CMD gunicorn --bind :8080 --workers 2 --threads 8 'googlekeep:create_app()' # 18. Dockerizing: docker-entrypoint.sh에서 정의
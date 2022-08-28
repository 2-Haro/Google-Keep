#!/bin/bash

set -e # 18. Dockerizing: 에러

flask db upgrade # 18. Dockerizing: docker-compose를 실행시킬 때 gk-db(DB)가 처음으로 뜨기 때문에(초기화된 상태이기 때문에) DB 업그레이드

# 18. Dockerizing: gunicorn 실행(8080 포트 바인딩) # --access-logfile: Docker Container 로그를 볼 때 HTTP request 등이 전달되면 Docker Container 로그 노출
# gunicorn --bind :8080 --workers 2 --threads 8 --access-logfile - 'googlekeep:create_app()'

# 18. Dockerizing: gunicorn 실행(socket으로 변경 -> tmp/gunicorn.sock 을 만들어서 통신) # --reload: 수정사항이 발생했을 때 graceful reload
gunicorn --bind unix:/tmp/gunicorn.sock --workers 2 --threads 8 --reload --access-logfile - 'googlekeep:create_app()'
# mecab-ko-dic-admin

Django Admin에서 MeCab 시스템·사용자 사전, 동의어, 불용어를 관리하는 프로젝트입니다.

## 기술 스택

- Python 3.12
- Django 5.2 LTS
- PostgreSQL 17
- uv

정확한 의존성 버전은 `uv.lock`으로 고정합니다.

## 로컬 환경 구성

의존성을 설치합니다.

```bash
uv sync
```

저장소 루트에 `.env`를 만들고 PostgreSQL 접속 정보를 설정합니다.

```dotenv
DJANGO_SECRET_KEY=replace-with-a-local-secret
DB_NAME=mecab_ko_dic
DB_USER=mecab_ko_dic
DB_PASSWORD=replace-with-a-local-password
DB_HOST=127.0.0.1
DB_PORT=6543
```

데이터베이스를 준비하고 개발 서버를 실행합니다.

```bash
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

브라우저에서 `http://127.0.0.1:8000/admin/`에 접속합니다.

## 검사

```bash
uv run python manage.py test
uv run ruff check .
uv run ruff format --check .
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
```

## CSV 가져오기

헤더가 없는 MeCab 12열 CSV를 가져옵니다. 기본 인코딩은 UTF-8입니다.

```bash
uv run python manage.py import_mecab_csv path/to/dictionary.csv --type SYSTEM
uv run python manage.py import_mecab_csv path/to/user-dictionary.csv --type USER
uv run python manage.py import_mecab_csv path/to/compound.csv --type COMPOUND
uv run python manage.py import_mecab_csv path/to/euc-kr.csv --type USER --encoding euc-kr
```

외부 MeCab 소스 디렉터리 전체를 가져오려면 다음 recipe를 사용합니다.

```bash
just import-all
just import-user
```

## CSV 내보내기

```bash
uv run python manage.py export_mecab_csv user-dictionary.csv --type USER
uv run python manage.py export_mecab_csv user-place-names.csv --type USER --category 지명
```

`just export-user-places`는 두 번째 명령의 단축 recipe입니다.

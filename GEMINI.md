# Project Context: mecab-ko-dic-admin

이 프로젝트는 한국어 형태소 분석기인 **MeCab-ko**의 사전을 관리하고 검색 엔진(Elasticsearch, Solr)과 연동하기 위한 Django 기반의 관리 도구입니다.

## 1. 기술 스택 및 주요 구성
- **Backend:** Python 3.12+, Django 5.1, Django Ninja
- **Package Manager:** `uv` (pyproject.toml)
- **Database:** PostgreSQL 17 (Docker)
- **Search Engines:** 
  - Elasticsearch 8.19.14 (ELK Stack)
  - Apache Solr 10.0.0
- **Infrastructure:** Docker Compose (PostgreSQL, ELK, Solr, MeCab Builder)

## 2. 프로젝트 구조
- `mecab_ko_dic/`: 사전 모델 및 관리 로직이 포함된 메인 Django 앱
- `mecab_ko_dic_admin/config/`: Django 설정 및 URL 구성
- `env/`: Docker 인프라 및 환경 설정 (`.env`, `docker-compose.yaml`)
- `Justfile`: 프로젝트 운영을 위한 커맨드 실행기

## 3. 주요 개발 명령어 (just 사용 권장)
프로젝트 루트에서 `just`를 사용하여 주요 작업을 수행할 수 있습니다.

### 인프라 관리
- `just up`: 모든 Docker 컨테이너 실행
- `just down`: 컨테이너 중지
- `just build`: 컨테이너 재빌드 및 실행 (설정 변경 시 사용)
- `just ps`: 서비스 상태 확인

### Django 개발
- `just run`: 개발 서버 실행 (`localhost:8000`)
- `just migrate`: 데이터베이스 마이그레이션 적용
- `just makemigrations`: 모델 변경사항 생성
- `just superuser`: 관리자 계정 생성

### 품질 관리 및 테스트
- `just test`: pytest 실행
- `just lint`: ruff를 통한 코드 검사
- `just format`: ruff를 통한 코드 포맷팅

## 4. 개발 컨벤션
- **Lint/Format:** `ruff`를 사용하여 PEP 8 스타일을 준수합니다.
- **Dependency:** 새로운 패키지 추가 시 `uv add <package>`를 사용하세요.
- **Environment:** 비밀번호나 버전 정보는 `env/.env`에서 관리합니다.

## 5. 특이 사항
- `mecab_ko_dic_builder` 서비스는 Ubuntu 환경에서 MeCab과 한국어 사전을 직접 소스 빌드하여 설치하도록 자동화되어 있습니다.
- Elasticsearch는 초기 실행 시 `es_setup` 서비스를 통해 SSL 인증서와 보안 설정을 자동으로 완료합니다.

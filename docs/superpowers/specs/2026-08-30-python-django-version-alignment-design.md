# Python 및 Django 버전 정렬 설계

- **상태:** Approved
- **날짜:** 2026-08-30
- **대상:** 로컬 개발 환경

## 목표

프로젝트의 공식 개발 환경을 Python 3.12와 Django 5.2 LTS로 통일한다. 의존성 설치, 테스트, Django 관리 명령이 같은 버전 범위에서 재현되도록 프로젝트 메타데이터, 잠금 파일, 개발 문서를 함께 갱신한다.

## 버전 정책

- Python은 `>=3.12,<3.13`으로 제한한다.
- `.python-version`에는 `3.12`를 기록해 pyenv와 uv가 사용 가능한 최신 Python 3.12 패치 버전을 선택하도록 한다.
- Django는 `>=5.2,<5.3`으로 제한해 5.2 LTS의 버그 및 보안 패치는 허용하고 6.x 자동 업그레이드는 방지한다.
- 정확한 패치 버전은 `uv.lock`에서 고정한다.

## 변경 범위

1. `pyproject.toml`의 Python 및 Django 버전 범위를 변경한다.
2. 저장소 루트에 `.python-version`을 추가한다.
3. Python 3.12 기준으로 `uv.lock`을 다시 생성한다.
4. 루트 `README.md`에 기술 스택, 환경 구성, 실행, 검사 및 CSV 명령 사용법을 기록한다.
5. 기존 Phase 1 설계 및 구현 계획 문서에 확정된 런타임 조합을 명시한다.

애플리케이션 모델, 마이그레이션, Admin 동작 및 dev/prod 설정 분리는 변경하지 않는다.

## 검증

Python 3.12 환경에서 다음 검사를 실행한다.

```bash
uv sync
uv run python --version
uv run python -m django --version
uv run pytest
uv run ruff check .
uv run python manage.py check
```

검증 결과는 Python 3.12.x와 Django 5.2.x를 보여야 한다. 실패할 경우 애플리케이션 코드를 우회 수정하지 않고 의존성 또는 환경 문제를 별도로 보고한다.

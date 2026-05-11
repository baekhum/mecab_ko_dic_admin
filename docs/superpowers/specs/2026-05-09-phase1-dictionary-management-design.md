# 설계 문서: mecab-ko-dic-admin Phase 1 (사전 관리 기반 구축)

- **상태:** Draft
- **날짜:** 2026-05-09
- **작성자:** Gemini CLI

## 1. 개요
이 문서는 `mecab-ko-dic-admin` 프로젝트의 첫 번째 단계인 '강력한 사전 관리 도구' 구축에 대한 설계를 다룹니다. 핵심 목표는 MeCab 시스템 사전과 사용자 정의 사전, 그리고 검색 최적화를 위한 동의어 사전을 통합 관리할 수 있는 기반을 마련하는 것입니다.

## 2. 아키텍처 및 데이터 모델

### 2.1 통합 MeCab 사전 모델 (`Mecab_Ko_Dic`)
기존 모델을 확장하여 시스템 사전과 사용자 정의 사전을 통합 관리합니다.
- **추가 필드:**
    - `origin_type`: (SYSTEM, USER, COMPOUND) - 데이터의 출처 구분
    - `is_active`: (Boolean) - 사전 빌드 포함 여부
- **특징:** 하나의 모델로 관리하되, Admin 필터링을 통해 시각적으로 분리.

### 2.2 검색 확장 사전 모델
- **동의어 모델 (`SynonymGroup`, `SynonymWord`):**
    - `SynonymGroup`: 동의어 묶음 (예: "휴대폰 그룹")
    - `SynonymWord`: 그룹에 속한 개별 단어들
- **불용어 모델 (`Stopword`):**
    - 인덱싱에서 제외할 단어 리스트

## 3. 주요 기능 설계

### 3.1 CSV Import Management Command (`import_mecab_csv`)
- **목적:** `sources/` 내의 대량 CSV 데이터를 DB로 임포트.
- **기능:**
    - 파일 경로를 인자로 받아 `bulk_create`를 통한 고속 인서트.
    - `origin_type` 자동 지정.
    - 기존 데이터와의 중복 체크 및 업데이트 로직.

### 3.2 고도화된 Django Admin
- **목록 뷰:** `origin_type`, `pos_tag` 별 필터링 제공.
- **검색:** 표층형 및 읽기에 대한 인덱싱 기반 고속 검색.
- **동의어 관리:** 인라인 편집을 통해 그룹별 동의어 추가/삭제 용이성 확보.

### 3.3 유효성 검사 (Validation)
- MeCab 사전 형식(품사 태그, 종성 유무 'T'/'F' 등)에 대한 필드 레벨 유효성 검사 로직 추가.

## 4. 로드맵 연계 (Next Steps)
- **Phase 2:** 본 단계에서 관리된 데이터를 바탕으로 Elasticsearch/Solr 인덱싱 연동.
- **Phase 3:** 사전 수정 시 Docker 컨테이너 내 MeCab 사전 빌드 자동화 트리거.

## 5. 승인 요청
위 설계 내용에 대해 승인을 요청합니다. 승인 후 구현 계획(Implementation Plan) 수립으로 넘어갑니다.

# CHANGELOG

## 2026-05-28

### Added

- `docs/source-file-catalog.md`를 추가해 주요 소스/문서 파일의 역할, 책임, 수정/운영 주의사항을 정리했다.
- Python 소스 파일에 한글 module docstring을 추가했다.
- `docs/worklog/2026-05-28.md`에 AWS Migration 전 초기 정리 작업 기록을 추가했다.

### Changed

- README에 전체 파일 카탈로그와 파일별 설명 주석 정리 상태를 반영했다.

### Notes

- 기능 변경 없음.
- 실제 크롤링, 외부 API 호출, DB DDL/DML, 주문 실행은 수행하지 않았다.
- 민감정보 값은 문서에 기록하지 않았다.

## 2026-05-27

### Changed

- Externalized DB connection settings to `INTEREST_DB_*` environment variables.
- Removed the hardcoded DB password from source configuration.

### Notes

- 기능 변경 없음.
- 실제 민감정보 값은 문서에 기록하지 않았다.

## 2026-05-26

### Added

- 초기 프로젝트 문서 초안을 추가했다.
  - `AGENTS.md`
  - `README.md`
  - `docs/worklog/2026-05-26.md`

### Notes

- 현재 로컬 파일 구조와 일부 핵심 모듈 확인 결과를 기준으로 작성했다.
- 실제 크롤링, 외부 API 호출, DB DDL/DML, 주문 실행은 수행하지 않았다.
- 민감정보 값은 문서에 기록하지 않았다.

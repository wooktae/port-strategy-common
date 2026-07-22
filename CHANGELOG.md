# CHANGELOG

## 2026-07-01

### Changed

- README에 Common core 책임 경계, consumer 의존성, AWS 운영 dependency 성격, 호환성 계약 section을 추가했다.
- AGENTS.md worklog 들여쓰기 규칙을 최신 고정 규칙(` 1) 큰 작업 명`)으로 정리하고 `1.` 형식 사용 금지를 명시했다.
- 상태 표기 규칙을 `작업 명:완료` 형식(공백 없음)으로 통일했다.

### Added

- `docs/worklog/2026-07-01.md`에 문서 최신화 작업 기록을 추가했다.

### Notes

- 기능 변경 없음. Python 코드, config key, enum 값, dataclass 필드명, decision reason 문자열은 변경하지 않았다.
- Common은 AWS Paper Daily Step에서 직접 실행되는 MS가 아니라 소비 MS가 import해 쓰는 공통 전략 코어라는 점을 재확인했다.
- PORT-STRATEGY-COMMON 외 MS(View, MarketConnector, Crawler, Preprocessor, StrategyDecision, StrategyResearch, StrategyExecution, Scheduler, Lambda, Step Functions)의 세부 운영 상세는 이 저장소 문서에 반영하지 않았다.
- 실제 크롤링, 외부 API 호출, DB DDL/DML, 주문 실행, Python 실행은 수행하지 않았다.
- 민감정보(비밀번호, 토큰, API key, 계좌번호, webhook URL, secret ARN, IAM Role ARN, task definition ARN, image URI, command id)는 문서에 기록하지 않았다.
- 이 저장소에 `.kiro` 하위 파일은 존재하지 않아 별도 제외 처리 대상이 없었다.

## 2026-05-28

### Added

- `docs/source-file-catalog.md`를 추가해 주요 소스/문서 파일의 역할, 책임, 수정/운영 주의사항을 정리했다.
- Python 소스 파일에 한글 module docstring을 추가했다.
- `docs/worklog/2026-05-28.md`에 AWS Migration 전 초기 정리 작업 기록을 추가했다.

### Changed

- Removed Common core database dependency and kept runtime config snapshots limited to strategy configuration.
- README에 전체 파일 카탈로그와 파일별 설명 주석 정리 상태를 반영했다.

### Notes

- 기능 변경 없음.
- 실제 크롤링, 외부 API 호출, DB DDL/DML, 주문 실행은 수행하지 않았다.
- 민감정보 값은 문서에 기록하지 않았다.

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

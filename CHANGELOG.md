# CHANGELOG

`port_strategy_common`의 주요 변경 이력을 기록한다.

현재 구조와 사용 방법은 `README.md`, 작업 규칙은 `AGENTS.md`,
파일별 책임과 영향은 `docs/source-file-catalog.md`를 기준으로 확인한다.

## 2026-07-30

### Common DevOps와 Version Package 배포 구성

| 항목 | 값 |
|---|---|
| 변경 범위 | DevOps 구성 파일과 문서 |
| 작업 성격 | Versioned Python Package Build·배포 구성 |
| Package Version | `1.0.0` |
| Strategy Version | `COMMON_STRATEGY_V1.0.0` |
| Artifact | Python Wheel |
| CI | GitHub Actions → AWS CodeBuild |
| Registry | AWS CodeArtifact |
| Consumer Contract | Research 48/48, Decision 24/24 |
| 정식 승격 | `1.0.0rc1` → `1.0.0` Publish |
| Rollback | 이전 Published Version Pin 재설치 |
| 전략 판단 변경 | 없음 |
| Config 변경 | 없음 |
| 공개 함수 변경 | 없음 |
| Dataclass·Enum·Reason 변경 | 없음 |
| DB·API·주문 실행 | 없음 |

전략 판단 로직, Config, 공개 함수, Dataclass, Enum과 Reason 변경은 없다.

### CI와 Wheel Build

| 파일 | 역할 |
|---|---|
| `pyproject.toml` | Package Metadata·Version·Dependency 선언 |
| `.github/workflows/common-codebuild.yml` | OIDC 인증과 CodeBuild 시작·대기 |
| `.devops/codebuild/buildspec.yml` | 품질 게이트·Wheel Build·조건부 Publish |
| `.devops/scripts/verify_wheel.py` | Wheel 이름·필수 Member·SHA-256 검증 |
| `tests/test_public_contract.py` | 설치된 Wheel 기준 공개 계약 테스트 |

품질 게이트는 Ruff, mypy(`.devops/scripts` 범위), Wheel Build,
Twine Check, Wheel 구조 검증과 공개 계약 테스트 4건이다.

### CodeArtifact 배포

| 항목 | 값 |
|---|---|
| RC Publish | `1.0.0rc1` CodeArtifact 배포 |
| RC 검증 | 설치된 Wheel 공개 계약 테스트 4건 통과 |
| 정식 Publish | `1.0.0` CodeArtifact 배포 |
| Version 보존 | RC와 정식 Version 동시 보존 |
| 기본 Publish | 프로젝트 기본값 `false` |
| Release Publish | 승인 Release Build에서만 일회성 Override |

### Consumer Contract

| Consumer | 결과 |
|---|---|
| StrategyResearch | 48건 통과 |
| StrategyDecision | 24건 통과 |
| StrategyExecution | 직접 Import 없음 · 대상 아님 |
| Legacy `utils.to_float` | Research가 직접 Import · pandas 필요 |
| pandas 제공 | Research 자체 Runtime Dependency |

### 정식 승격과 Rollback

| 항목 | 값 |
|---|---|
| 정식 설치 검증 | `1.0.0` Wheel 설치 후 검증 |
| 공개 Symbol | 6개 확인 |
| 공개 계약 테스트 | 4건 통과 |
| Rollback 재설치 | `1.0.0rc1` Version Pin 재설치 |
| Rollback 검증 | 공개 계약 테스트 4건 재통과 |
| Git Repository | 무변경 |
| 방식 | Version Pin 재설치 |

### 작업 경계

| 항목 | 결과 |
|---|---|
| 전략 Python 로직 변경 | 없음 |
| DB DDL·DML | 없음 |
| 외부 API 호출 | 없음 |
| 주문 실행 | 없음 |
| Consumer Repository 수정 | 없음 |
| 민감정보 문서 기록 | 없음 |
| 배포 Slack 알림 연계 | 없음 |

## 2026-07-23

### Common 문서 기준 재정비

| 항목 | 변경 내용 |
|---|---|
| 변경 범위 | `AGENTS.md`, `README.md`, `CHANGELOG.md`, `docs/source-file-catalog.md` 문서 기준 재정비 |
| 작업 성격 | 현재 Common 책임과 공개 계약을 기준으로 한 문서 개선 |
| 기능 변경 | 없음 |
| Python 코드 변경 | 없음 |
| Config 변경 | 없음 |
| Enum 변경 | 없음 |
| Dataclass 변경 | 없음 |
| Reason 변경 | 없음 |
| Consumer 변경 | 없음 |
| Version 변경 | 없음 |
| 외부 실행 | 없음 |

### AGENTS.md

| 항목 | 변경 내용 |
|---|---|
| 문서 가독성 | 2열 표, 긴 셀 분리, 500자 Line 제한을 최우선 규칙으로 추가 |
| 규칙 우선순위 | 사용자 지시, Workspace 공통 규칙과 Common 전용 규칙 관계 정리 |
| 프로젝트 역할 | Common을 독립 실행 MS가 아닌 공유 전략 Library로 명확화 |
| 책임 경계 | Research·Decision·Execution·MarketConnector와 역할 분리 |
| Consumer 관계 | Consumer Adapter와 Common Context 경계 추가 |
| 작업 범위 | Common Root만 수정하고 Consumer 저장소는 읽기 전용으로 제한 |
| 실행 안전 | DB·API·AWS·주문·File Write·Side Effect 실행 금지 강화 |
| 순수성 | DB·HTTP·File IO·환경변수·Clock·Random·Global Mutation 금지 |
| 공개 API | Module·함수·Parameter·Return·Export 호환성 기준 추가 |
| Context 계약 | Field·순서·Default·Optional·단위·날짜·Serialization 기준 추가 |
| Result 계약 | Signal·Status·Reason·Numeric·Detail 역할과 Default 기준 추가 |
| Enum 계약 | Member·Value·대소문자·직렬화 호환성 기준 추가 |
| Reason 계약 | DB·Report·Slack·View·Test 문자열 영향 추가 |
| Config 계약 | Key·Default·단위·Override·Snapshot 호환성 기준 추가 |
| Config Mutation | Deep Copy·원본 보존·호출 순서 독립성 기준 추가 |
| Market 계약 | Regime·Exposure·Threshold Boundary 확인 기준 추가 |
| BUY 계약 | Filter·Guard·Sizing·Decision 책임과 Orchestration 분리 |
| SELL 계약 | Guard·Decision·Backtest 호환 평가 기준 추가 |
| Block Watch | Block·Watch·해제 조건·날짜 의미 분리 |
| 결정론 | 동일 입력과 Config에서 동일 결과 유지 기준 추가 |
| Look-ahead | Feature·Price·Trade Date와 Holding Days 안전 기준 추가 |
| 수치 안전 | Float·Decimal·NaN·Inf·Rounding·단위 기준 추가 |
| Import 계약 | Package Export·Circular Import·Import Side Effect 기준 추가 |
| Version | 전략 결과 변경과 Version Metadata 관계 추가 |
| Legacy | `utils.py` 등 실제 참조 확인 전 삭제 금지 |
| 테스트 | Context·Enum·Config·Boundary·Consumer Contract 검증 기준 추가 |
| 변경 분류 | 문서·리팩터링·전략 변경·Breaking Change 구분 |
| 문서 체계 | AGENTS·README·CHANGELOG·Source Catalog 역할 분리 |
| Worklog | 날짜별 Worklog 신규 생성 금지 |
| 완료 보고 | 공개 계약·Consumer 영향·전략 결과 변경 여부 보고 기준 추가 |

### README.md

| 항목 | 변경 내용 |
|---|---|
| 서비스 요약 | 입력·출력·Consumer·실행 형태·순수성 원칙 추가 |
| 책임 경계 | Common 판단 계약과 Consumer Persistence 책임 분리 |
| Consumer 구조 | Adapter → Context → Common → Result 흐름 추가 |
| Research | Backtest 판단 재사용과 Look-ahead 책임 구분 |
| Decision | Daily Adapter와 Persistence 책임 구분 |
| Execution | 실제 Import 범위를 코드 확인 대상으로 제한 |
| 기타 MS | Import 근거 없이 Consumer로 단정하지 않도록 정리 |
| 순수 함수 | DB·HTTP·File IO·Clock·Random·Global Mutation 금지 명시 |
| 결정론 | 동일 입력·Config에서 동일 결과 원칙 추가 |
| 공개 계약 | 함수·Field·Enum·Reason·Config·Export 계약 추가 |
| Context | Field·Type·Default·Optional·단위·날짜 기준 추가 |
| Result | Signal·Status·Reason·Numeric·Detail 역할 분리 |
| Enum | 실제 Class·Value를 코드에서 확인하도록 정리 |
| Reason | 저장·집계·표시·Test 영향 추가 |
| Config | Threshold·Default·Weight·Key 변경 영향 정리 |
| Snapshot | Copy·Mutation·Override·Secret 배제 기준 추가 |
| Market | Regime·Exposure·Boundary 확인 기준 추가 |
| BUY 흐름 | Filter → Guard → Sizing → Decision 구조 추가 |
| SELL 흐름 | Guard → SELL·HOLD와 Backtest 호환 구조 추가 |
| Block Watch | Block·Watch·Release 의미 분리 |
| 수치 안전 | Float·Decimal·NaN·Inf·단위·Rounding 기준 추가 |
| 날짜 안전 | Trade·Feature·Price Date와 Look-ahead 기준 추가 |
| Package | `__init__.py`, `common_utils.py`, `utils.py` 책임 구분 |
| Version | 결과 변경과 Metadata 갱신 관계 추가 |
| 파일 구조 | 현재 Root와 `docs/source-file-catalog.md` 구조 반영 |
| Worklog | 현재 파일 구조에서 제거하고 신규 생성 금지 반영 |
| AWS | 독립 실행 대상이 아닌 Consumer Dependency로 명확화 |
| 보안 | Config Snapshot과 Detail Payload의 Secret 배제 추가 |
| 검증 | 문서 변경과 코드 변경 검증 범위 분리 |
| 변경 영향 | 문서·리팩터링·전략 결과·Breaking Change 분류 추가 |
| 확인 항목 | Public API·Consumer Import·Config·Determinism 등 미확정 사항 분리 |

### CHANGELOG.md

| 항목 | 변경 내용 |
|---|---|
| 구조 | 장문 Bullet과 반복 Notes를 날짜별 2열 변경 요약으로 재구성 |
| 최신 이력 | 2026-07-23 Common 문서 기준 재정비 내역 추가 |
| 변경 경계 | 문서 변경과 코드·Config·Enum·Dataclass 변경을 분리 |
| 과거 이력 | 2026-05-26~2026-07-01 실제 변경 사실 보존 |
| 언어 | 2026-05-28 영문 변경 문장을 한글 사실형 문장으로 정리 |
| Worklog | 과거 생성 사실은 보존하고 현재 신규 생성 금지 정책과 구분 |
| 민감정보 | Credential과 AWS 운영 식별자 원문 미기록 원칙 유지 |

### docs/source-file-catalog.md

| 항목 | 변경 내용 |
|---|---|
| 구조 | 파일 설명 목록을 책임·공개 계약·Consumer 영향 구조로 재구성 |
| 계약 분리 | Context·Result·Enum·Config·Decision 파일 책임 분리 |
| Consumer 영향 | Research·Decision·Execution 영향 지도 추가 |
| 순수성 | 순수성과 Import Side Effect 지도 추가 |
| 결정론 | 결정론과 재현성 위험 지도 추가 |
| 수치·날짜 | 수치·날짜·Look-ahead 영향 지도 추가 |
| 변경 관계 | 파일 변경 영향 관계 표 추가 |
| Worklog | 현재 파일 구조와 Catalog 목록에서 Worklog 제거 |
| 갱신 조건 | Public API·Field·Enum·Reason·Config·Consumer 변경 시 갱신 조건 추가 |

### 공개 계약 보강

| 계약 | 보강 내용 |
|---|---|
| 함수 | 공개 함수명·Parameter·Return Type을 Consumer 계약으로 취급 |
| Context | Dataclass Field와 Default 변경을 호환성 영향으로 분류 |
| Result | Signal·Status·Reason·Detail 구조 유지 기준 추가 |
| Enum | Member와 Value 문자열을 외부 계약으로 취급 |
| Reason | 문구 수정도 집계·View·Slack·Test 영향 가능성 명시 |
| Config | Key·Default·Threshold 변경을 전략 결과 영향으로 분류 |
| Export | `__init__.py` 공개 Symbol 변경 위험 추가 |
| Version | 전략 Rule 변경과 Metadata 갱신 판단 기준 추가 |

### 순수성과 재현성 보강

| 항목 | 기준 |
|---|---|
| DB | Common 전략 Module에서 접근하지 않음 |
| HTTP·API | 외부 Client 호출 금지 |
| File IO | 판단 함수 내부 읽기·쓰기 금지 |
| Environment | 함수 내부 직접 환경변수 조회 금지 |
| Clock | 현재 시각 직접 사용 금지 |
| Random | Seed 없는 난수 금지 |
| Global State | Mutable Global 변경 금지 |
| Config | Caller Mutation이 원본에 영향을 주지 않음 |
| Determinism | 동일 입력·Config에 동일 결과 |
| Look-ahead | 미래 Feature·Price 참조 금지 |

### 작업 경계

| 항목 | 결과 |
|---|---|
| Python 실행 | 수행하지 않음 |
| Import Test | 수행하지 않음 |
| Consumer 실행 | 수행하지 않음 |
| Backtest·Daily 실행 | 수행하지 않음 |
| DB DDL·DML | 수행하지 않음 |
| 외부 API·Crawler | 수행하지 않음 |
| 주문·Broker 호출 | 수행하지 않음 |
| AWS CLI·SDK | 수행하지 않음 |
| 민감정보 조회·기록 | 수행하지 않음 |
| 문서 정적 검토 | 수행 |

## 2026-07-01

### Common 운영 문서 보강

| 항목 | 변경 내용 |
|---|---|
| README | Common 책임 경계와 Consumer 의존성 추가 |
| AWS | 직접 실행 MS가 아닌 Dependency 성격 명시 |
| 호환성 | 공개 함수·Dataclass·Enum·Reason·Config Key 유지 기준 추가 |
| AGENTS | 당시 Worklog 들여쓰기 형식을 ` 1)` 기준으로 정리 |
| 상태 표기 | 당시 Worklog 상태를 `작업 명:완료` 형식으로 통일 |

### 당시 추가 문서

| 항목 | 변경 내용 |
|---|---|
| Worklog | `docs/worklog/2026-07-01.md` 생성 |
| 현재 정책 | 과거 생성 사실은 보존하되 신규 Worklog는 만들지 않음 |

### 당시 작업 경계

| 항목 | 결과 |
|---|---|
| 기능 변경 | 없음 |
| Python 코드 변경 | 없음 |
| Config Key 변경 | 없음 |
| Enum 변경 | 없음 |
| Dataclass Field 변경 | 없음 |
| Reason 변경 | 없음 |
| Python 실행 | 수행하지 않음 |
| DB DDL·DML | 수행하지 않음 |
| 외부 API·Crawler | 수행하지 않음 |
| 주문 실행 | 수행하지 않음 |
| 민감정보 기록 | 하지 않음 |

### 당시 책임 경계

당시 Common과 직접 관련된 내용만 문서화했다.

| 제외 영역 | 담당 |
|---|---|
| View 화면·승인 UI | port-view |
| Broker·KIS API | MarketConnector |
| 원천 데이터 수집 | Crawler |
| Feature 생성 | Preprocessor |
| Daily 저장 | StrategyDecision |
| Backtest·Report 저장 | StrategyResearch |
| Execution Plan·Order | StrategyExecution |
| Scheduler·Lambda·Step Functions | 해당 운영 구성 |

## 2026-05-28

### Source와 문서 정리

| 항목 | 변경 내용 |
|---|---|
| Source Catalog | `docs/source-file-catalog.md` 최초 추가 |
| Module Docstring | 주요 Python 파일에 한글 설명 추가 |
| DB Dependency | Common Core의 DB 의존성 제거 |
| Runtime Config | Snapshot 범위를 전략 설정으로 제한 |
| README | 파일 Catalog와 설명 주석 상태 반영 |
| Worklog | `docs/worklog/2026-05-28.md` 생성 |

### 당시 변경 성격

| 항목 | 결과 |
|---|---|
| Common DB Dependency | 제거 |
| Runtime Config 범위 | 전략 설정으로 제한 |
| 외부 실행 | 수행하지 않음 |
| DB DDL·DML | 수행하지 않음 |
| 외부 API·Crawler | 수행하지 않음 |
| 주문 실행 | 수행하지 않음 |
| 민감정보 기록 | 하지 않음 |

이 날짜의 DB Dependency 제거는 실제 코드·구조 변경 이력이다.
현재 구현과 일치하는지는 최신 소스에서 확인한다.

## 2026-05-26

### 초기 문서

| 항목 | 변경 내용 |
|---|---|
| AGENTS | 초기 `AGENTS.md` 추가 |
| README | 초기 `README.md` 추가 |
| Worklog | `docs/worklog/2026-05-26.md` 생성 |

### 당시 작업 기준

| 항목 | 기준 |
|---|---|
| 문서 근거 | 당시 로컬 파일 구조와 일부 핵심 Module 확인 |
| Python 실행 | 수행하지 않음 |
| DB DDL·DML | 수행하지 않음 |
| 외부 API·Crawler | 수행하지 않음 |
| 주문 실행 | 수행하지 않음 |
| 민감정보 | 실제 값을 기록하지 않음 |

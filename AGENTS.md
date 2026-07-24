# AGENTS.md - port_strategy_common

## 1. 최우선 문서 가독성 규칙

이 규칙은 `port_strategy_common`의 모든 Markdown 문서 작성과 수정에 우선 적용한다.

- 새로 만드는 독립 요약 표는 기본적으로 2컬럼을 사용한다.
- 기본 컬럼은 `항목 / 값`이며, 문맥에 따라 `파일 / 역할`, `계약 / 기준`, `Consumer / 영향`을 사용할 수 있다.
- 기존 표에 행을 추가할 때는 기존 컬럼 구조를 유지한다.
- 표 셀은 가능하면 2문장 이하로 작성한다.
- 한 셀에 3개 이상의 사실을 장문으로 넣지 않는다.
- 3개 이상의 사실은 여러 행으로 나누거나 상세 문서 링크로 분리한다.
- 새로 만드는 표 셀은 300자를 넘기지 않는다.
- 한 줄은 500자를 넘기지 않는다.
- 긴 파일 목록, 전체 로그, 전체 테스트 출력과 전체 설정 Dump를 문서 본문에 붙이지 않는다.
- 같은 사실을 `README.md`, `CHANGELOG.md`, `docs/source-file-catalog.md`에 장문으로 반복하지 않는다.
- 현재 상태와 과거 변경 이력을 한 문단에서 섞지 않는다.
- 파일명, 함수명, Class명, Enum, Config Key, Signal과 Reason 문자열은 코드 표기를 유지한다.
- 한글 Markdown은 UTF-8 No BOM으로 저장한다.
- 탭 문자와 후행 공백을 만들지 않는다.

## 2. 규칙 우선순위

| 범위 | 우선 기준 |
|---|---|
| 사용자 최신 명시 요청 | 가장 높은 작업 지시 |
| Workspace 공통 안전·작업 방식 | `.kiro/AGENTS.md`가 있으면 최신 규칙 |
| Common 책임·호환성·순수성 계약 | 이 `AGENTS.md` |
| 직접 충돌 | 더 제한적이고 안전한 규칙 |

- `.kiro/AGENTS.md`가 없으면 이 파일을 Common 작업 기준으로 사용한다.
- 사용자가 대상 파일과 범위를 지정하면 그 범위를 넘기지 않는다.
- 구현 사실이 불명확하면 실행하거나 추정하지 말고 정적 확인 결과와 한계를 보고한다.
- Consumer 전체 수정이 필요한 변경은 Common 단독 작업으로 진행하지 않는다.

## 3. 프로젝트 역할

`port_strategy_common`은 StrategyResearch, StrategyDecision과
StrategyExecution이 공유하는 Python 전략 계약과 판단 코어다.

| 영역 | 책임 |
|---|---|
| Context | Market·Stock·Position 입력 계약 |
| Result | Market·Filter·Guard·Sizing·BUY·SELL 결과 계약 |
| Types | Signal·Side·Status·Position·Execution Mode Enum |
| Market | 시장 Regime과 Exposure 판단 |
| BUY Filter | 매수 가능 조건 판단 |
| BUY Guard | 매수 Risk Guard |
| BUY Sizing | 목표 비중·금액·수량 계산 |
| BUY Decision | Filter·Guard·Sizing 결과 Orchestration |
| SELL Guard | 매도 Risk Flag와 Guard |
| SELL Decision | SELL·HOLD 판단과 Backtest 호환 평가 |
| Block Watch | 공통 Block·Watch 판단 |
| Config | 전략 상수와 Runtime Config Snapshot |
| Version | Strategy Name·Engine Version Metadata |

Common은 실행 서비스가 아니라 소비 MS가 Import하여 사용하는 공통 라이브러리다.

## 4. 책임 경계

Common이 직접 책임지는 범위는 아래와 같다.

- Context Dataclass
- Result Dataclass
- Enum과 공개 상수
- 순수 전략 판단 함수
- Strategy Config Key와 Snapshot
- Version Metadata
- Consumer 간 판단 호환성
- 진단용 Reason과 Detail Payload 계약

Common이 직접 책임지지 않는 범위는 아래와 같다.

| 영역 | 담당 |
|---|---|
| 원천 데이터 수집 | Crawler |
| Raw 전처리와 Feature 생성 | Preprocessor |
| Daily Signal DB 저장 | StrategyDecision |
| Daily Position Decision DB 저장 | StrategyDecision |
| Backtest Run·Trade·Report 저장 | StrategyResearch |
| Execution Plan·Order·Position 저장 | StrategyExecution |
| Broker·KIS API | MarketConnector |
| 승인 UI와 화면 | port-view |
| Daily Orchestration | Scheduler·Step Functions |
| DB Connection·Persistence | 각 소비 MS |

- Common에 DB Helper, HTTP Client, File Persistence와 AWS 실행 코드를 추가하지 않는다.
- 다른 MS의 Adapter와 Persistence 책임을 Common으로 끌어오지 않는다.
- Common 문서에는 Consumer 내부 운영 상세를 복제하지 않는다.

## 5. Consumer 관계

| Consumer | Common 사용 범위 |
|---|---|
| StrategyResearch | Market·BUY·SELL·Sizing·Config·Version 계약 |
| StrategyDecision | Daily Market·Filter·Guard·Sizing·BUY·SELL·Block Watch |
| StrategyExecution | Enum·Status·Config·Result 계약 일부 |
| 기타 MS | 직접 Import 근거가 확인된 경우에만 기록 |

- Research와 Decision은 같은 Common 판단 함수를 재사용할 수 있다.
- Execution이 Common을 직접 호출하는지, Enum만 참조하는지는 실제 Import로 확인한다.
- View·Crawler·Preprocessor·MarketConnector를 Common Consumer로 추정하지 않는다.
- Consumer별 입력 변환은 각 Consumer Adapter 책임이다.
- Common 함수가 특정 Consumer DB Row 구조를 직접 받도록 만들지 않는다.

## 6. 작업 범위

- 기본 작업 범위는 `port_strategy_common` 루트와 하위 파일이다.
- 루트 밖 파일은 Consumer 영향 확인을 위한 읽기 전용으로만 사용한다.
- 사용자 요청 없이 Consumer 저장소 파일을 수정하지 않는다.
- 문서 작업 요청이면 대상 Markdown 파일만 수정한다.
- 코드 작업 요청이면 지정된 Common Python·설정·테스트 파일만 수정한다.
- 전체 Repository 전수 스캔, Sub-agent, Orchestrator와 새 Scanner를 만들지 않는다.
- 존재하지 않는 API, Test, Consumer와 Config Key를 문서 편의를 위해 만들지 않는다.
- Generated Output, Cache, Dump와 임시 파일을 운영 소스로 단정하지 않는다.

## 7. 작업 시작 전 정적 확인

수정 전 필요한 범위에서 아래 순서로 확인한다.

1. 사용자 지정 대상 파일
2. 이 `AGENTS.md`
3. 대상 Common Module
4. 대상 Module이 Import하는 Context·Result·Types·Config
5. 대상 공개 함수를 Import하는 Consumer
6. 관련 테스트
7. 문서 변경 영향이 있는 README·CHANGELOG·Source Catalog

정적 확인 시 아래를 구분한다.

| 구분 | 판단 기준 |
|---|---|
| 현재 구현 | 실제 코드에서 직접 확인 |
| 공개 계약 | Consumer Import와 호출 방식으로 확인 |
| 설계 원칙 | AGENTS와 현재 문서 기준 |
| 미검증 | 근거가 부족한 내용 |
| 추정 금지 | 이름만 보고 Consumer·호환성·Legacy 여부를 단정하지 않음 |

## 8. 실행 안전

Common은 원칙적으로 순수 라이브러리지만, 안전성을 확인하기 전 Module을 실행하지 않는다.

사용자 승인 없이 아래를 수행하지 않는다.

- 외부 API 호출
- DB 연결과 DDL·DML
- 파일 Write
- AWS CLI·SDK 호출
- ECS·Lambda·Batch·Step Functions 실행
- 주문 제출과 Broker 호출
- 크롤링
- Git Commit·Push·Reset·Restore·Checkout
- 민감정보 조회 또는 출력

- Import 시 Side Effect가 없는지 먼저 읽어서 확인한다.
- `if __name__ == "__main__":`가 있는 파일은 실행하지 않는다.
- `utils.py`와 Helper도 이름만 보고 안전하다고 판단하지 않는다.
- 문서 작업에서는 Python 실행과 Import Test를 기본적으로 수행하지 않는다.

## 9. Common 순수성 계약

`common_*` 전략 Module은 순수 함수 중심으로 유지한다.

| 금지 의존 | 기준 |
|---|---|
| DB | Connection, Cursor, SQL, ORM 금지 |
| HTTP·API | Requests, SDK, Broker Client 금지 |
| File IO | Config·Result 파일 읽기·쓰기 금지 |
| Environment | 판단 함수 내부에서 직접 환경변수 조회 금지 |
| Clock | 함수 내부에서 현재 시각 직접 조회 금지 |
| Random | Seed 없는 난수 사용 금지 |
| Global Mutation | Module Global 상태 변경 금지 |
| Logging Side Effect | 민감 Payload 전체 출력 금지 |

허용 입력은 명시적인 Argument, Context Dataclass와 Config Dictionary다.

동일한 입력과 동일한 Config에는 동일한 결과를 반환해야 한다.

## 10. 공개 API 호환성 계약

아래 항목은 공개 계약으로 취급한다.

- 공개 Module 경로
- 공개 함수명
- 함수 Parameter 이름과 순서
- Default 값
- Return Type
- Context Dataclass 이름과 Field
- Result Dataclass 이름과 Field
- Enum Class와 Value
- Decision Reason 문자열
- Detail Dictionary Key
- Config Dictionary Key
- Version Metadata Key
- Package Export

변경 전 아래를 확인한다.

| 항목 | 확인 대상 |
|---|---|
| Import | Consumer의 직접 Import |
| 호출 | Positional·Keyword Argument |
| 반환 | Attribute 접근과 Serialization |
| Enum | DB·Report·Slack·View 문자열 사용 |
| Reason | 비교·집계·표시 로직 |
| Config | Consumer Override와 Snapshot |
| Export | `__init__.py` 공개 Symbol |

모든 Consumer를 함께 수정하고 검증하지 않는 한 Breaking Change를 만들지 않는다.

## 11. Context Dataclass 계약

`common_context.py` 변경 시 아래를 확인한다.

- Class 이름
- Field 이름
- Field 순서
- Type Annotation
- Default 값
- Optional 여부
- 단위
- 날짜 표현
- Consumer 생성 방식
- `asdict` 또는 Serialization 사용
- Frozen 여부
- 추가 Field의 하위 호환성

Context는 Consumer의 DB Row 자체가 아니다.

- DB Column 이름을 그대로 강제하지 않는다.
- Consumer Adapter가 DB·Feature Row를 Context로 변환한다.
- Context 내부에서 데이터 조회나 정규화를 수행하지 않는다.
- 동일 의미의 날짜 Field를 중복 추가하지 않는다.
- 가격·수량·비율의 단위를 문서와 테스트에서 명확히 한다.

## 12. Result Dataclass 계약

`common_result.py` 변경 시 아래를 확인한다.

- Signal
- Status
- Reason
- Score
- Exposure
- Weight
- Amount
- Quantity
- Guard Flag
- Detail Payload
- Default 값
- Serialization 형태

Result는 기계 처리용 값과 진단 정보를 구분한다.

| 구분 | 용도 |
|---|---|
| Signal·Status | Consumer 분기와 저장 |
| Reason | 집계·Report·Slack·View 표시 |
| Numeric Result | Sizing·Execution 후보 입력 |
| Detail | 진단과 설명 |

- Detail Dictionary에만 존재하던 값을 공개 Field로 승격할 때 Consumer 영향을 확인한다.
- 기존 Field를 Detail로 이동하지 않는다.
- `None`, 0, Empty Dictionary의 의미를 임의로 바꾸지 않는다.
- Mutable Default는 `default_factory`를 사용한다.

## 13. Enum과 문자열 계약

`common_types.py`의 Enum과 문자열은 외부 계약으로 취급한다.

| 계약 | 위험 |
|---|---|
| Market Signal | 시장 노출과 BUY 허용 변화 |
| Trade Signal | BUY·SELL·HOLD·SKIP 분기 변화 |
| Order Side | Execution 연결 오류 |
| Decision Status | DB·Report 집계 오류 |
| Position Status | Position 상태 해석 오류 |
| Execution Mode | Paper·Live 경계 오류 |

- Enum Value의 대소문자와 문자열을 임의 변경하지 않는다.
- Enum Member 이름 변경도 Consumer Import에 영향을 줄 수 있다.
- Alias 추가는 Serialization과 비교 결과를 확인한다.
- 문자열 비교를 Enum 비교로 바꾸는 경우 모든 Consumer를 확인한다.
- 문서 편의를 위해 코드에 없는 Enum을 추가하지 않는다.

## 14. Decision Reason 계약

Decision Reason은 단순 설명 문구가 아니라 Consumer 계약일 수 있다.

변경 시 아래를 확인한다.

- Consumer의 문자열 비교
- Report 집계
- Slack 문구
- View 표시
- DB 저장과 분석 Query
- Test Fixture
- Backtest와 Daily 결과 비교

- 기존 Reason을 문장 다듬기 목적으로 변경하지 않는다.
- 오탈자 수정도 Consumer 비교 여부를 확인한다.
- 새 Reason 추가 시 발생 조건과 우선순위를 명확히 한다.
- 동일 조건에서 Reason이 비결정적으로 달라지지 않도록 한다.
- Human-readable 설명이 필요하면 별도 Detail Field를 우선 검토한다.

## 15. Config 계약

`config.py`와 Runtime Config 변경 시 아래를 확인한다.

- Config Key 이름
- Default 값
- 단위
- Type
- Nested 구조
- Override Merge 방식
- Unknown Key 처리
- Snapshot 결과
- Version과의 연결
- Consumer별 Override 사용

Config 변경은 전략 결과 변경으로 취급한다.

| 변경 | 확인 기준 |
|---|---|
| Threshold | Boundary 결과와 신호 변화 |
| Weight | Exposure·Sizing 결과 |
| Max Positions | Portfolio 제한 |
| Minimum Score | BUY 후보 수 |
| Sell Rule | HOLD·SELL 전이 |
| Report Config | Consumer 출력 영향 |
| Default | Override 없는 모든 Consumer 영향 |

모든 Consumer를 함께 수정하지 않는 한 Config Key를 Rename·Remove하지 않는다.

## 16. Config Snapshot과 Mutation

`get_runtime_config()`와 `get_config_snapshot()` 계열이 있다면 아래를 확인한다.

- 반환 객체가 새 Copy인지
- Nested Dictionary가 Deep Copy인지
- Caller Mutation이 Global Config에 영향을 주는지
- Override가 원본 Config를 변경하는지
- Snapshot의 Key 순서에 의존하는 Consumer가 있는지
- Serialization 가능한 값만 포함하는지

- Shared Mutable Dictionary를 그대로 반환하지 않는다.
- Config Merge는 입력 Dictionary를 변경하지 않는다.
- 테스트는 호출 순서에 따라 결과가 달라지지 않아야 한다.

## 17. Market 판단 계약

`common_market.py` 변경 시 아래를 확인한다.

- 입력 Context Field
- Regime Score
- Breadth·Flow·Macro Pressure
- Threshold
- Exposure
- Max Positions
- Minimum Score
- Signal
- Status
- Reason
- Detail

Boundary 값에서 비교 연산을 확인한다.

- `<`와 `<=`
- `>`와 `>=`
- `None`
- NaN
- Inf
- 음수와 0
- Threshold와 정확히 같은 값

Market 결과는 BUY Filter·Sizing과 Consumer Adapter에 영향을 줄 수 있다.

## 18. BUY Filter 계약

`common_buy_filter.py` 변경 시 아래를 확인한다.

- 시장 BUY 허용 여부
- Stock Final Score
- Flow·Liquidity·Quality 조건
- Missing Input
- Block·Watch 상태
- 최소 점수
- Filter 우선순위
- Reason
- Detail

Filter는 BUY 수량을 계산하지 않는다.
Sizing과 Guard 책임을 혼합하지 않는다.

여러 실패 조건이 동시에 존재할 때 반환 Reason 우선순위를 유지한다.

## 19. BUY Guard 계약

`common_buy_guard.py` 변경 시 아래를 확인한다.

- Risk Flag
- Exposure 제한
- Current Position
- Duplicate Holding
- Maximum Position
- Cash Guard
- Market Guard
- Haircut
- Reason 우선순위

Guard는 원칙적으로 입력을 검증하고 Risk를 제한한다.

- Guard가 Consumer DB를 조회하지 않는다.
- Guard가 주문을 생성하지 않는다.
- Guard 결과와 Sizing 결과의 적용 순서를 확인한다.
- Research와 Decision에서 Guard 적용 순서가 같아야 하는지 실제 Adapter로 확인한다.

## 20. BUY Sizing 계약

`common_buy_sizing.py` 변경 시 아래를 확인한다.

- Available Cash
- Target Weight
- Target Amount
- Current Exposure
- Current Position Value
- Price
- Maximum Amount
- Minimum Amount
- Haircut
- Quantity
- Rounding
- 0주 처리

수치 계산 변경 시 아래 위험을 확인한다.

| 위험 | 확인 기준 |
|---|---|
| Float 오차 | Decimal 또는 허용 오차 |
| 음수 수량 | 0 이하 방지 |
| 0 Price | Skip 또는 Error |
| 반올림 | Floor·Round·Ceiling |
| 단위 | 비율 0~1과 Percent 혼동 |
| 현금 | 여러 후보 간 공유 여부 |
| 최대치 | Cap 적용 순서 |

Common Sizing은 Broker 호가 단위와 실제 주문 가능 수량을 직접 조회하지 않는다.

## 21. BUY Decision Orchestration

`common_buy_decision.py` 변경 시 아래 순서를 실제 코드에서 확인한다.

- Market 결과
- Filter
- Guard
- Sizing
- 최종 BUY·SKIP
- Reason
- Detail Merge

- 호출 순서를 임의로 변경하지 않는다.
- 선행 실패 이후 불필요한 계산을 수행하는지 확인한다.
- Detail Merge에서 같은 Key가 덮어써지는지 확인한다.
- 최종 Signal과 하위 결과가 모순되지 않게 한다.
- Daily와 Backtest Adapter가 같은 Orchestration을 사용하는지 확인한다.

## 22. SELL Guard 계약

`common_sell_guard.py` 변경 시 아래를 확인한다.

- Position 상태
- Holding Period
- Stop Loss
- Take Profit
- Risk Flag
- Market 상태
- Missing Price
- Reason 우선순위

SELL Guard는 실제 Position DB를 수정하지 않는다.
SELL 주문이나 Execution Order를 생성하지 않는다.

## 23. SELL Decision 계약

`common_sell_decision.py` 변경 시 아래를 확인한다.

- Position Context
- Current Price
- Entry Price
- Highest Price
- Holding Period
- Stop·Take Profit
- Market·Stock Signal
- SELL·HOLD 결과
- Reason
- Detail

`common_evaluate_backtest_sell`의 호환 동작은 별도 계약이다.

- Backtest와 Daily의 입력 차이를 Adapter가 처리하는지 확인한다.
- Backtest 전용 가격 시점이 Look-ahead를 만들지 않는지 확인한다.
- 같은 Context에서 Consumer별 결과가 달라지면 Config와 Adapter 차이를 명확히 한다.
- SELL Reason 문자열과 우선순위를 유지한다.

## 24. Block Watch 계약

`common_block_watch.py` 변경 시 아래를 확인한다.

- Block 상태
- Watch 상태
- 적용 대상
- 해제 조건
- 기간 또는 날짜
- Reason
- BUY Filter와의 연결
- Consumer별 사용 여부

Block과 Watch를 같은 상태로 처리하지 않는다.

- Block은 BUY 금지인지 확인한다.
- Watch는 감시·감점·조건부 허용 중 실제 의미를 확인한다.
- 날짜 비교는 거래일과 Calendar Date를 구분한다.
- StrategyDecision 전용 DB 상태를 Common에 직접 연결하지 않는다.

## 25. 결정론과 재현성

Common 결과는 동일 입력과 Config에서 재현 가능해야 한다.

아래를 금지하거나 통제한다.

- 현재 시각 직접 사용
- Timezone 의존 암묵 변환
- Unordered Collection 순회 결과 의존
- Seed 없는 Random
- Global Mutable State
- 호출 순서에 따른 Config Mutation
- Locale 의존 문자열 처리
- Platform별 Float 차이를 무시한 Exact 비교

테스트에서는 같은 입력을 여러 번 호출해 같은 결과를 확인한다.

## 26. 날짜와 Look-ahead 안전

Common은 입력 날짜를 직접 조회하지 않지만 Consumer가 제공하는 날짜 계약을 유지해야 한다.

- Trade Date
- Feature Date
- Price Date
- Position Evaluation Date
- Entry Date
- Exit Date
- Holding Days

- 미래 Feature나 가격을 참조하는 로직을 추가하지 않는다.
- Backtest Sell Helper에서 당일 종가 사용 시점과 거래 체결 시점을 구분한다.
- 날짜 문자열 비교 대신 명시적 Date 변환 여부를 확인한다.
- Naive Datetime과 Timezone-aware Datetime을 혼합하지 않는다.
- Holding Period 계산의 포함·제외 기준을 유지한다.

## 27. 수치 안전

전략 수치 계산 변경 시 아래를 확인한다.

- Float·Decimal 혼용
- NaN·Inf
- 0 Division
- 음수 값
- Missing Value
- Clipping
- Min·Max Boundary
- Rounding
- 단위
- Overflow 가능성

- NaN 비교 결과를 정상 False로 조용히 통과시키지 않는다.
- `None`, NaN과 0을 같은 의미로 처리하지 않는다.
- 비율은 0~1인지 0~100인지 확인한다.
- 가격과 금액은 Currency 단위를 확인한다.
- Quantity는 정수 계약 여부를 확인한다.

## 28. Import와 Package 계약

아래를 확인한다.

- `__init__.py` 공개 Export
- 상대 Import와 절대 Import
- Circular Import
- Import Side Effect
- Consumer의 Module Path
- 설치 Package 이름과 Folder 이름
- Legacy `utils.py` 참조

- Import 편의를 위해 모든 Symbol을 무분별하게 Export하지 않는다.
- Module Rename은 모든 Consumer Import를 함께 수정하지 않는 한 금지한다.
- Circular Import 해결을 위해 Runtime Import를 남발하지 않는다.
- Type Hint용 Import는 `TYPE_CHECKING` 사용 가능성을 검토한다.
- `utils.py`는 실제 참조 확인 전 삭제하지 않는다.

## 29. Version Metadata 계약

`common_version.py`와 Package Metadata 변경 시 아래를 확인한다.

- Strategy Name
- Engine Version
- Component Version
- Config Version
- Consumer 저장·Report 사용
- Snapshot 포함 여부
- 문자열 형식
- 하위 호환성

Version은 실제 기능 변경과 연결해 갱신한다.

- 문서만 수정한 경우 Version을 올리지 않는다.
- 함수 내부 리팩터링이 결과를 바꾸지 않으면 정책에 따라 판단한다.
- 결과가 바뀌는 Threshold·Rule 변경은 Version 영향 여부를 보고한다.
- Consumer가 Version을 DB Key로 사용하는지 확인한다.

## 30. Legacy와 정리 후보

`utils.py` 등 Legacy 가능성이 있는 파일은 아래를 확인하기 전 삭제하지 않는다.

| 항목 | 확인 내용 |
|---|---|
| Import | Common 내부 직접·동적 Import |
| Consumer | Research·Decision·Execution Import |
| Export | `__init__.py` 공개 여부 |
| Test | Fixture와 Patch 대상 |
| Documentation | 사용 예시와 운영 문서 |
| Git | 최근 변경과 사용자 미커밋 작업 |

미사용 근거가 충분하지 않으면 삭제하지 않고 정리 후보로만 기록한다.

## 31. 테스트 계약

코드 변경 시 영향 범위에 맞는 가장 좁은 테스트부터 사용한다.

우선 확인할 테스트 유형은 아래와 같다.

| 유형 | 검증 |
|---|---|
| Context | 생성·Default·Serialization |
| Result | Field·Default·Detail Mutation |
| Enum | Value와 Serialization |
| Config | Copy·Override·Mutation |
| Market | Threshold Boundary |
| BUY Filter | 실패 Reason 우선순위 |
| BUY Guard | Risk Boundary |
| BUY Sizing | Cash·Price·Rounding Boundary |
| BUY Decision | Orchestration과 Short-circuit |
| SELL Guard | Stop·Holding Boundary |
| SELL Decision | SELL·HOLD와 Backtest 호환 |
| Determinism | 반복 호출 동일 결과 |
| Consumer Contract | Import·Signature·Field 접근 |

실제 테스트 명령은 Repository에 존재하는 설정을 확인한 뒤 사용한다.

- 존재하지 않는 Test Runner를 가정하지 않는다.
- 문서 작업에서는 테스트를 실행하지 않는다.
- 테스트 실행이 외부 API·DB·파일 Write로 이어지는지 확인한다.
- Snapshot Test만으로 전략 수치 변경을 승인하지 않는다.

## 32. 변경 분류

변경 전 영향 수준을 분류한다.

| 수준 | 예시 |
|---|---|
| 문서 변경 | 설명·링크·가독성 |
| 내부 리팩터링 | 공개 계약과 결과 불변 |
| 호환 확장 | Optional Field·새 Helper 추가 |
| 전략 결과 변경 | Threshold·Rule·Order 변경 |
| Breaking Change | 함수·Field·Enum·Config Key 변경 |
| Consumer 공동 변경 | Adapter와 호출부 동시 수정 필요 |

전략 결과 변경과 Breaking Change는 사용자에게 명확히 보고하고,
승인 없이 범위를 확대하지 않는다.

## 33. 보안 규칙

- Password, Token, API Key, Account Number, Webhook URL과 ARN 실제 값을 출력하지 않는다.
- Common Source에 Secret과 Runtime Credential을 추가하지 않는다.
- 예제에는 Placeholder만 사용한다.
- Config Snapshot에 Secret이 포함되지 않도록 한다.
- Detail Payload에 Consumer Credential이 들어오더라도 그대로 Logging하지 않는다.
- 민감정보를 언급해야 하면 `[REDACTED]`를 사용한다.

## 34. Git 규칙

- 작업 전후 `git status --short`로 변경 범위를 확인한다.
- 작업 후 `git diff --stat`와 대상 파일 Diff를 확인한다.
- 미추적 파일은 `git diff --stat`에 잡히지 않을 수 있으므로 Status를 함께 확인한다.
- 사용자 변경을 되돌리지 않는다.
- 명시 요청 없이 Commit하지 않는다.
- 사용자 승인 없이 파일을 삭제하거나 Rename하지 않는다.

## 35. 문서 체계

| 문서 | 역할 |
|---|---|
| `AGENTS.md` | 작업·호환성·순수성·검증 규칙 |
| `README.md` | 현재 구조와 사용 AS-IS |
| `CHANGELOG.md` | 날짜별 실제 변경 이력 |
| `docs/source-file-catalog.md` | 파일 책임·Consumer·변경 영향 |

- 날짜별 `docs/worklog/*.md`는 새로 만들지 않는다.
- 과거 Worklog 생성 사실은 CHANGELOG에만 보존한다.
- README에는 현재 상태를 기록한다.
- CHANGELOG에는 과거 변경 사실을 기록한다.
- Source Catalog에는 파일 책임과 영향 범위를 기록한다.
- 같은 내용을 네 문서에 장문으로 반복하지 않는다.

## 36. 문서 갱신 조건

### 36.1 README.md

아래가 바뀌면 README 갱신 여부를 확인한다.

- 현재 파일 구조
- Common 책임 경계
- 공개 API
- Consumer 관계
- Config 구조
- 사용 예시
- 설치·Import 방법
- 검증 방법

### 36.2 CHANGELOG.md

아래가 실제로 바뀌면 기록한다.

- 공개 함수
- Context·Result Field
- Enum·Reason
- Config Key·Default
- 판단 Rule과 Threshold
- Version Metadata
- Consumer 호환성
- 문서 기준

### 36.3 docs/source-file-catalog.md

아래가 바뀌면 같은 작업에서 갱신 여부를 확인한다.

- 파일 추가·삭제·Rename
- 파일 책임
- 공개 함수와 Export
- 입력·출력 계약
- Consumer Import
- Config·Version 역할
- Legacy 분류
- 순수성·Side Effect

단순 오탈자 수정으로 관련 없는 모든 문서를 기계적으로 수정하지 않는다.

## 37. 완료 전 정합성 점검

작업 완료 전 아래를 확인한다.

### 37.1 범위

- 지정 파일만 수정했는가
- Consumer 저장소를 수정하지 않았는가
- 사용자 기존 변경을 보존했는가
- 새 Worklog·Scanner·임시 문서를 만들지 않았는가

### 37.2 계약

- 공개 함수 Signature가 유지되는가
- Context·Result Field가 유지되는가
- Enum Value와 Reason이 유지되는가
- Config Key와 Default가 의도대로 유지되는가
- `__init__.py` Export가 유지되는가
- Consumer Import와 호출 방식이 깨지지 않는가

### 37.3 순수성

- DB·HTTP·File IO가 추가되지 않았는가
- Environment·Clock·Random 의존이 추가되지 않았는가
- Global Mutable State가 추가되지 않았는가
- Import Side Effect가 없는가
- Config Mutation이 없는가

### 37.4 전략 결과

- Threshold Boundary가 의도대로 유지되는가
- Reason 우선순위가 바뀌지 않았는가
- BUY·SELL Orchestration 순서가 유지되는가
- Backtest와 Daily 호환 동작이 유지되는가
- Look-ahead 가능성이 추가되지 않았는가
- Numeric Unit과 Rounding이 유지되는가

### 37.5 문서

- README 현재 상태와 일치하는가
- CHANGELOG가 실제 변경만 기록하는가
- Source Catalog 책임이 일치하는가
- Worklog 신규 생성 규칙이 없는가
- UTF-8 No BOM인가
- 500자 초과 Line, Tab과 후행 공백이 없는가

## 38. 안전한 검증

문서만 수정한 경우 아래 범위로 확인한다.

```powershell
git status --short
git diff --stat
git diff -- AGENTS.md
```

코드 수정 시에도 먼저 정적 확인과 기존 테스트 구조를 확인한다.

허용 가능한 검증 후보는 아래와 같다.

- Target Module Syntax 확인
- Side Effect 없는 Import 확인
- 기존 Unit Test
- Pure Function 직접 호출
- Consumer Contract Test

단, 실제 명령은 사용자 요청과 Repository 상태를 확인한 뒤 선택한다.

아래 검증은 수행하지 않는다.

- DB 연결
- 외부 API
- AWS
- 주문
- 파일 Write가 발생하는 Entrypoint
- Consumer Batch·Backtest·Daily 운영 실행

## 39. 완료 보고

완료 보고는 아래 순서로 작성한다.

1. 변경 파일
2. 변경 요약
3. 공개 계약 영향
4. Consumer 영향
5. 검증 결과
6. 수행하지 않은 검증
7. 남은 위험 또는 후속 확인

- 문서 변경과 기능 변경을 구분한다.
- 실제 확인하지 않은 Consumer 호환성을 완료로 보고하지 않는다.
- 전략 결과 변경 여부를 명확히 적는다.
- 추정한 내용을 사실처럼 보고하지 않는다.

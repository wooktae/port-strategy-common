# port_strategy_common

`port_strategy_common`은 전략 판단 로직과 Consumer 공통 계약을 제공하는
Python 전략 판단 코어다.

시장·매수·매도 판단, Sizing, Guard, Context, Result, Enum,
Config와 Version Metadata를 공통 계약으로 제공한다.

설계 목적상 StrategyResearch, StrategyDecision과 StrategyExecution의
전략 계약 정렬 대상이다.
현재 직접 Import Consumer는 StrategyResearch와 StrategyDecision이다.
StrategyExecution은 현재 `port_strategy_common`을 직접 Import하지 않는다.

Common 자체는 독립 실행 서비스가 아니다.
Versioned Python Package로 Build되어 각 Consumer가 Context와 Config를 전달하면
순수 판단 결과를 반환하는 공통 라이브러리다.

## 1. 서비스 요약

| 항목 | 값 |
|---|---|
| Package Name | `port-strategy-common` |
| Import Package | `port_strategy_common` |
| 주 책임 | 전략 판단 로직과 Consumer 공통 계약 제공 |
| 실행 형태 | Consumer가 Import하는 Versioned Python Package |
| Package Version | `1.0.0` |
| Strategy Version | `COMMON_STRATEGY_V1.0.0` |
| Artifact | Python Wheel |
| Registry | AWS CodeArtifact |
| Build | GitHub Actions → AWS CodeBuild |
| 기본 Publish | 비활성 |
| Rollback | 이전 Published Version 재설치 |
| 주요 입력 | Context Dataclass와 Config Dictionary |
| 주요 출력 | Result Dataclass, Enum, Reason, Detail |
| 직접 Consumer | StrategyResearch, StrategyDecision |
| 직접 실행 | 하지 않음 |
| DB | 직접 접근하지 않음 |
| 외부 API | 직접 호출하지 않음 |
| File IO | 전략 Module에서 수행하지 않음 |
| 기본 원칙 | 동일 입력과 동일 Config에는 동일 결과 반환 |
| 문서 기준 | 현재 파일 구조와 소스의 정적 확인 결과 |

## 2. 주요 책임

| 영역 | 책임 |
|---|---|
| Context | Market·Stock·Position 입력 구조 |
| Result | Market·Filter·Guard·Sizing·BUY·SELL 결과 구조 |
| Types | Signal·Side·Status·Position·Execution Mode Enum |
| Market | Regime과 Exposure 판단 |
| BUY Filter | 매수 가능 조건 판정 |
| BUY Guard | 매수 Risk 제한 |
| BUY Sizing | 목표 비중·금액·수량 계산 |
| BUY Decision | Filter·Guard·Sizing Orchestration |
| SELL Guard | 매도 Risk Flag와 Guard |
| SELL Decision | SELL·HOLD 판단과 Backtest 호환 평가 |
| Block Watch | 공통 Block·Watch 조건 |
| Config | Strategy Config와 Runtime Snapshot |
| Version | Strategy·Engine Version Metadata |
| Utility | 공통 순수 Helper |

## 3. 책임 경계

Common은 판단 로직과 계약만 제공한다.

| 영역 | 담당 |
|---|---|
| 원천 데이터 수집 | Crawler |
| Raw 전처리와 Feature 생성 | Preprocessor |
| Daily Signal DB 저장 | StrategyDecision |
| Daily Position Decision 저장 | StrategyDecision |
| Backtest·Trade·Report 저장 | StrategyResearch |
| Execution Plan·Order·Position 저장 | StrategyExecution |
| Broker·KIS API | MarketConnector |
| 화면과 승인 UI | port-view |
| 전체 Daily Orchestration | Scheduler와 Step Functions |
| DB Connection·Persistence | 각 Consumer MS |
| 공통 판단·계약 | StrategyCommon |

Common에 아래 책임을 추가하지 않는다.

- DB Connection과 SQL
- HTTP·Broker Client
- AWS SDK
- File Persistence
- Consumer DB Row 직접 처리
- Scheduler·State Machine 실행
- 주문 생성·제출·체결
- Report·Slack·View 렌더링

## 4. Consumer 관계

Common은 Consumer 내부 구현을 소유하지 않는다.
Consumer는 자신의 입력을 Common Context로 변환하고 결과를 저장·표시한다.

```text
Crawler · Preprocessor · DB Row
                 │
                 ▼
          Consumer Adapter
                 │
                 ▼
       Common Context · Config
                 │
                 ▼
      Common Pure Decision Logic
                 │
                 ▼
     Common Result · Enum · Reason
                 │
                 ▼
   Consumer Persistence · Report · Execution
```

### 4.1 StrategyResearch

| 항목 | 값 |
|---|---|
| 주요 사용 | Market·BUY·SELL·Sizing·Config·Version |
| 목적 | Backtest 판단과 공통 Rule 재사용 |
| Consumer 책임 | Backtest Run·Trade·Metric·Report 저장 |
| 주의 | Research 가격 시점이 Look-ahead를 만들지 않아야 함 |

### 4.2 StrategyDecision

| 항목 | 값 |
|---|---|
| 주요 사용 | Market·Filter·Guard·Sizing·BUY·SELL·Block Watch |
| 목적 | Daily 운영 판단에 공통 Rule 적용 |
| Consumer 책임 | Daily Signal·Position Decision 저장 |
| 주의 | DB·Feature Row를 Context로 변환하는 Adapter 유지 |

### 4.3 StrategyExecution

| 항목 | 값 |
|---|---|
| 현재 상태 | `port_strategy_common`을 직접 Import하지 않음 |
| 소스 근거 | Common Config를 직접 사용하지 않는다는 주석만 존재 |
| 설계 목적 | 실행 후보 이전 단계의 공통 의미 정렬 대상 |
| Consumer 책임 | Plan·Order·Fill·Position 저장 |
| 승격 조건 | 향후 직접 Import 추가 시 직접 Consumer로 기록 |

StrategyExecution은 설계상 계약 정렬 대상이지만 현재 직접 Consumer는 아니다.
현재 직접 Consumer Contract Test 대상도 아니다.

### 4.4 기타 MS

View, Crawler, Preprocessor와 MarketConnector가 Common을 직접 Import하는지는
실제 Import 근거가 있을 때만 기록한다.

간접적으로 문자열이나 DB 결과를 소비한다는 이유만으로
Common Consumer라고 단정하지 않는다.

## 5. 설계 원칙

### 5.1 순수 함수

`common_*` 전략 Module은 순수 함수 중심으로 유지한다.

| 금지 의존 | 이유 |
|---|---|
| DB | Consumer Persistence와 결합 방지 |
| HTTP·API | 외부 상태 의존 방지 |
| File IO | 호출 순서와 환경 의존 방지 |
| 환경변수 직접 조회 | 입력 계약 불투명화 방지 |
| 현재 시각 직접 조회 | 재현성 저하 방지 |
| Seed 없는 Random | 비결정적 결과 방지 |
| Global Mutation | 테스트 순서 의존 방지 |

판단 함수는 Argument, Context와 Config를 통해 필요한 값을 받는다.

### 5.2 결정론

동일한 입력과 동일한 Config에는 동일한 결과를 반환해야 한다.

다음 요소가 결과에 암묵적으로 영향을 주면 안 된다.

- 현재 시각
- Timezone
- Locale
- 호출 순서
- Global Mutable State
- Dictionary 원본 Mutation
- Unordered Collection 순서
- Seed 없는 Random
- Consumer 실행 환경

### 5.3 Consumer 독립성

Common은 특정 Consumer의 DB Schema나 Row 구조를 직접 알지 않는다.

```text
Consumer Row
  → Consumer Adapter
  → Common Context
  → Common Result
  → Consumer 저장 구조
```

Consumer별 Adapter 차이로 결과가 달라질 수 있다면,
그 차이는 Consumer에서 명시적으로 관리한다.

## 6. 공개 계약

Common은 여러 Consumer가 함께 사용하는 공개 계약이다.

| 계약 | 예시 |
|---|---|
| Module Path | `port_strategy_common.common_market` |
| 함수명 | `common_decide_market` |
| Parameter | 이름·순서·Default |
| Return Type | Result Dataclass |
| Context Field | 입력 필드명·Type·Default |
| Result Field | Signal·Reason·Detail |
| Enum Value | 직렬화되는 문자열 |
| Reason | 집계·Report·View 기준 문자열 |
| Config Key | Consumer Override Key |
| Export | `__init__.py` 공개 Symbol |
| Version | Strategy·Engine Metadata |

모든 Consumer를 함께 수정하고 검증하지 않는 한 아래 변경을 하지 않는다.

- 공개 함수 Rename
- Parameter Rename·순서 변경
- 필수 Parameter 추가
- Return Type 변경
- Dataclass Field 삭제·Rename
- Enum Value 변경
- Reason 문자열 수정
- Config Key 삭제·Rename
- Module 이동
- Package Export 제거

## 7. Context 계약

`common_context.py`는 Common 입력 계약을 정의한다.

주요 Context는 실제 코드에서 확인한다.

| Context | 개념 역할 |
|---|---|
| Market Context | 시장 Regime 판단 입력 |
| Stock Context | 종목 BUY·Filter·Guard 입력 |
| Position Context | SELL·HOLD 판단 입력 |

Context 변경 시 아래를 확인한다.

| 항목 | 확인 내용 |
|---|---|
| Field Name | Consumer Keyword Argument |
| Field Order | Positional 생성 여부 |
| Type | 숫자·문자열·날짜 계약 |
| Default | 기존 Consumer 생략 가능 여부 |
| Optional | Missing Input 의미 |
| Unit | 가격·비율·수량 |
| Date | Trade·Feature·Evaluation Date |
| Serialization | `asdict`·JSON·Snapshot 사용 |
| Mutability | Frozen·Mutable 여부 |

Context는 DB Row 자체가 아니다.
DB Column을 Common Field로 직접 강제하지 않는다.

## 8. Result 계약

`common_result.py`는 Common 판단 결과 계약을 정의한다.

| 구분 | 용도 |
|---|---|
| Signal | Consumer 분기 |
| Status | 처리 상태 |
| Reason | 집계·표시·저장 |
| Numeric Result | Exposure·Weight·Amount·Quantity |
| Guard Flag | Risk 제한 |
| Detail | 진단용 Payload |

다음 값의 의미를 임의로 바꾸지 않는다.

- `None`
- 0
- Empty Dictionary
- Empty String
- False
- Missing Field

Mutable Default는 `default_factory`를 사용한다.

## 9. Enum 계약

`common_types.py`는 공통 상태와 Signal 문자열을 제공한다.

개념상 아래 유형을 포함할 수 있다.

| Enum | 역할 |
|---|---|
| Market Signal | 시장 상태 |
| Trade Signal | BUY·SELL·HOLD·SKIP |
| Order Side | BUY·SELL 방향 |
| Decision Status | 판단 처리 상태 |
| Position Status | 전략 Position 상태 |
| Execution Mode | Dry Run·Paper·Live 경계 |

실제 Class와 Value는 코드에서 확인한다.

- Enum Member 이름을 임의 변경하지 않는다.
- Enum Value의 대소문자를 바꾸지 않는다.
- Alias 추가도 Serialization 영향을 확인한다.
- 코드에 없는 Enum이나 Value를 문서 편의상 추가하지 않는다.

## 10. Decision Reason 계약

Reason 문자열은 단순 설명 문구가 아닐 수 있다.

Consumer는 Reason을 아래 용도로 사용할 수 있다.

- DB 저장
- Report 집계
- Slack 문구
- View 표시
- Test Fixture
- Backtest와 Daily 비교
- 운영 진단

따라서 오탈자 수정이나 문장 다듬기도 호환성 변경일 수 있다.

새 Reason을 추가할 때는 아래를 확인한다.

| 항목 | 확인 내용 |
|---|---|
| 발생 조건 | 어떤 입력에서 반환되는지 |
| 우선순위 | 여러 조건 동시 발생 시 선택 기준 |
| Consumer | 문자열 비교와 집계 |
| Detail | 설명을 Detail로 분리할 수 있는지 |
| Test | 기존 Fixture와 Expected 결과 |

## 11. Config 계약

`config.py`는 전략 상수와 Runtime Config Dictionary를 제공한다.

개념상 다음 영역을 포함할 수 있다.

| Config | 역할 |
|---|---|
| Strategy | Strategy Name과 Version |
| Market | Regime·Exposure Threshold |
| Filter | BUY 가능 조건 |
| Guard | Risk 제한 |
| Sizing | Weight·Amount·Quantity |
| BUY | BUY Decision Rule |
| SELL | SELL·HOLD Rule |
| Report | Consumer 출력 설정 |

실제 Key와 구조는 코드에서 확인한다.

Config 변경은 전략 결과 변경으로 취급한다.

| 변경 | 영향 |
|---|---|
| Threshold | Boundary Signal 변화 |
| Default | Override 없는 Consumer 전체 |
| Weight | Exposure·Sizing |
| Max Positions | Portfolio 제한 |
| Minimum Score | BUY 후보 수 |
| Sell Rule | SELL·HOLD 결과 |
| Key Rename | Consumer Override 실패 |

## 12. Runtime Config와 Snapshot

`get_runtime_config()`와 `get_config_snapshot()` 계열이 있다면
전략 설정만 반환해야 한다.

확인할 계약은 아래와 같다.

| 항목 | 기준 |
|---|---|
| Copy | 호출마다 독립 객체 반환 |
| Nested Copy | Nested Dictionary Mutation 격리 |
| Override | 원본 Config 변경 금지 |
| Unknown Key | 실제 처리 정책 확인 |
| Serialization | JSON 가능한 값 사용 |
| Secret | 포함 금지 |
| Version | Snapshot과 Metadata 연결 |

Caller가 반환 Dictionary를 수정해도 다음 호출 결과가 바뀌지 않아야 한다.

## 13. Market 판단

`common_market.py`는 Market Context를 시장 판단 결과로 변환한다.

개념 흐름은 아래와 같다.

```text
Market Regime Score
Breadth Pressure
Flow Pressure
Macro Pressure
        │
        ▼
Market Signal
Exposure
Max Positions
Minimum Score
Reason · Detail
```

변경 시 아래를 확인한다.

- Threshold
- Exposure
- Max Positions
- Minimum Score
- Signal
- Status
- Reason
- Detail
- Missing Value
- NaN·Inf
- Boundary 비교

Threshold와 정확히 같은 값에서 `<`, `<=`, `>`, `>=` 차이를 확인한다.

## 14. BUY 판단 흐름

BUY 판단은 여러 책임을 조합한다.

```text
Market Decision
      │
      ▼
BUY Filter
      │
      ▼
BUY Guard
      │
      ▼
BUY Sizing
      │
      ▼
BUY or SKIP
```

실제 호출 순서는 `common_buy_decision.py`에서 확인한다.

### 14.1 BUY Filter

`common_buy_filter.py`는 매수 가능 조건을 판단한다.

확인 대상:

- Market BUY 허용
- Final Score
- Flow·Liquidity·Quality
- Block·Watch
- Minimum Score
- Missing Input
- Reason 우선순위

Filter는 주문 수량을 계산하지 않는다.

### 14.2 BUY Guard

`common_buy_guard.py`는 BUY Risk를 제한한다.

확인 대상:

- Market Guard
- Exposure
- Current Position
- Duplicate Holding
- Max Positions
- Cash Guard
- Haircut
- Risk Flag
- Reason 우선순위

Guard는 DB를 조회하거나 Order를 생성하지 않는다.

### 14.3 BUY Sizing

`common_buy_sizing.py`는 목표 Weight·Amount·Quantity를 계산한다.

| 입력 | 확인 내용 |
|---|---|
| Available Cash | 사용 가능한 현금 |
| Target Weight | 목표 비중 |
| Current Exposure | 현재 노출 |
| Position Value | 기존 보유 가치 |
| Price | 계산 기준 가격 |
| Maximum Amount | 주문 상한 |
| Minimum Amount | 최소 금액 |
| Haircut | Risk 조정 |
| Rounding | 수량 정수화 |

Common은 Broker 호가 단위와 실제 주문 가능 수량을 직접 조회하지 않는다.

### 14.4 BUY Decision

`common_buy_decision.py`는 Filter·Guard·Sizing 결과를 조합한다.

확인 대상:

- Short-circuit 순서
- 최종 Signal
- 최종 Reason
- Detail Merge
- 중복 Key 덮어쓰기
- 실패 이후 불필요한 계산
- Market 결과와 최종 BUY 모순

## 15. SELL 판단 흐름

SELL 판단은 Position Context와 Guard를 사용한다.

```text
Position Context
Market · Stock Input
        │
        ▼
SELL Guard
        │
        ▼
SELL or HOLD
Reason · Detail
```

### 15.1 SELL Guard

`common_sell_guard.py` 변경 시 아래를 확인한다.

- Position 상태
- Holding Period
- Stop Loss
- Take Profit
- Current Price
- Entry Price
- Market 상태
- Missing Value
- Risk Flag
- Reason 우선순위

### 15.2 SELL Decision

`common_sell_decision.py`는 최종 SELL·HOLD 결과를 반환한다.

확인 대상:

- Current Price
- Entry Price
- Highest Price
- Holding Period
- Stop·Take Profit
- Market·Stock Signal
- SELL·HOLD
- Reason
- Detail

### 15.3 Backtest 호환 평가

`common_evaluate_backtest_sell`은 Backtest 호환 계약으로 취급한다.

- 공개 함수명을 유지한다.
- Parameter와 Return 계약을 유지한다.
- 가격 시점이 Look-ahead를 만들지 않는지 확인한다.
- Daily와 Backtest 입력 차이는 Adapter에서 처리한다.
- 동일 Context와 Config에서는 동일 결과를 유지한다.

## 16. Block Watch

`common_block_watch.py`는 Block·Watch 공통 판단을 제공한다.

| 상태 | 확인할 의미 |
|---|---|
| Block | BUY 금지 여부 |
| Watch | 감시·감점·조건부 허용 여부 |
| Release | 해제 조건 |
| Period | 적용 기간 |
| Reason | 결과 설명 |

Block과 Watch를 같은 상태로 처리하지 않는다.

날짜가 포함되면 거래일과 Calendar Date를 구분한다.

## 17. 수치 안전

Common은 전략 수치를 직접 계산하므로 Boundary가 중요하다.

확인 대상:

- Float·Decimal 혼용
- NaN
- Inf
- 0 Division
- 음수
- Missing Value
- Clipping
- Min·Max
- Rounding
- 단위
- Quantity 정수 여부

| 위험 | 기준 |
|---|---|
| 비율 | 0~1과 0~100 구분 |
| 가격 | Currency 단위 확인 |
| 수량 | 음수와 소수 방지 |
| 현금 | 여러 후보 공유 여부는 Consumer 책임 확인 |
| Exact 비교 | Float 허용 오차 검토 |
| NaN | 정상 False로 조용히 통과하지 않음 |

## 18. 날짜와 Look-ahead 안전

Common은 Consumer가 전달한 날짜와 가격 시점을 신뢰하되,
판단 계약에서 미래 데이터를 요구하면 안 된다.

확인할 날짜는 아래와 같다.

- Trade Date
- Feature Date
- Price Date
- Evaluation Date
- Entry Date
- Exit Date
- Holding Days

주의사항:

- 미래 Feature 참조 금지
- 미래 가격 참조 금지
- Backtest 당일 종가와 실제 체결 시점 구분
- 날짜 문자열 단순 비교 주의
- Naive·Timezone-aware Datetime 혼합 금지
- Holding Days 포함·제외 기준 유지

## 19. Package와 Import

### 19.1 `__init__.py`

`__init__.py`는 Package Metadata와 공개 Symbol을 Export할 수 있다.

변경 시 아래를 확인한다.

- Consumer의 Package-level Import
- Export Symbol
- Import 순서
- Circular Import
- Import Side Effect
- Version Metadata

모든 Symbol을 편의상 무분별하게 Export하지 않는다.

### 19.2 `common_utils.py`

공통 순수 Helper를 제공하는 파일이다.

- 전략 계약을 숨기는 과도한 Generic Helper를 만들지 않는다.
- Input Mutation 여부를 확인한다.
- 날짜·수치 Helper의 Boundary를 확인한다.
- 다른 Module과 중복 구현을 만들지 않는다.

### 19.3 `utils.py`

Legacy 가능성이 있는 Utility Module이다.

실제 Import와 Consumer 참조를 확인하기 전 삭제하지 않는다.

파일명만 보고 미사용이라고 단정하지 않는다.

## 20. Version Metadata

`common_version.py`는 Strategy와 Engine Metadata를 제공한다.

| 항목 | 확인 내용 |
|---|---|
| Strategy Name | Consumer 저장·표시 |
| Engine Version | 판단 엔진 식별 |
| Config Version | Config Snapshot 연결 |
| Component Version | 세부 Module 버전 여부 |
| Format | 문자열 형식과 호환성 |

문서만 수정한 경우 Version을 올리지 않는다.

Threshold·Rule·Default가 바뀌어 결과가 달라지면
Version 영향 여부를 함께 판단한다.

## 21. Package, Build와 배포

### 21.1 Package 기준

| 항목 | 값 |
|---|---|
| Package Name | `port-strategy-common` |
| Import Package | `port_strategy_common` |
| Package Version | `1.0.0` |
| Strategy Version | `COMMON_STRATEGY_V1.0.0` |
| Wheel 이름 | `port_strategy_common-1.0.0-py3-none-any.whl` |
| Registry | AWS CodeArtifact |
| RC·정식 보존 | RC와 정식 Version을 별도 Version으로 동시 보존 |
| 공개 계약 검증 | 설치된 Wheel 기준으로 실행 |
| 기본 Publish | 프로젝트 기본값 비활성 |
| Release Publish | 승인 Release Build에서만 일회성 Override |

Package Version은 `pyproject.toml`을 기준으로 한다.
Wheel 이름은 Version과 함께 여러 검사 지점에서 사용하므로 함께 갱신한다.

실제 AWS Account, Repository Endpoint, Token과 ARN은 문서에 기록하지 않는다.

### 21.2 CI/CD 흐름

```text
GitHub Push
    → GitHub Actions OIDC
    → AWS CodeBuild
    → Ruff · mypy
    → Wheel Build · Twine Check
    → Wheel 구조 검증
    → 설치된 Wheel 공개 계약 테스트
    → 기본 Publish Skip
    → 승인 Release Build에서만 CodeArtifact Publish
```

GitHub Actions는 OIDC로 인증하고 CodeBuild를 시작한다.
장기 AWS Access Key를 GitHub Secret에 저장하는 방식은 사용하지 않는다.
요청 Source SHA와 CodeBuild Resolved Source SHA 일치를 확인한다.

### 21.3 품질 게이트

| 게이트 | 기준 |
|---|---|
| Ruff | 정적 검증 통과 |
| mypy | `.devops/scripts` 범위 통과 |
| Wheel Build | Wheel 산출 |
| Twine Check | 배포 Metadata 검증 |
| Wheel 구조 | 필수 Member와 금지 경로 검증 |
| 공개 계약 테스트 | 설치된 Wheel 기준 4건 통과 |
| Source SHA 일치 | 요청 SHA와 Resolved SHA 확인 |
| Publish 기본값 | 비활성 유지 |

### 21.4 Consumer Contract 결과

| Consumer | 결과 |
|---|---|
| StrategyResearch | 48/48 통과 |
| StrategyDecision | 24/24 통과 |
| StrategyExecution | N/A · 직접 Import 없음 |

pandas 관련 사실:

- Legacy `utils.to_float`는 pandas를 사용한다.
- Research는 자체 Runtime Dependency로 pandas를 제공한다.
- Common Package Dependency 정책 변경은 이번 문서 작업 범위가 아니다.

### 21.5 승격과 Rollback

```text
1.0.0rc1 Publish
    → 설치 검증
    → Research·Decision Contract Test
    → 1.0.0 Publish
    → 정식 버전 설치 검증
    → 1.0.0rc1 Version Pin 재설치
    → 공개 계약 재검증
```

Rollback은 Package 삭제나 Git Reset이 아니라
이전 Published Version을 명시적으로 재설치하는 방식이다.

## 22. 주요 파일 구조

```text
.
├── AGENTS.md
├── CHANGELOG.md
├── README.md
├── __init__.py
├── common_block_watch.py
├── common_buy_decision.py
├── common_buy_filter.py
├── common_buy_guard.py
├── common_buy_sizing.py
├── common_context.py
├── common_market.py
├── common_result.py
├── common_sell_decision.py
├── common_sell_guard.py
├── common_types.py
├── common_utils.py
├── common_version.py
├── config.py
├── utils.py
├── pyproject.toml
├── .github/
│   └── workflows/
│       └── common-codebuild.yml
├── .devops/
│   ├── codebuild/
│   │   └── buildspec.yml
│   └── scripts/
│       └── verify_wheel.py
├── tests/
│   └── test_public_contract.py
└── docs/
    └── source-file-catalog.md
```

날짜별 `docs/worklog/*.md`는 현재 문서 구조에 포함하지 않는다.
새 Worklog 파일을 만들지 않는다.

실제 파일 추가·삭제가 있으면 Source Catalog와 함께 갱신한다.

## 23. 파일 그룹

### 22.1 계약

| 파일 | 역할 |
|---|---|
| `common_context.py` | 입력 Context Dataclass |
| `common_result.py` | 판단 Result Dataclass |
| `common_types.py` | Enum과 상태 문자열 |
| `common_version.py` | Version Metadata |
| `__init__.py` | Package Export |

### 22.2 Market·BUY

| 파일 | 역할 |
|---|---|
| `common_market.py` | Market 판단 |
| `common_buy_filter.py` | BUY Filter |
| `common_buy_guard.py` | BUY Guard |
| `common_buy_sizing.py` | BUY Sizing |
| `common_buy_decision.py` | BUY Orchestration |

### 22.3 SELL·Block

| 파일 | 역할 |
|---|---|
| `common_sell_guard.py` | SELL Guard |
| `common_sell_decision.py` | SELL·HOLD와 Backtest 호환 |
| `common_block_watch.py` | Block·Watch 판단 |

### 22.4 Config·Utility

| 파일 | 역할 |
|---|---|
| `config.py` | Strategy Config와 Snapshot |
| `common_utils.py` | 공통 순수 Helper |
| `utils.py` | Legacy 가능 Utility |

## 24. 사용 예시

아래 예시는 Common의 호출 형태를 설명하기 위한 Placeholder다.

실제 Constructor Field와 함수 Signature는 현재 소스에서 확인한다.

```python
from port_strategy_common.common_context import CommonMarketContext
from port_strategy_common.common_market import common_decide_market

market_context = CommonMarketContext(
    trade_date="2026-05-26",
    market_regime_score=0.02,
    breadth_pressure_score=0.10,
    flow_pressure_score=0.05,
    macro_pressure_score=0.00,
)

market_decision = common_decide_market(market_context)
```

예제에 실제 계좌번호, Token, Password, Webhook, API Key와 ARN을 사용하지 않는다.

## 25. AWS 운영에서의 위치

Common은 AWS에서 독립 실행되는 MS가 아니다.

| 항목 | Common 역할 |
|---|---|
| ECS RunTask | 직접 대상 아님 |
| Lambda | 직접 Handler 아님 |
| Step Functions | 직접 Step 아님 |
| EventBridge | 직접 Schedule 대상 아님 |
| AWS Batch | 직접 Job 아님 |
| Container | Consumer Image에 Dependency로 포함 가능 |

실제 Cluster, Task Definition, Image URI, Subnet, Security Group,
Secret ARN과 Command ID는 Consumer 문서에서 관리한다.

## 26. 보안

Common Source와 Config에는 Runtime Secret을 포함하지 않는다.

문서와 예제에 기록하지 않는 값:

- Password
- Token
- API Key
- Account Number
- Webhook URL
- Secret ARN
- IAM Role ARN
- Task Definition ARN
- Image URI
- 일회성 Command ID

필요한 경우 `[REDACTED]` 또는 일반 Placeholder를 사용한다.

Config Snapshot과 Detail Payload에도 Secret이 포함되지 않도록 한다.

## 27. 안전한 검증

문서 작업에서는 아래 정적 확인만 수행한다.

```powershell
git status --short
git diff --stat
git diff -- README.md
```

코드 변경 시에는 Repository에 실제로 존재하는 테스트 구조를 먼저 확인한다.

검증 후보:

- Context 생성
- Result Default
- Enum Value
- Config Copy·Override
- Market Threshold Boundary
- BUY Filter·Guard·Sizing Boundary
- BUY Decision Orchestration
- SELL Decision과 Backtest 호환
- 반복 호출 결정론
- Consumer Import·Signature

다음 검증은 Common 작업에서 수행하지 않는다.

- DB 연결
- 외부 API
- 크롤링
- 주문
- AWS 실행
- Consumer Batch·Backtest·Daily 운영 실행
- File Write Side Effect가 있는 Entrypoint

## 28. 변경 영향 분류

| 변경 | 영향 |
|---|---|
| 문서 정리 | 기능 결과 없음 |
| 내부 리팩터링 | 공개 계약·결과 불변 |
| Optional 확장 | Consumer 하위 호환 확인 |
| Threshold·Rule 변경 | 전략 결과 변경 |
| Function·Field·Enum 변경 | Breaking Change 가능 |
| Config Key 변경 | 모든 Consumer 영향 |
| Reason 변경 | 저장·집계·표시 영향 |
| Export 변경 | Import 실패 가능 |
| Version 변경 | 저장·Report 식별 영향 |

전략 결과가 달라지는 변경은 단순 리팩터링으로 보고하지 않는다.

## 29. 현재 확인이 필요한 항목

아래 항목은 실제 소스와 Consumer Import를 정적으로 대조해 확정한다.

| 항목 | 확인 대상 |
|---|---|
| Public API | 실제 공개 함수와 Signature |
| Context | 실제 Dataclass Field·Default |
| Result | 실제 Field·Detail 구조 |
| Enum | 실제 Member·Value |
| Reason | 실제 문자열과 Consumer 비교 |
| Config | Key·Default·Nested 구조 |
| Snapshot | Copy·Mutation·Override |
| BUY 순서 | Filter·Guard·Sizing Orchestration |
| SELL 호환 | `common_evaluate_backtest_sell` 실제 계약 |
| Block Watch | Block·Watch 의미와 Consumer 사용 |
| Determinism | Clock·Random·Global Mutation |
| Numeric | Float·Decimal·Boundary |
| Date | Look-ahead와 Holding Days |
| Export | `__init__.py` 공개 Symbol |

2026-07-30 기준 아래 항목은 확정되어 미확정 목록에서 제외한다.

| 항목 | 값 |
|---|---|
| Research 직접 Import | 확인 · Contract 48/48 |
| Decision 직접 Import | 확인 · Contract 24/24 |
| Execution 직접 Import | 없음 · 직접 Consumer 아님 |
| Legacy `utils.py` | Research가 `to_float` 직접 Import |
| 공개 계약 테스트 | 설치된 Wheel 기준 4건 존재 |
| Package Version | `1.0.0` |
| Wheel 구조 | 필수 Member·금지 경로 검증 존재 |
| CI·Publish 방식 | GitHub Actions → CodeBuild, 기본 Publish 비활성 |

실제 소스 확인 없이 Public API 전체 Signature나 Reason 전체 목록까지 확정하지 않는다.
확인되지 않은 항목을 운영 사실로 단정하지 않는다.

## 30. 문서 체계

| 문서 | 역할 |
|---|---|
| `AGENTS.md` | 작업·호환성·순수성·검증 규칙 |
| `README.md` | 현재 구조와 사용 AS-IS |
| `CHANGELOG.md` | 날짜별 실제 변경 이력 |
| `docs/source-file-catalog.md` | 파일 책임·Consumer·변경 영향 |

- README에는 현재 상태를 기록한다.
- CHANGELOG에는 과거 변경 사실을 기록한다.
- Source Catalog에는 파일별 책임과 영향 범위를 기록한다.
- 날짜별 Worklog는 새로 만들지 않는다.
- 같은 내용을 여러 문서에 장문으로 반복하지 않는다.

## 31. 관련 문서

- [AGENTS.md](AGENTS.md)
- [CHANGELOG.md](CHANGELOG.md)
- [Source File Catalog](docs/source-file-catalog.md)

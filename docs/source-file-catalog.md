# Source File Catalog

`port_strategy_common`의 주요 소스와 문서가 담당하는 책임,
공개 계약, Consumer 영향과 변경 위험을 정리한다.

이 문서는 전체 파일 Inventory가 아니라 Common 유지보수에 필요한
파일 책임 지도다.

Common Source를 실행하거나 Import하지 않고 현재 파일을 정적으로 확인한 기준이다.

## 1. 문서 사용 기준

| 항목 | 값 |
|---|---|
| 대상 | `port_strategy_common` Root와 주요 문서 |
| 기준 | 현재 파일 구조와 소스의 정적 확인 |
| 주요 관점 | 책임, 입력, 출력, 공개 계약, Consumer 영향, 순수성 |
| 제외 | Cache, Build 산출물, IDE 임시 파일 |
| 실행 | 문서 작업 중 Python과 Consumer Workflow를 실행하지 않음 |
| 민감정보 | 실제 값을 기록하지 않음 |
| 갱신 시점 | 파일·API·Field·Enum·Reason·Config·Consumer 관계 변경 시 |
| 현재 구조 | `README.md` |
| 작업 규칙 | `AGENTS.md` |
| 변경 이력 | `CHANGELOG.md` |

## 2. Common 책임 지도

```text
Consumer DB · Feature · Backtest Row
                  │
                  ▼
            Consumer Adapter
                  │
                  ▼
        Common Context · Config
                  │
                  ▼
 Market · Filter · Guard · Sizing · Decision
                  │
                  ▼
        Result · Enum · Reason · Detail
                  │
                  ▼
 Consumer Persistence · Report · Execution
```

| 계층 | Common 책임 |
|---|---|
| 입력 계약 | Market·Stock·Position Context |
| 결과 계약 | Signal·Status·Reason·Numeric·Detail |
| 상태 계약 | Market·Trade·Order·Decision·Position·Execution Enum |
| Market | Regime·Exposure·최소 기준 판단 |
| BUY | Filter·Guard·Sizing·Decision |
| SELL | Guard·Decision·Backtest 호환 |
| Block Watch | Block·Watch 판단 |
| Config | Strategy Default·Override·Snapshot |
| Version | Strategy·Engine Metadata |
| Utility | 순수 변환과 Boundary Helper |

Common은 DB·HTTP·File IO·AWS·주문을 직접 수행하지 않는다.

## 3. Root 문서

### `AGENTS.md`

| 항목 | 값 |
|---|---|
| 책임 | Common 작업·호환성·순수성·검증 규칙 |
| 주요 내용 | Public API, Context·Result, Enum·Reason, Config, Consumer |
| 사용 시점 | 모든 Common 코드·문서 작업 시작 전 |
| 변경 영향 | 작업 범위와 안전 기준 전체 |
| 주의 | 현재 구조나 과거 변경 이력을 대신하지 않음 |
| 갱신 조건 | 공개 계약·Consumer·순수성·검증 기준 변경 시 |

### `README.md`

| 항목 | 값 |
|---|---|
| 책임 | 현재 Common 구조와 사용 AS-IS 설명 |
| 주요 내용 | 책임 경계, Consumer, 판단 흐름, Config, 안전 |
| 사용 시점 | Common 이해와 사용 방법 확인 |
| 변경 영향 | Consumer 개발과 유지보수 |
| 주의 | 과거 변경 사실을 장문으로 누적하지 않음 |
| 갱신 조건 | 현재 파일·API·Consumer·사용 구조 변경 시 |

### `CHANGELOG.md`

| 항목 | 값 |
|---|---|
| 책임 | 날짜별 주요 변경 사실 보존 |
| 주요 내용 | 문서·API·Config·전략 Rule·호환성 변경 |
| 사용 시점 | 변경 배경과 당시 사실 확인 |
| 변경 영향 | 회귀 분석과 Consumer 영향 추적 |
| 주의 | 현재 상태 설명을 반복하지 않음 |
| 갱신 조건 | 실제 주요 변경 발생 시 |

### `docs/source-file-catalog.md`

| 항목 | 값 |
|---|---|
| 책임 | 파일별 책임·공개 계약·Consumer 영향 지도 |
| 주요 내용 | Context, Result, Types, Decision, Config, Utility |
| 사용 시점 | 수정 대상과 연관 파일 확인 |
| 변경 영향 | 영향 범위 누락 방지 |
| 주의 | 모든 사소한 파일을 무조건 나열하지 않음 |
| 갱신 조건 | 파일·책임·호출·Export·Consumer 변경 시 |

## 4. Package Export와 Metadata

### `__init__.py`

| 항목 | 값 |
|---|---|
| 책임 | Package-level Metadata와 Public Symbol Export |
| 입력 | Common Module의 Version·Metadata Symbol |
| 출력 | Consumer Package Import 경로 |
| Side Effect | 없어야 함 |
| 공개 계약 | Export Symbol과 Package Import Path |
| Consumer 영향 | `from port_strategy_common import ...` |
| 변경 위험 | Import 실패, Circular Import, Startup Side Effect |
| 확인 대상 | 실제 Export 목록과 Consumer Import |
| 삭제·이동 | 모든 Consumer를 함께 수정하지 않는 한 금지 |

### `common_version.py`

| 항목 | 값 |
|---|---|
| 책임 | Strategy·Engine Version Metadata 제공 |
| 입력 | Module 상수 |
| 출력 | Name·Version·Description·Metadata |
| Side Effect | 없어야 함 |
| 공개 계약 | Metadata Key와 문자열 형식 |
| Consumer 영향 | Backtest·Daily·Execution 결과 식별 |
| 변경 위험 | 다른 전략 결과를 같은 Version으로 저장 |
| 확인 대상 | Consumer 저장·Report 사용 여부 |
| 갱신 기준 | 실제 전략 Rule·Config 결과 변경과 연결 |

## 5. Context 계약

### `common_context.py`

| 항목 | 값 |
|---|---|
| 책임 | Common 입력 Context Dataclass 정의 |
| 주요 구조 | Market·Stock·Position Context |
| 입력 | Consumer Adapter가 변환한 명시적 값 |
| 출력 | 공통 판단 함수 입력 객체 |
| Mutability | Frozen 여부를 실제 코드에서 확인 |
| 공개 계약 | Class·Field·순서·Type·Default·Optional |
| Consumer 영향 | Keyword·Positional 생성과 Serialization |
| 변경 위험 | Consumer 생성 실패, 단위·날짜 의미 불일치 |
| 확인 대상 | `asdict`, JSON, DB Payload 변환 사용 |
| 순수성 | 데이터 조회·정규화·현재 시각 사용 금지 |

Context는 Consumer DB Row 자체가 아니다.

Consumer별 Row와 Feature 변환은 Consumer Adapter가 담당한다.

## 6. Result 계약

### `common_result.py`

| 항목 | 값 |
|---|---|
| 책임 | 공통 판단 Result Dataclass 정의 |
| 주요 구조 | Market·Filter·Guard·Sizing·BUY·SELL Result |
| 입력 | 판단 단계의 계산 결과 |
| 출력 | Consumer 분기·저장·표시용 객체 |
| 공개 계약 | Class·Field·Type·Default·Detail 구조 |
| Consumer 영향 | Attribute 접근, `asdict`, JSON, DB 저장 |
| 변경 위험 | 분기 실패, Result Serialization 변화 |
| 확인 대상 | Mutable Default와 `default_factory` |
| 주의 | `None`, 0, Empty 값의 의미 유지 |

Result에서 기계 처리용 값과 진단용 Detail을 구분한다.

| 구분 | 용도 |
|---|---|
| Signal·Status | Consumer 분기 |
| Reason | 저장·집계·표시 |
| Numeric | Exposure·Weight·Amount·Quantity |
| Guard Flag | Risk 제한 |
| Detail | 진단 정보 |

## 7. Enum과 상태 계약

### `common_types.py`

| 항목 | 값 |
|---|---|
| 책임 | Common Enum과 상태 문자열 정의 |
| 주요 유형 | Market·Trade·Order·Decision·Position·Execution |
| 입력 | 코드 상수 정의 |
| 출력 | Consumer 비교·저장·직렬화 값 |
| 공개 계약 | Enum Class·Member·Value |
| Consumer 영향 | DB, Report, View, Execution 분기 |
| 변경 위험 | 문자열 불일치와 상태 해석 오류 |
| 확인 대상 | Value 대소문자, Alias, Serialization |
| 주의 | 코드에 없는 Enum을 문서 편의로 추가하지 않음 |

Enum Member 이름과 Value 모두 호환성 영향이 있다.

## 8. Config 계약

### `config.py`

| 항목 | 값 |
|---|---|
| 책임 | Strategy Default Config와 Runtime Snapshot 제공 |
| 주요 영역 | Market·Filter·Guard·Sizing·BUY·SELL·Report |
| 입력 | Default와 Optional Override |
| 출력 | Runtime Config와 Snapshot Dictionary |
| Side Effect | Global Config Mutation이 없어야 함 |
| 공개 계약 | Key·Nested 구조·Default·Type·단위 |
| Consumer 영향 | Threshold·Rule·Sizing·Report 결과 |
| 변경 위험 | 모든 Consumer 전략 결과 변화 |
| 확인 대상 | Copy·Deep Copy·Merge·Unknown Key 처리 |
| 보안 | Secret과 Persistence Setting 포함 금지 |

Config Key Rename·Remove는 모든 Consumer를 함께 수정하지 않는 한 금지한다.

Snapshot 반환 객체를 Caller가 변경해도 원본 Config가 바뀌지 않아야 한다.

## 9. 공통 Utility

### `common_utils.py`

| 항목 | 값 |
|---|---|
| 책임 | 공통 안전 변환과 Boundary Helper |
| 주요 기능 | Null 확인, Float·Int·String·Boolean 변환, Clamp, Config 조회 |
| 입력 | Primitive 또는 Config 값 |
| 출력 | 변환 값과 Fallback |
| Side Effect | 없어야 함 |
| 공개 계약 | 함수명·Fallback·예외 처리 |
| Consumer 영향 | 모든 판단 Module의 입력 방어 |
| 변경 위험 | Missing·NaN·False·0 의미 변화 |
| 확인 대상 | Pandas Optional 사용과 Fallback |
| 주의 | 입력 객체를 변경하지 않음 |

Pandas가 없거나 `pd.isna`가 실패해도 안전한 Fallback을 유지하는지 확인한다.

### `utils.py`

| 항목 | 값 |
|---|---|
| 책임 | Legacy 호환 Helper |
| 주요 기능 | `to_float` |
| 의존성 | pandas 사용 |
| Consumer | Research가 `to_float` 직접 Import |
| 현재 분류 | Legacy 보존 대상 |
| 공개 계약 | Module Path와 함수명 |
| 변경 위험 | Research Import 실패 |
| 확인 대상 | Common 내부·Consumer 직접 Import |
| 삭제 기준 | 제거 전 Consumer 계약 확인 필요 |

신규 코드는 실제 필요와 기존 패턴을 확인한 뒤 `common_utils.py`를 우선 검토한다.

## 10. Market 판단

### `common_market.py`

| 항목 | 값 |
|---|---|
| 책임 | Market Context를 시장 판단 결과로 변환 |
| 입력 | Regime·Breadth·Flow·Macro 관련 값 |
| 출력 | Signal·Exposure·Max Positions·Minimum Score·Reason |
| Side Effect | 없어야 함 |
| 공개 계약 | 공개 함수 Signature와 Result |
| Consumer 영향 | BUY 허용·Sizing·후보 기준 |
| 변경 위험 | Market Signal과 Portfolio Exposure 변화 |
| 확인 대상 | Threshold Boundary와 Downgrade 순서 |
| 수치 안전 | None·NaN·Inf·음수·0 처리 |

Reason과 Signal 우선순위는 Backtest·Daily 동일성에 영향을 준다.

## 11. BUY Filter

### `common_buy_filter.py`

| 항목 | 값 |
|---|---|
| 책임 | BUY 후보 기본 조건과 후보 정렬·선별 Helper |
| 입력 | Stock Context 또는 변환 가능한 후보 값 |
| 출력 | Filter Result와 후보 목록 |
| 주요 조건 | Score·Flow·Volatility·Intraday Range 등 |
| Side Effect | 없어야 함 |
| 공개 계약 | 함수·Sort Key·Filter Reason |
| Consumer 영향 | BUY 후보 통과와 우선순위 |
| 변경 위험 | 후보 수·순서·Reason 변화 |
| 확인 대상 | Context 변환, Strong·Normal 분류, Cut 기준 |
| 주의 | Filter와 Sizing 책임을 혼합하지 않음 |

이 파일이 Dict·Object를 `CommonStockContext`로 변환한다면
그 동작은 Consumer Adapter와 중복되는지 확인한다.

후보 정렬은 동일 점수의 Tie-breaker와 입력 순서 안정성을 확인한다.

## 12. BUY Guard

### `common_buy_guard.py`

| 항목 | 값 |
|---|---|
| 책임 | BUY Risk Flag와 Haircut 판단 |
| 입력 | Market·Stock·Position·Config |
| 출력 | Guard Result, Flag, Reason, Detail |
| 주요 조건 | Hot Chase·Stop Risk·Flow·Range·Soft Risk |
| Side Effect | 없어야 함 |
| 공개 계약 | Flag Name·Reason·Result Field |
| Consumer 영향 | Sizing Haircut과 진단 Payload |
| 변경 위험 | BUY 수량과 Risk 표시 변화 |
| 확인 대상 | Flag 우선순위와 중복 조건 |
| 주의 | BUY 차단과 Haircut 의미를 실제 코드에서 구분 |

Flag 이름이 Consumer 저장 Payload와 연결되는지 확인한다.

## 13. BUY Sizing

### `common_buy_sizing.py`

| 항목 | 값 |
|---|---|
| 책임 | 단일 종목 Sizing과 Backtest Allocation |
| 입력 | Cash·Score·Volatility·Guard Flag·Price·Config |
| 출력 | Weight·Amount·Quantity 또는 Position Size |
| 계산 | Float·Decimal 사용 범위를 실제 코드에서 확인 |
| Side Effect | 없어야 함 |
| 공개 계약 | 함수 Signature·Return·Sort Key |
| Consumer 영향 | 주문 후보 금액과 Backtest Position |
| 변경 위험 | 전략 성과와 실제 후보 규모 변화 |
| 확인 대상 | Haircut 순서, Cap, Minimum, Rounding |
| 결정론 | 동일 후보 목록에서 동일 Allocation 순서 |

Daily·Execution 단일 종목 Sizing과 Backtest 후보 Allocation을
같은 계산으로 단정하지 않는다.

Decimal과 Float를 혼용하면 변환 위치와 반올림 기준을 확인한다.

## 14. BUY Decision

### `common_buy_decision.py`

| 항목 | 값 |
|---|---|
| 책임 | 최종 BUY·SKIP Orchestration |
| 입력 | Stock Context, Market Result, Cash, Config |
| 호출 | Filter·Guard·Sizing |
| 출력 | `CommonBuyDecision` 계열 Result |
| Side Effect | 없어야 함 |
| 공개 계약 | 호출 순서, Signal, Reason, Detail |
| Consumer 영향 | Daily·Backtest 최종 BUY 결과 |
| 변경 위험 | Short-circuit와 Reason 우선순위 변화 |
| 확인 대상 | 실패 후 계산, Detail Merge, Key 충돌 |
| 결정론 | 동일 입력에서 동일 최종 결과 |

실제 Filter·Guard·Sizing 호출 순서는 코드에서 확인한다.

하위 Result와 최종 Signal이 모순되지 않아야 한다.

## 15. SELL Guard

### `common_sell_guard.py`

| 항목 | 값 |
|---|---|
| 책임 | SELL Risk Flag와 Active Reason 계산 |
| 입력 | Position·Market·Stock Context와 Config |
| 출력 | Guard Result, Flag, Reason, Detail |
| 주요 조건 | Stop Loss·Profit Protect·Holding·Market Block·Flow·Score |
| Side Effect | 없어야 함 |
| 공개 계약 | Flag·Reason·Result Field |
| Consumer 영향 | SELL·HOLD 최종 판단 |
| 변경 위험 | 청산 시점과 Reason 변화 |
| 확인 대상 | 조건 우선순위, Missing Price, Holding Boundary |
| 주의 | 최종 SELL·HOLD Orchestration과 책임 분리 |

Guard는 Position DB를 수정하거나 SELL Order를 만들지 않는다.

## 16. SELL Decision

### `common_sell_decision.py`

| 항목 | 값 |
|---|---|
| 책임 | 최종 SELL·HOLD와 Backtest 호환 평가 |
| 입력 | Position Context, Guard Result, Market·Stock Input |
| 출력 | `CommonSellDecision`과 Backtest 호환 Dictionary |
| Side Effect | 없어야 함 |
| 공개 계약 | 함수 Signature·Return Key·Reason |
| Consumer 영향 | Daily Position Decision과 Backtest Exit |
| 변경 위험 | SELL 시점·성과·저장 Payload 변화 |
| 확인 대상 | Reason 우선순위와 비교 연산 |
| 특수 계약 | `common_evaluate_backtest_sell` 호환 동작 |

`common_evaluate_backtest_sell` 변경 시 아래를 확인한다.

- Parameter 이름과 Default
- Return Dictionary Key
- Sell Reason 문자열
- 가격 비교 연산
- Holding Days
- Daily와 Backtest Adapter 차이
- Look-ahead 가능성

## 17. Block Watch

### `common_block_watch.py`

| 항목 | 값 |
|---|---|
| 책임 | Market Block 구간의 Watch 후보 판단 |
| 입력 | Stock Context 또는 호환 후보 값 |
| 출력 | Watch 여부와 실패 Reason |
| Side Effect | 없어야 함 |
| 공개 계약 | 함수 Signature·Reason·Return 구조 |
| Consumer 영향 | Daily Watch 저장 또는 진단 |
| 변경 위험 | Block 구간 후보 범위 변화 |
| 확인 대상 | Score Field, Dict·Object 처리, Threshold |
| 주의 | 실제 BUY Signal이나 성과 계산으로 자동 승격하지 않음 |

Block과 Watch는 같은 상태가 아니다.

Watch가 감시·감점·조건부 허용 중 무엇인지 Consumer에서 확인한다.

## 18. 공개 계약 지도

### 18.1 함수

| 파일 | 주요 공개 계약 |
|---|---|
| `common_market.py` | Market Decision 함수 |
| `common_buy_filter.py` | BUY Filter·정렬·선별 Helper |
| `common_buy_guard.py` | BUY Guard |
| `common_buy_sizing.py` | BUY Sizing·Allocation |
| `common_buy_decision.py` | 최종 BUY Decision |
| `common_sell_guard.py` | SELL Guard |
| `common_sell_decision.py` | SELL Decision·Backtest 평가 |
| `common_block_watch.py` | Block Watch |
| `config.py` | Runtime Config·Snapshot |
| `common_version.py` | Metadata 조회 |

실제 함수명과 Signature는 소스와 Consumer Import에서 확인한다.

### 18.2 데이터 구조

| 파일 | 계약 |
|---|---|
| `common_context.py` | Input Dataclass |
| `common_result.py` | Result Dataclass |
| `common_types.py` | Enum Value |
| `config.py` | Config Key와 Nested 구조 |
| `common_version.py` | Metadata Key |
| `__init__.py` | Package Export |

## 19. Consumer 영향 지도

### StrategyResearch

| Common 파일 | 주요 영향 |
|---|---|
| Market | Backtest Market Regime |
| BUY Guard | Risk Flag와 Haircut |
| BUY Sizing | Position Allocation |
| SELL Decision | Exit 판단 |
| Config | Backtest Rule |
| Version | Run Metadata |

### StrategyDecision

| Common 파일 | 주요 영향 |
|---|---|
| Market | Daily Market Decision |
| BUY Filter | Candidate 통과 |
| BUY Guard | Risk 제한 |
| BUY Sizing | Target Weight·Amount |
| BUY Decision | Daily BUY·SKIP |
| SELL Decision | Position SELL·HOLD |
| Block Watch | Block 구간 Watch |
| Context·Result | Adapter와 저장 Payload |

### StrategyExecution

| 항목 | 값 |
|---|---|
| 현재 상태 | `port_strategy_common` 직접 Import 없음 |
| 소스 근거 | Common Config 미사용 주석만 존재 |
| 설계 목적 | Signal·Status·Mode 의미 정렬 대상 |
| 승격 조건 | 향후 직접 Import 추가 시 직접 Consumer 기록 |

Execution은 현재 직접 Consumer가 아니며 Consumer Contract Test 대상도 아니다.

### 기타 MS

| 항목 | 값 |
|---|---|
| View·Crawler·Preprocessor·MarketConnector | 직접 Import 근거 없음 |

실제 Import가 확인되지 않은 항목은 직접 Consumer 계약으로 확정하지 않는다.

## 20. 순수성과 Side Effect 지도

| 파일 그룹 | 기대 기준 |
|---|---|
| Context·Result·Types | 정의만 제공 |
| Market·Filter·Guard | 입력 판단만 수행 |
| Sizing | 수치 계산만 수행 |
| Decision | 하위 판단 Orchestration |
| Config | Copy·Override·Snapshot |
| Version | Metadata 반환 |
| Utility | 변환과 Boundary Helper |
| Package Export | Symbol Export만 수행 |

모든 Common 전략 파일에서 아래가 발견되면 책임 경계를 재검토한다.

- SQL 또는 DB Client
- HTTP·Broker Client
- AWS SDK
- File Read·Write
- 환경변수 직접 조회
- 현재 시각 직접 조회
- Seed 없는 Random
- Global Mutable State 변경
- Import 시 실행
- Secret 또는 Runtime Credential

## 21. 결정론과 재현성 지도

| 위험 | 관련 파일 |
|---|---|
| Global Config Mutation | `config.py` |
| Dictionary Mutation | Config·Decision·Utility |
| Unstable Sort | BUY Filter·Sizing |
| Current Time | Block Watch·SELL Holding |
| Random | 모든 판단 Module |
| Float Exact Compare | Market·Sizing·SELL |
| NaN Silent Pass | Utility·Filter·Guard |
| Timezone | Context·Block Watch·SELL |
| Look-ahead | SELL Decision·Research Adapter |

같은 입력을 반복 호출했을 때 같은 Result가 나와야 한다.

## 22. 수치·날짜 영향 지도

### 수치

| 영역 | 확인 대상 |
|---|---|
| Market | Threshold Boundary |
| BUY Filter | Score·Volatility·Range |
| BUY Guard | Risk Flag·Haircut |
| BUY Sizing | Decimal·Float·Rounding·Cap |
| SELL Guard | Stop·Profit·Score 붕괴 |
| SELL Decision | 가격 비교와 Holding Boundary |
| Utility | None·NaN·Inf·Fallback |

### 날짜

| 영역 | 확인 대상 |
|---|---|
| Context | Trade·Feature·Evaluation Date |
| Block Watch | 적용 기간과 해제일 |
| SELL Guard | Entry Date와 Holding Days |
| SELL Decision | Price Date와 Exit 시점 |
| Backtest Helper | 당일 가격 사용과 Look-ahead |
| Consumer Adapter | Calendar Date와 거래일 변환 |

## 23. 변경 영향 관계

| 변경 대상 | 함께 확인할 파일 |
|---|---|
| Context Field | Result 소비부, BUY·SELL 함수, Consumer Adapter |
| Result Field | Decision Module, Consumer 저장·Report |
| Enum Value | 모든 Consumer 비교·저장 |
| Reason | Filter·Guard·Decision, Consumer 집계 |
| Config Key | Config 호출부와 Consumer Override |
| Market Rule | BUY Filter·Sizing·Decision |
| BUY Filter | BUY Decision과 Candidate Sort |
| BUY Guard | BUY Sizing과 BUY Decision |
| BUY Sizing | BUY Decision과 Research Allocation |
| SELL Guard | SELL Decision과 Backtest Helper |
| SELL Decision | Research·Decision Consumer |
| Block Watch | BUY Filter와 Decision Consumer |
| Version | Package Export와 Consumer Metadata |
| Package Export | 모든 Package-level Import |
| Utility | 모든 호출 Module |
| Legacy 파일 | Common과 Consumer Import |
| 파일 추가·삭제 | README와 Source Catalog |
| 공개 계약 변경 | AGENTS·README·CHANGELOG·Catalog |

## 24. Legacy와 삭제 판단

파일을 정리하거나 삭제하기 전 아래를 확인한다.

| 항목 | 확인 내용 |
|---|---|
| Common Import | Root 내부 직접·동적 Import |
| Consumer Import | Research·Decision·Execution |
| Export | `__init__.py` 공개 Symbol |
| Test | Fixture·Monkeypatch·Import |
| Documentation | README·Catalog·예제 |
| Git | 최근 변경과 사용자 미커밋 작업 |
| Runtime | 설치 Package와 Deployment Copy |

미사용 근거가 충분하지 않으면 삭제하지 않고 정리 후보로만 표시한다.

`utils.py`는 실제 Consumer 참조 확인 전 삭제하지 않는다.

## 25. AWS 운영 위치

Common은 독립 실행 대상이 아니다.

| AWS 구성 | Common 위치 |
|---|---|
| ECS RunTask | Consumer Image Dependency |
| Lambda | Consumer Package Dependency |
| Step Functions | 직접 Step 아님 |
| EventBridge | 직접 Schedule 아님 |
| AWS Batch | 직접 Job 아님 |

Cluster, Task Definition, Image URI, Secret ARN과 Command ID는
Consumer 운영 문서에서 관리한다.

## 26. 민감정보

Common에 아래 값을 추가하거나 문서에 기록하지 않는다.

- Password
- Token
- API Key
- Account Number
- Webhook URL
- Secret ARN
- IAM Role ARN
- Task Definition ARN
- Image URI
- Command ID

Config Snapshot과 Result Detail에도 Secret이 포함되지 않도록 한다.

필요하면 `[REDACTED]` 또는 일반 Placeholder를 사용한다.

## 27. 현재 문서에서 제외한 항목

날짜별 `docs/worklog/*.md`는 현재 파일 구조와 Catalog 목록에서 제외한다.

과거 Worklog 생성 사실은 `CHANGELOG.md`에만 보존한다.
새 Worklog 파일을 만들지 않는다.

아래 산출물도 Catalog 대상에서 제외한다.

- `__pycache__/`
- `.pytest_cache/`
- `build/`
- `dist/`
- `*.egg-info/`
- IDE 임시 파일
- Coverage 산출물
- 일회성 Log·Dump
- Secret 원문 파일

## 28. 현재 확인이 필요한 항목

| 항목 | 확인 대상 |
|---|---|
| Public Function | 실제 함수명·Signature·Default |
| Context | Dataclass Field·순서·Default·Frozen |
| Result | Field·Default·Detail 구조 |
| Enum | Member·Value·Alias |
| Reason | 실제 문자열과 Consumer 비교 |
| Config | Key·Default·Nested 구조 |
| Snapshot | Deep Copy·Override·Mutation |
| Export | `__init__.py` Public Symbol |
| Market | Threshold·Downgrade 순서 |
| BUY Filter | Context 변환·Sort·Cut |
| BUY Guard | Flag 의미와 Haircut |
| BUY Sizing | Decimal·Allocation·Rounding |
| BUY Decision | 실제 호출 순서와 Detail Merge |
| SELL Guard | Flag·Reason 우선순위 |
| SELL Decision | SELL·HOLD와 Backtest Return Key |
| Block Watch | Dict·Object 입력과 Watch 의미 |
| Determinism | Clock·Random·Global Mutation |
| Look-ahead | 가격·Feature·Holding 시점 |
| Consumer | Research·Decision·Execution Import |
| Legacy | `utils.py` 실제 참조 |
| Tests | Test Runner와 Consumer Contract Coverage |

확인되지 않은 항목을 운영 사실로 단정하지 않는다.

## 29. Catalog 갱신 조건

아래 변경이 있으면 이 문서를 같은 작업에서 확인한다.

- 파일 추가·삭제·Rename
- Public Function과 Signature 변경
- Context·Result Dataclass 변경
- Enum Member·Value 변경
- Reason 문자열 변경
- Config Key·Default·Nested 구조 변경
- Snapshot·Override·Mutation 정책 변경
- Package Export 변경
- Consumer Import와 Adapter 관계 변경
- Market·BUY·SELL Rule 변경
- Filter·Guard·Sizing Orchestration 변경
- Block·Watch 의미 변경
- Version Metadata 변경
- Utility·Legacy 분류 변경
- 순수성 또는 Import Side Effect 변경
- 테스트 구조 변경
- 문서 구조와 Worklog 정책 변경

단순 오탈자나 설명 정리로 관련 없는 모든 파일을
기계적으로 갱신하지 않는다.

## 30. DevOps와 Package 파일

Build·CI·배포 관련 파일의 책임과 변경 영향을 정리한다.

전략 판단 로직은 포함하지 않는다.

### `pyproject.toml`

| 항목 | 값 |
|---|---|
| 책임 | Package Metadata와 Build 정의 |
| Package Name | `port-strategy-common` |
| Package Version | `1.0.0` |
| Python Version | `>=3.10` |
| Dependency 선언 | 현재 비어 있음 |
| Build Backend | setuptools |
| 변경 위험 | Version·Package 구성과 Wheel 산출 영향 |
| 확인 대상 | Buildspec·verify_wheel·공개 계약 테스트 Version 정합 |

### `.github/workflows/common-codebuild.yml`

| 항목 | 값 |
|---|---|
| 책임 | GitHub OIDC 인증과 CodeBuild 시작 |
| Trigger | `workflow_dispatch` |
| 실행 | CodeBuild 시작·상태 대기·결과 판정 |
| Source SHA | Commit SHA를 Source Version으로 전달 |
| 변경 위험 | 인증 경계와 Build 시작 방식 |
| 확인 대상 | 장기 Access Key 미사용과 Source SHA 확인 |

### `.devops/codebuild/buildspec.yml`

| 항목 | 값 |
|---|---|
| 책임 | 품질 게이트·Wheel Build·조건부 Publish |
| 품질 게이트 | Ruff, mypy, Wheel Build, Twine Check |
| Wheel 검증 | `verify_wheel.py`와 설치 후 공개 계약 테스트 |
| 설치 검증 | Build한 Wheel 설치 후 테스트 실행 |
| Publish | 기본 비활성 · Wheel 존재 시에만 진입 |
| 변경 위험 | 게이트 우회와 실패의 성공 처리 |
| 확인 대상 | `PUBLISH_TO_CODEARTIFACT` 기본값과 Wheel 경로 확인 |

### `.devops/scripts/verify_wheel.py`

| 항목 | 값 |
|---|---|
| 책임 | Wheel 이름과 내부 구조 검증 |
| Wheel 이름 | `port_strategy_common-1.0.0-py3-none-any.whl` |
| 필수 Member | 주요 공개 Module 포함 확인 |
| 금지 경로 | `__pycache__`·`.pyc`·`.git`·`docs` 배제 |
| 무결성 | SHA-256과 Member 수 출력 |
| 변경 위험 | Version·Wheel 이름 불일치 |
| 확인 대상 | Version 변경 시 검사 기준 동시 갱신 |

### `tests/test_public_contract.py`

| 항목 | 값 |
|---|---|
| 책임 | 설치된 Wheel 기준 공개 계약 검증 |
| Distribution Name | `port-strategy-common` 확인 |
| Package Version | `1.0.0` 확인 |
| Strategy Version | `COMMON_STRATEGY_V1.0.0` 확인 |
| 공개 Symbol | 공개 Symbol 6개 Import 확인 |
| 설치 출처 | `site-packages` 설치 확인 |
| 변경 위험 | Repository Source Import를 배포 검증으로 오인 |
| 확인 대상 | Version·Symbol·설치 출처 정합 |

## 31. 관련 문서

- [AGENTS.md](../AGENTS.md)
- [README.md](../README.md)
- [CHANGELOG.md](../CHANGELOG.md)

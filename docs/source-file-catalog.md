# Source File Catalog

이 문서는 `port_strategy_common` repository root 기준 주요 소스/문서 파일의 역할을 정리한다. build 결과물, cache, IDE 임시 파일, `__pycache__` 계열 생성물은 제외한다.

## Python 소스

### `__init__.py` - 패키지 metadata export
- 파일 내용: `port_strategy_common` 패키지의 공통 전략 이름, 버전, 설명 조회 함수를 export한다.
- 주요 역할: consumer가 패키지 단위로 version metadata를 확인할 수 있게 한다.
- 수정/운영 시 주의사항: public export 목록 변경은 downstream import에 영향을 줄 수 있다.

### `common_block_watch.py` - BLOCK 관찰 후보 판단
- 파일 내용: MARKET BLOCK 구간에서 실제 매수는 하지 않고 강한 예외 후보를 watch 대상으로 선별한다.
- 주요 역할: dict 또는 객체 형태의 stock context에서 score 값을 읽어 관찰 후보 여부와 실패 사유를 반환한다.
- 수정/운영 시 주의사항: 주문 신호나 성과 계산에 포함하지 않는 보조 판단으로 유지해야 한다.

### `common_buy_decision.py` - 최종 매수 판단 orchestration
- 파일 내용: BUY filter, BUY guard, BUY sizing을 순서대로 호출해 최종 BUY/SKIP 결과를 만든다.
- 주요 역할: backtest와 daily 흐름이 동일한 매수 판단 순서를 사용하도록 묶는다.
- 수정/운영 시 주의사항: 단계 순서, reason 문자열, 반환 detail 구조 변경은 consumer 호환성에 영향을 준다.

### `common_buy_filter.py` - 매수 후보 기본 필터
- 파일 내용: 종목 점수, 수급, 변동성, 장중 범위 등으로 BUY 후보 통과 여부를 판단한다.
- 주요 역할: 후보 row를 `CommonStockContext`로 변환하고, strong/normal 후보 정렬 및 cut helper를 제공한다.
- 수정/운영 시 주의사항: 기존 backtest 필드명과 sort key 호환을 유지해야 한다.

### `common_buy_guard.py` - 매수 risk flag 판단
- 파일 내용: hot chase, buy day stop risk, mid flow tight range risk, soft risk flag를 계산한다.
- 주요 역할: BUY 차단 자체보다 sizing haircut과 진단용 risk flag를 제공한다.
- 수정/운영 시 주의사항: flag 이름은 기존 buy_info 저장명과 연결되므로 임의 변경하지 않는다.

### `common_buy_sizing.py` - 매수 sizing과 allocation
- 파일 내용: Daily/Execution 단일 종목 sizing과 backtest 후보 리스트 allocation을 계산한다.
- 주요 역할: score, volatility, guard flag를 반영해 target weight/amount/qty 또는 position size를 산출한다.
- 수정/운영 시 주의사항: Decimal 기반 backtest allocation, haircut 우선순위, sort key는 전략 결과에 직접 영향을 준다.

### `common_context.py` - 공통 입력 context
- 파일 내용: 시장, 종목, 포지션 입력값을 담는 frozen dataclass를 정의한다.
- 주요 역할: backtest와 daily decision이 동일한 입력 형태를 공유하게 한다.
- 수정/운영 시 주의사항: dataclass 필드명 변경은 caller와 저장/리포트 변환 로직에 영향을 준다.

### `common_market.py` - 시장 regime 판단
- 파일 내용: 시장 점수와 breadth/flow/macro 압력을 기준으로 market signal과 exposure 기준을 계산한다.
- 주요 역할: BUY/SIZING 판단의 상위 시장 상태와 최소 점수/수급 기준을 제공한다.
- 수정/운영 시 주의사항: signal downgrade 순서와 reason 문자열은 backtest/daily 동일성에 중요하다.

### `common_result.py` - 공통 판단 결과
- 파일 내용: 시장, filter, guard, sizing, buy, sell 판단 결과 dataclass를 정의한다.
- 주요 역할: 각 판단 단계의 반환 형태를 표준화한다.
- 수정/운영 시 주의사항: 필드명과 자료형 변경은 downstream consumer 호환성에 영향을 준다.

### `common_sell_decision.py` - 최종 매도 판단과 backtest sell 호환
- 파일 내용: SELL guard 결과를 우선순위에 따라 SELL/HOLD로 변환하고 기존 backtest sell helper를 제공한다.
- 주요 역할: daily sell decision과 backtest 호환 sell 평가 경로를 함께 유지한다.
- 수정/운영 시 주의사항: `common_evaluate_backtest_sell`의 반환 dict key, 비교 연산, sell_reason 문자열은 변경하지 않아야 한다.

### `common_sell_guard.py` - 매도 guard와 risk flag
- 파일 내용: 손절, 이익 보호, 보유일, MARKET BLOCK 세부 조건, 수급/점수 붕괴 flag를 계산한다.
- 주요 역할: 최종 매도 판단 전에 sell risk 상태와 active reason을 구조화한다.
- 수정/운영 시 주의사항: 최종 SELL/HOLD 우선순위는 `common_sell_decision.py`에서 관리하므로 역할을 섞지 않는다.

### `common_types.py` - 공통 enum
- 파일 내용: market signal, trade signal, order side, decision status, position status, execution mode enum을 정의한다.
- 주요 역할: 문자열 기반 signal/status 값을 표준화한다.
- 수정/운영 시 주의사항: enum 값은 저장 데이터와 분기 조건에 영향을 주므로 호환성 검토가 필요하다.

### `common_utils.py` - 공통 안전 변환 helper
- 파일 내용: null 판정, 안전한 float/int/str/bool 변환, clamp, config 조회 helper를 제공한다.
- 주요 역할: 전략 판단 함수의 입력 방어 로직을 일관되게 처리한다.
- 수정/운영 시 주의사항: pandas가 있으면 `pd.isna`를 사용하지만, 없거나 실패해도 fallback하도록 유지한다.

### `common_version.py` - 공통 전략 version metadata
- 파일 내용: 공통 전략 이름, 버전, 설명과 metadata 조회 함수를 제공한다.
- 주요 역할: research/daily/execution이 같은 전략 코어를 쓰는지 추적한다.
- 수정/운영 시 주의사항: 버전 문자열 변경은 배포/리포트 식별 기준과 연결될 수 있다.

### `config.py` - 전략 기본 설정
- 파일 내용: 시장, 필터, sizing, 매수/매도, 리포트 설정과 runtime config snapshot 함수를 제공한다.
- 주요 역할: 공통 전략 core의 기본 threshold와 config dictionary를 한곳에서 관리한다.
- 수정/운영 시 주의사항: runtime config snapshot은 전략 설정만 반환한다. external persistence setting은 Common core에서 관리하지 않는다.


### `utils.py` - legacy utility
- 파일 내용: 기존 consumer 호환용 `to_float` helper를 제공한다.
- 주요 역할: 과거 utility import를 유지하는 정리 후보 성격의 파일이다.
- 수정/운영 시 주의사항: 정리 후보지만 삭제하지 않는다. 신규 코드는 `common_utils.py` 사용을 우선한다.

## 문서

### `AGENTS.md` - 작업 지침
- 파일 내용: 프로젝트 범위, 허용/금지 작업, 보안, Git, 검증, 문서화 규칙을 정의한다.
- 주요 역할: 이 저장소에서 작업할 때 유지해야 할 운영 제약을 명시한다.
- 수정/운영 시 주의사항: 민감정보 기록 금지, 기능 호환성 유지, Git 금지 작업 규칙을 우선한다.

### `CHANGELOG.md` - 변경 기록
- 파일 내용: 날짜별 주요 변경 사항과 기능 변경 여부를 기록한다.
- 주요 역할: 문서화, 설정, 전략 로직 변경 이력을 짧게 추적한다.
- 수정/운영 시 주의사항: 실제 변경된 내용만 기록하고, 기능 변경이 없으면 명시한다.

### `README.md` - 프로젝트 안내
- 파일 내용: 프로젝트 목적, 구조, 설계 원칙, 사용 예시, 설정, 안전 제약, 검증 방법을 설명한다.
- 주요 역할: 사용자와 consumer가 공통 전략 코어의 역할과 사용 방식을 빠르게 이해하게 한다.
- 수정/운영 시 주의사항: 실행 방법, 설정, 구조, 주요 기능이 바뀐 경우에만 갱신한다.

### `docs/source-file-catalog.md` - 전체 파일 카탈로그
- 파일 내용: repository root 기준 주요 소스/문서 파일의 역할과 운영 주의사항을 정리한다.
- 주요 역할: AWS Migration 전 초기 정리 대상으로 파일별 책임과 정리 후보를 파악하게 한다.
- 수정/운영 시 주의사항: 생성물/cache는 제외하고, unused/legacy 의심 파일은 삭제하지 않고 정리 후보로만 표시한다.

### `docs/worklog/2026-05-26.md` - 2026-05-26 작업 일지
- 파일 내용: 초기 문서 초안 작성, 구조 확인, 금지 작업 미수행 확인을 기록한다.
- 주요 역할: 프로젝트 문서화 시작 시점의 작업 내역을 보존한다.
- 수정/운영 시 주의사항: 기존 worklog 들여쓰기와 상태 표기 형식을 유지한다.

### `docs/worklog/2026-05-27.md` - 2026-05-27 작업 일지
- 파일 내용: 과거 sensitive configuration cleanup 문서 갱신 내역을 기록한다.
- 주요 역할: hardcoded secret value 제거 이력을 보존한다.
- 수정/운영 시 주의사항: 실제 민감정보 값은 기록하지 않는다.

### `docs/worklog/2026-05-28.md` - 2026-05-28 작업 일지
- 파일 내용: Git 상태 확인, 전체 파일 카탈로그 작성, 파일별 설명 주석 추가, README/CHANGELOG 반영을 기록한다.
- 주요 역할: AWS Migration 전 초기 정리 작업의 문서화 결과를 추적한다.
- 수정/운영 시 주의사항: 기능 로직 변경 없이 문서/주석 작업만 기록한다.

### `docs/worklog/2026-07-01.md` - 2026-07-01 작업 일지
- 파일 내용: Common 책임 경계, consumer 의존성, AWS 운영 dependency 성격, 호환성 계약 관점의 README/AGENTS/CHANGELOG 최신화 작업을 기록한다.
- 주요 역할: PORT-STRATEGY-COMMON 문서 최신화 결과를 소비 MS 세부 상세와 분리하여 추적한다.
- 수정/운영 시 주의사항: 최신 worklog 들여쓰기 규칙(` 1)`/`   (1)`/`       -`, `:완료` 공백 없음)을 유지한다.

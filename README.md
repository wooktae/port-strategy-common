# port_strategy_common

포트폴리오 전략 research, daily decision, execution 후보 생성에서 함께 사용하는 Python 공통 전략 코어다.

이 패키지는 시장 판단, 매수 판단, 매도 판단, sizing, guard, context, result, version metadata를 한곳에 모아 backtest와 daily 흐름이 동일한 판단 로직을 재사용하도록 한다.

## 현재 구조

- `common_context.py`: 시장, 종목, 포지션 입력 context dataclass.
- `common_result.py`: 시장, filter, guard, sizing, buy, sell 판단 결과 dataclass.
- `common_types.py`: market signal, trade signal, order side, decision status, position status, execution mode enum.
- `common_market.py`: 시장 regime 판단과 exposure / max positions / 최소 점수 기준 계산.
- `common_buy_filter.py`: 매수 가능 여부 filter 판단.
- `common_buy_guard.py`: 매수 측 risk guard 판단.
- `common_buy_sizing.py`: target weight, amount, quantity 계산.
- `common_buy_decision.py`: 최종 BUY/SKIP 판단 orchestration.
- `common_sell_guard.py`: 매도 측 guard와 risk flag 계산.
- `common_sell_decision.py`: 최종 SELL/HOLD 판단과 backtest 호환 sell 평가 helper.
- `common_block_watch.py`: block watch 관련 공통 로직.
- `common_utils.py`: 공통 utility helper.
- `common_version.py`: 공통 전략 코어 metadata.
- `config.py`: 전략 상수와 runtime config dictionary.
- `utils.py`: legacy utility module.
- `__init__.py`: strategy metadata export.

전체 파일별 역할과 운영 주의사항은 `docs/source-file-catalog.md`에 정리한다. `utils.py`처럼 legacy 성격이 있는 파일은 삭제하지 않고 정리 후보로만 표시한다.

## 설계 원칙

- `common_*` 전략 모듈은 순수 함수 중심으로 유지한다.
- `common_*` 전략 모듈에서 DB 접근, HTTP/API 호출, 파일 IO를 하지 않는다.
- caller가 context dataclass와 optional config dictionary를 제공한다.
- 판단 결과는 signal/reason 같은 기계 처리용 값과 진단용 detail dictionary를 함께 제공한다.
- backtest와 daily decision은 같은 입력을 받으면 같은 결과를 내야 한다.
- enum 값, decision reason, dataclass 필드명은 호환성 영향이 있으므로 신중하게 바꾼다.

## 사용 예시

```python
from port_strategy_common.common_context import CommonMarketContext, CommonStockContext
from port_strategy_common.common_market import common_decide_market
from port_strategy_common.common_buy_decision import common_decide_buy

market_context = CommonMarketContext(
    trade_date="2026-05-26",
    market_regime_score=0.02,
    breadth_pressure_score=0.10,
    flow_pressure_score=0.05,
    macro_pressure_score=0.00,
)

market = common_decide_market(market_context)

stock = CommonStockContext(
    trade_date="2026-05-26",
    ticker_code="000000",
    final_score=0.12,
    flow_pressure_score=0.30,
    close_price=10000,
)

decision = common_decide_buy(
    stock,
    market,
    available_cash=1_000_000,
)
```

위 예시는 placeholder 값만 사용한다. 실제 계좌번호, 토큰, 비밀번호, webhook URL, API key는 source나 문서에 기록하지 않는다.

## Runtime Configuration

`config.py`에는 strategy name, engine version, risk threshold, market threshold, buy/sell config, sizing config, report config가 있다.

민감정보 값은 출력하거나 문서에 복사하지 않는다. 실행 서비스와 통합할 때 secret은 local 설정 또는 환경별 설정으로 분리하는 방향이 적합하다.

## 안전 제약

- 이 저장소에서 실제 크롤링을 실행하지 않는다.
- 공통 전략 모듈에서 외부 trading/broker API를 호출하지 않는다.
- 이 저장소에서 주문을 제출하거나 실행하지 않는다.
- 명시 요청과 안전한 환경 확인 없이 DB DDL/DML을 실행하지 않는다.
- secret 값은 log, 문서, 예제, 완료 보고에 노출하지 않는다.

## 검증

초기 문서화 시점에는 현재 루트에서 프로젝트 단위 test runner를 확인하지 못했다. 문서만 수정한 경우에는 변경 파일 범위를 확인한다.

```powershell
git status --short
git diff --stat
```

코드 수정 시에는 수정 모듈에 맞는 집중 검증을 추가하거나 실행하고, 부족한 test coverage가 있으면 완료 보고에 남긴다.

## 문서화 상태

- `docs/source-file-catalog.md`: repository root 기준 전체 주요 파일의 역할, 책임, 수정/운영 주의사항을 정리한다.
- Python 소스 파일에는 파일별 module docstring을 추가해 실행 진입점, 외부 연동 여부, 호환성 주의사항을 확인할 수 있게 한다.
- Common core는 database persistence helper와 connection setting을 포함하지 않으며, runtime config snapshot은 전략 설정만 제공한다.

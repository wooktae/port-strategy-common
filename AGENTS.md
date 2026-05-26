# AGENTS.md - port_strategy_common

## 프로젝트
- 이 저장소는 포트폴리오 전략의 research, daily decision, execution 후보 생성에서 함께 사용하는 Python 공통 전략 코어다.
- `common_*` 모듈은 시장 판단, 매수/매도 판단, sizing, guard, context, result, enum 로직을 제공한다.
- 동일한 입력 context와 config를 주면 backtest와 daily 흐름에서 동일한 결과를 반환해야 한다.
- 공개 함수명, dataclass 필드, enum 값, decision reason 문자열은 호환성 영향이 있으므로 명시 요청 없이 바꾸지 않는다.

## 작업 범위
- 현재 `port_strategy_common` 루트 안에서만 작업한다.
- 현재 루트 밖 파일은 수정하지 않는다.
- `port-view`를 포함한 sibling 프로젝트는 명시 요청이 없으면 읽기 전용 참고 자료로만 사용한다.
- 변경은 작고 검토 가능한 단위로 유지한다.
- 코드나 문서 수정 전 현재 구조를 먼저 확인한다.

## 허용 작업
- README / docs 작성 및 수정
- 공통 전략 로직 분석
- `common_*` 순수 함수 중심의 제한적 리팩터링
- dataclass, enum, version metadata 정리
- 사용 가능한 범위의 집중 검증
- 제약, 위험, 후속 작업 문서화

## 금지 작업
- 실제 크롤링 실행
- 외부 API 호출
- 주문 제출 또는 주문 실행
- 직접 DB DDL/DML 실행
- 실서비스 대상 trading, batch, execution workflow 실행
- 비밀번호, 토큰, API key, 계좌번호, webhook URL 등 민감정보 값 출력 또는 문서 기록
- 실제 로컬 운영 설정값 수정
- 후보 식별 및 명시 승인 없는 파일 삭제
- 명시 요청 없는 commit

## 유지해야 할 것
- 기존 전략 signal 이름과 enum 값
- 기존 decision reason 문자열
- 기존 dataclass 필드명과 반환 객체 형태
- `common_*` 모듈의 순수성 원칙: DB 접근 금지, HTTP/API 호출 금지, 파일 IO 금지
- `common_evaluate_backtest_sell`의 backtest 호환 동작
- 모든 consumer를 함께 수정하지 않는 한 runtime config key 이름 유지

## 보안 규칙
- 로컬 파일에서 민감정보를 발견해도 값을 노출하지 않는다.
- 민감정보를 언급해야 할 때는 `[REDACTED]`로 마스킹한다.
- 예제에는 실제 credential을 넣지 않는다.
- secret은 committed source가 아니라 환경별/local 설정으로 분리하는 방향을 우선한다.

## Git 규칙
- 작업 전후 `git status --short`를 확인한다.
- 작업 후 변경 범위를 확인한다. 미추적 파일은 `git diff --stat`에 잡히지 않을 수 있으므로 `git status --short`도 함께 본다.
- 사용자 변경을 되돌리지 않는다.
- 명시 요청 없이는 commit하지 않는다.

## 검증 명령
문서만 수정한 경우:

```powershell
git status --short
git diff --stat
```

코드 수정 시에는 영향 범위에 맞는 가장 좁은 검증부터 수행한다. 프로젝트 단위 테스트 명령이 없으면 import와 호출부를 확인하고, 검증 한계를 완료 보고에 남긴다.

## 완료 보고
작업 완료 후 아래만 짧게 보고한다.

- 변경 파일
- 변경 요약
- 검증 결과
- 남은 위험 또는 후속 작업

## 문서화 규칙
- 프로젝트 동작, 공개 사용법, 운영 제약이 바뀌면 `README.md`, `CHANGELOG.md`, `docs/worklog/YYYY-MM-DD.md` 중 필요한 문서를 함께 갱신한다.
- README는 사용자가 프로젝트를 이해하고 실행하는 데 필요한 확인된 내용만 담는다.
- CHANGELOG에는 실제 변경된 주요 내용만 기록한다.
- worklog에는 계획/완료/보류/확인 상태를 명확히 남긴다.
- 민감정보 값은 문서에 기록하지 않는다.

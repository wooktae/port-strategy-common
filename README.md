# port_strategy_common

`port_strategy_common` is the Python strategy decision core that provides
strategy decision logic and the common Consumer contracts.

It provides Market Decision, Buy Decision, Sell Decision, Sizing, Guard, Context, Result, Enum,
Config, and Version Metadata as common contracts.

By design, it is the strategy contract alignment target for StrategyResearch, StrategyDecision, and StrategyExecution.
The current direct-import Consumers are StrategyResearch and StrategyDecision.
StrategyExecution currently does not import `port_strategy_common` directly.

Common is not a standalone runtime service.
It is built as a Versioned Python Package, and it is a shared library that returns
pure decision results when each Consumer passes in a Context and Config.

## 1. Service Summary

| Item | Value |
|---|---|
| Package Name | `port-strategy-common` |
| Import Package | `port_strategy_common` |
| Primary responsibility | Provide strategy decision logic and the common Consumer contracts |
| Execution form | Versioned Python Package imported by Consumers |
| Package Version | `1.0.1` |
| Strategy Version | `COMMON_STRATEGY_V1.0.0` |
| Artifact | Python Wheel |
| Registry | AWS CodeArtifact |
| Build | GitHub Actions → AWS CodeBuild |
| Release | Automatic Versioned Package publish on main Push |
| Manual run | `workflow_dispatch` Build-only |
| Rollback | Reinstall pinned to the previously published Version |
| Primary input | Context Dataclass and Config Dictionary |
| Primary output | Result Dataclass, Enum, Reason, Detail |
| Direct Consumer | StrategyResearch, StrategyDecision |
| Direct execution | Not performed |
| DB | Not accessed directly |
| External API | Not called directly |
| File IO | Not performed in strategy Modules |
| Core principle | Return the same result for the same input and the same Config |
| Documentation basis | Static confirmation of the current file structure and source |

## 2. Primary Responsibilities

| Area | Responsibility |
|---|---|
| Context | Market·Stock·Position input structure |
| Result | Market·Filter·Guard·Sizing·BUY·SELL result structure |
| Types | Signal·Side·Status·Position·Execution Mode Enum |
| Market | Regime and Exposure decision |
| BUY Filter | Judge buy eligibility conditions |
| BUY Guard | Limit buy Risk |
| BUY Sizing | Compute target weight·amount·quantity |
| BUY Decision | Filter·Guard·Sizing Orchestration |
| SELL Guard | Sell Risk Flag and Guard |
| SELL Decision | SELL·HOLD decision and Backtest-compatible evaluation |
| Block Watch | Common Block·Watch conditions |
| Config | Strategy Config and Runtime Snapshot |
| Version | Strategy·Engine Version Metadata |
| Utility | Common pure Helper |

## 3. Responsibility Boundary

Common provides only decision logic and contracts.

| Area | Owner |
|---|---|
| Source data collection | Crawler |
| Raw preprocessing and Feature generation | Preprocessor |
| Daily Signal DB storage | StrategyDecision |
| Daily Position Decision storage | StrategyDecision |
| Backtest·Trade·Report storage | StrategyResearch |
| Execution Plan·Order·Position storage | StrategyExecution |
| Broker·KIS API | MarketConnector |
| Screens and approval UI | port-view |
| Full Daily Orchestration | Scheduler and Step Functions |
| DB Connection·Persistence | Each Consumer MS |
| Common decision·contracts | StrategyCommon |

Do not add the following responsibilities to Common.

- DB Connection and SQL
- HTTP·Broker Client
- AWS SDK
- File Persistence
- Direct handling of Consumer DB Rows
- Scheduler·State Machine execution
- Order creation·submission·fill
- Report·Slack·View rendering

## 4. Consumer Relationships

Common does not own the Consumer internal implementation.
Each Consumer converts its own input into a Common Context and stores·displays the result.

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

| Item | Value |
|---|---|
| Primary use | Market·BUY·SELL·Sizing·Config·Version |
| Purpose | Reuse common Rules for Backtest decisions |
| Consumer responsibility | Store Backtest Run·Trade·Metric·Report |
| Caution | The Research price timing must not create Look-ahead |

### 4.2 StrategyDecision

| Item | Value |
|---|---|
| Primary use | Market·Filter·Guard·Sizing·BUY·SELL·Block Watch |
| Purpose | Apply common Rules to Daily operational decisions |
| Consumer responsibility | Store Daily Signal·Position Decision |
| Caution | Maintain the Adapter that converts DB·Feature Rows into a Context |

### 4.3 StrategyExecution

| Item | Value |
|---|---|
| Current state | Does not import `port_strategy_common` directly |
| Source basis | Only a comment stating that Common Config is not used directly |
| Design purpose | Common-meaning alignment target for the stage before execution candidates |
| Consumer responsibility | Store Plan·Order·Fill·Position |
| Promotion condition | Record as a direct Consumer once a direct Import is added in the future |

StrategyExecution is a contract alignment target by design, but it is not currently a direct Consumer.
It is also not currently a direct Consumer Contract Test target.

### 4.4 Other MS

Whether View, Crawler, Preprocessor, and MarketConnector import Common directly
is recorded only when there is actual Import evidence.

Do not conclude a service is a Common Consumer merely because it
indirectly consumes strings or DB results.

## 5. Design Principles

### 5.1 Pure Functions

The `common_*` strategy Modules are kept centered on pure functions.

| Prohibited dependency | Reason |
|---|---|
| DB | Prevent coupling with Consumer Persistence |
| HTTP·API | Prevent dependence on external state |
| File IO | Prevent dependence on call order and environment |
| Direct environment variable lookup | Prevent making the input contract opaque |
| Direct current-time lookup | Prevent reduced reproducibility |
| Random without a Seed | Prevent nondeterministic results |
| Global Mutation | Prevent dependence on test order |

Decision functions receive the values they need through Arguments, a Context, and a Config.

### 5.2 Determinism

The same input and the same Config must return the same result.

The following factors must not implicitly affect the result.

- Current time
- Timezone
- Locale
- Call order
- Global Mutable State
- Mutation of the original Dictionary
- Order of an Unordered Collection
- Random without a Seed
- The Consumer execution environment

### 5.3 Consumer Independence

Common does not directly know a specific Consumer's DB Schema or Row structure.

```text
Consumer Row
  → Consumer Adapter
  → Common Context
  → Common Result
  → Consumer storage structure
```

If differences in per-Consumer Adapters can change results,
those differences are managed explicitly in the Consumer.

## 6. Public API

Common is a Public API used together by multiple Consumers.

| Contract | Example |
|---|---|
| Module Path | `port_strategy_common.common_market` |
| Function name | `common_decide_market` |
| Parameter | name·order·Default |
| Return Type | Result Dataclass |
| Context Field | input field name·Type·Default |
| Result Field | Signal·Reason·Detail |
| Enum Value | Serialized string |
| Reason | Reason string used for aggregation·Report·View |
| Config Key | Consumer Override Key |
| Export | `__init__.py` public Symbol |
| Version | Strategy·Engine Metadata |

Do not make the following changes unless all Consumers are modified and validated together.

- Rename a public function
- Rename a Parameter or change its order
- Add a required Parameter
- Change the Return Type
- Delete·Rename a Dataclass Field
- Change an Enum Value
- Modify a Reason string
- Delete·Rename a Config Key
- Move a Module
- Remove a Package Export

## 7. Context Contract

`common_context.py` defines the Common input contract.

Confirm the primary Contexts in the actual code.

| Context | Conceptual role |
|---|---|
| Market Context | Input for market Regime decisions |
| Stock Context | Input for per-stock BUY·Filter·Guard |
| Position Context | Input for SELL·HOLD decisions |

When changing a Context, confirm the following.

| Item | Confirmation content |
|---|---|
| Field Name | Consumer Keyword Argument |
| Field Order | Whether Positional construction is used |
| Type | Numeric·string·date contract |
| Default | Whether existing Consumers can omit it |
| Optional | Meaning of Missing Input |
| Unit | Price·ratio·quantity |
| Date | Trade·Feature·Evaluation Date |
| Serialization | Use of `asdict`·JSON·Snapshot |
| Mutability | Whether Frozen·Mutable |

A Context is not a DB Row itself.
Do not force DB Columns directly into Common Fields.

## 8. Result Contract

`common_result.py` defines the Common decision result contract.

| Category | Use |
|---|---|
| Signal | Consumer branching |
| Status | Processing status |
| Reason | Aggregation·display·storage |
| Numeric Result | Exposure·Weight·Amount·Quantity |
| Guard Flag | Risk limit |
| Detail | Diagnostic Payload |

Do not arbitrarily change the meaning of the following values.

- `None`
- 0
- Empty Dictionary
- Empty String
- False
- Missing Field

Use `default_factory` for a Mutable Default.

## 9. Enum Contract

`common_types.py` provides common status and Signal strings.

Conceptually it may include the following types.

| Enum | Role |
|---|---|
| Market Signal | Market state |
| Trade Signal | BUY·SELL·HOLD·SKIP |
| Order Side | BUY·SELL direction |
| Decision Status | Decision processing status |
| Position Status | Strategy Position status |
| Execution Mode | Dry Run·Paper·Live boundary |

Confirm the actual Class and Value in the code.

- Do not arbitrarily change an Enum Member name.
- Do not change the case of an Enum Value.
- For an added Alias, also confirm the Serialization impact.
- Do not add an Enum or Value that is not in the code for documentation convenience.

## 10. Decision Reason Contract

A Reason string may not be a mere descriptive phrase.

A Consumer may use a Reason for the following purposes.

- DB storage
- Report aggregation
- Slack phrasing
- View display
- Test Fixture
- Backtest vs Daily comparison
- Operational diagnostics

Therefore, even a typo fix or wording cleanup may be a compatibility change.

When adding a new Reason, confirm the following.

| Item | Confirmation content |
|---|---|
| Occurrence condition | Which input returns it |
| Priority | Selection criterion when multiple conditions occur simultaneously |
| Consumer | String comparison and aggregation |
| Detail | Whether the explanation can be split into Detail |
| Test | Existing Fixtures and Expected results |

## 11. Config Contract

`config.py` provides strategy constants and the Runtime Config Dictionary.

Conceptually it may include the following areas.

| Config | Role |
|---|---|
| Strategy | Strategy Name and Version |
| Market | Regime·Exposure Threshold |
| Filter | BUY eligibility conditions |
| Guard | Risk limit |
| Sizing | Weight·Amount·Quantity |
| BUY | BUY Decision Rule |
| SELL | SELL·HOLD Rule |
| Report | Consumer output settings |

Confirm the actual Keys and structure in the code.

Treat a Config change as a strategy result change.

| Change | Impact |
|---|---|
| Threshold | Boundary Signal change |
| Default | All Consumers without an Override |
| Weight | Exposure·Sizing |
| Max Positions | Portfolio limit |
| Minimum Score | Number of BUY candidates |
| Sell Rule | SELL·HOLD result |
| Key Rename | Consumer Override failure |

## 12. Runtime Config and Snapshot

If `get_runtime_config()` and `get_config_snapshot()` families exist,
they must return only strategy settings.

The contracts to confirm are as follows.

| Item | Criterion |
|---|---|
| Copy | Return an independent object on each call |
| Nested Copy | Isolate Nested Dictionary Mutation |
| Override | Prohibit changing the original Config |
| Unknown Key | Confirm the actual handling policy |
| Serialization | Use JSON-capable values |
| Secret | Prohibited to include |
| Version | Link the Snapshot with the Metadata |

Even if a Caller modifies the returned Dictionary, the result of the next call must not change.

## 13. Market Decision

`common_market.py` converts a Market Context into a market decision result.

The conceptual flow is as follows.

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

When changing it, confirm the following.

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
- Boundary comparison

At a value exactly equal to the Threshold, confirm the difference between `<`, `<=`, `>`, and `>=`.

## 14. BUY Decision Flow

The BUY decision composes multiple responsibilities.

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

Confirm the actual call order in `common_buy_decision.py`.

### 14.1 BUY Filter

`common_buy_filter.py` judges buy eligibility conditions.

Confirmation targets:

- Market BUY allowance
- Final Score
- Flow·Liquidity·Quality
- Block·Watch
- Minimum Score
- Missing Input
- Reason priority

The Filter does not compute order quantity.

### 14.2 BUY Guard

`common_buy_guard.py` limits BUY Risk.

Confirmation targets:

- Market Guard
- Exposure
- Current Position
- Duplicate Holding
- Max Positions
- Cash Guard
- Haircut
- Risk Flag
- Reason priority

The Guard does not query the DB or create an Order.

### 14.3 BUY Sizing

`common_buy_sizing.py` computes the target Weight·Amount·Quantity.

| Input | Confirmation content |
|---|---|
| Available Cash | Usable cash |
| Target Weight | Target weight |
| Current Exposure | Current exposure |
| Position Value | Existing holding value |
| Price | Calculation reference price |
| Maximum Amount | Order cap |
| Minimum Amount | Minimum amount |
| Haircut | Risk adjustment |
| Rounding | Quantity integerization |

Common does not directly query the Broker tick size or the actual orderable quantity.

### 14.4 BUY Decision

`common_buy_decision.py` composes the Filter·Guard·Sizing results.

Confirmation targets:

- Short-circuit order
- Final Signal
- Final Reason
- Detail Merge
- Duplicate Key overwrite
- Unnecessary computation after a failure
- Contradiction between the Market result and the final BUY

## 15. SELL Decision Flow

The SELL decision uses the Position Context and the Guard.

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

When changing `common_sell_guard.py`, confirm the following.

- Position status
- Holding Period
- Stop Loss
- Take Profit
- Current Price
- Entry Price
- Market status
- Missing Value
- Risk Flag
- Reason priority

### 15.2 SELL Decision

`common_sell_decision.py` returns the final SELL·HOLD result.

Confirmation targets:

- Current Price
- Entry Price
- Highest Price
- Holding Period
- Stop·Take Profit
- Market·Stock Signal
- SELL·HOLD
- Reason
- Detail

### 15.3 Backtest-Compatible Evaluation

`common_evaluate_backtest_sell` is treated as a Backtest-compatible contract.

- Keep the public function name.
- Keep the Parameter and Return contract.
- Confirm that the price timing does not create Look-ahead.
- Differences between Daily and Backtest input are handled in the Adapter.
- The same Context and Config keep the same result.

## 16. Block Watch

`common_block_watch.py` provides the common Block·Watch decision.

| State | Meaning to confirm |
|---|---|
| Block | Whether BUY is prohibited |
| Watch | Whether it is monitoring·penalizing·conditionally allowing |
| Release | Release condition |
| Period | Application period |
| Reason | Result explanation |

Do not treat Block and Watch as the same state.

When a date is involved, distinguish the trading day from the Calendar Date.

## 17. Numeric Safety

Because Common computes strategy numbers directly, Boundaries are important.

Confirmation targets:

- Mixing Float·Decimal
- NaN
- Inf
- Division by 0
- Negatives
- Missing Value
- Clipping
- Min·Max
- Rounding
- Unit
- Whether Quantity is an integer

| Risk | Criterion |
|---|---|
| Ratio | Distinguish 0~1 from 0~100 |
| Price | Confirm the Currency unit |
| Quantity | Prevent negatives and fractions |
| Cash | Confirm the Consumer responsibility for whether it is shared across candidates |
| Exact comparison | Consider a Float tolerance |
| NaN | Do not silently pass as a normal False |

## 18. Date and Look-ahead Safety

Common trusts the dates and price timing that the Consumer passes in,
but the decision contract must not require future data.

The dates to confirm are as follows.

- Trade Date
- Feature Date
- Price Date
- Evaluation Date
- Entry Date
- Exit Date
- Holding Days

Cautions:

- Prohibit referencing future Features
- Prohibit referencing future prices
- Distinguish the Backtest same-day close from the actual fill timing
- Beware simple string comparison of dates
- Prohibit mixing Naive·Timezone-aware Datetime
- Maintain the include·exclude criterion for Holding Days

## 19. Package and Import

### 19.1 `__init__.py`

`__init__.py` may export Package Metadata and public Symbols.

When changing it, confirm the following.

- Consumer Package-level Import
- Export Symbol
- Import order
- Circular Import
- Import Side Effect
- Version Metadata

Do not export all Symbols indiscriminately for convenience.

### 19.2 `common_utils.py`

This file provides common pure Helpers.

- Do not create an excessive Generic Helper that hides the strategy contract.
- Confirm whether there is Input Mutation.
- Confirm the Boundary of date·numeric Helpers.
- Do not create duplicate implementations with other Modules.

### 19.3 `utils.py`

This is a Utility Module with Legacy potential.

Do not delete it before confirming the actual Import and Consumer references.

Do not conclude it is unused based on the filename alone.

## 20. Version Metadata

`common_version.py` provides Strategy and Engine Metadata.

| Item | Confirmation content |
|---|---|
| Strategy Name | Consumer storage·display |
| Engine Version | Decision engine identification |
| Config Version | Link with the Config Snapshot |
| Component Version | Whether there is a detailed Module version |
| Format | String format and compatibility |

Do not bump the Version when only documentation is modified.

When a Threshold·Rule·Default change alters results,
also judge whether it affects the Version.

## 21. Package, Build, and Deployment

### 21.1 Package Basis

| Item | Value |
|---|---|
| Package Name | `port-strategy-common` |
| Import Package | `port_strategy_common` |
| Package Version | `1.0.1` |
| Strategy Version | `COMMON_STRATEGY_V1.0.0` |
| Wheel name | `port_strategy_common-1.0.1-py3-none-any.whl` |
| Registry | AWS CodeArtifact |
| RC·release preservation | Preserve RC and release Versions simultaneously as separate Versions |
| Public API validation | Run against the installed Wheel |
| CodeBuild default Publish | Project default `false` (safeguard) |
| main Push | Enable automatic Release Publish |
| workflow_dispatch | Build-only |

The Canonical Source of the Package Version is `pyproject.toml`.
The Wheel name and Version validation are performed dynamically based on the `pyproject.toml` Version.

Do not record the actual AWS Account, Repository Endpoint, Token, or ARN in documentation.

### 21.2 CI/CD Flow

```text
main Push
    → GitHub Actions OIDC
    → AWS CodeBuild
    → Ruff · mypy
    → Wheel Build · Twine Check
    → Wheel structure validation
    → Installed-Wheel Public API test
    → Build Gate
    → CodeArtifact Version Guard
    → CodeArtifact Publish

workflow_dispatch
    → Same quality gates
    → Build-only (Publish disabled)
```

GitHub Actions authenticates with OIDC and starts CodeBuild.
The approach of storing a long-lived AWS Access Key in a GitHub Secret is not used.
main Push enables Publish via a CodeBuild environment Override, and `workflow_dispatch` is Build-only.
The CodeBuild project's own default `false` is kept as a safeguard.
If a Build quality gate fails, Publish does not proceed.
If the same Version already exists in CodeArtifact, Publish is blocked before publishing.

### 21.3 Quality Gates

| Gate | Criterion |
|---|---|
| Ruff | Static validation passes |
| mypy | Passes for the `.devops/scripts` scope |
| Wheel Build | Wheel is produced |
| Twine Check | Distribution Metadata validation |
| Wheel structure | Validate required Members and prohibited paths |
| Public API test | 4 tests pass against the installed Wheel |
| Source SHA match | Confirm the requested SHA and the Resolved SHA |
| Build Gate | Block Publish if `CODEBUILD_BUILD_SUCCEEDING` fails |
| Version Guard | Block Publish if the same Version exists |
| CodeBuild default Publish | Keep the `false` safeguard |
| main Push Publish | Enabled via Override |

### 21.4 Consumer Contract Results

| Consumer | Result |
|---|---|
| StrategyResearch | 48/48 passed |
| StrategyDecision | 24/24 passed |
| StrategyExecution | N/A · No direct Import |

pandas-related facts:

- Legacy `utils.to_float` uses pandas.
- Research provides pandas as its own Runtime Dependency.
- Changing the Common Package Dependency policy is out of scope for this documentation work.

### 21.5 Promotion and Rollback

The flow below is the initial Release (`1.0.0rc1` → `1.0.0`) validation case.
The current Package Version is `1.0.1`, and the promotion·Rollback method is the same.

```text
1.0.0rc1 Publish
    → Installation validation
    → Research·Decision Contract Test
    → 1.0.0 Publish
    → Release-version installation validation
    → Reinstall pinned to 1.0.0rc1 Version
    → Public API re-validation
```

Rollback is not a Package deletion or a Git Reset;
it is an explicit reinstall of the previously published Version.

## 22. Primary File Structure

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

Date-specific `docs/worklog/*.md` files are not included in the current documentation structure.
Do not create new Worklog files.

When files are actually added or deleted, update the Source Catalog together.

## 23. File Groups

### 22.1 Contracts

| File | Role |
|---|---|
| `common_context.py` | Input Context Dataclass |
| `common_result.py` | Decision Result Dataclass |
| `common_types.py` | Enum and status strings |
| `common_version.py` | Version Metadata |
| `__init__.py` | Package Export |

### 22.2 Market·BUY

| File | Role |
|---|---|
| `common_market.py` | Market Decision |
| `common_buy_filter.py` | BUY Filter |
| `common_buy_guard.py` | BUY Guard |
| `common_buy_sizing.py` | BUY Sizing |
| `common_buy_decision.py` | BUY Orchestration |

### 22.3 SELL·Block

| File | Role |
|---|---|
| `common_sell_guard.py` | SELL Guard |
| `common_sell_decision.py` | SELL·HOLD and Backtest compatibility |
| `common_block_watch.py` | Block·Watch decision |

### 22.4 Config·Utility

| File | Role |
|---|---|
| `config.py` | Strategy Config and Snapshot |
| `common_utils.py` | Common pure Helper |
| `utils.py` | Utility with Legacy potential |

## 24. Usage Example

The example below is a Placeholder to illustrate Common's call form.

Confirm the actual Constructor Fields and function Signatures in the current source.

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

Do not use an actual account number, Token, Password, Webhook, API Key, or ARN in examples.

## 25. Position in AWS Operations

Common is not an MS that runs standalone in AWS.

| Item | Common role |
|---|---|
| ECS RunTask | Not a direct target |
| Lambda | Not a direct Handler |
| Step Functions | Not a direct Step |
| EventBridge | Not a direct Schedule target |
| AWS Batch | Not a direct Job |
| Container | Can be included as a Dependency in a Consumer Image |

The actual Cluster, Task Definition, Image URI, Subnet, Security Group,
Secret ARN, and Command ID are managed in the Consumer documentation.

## 26. Security

Do not include Runtime Secrets in the Common Source and Config.

Values not recorded in documentation and examples:

- Password
- Token
- API Key
- Account Number
- Webhook URL
- Secret ARN
- IAM Role ARN
- Task Definition ARN
- Image URI
- One-time Command ID

Use `[REDACTED]` or a generic Placeholder when needed.

Ensure that no Secret is included in the Config Snapshot or the Detail Payload.

## 27. Safe Validation

For documentation work, perform only the following static checks.

```powershell
git status --short
git diff --stat
git diff -- README.md
```

For code changes, first confirm the test structure that actually exists in the Repository.

Validation candidates:

- Context construction
- Result Default
- Enum Value
- Config Copy·Override
- Market Threshold Boundary
- BUY Filter·Guard·Sizing Boundary
- BUY Decision Orchestration
- SELL Decision and Backtest compatibility
- Determinism across repeated calls
- Consumer Import·Signature

The following validations are not performed in Common work.

- DB connection
- External API
- Crawling
- Orders
- AWS execution
- Consumer Batch·Backtest·Daily operational execution
- Entrypoints with a File Write Side Effect

## 28. Change Impact Classification

| Change | Impact |
|---|---|
| Documentation cleanup | No functional result |
| Internal refactoring | Public API·result unchanged |
| Optional extension | Confirm Consumer backward compatibility |
| Threshold·Rule change | Strategy result change |
| Function·Field·Enum change | Possible Breaking Change |
| Config Key change | Affects all Consumers |
| Reason change | Affects storage·aggregation·display |
| Export change | Possible Import failure |
| Version change | Affects storage·Report identification |

Do not report a change that alters strategy results as a simple refactoring.

## 29. Items Requiring Confirmation

Confirm the items below by statically cross-checking the actual source and Consumer Imports.

| Item | Confirmation target |
|---|---|
| Public API | Actual public functions and Signatures |
| Context | Actual Dataclass Field·Default |
| Result | Actual Field·Detail structure |
| Enum | Actual Member·Value |
| Reason | Actual strings and Consumer comparison |
| Config | Key·Default·Nested structure |
| Snapshot | Copy·Mutation·Override |
| BUY order | Filter·Guard·Sizing Orchestration |
| SELL compatibility | Actual `common_evaluate_backtest_sell` contract |
| Block Watch | Block·Watch meaning and Consumer use |
| Determinism | Clock·Random·Global Mutation |
| Numeric | Float·Decimal·Boundary |
| Date | Look-ahead and Holding Days |
| Export | `__init__.py` public Symbol |

As of 2026-08-12, the items below are confirmed and removed from the unconfirmed list.

| Item | Value |
|---|---|
| Research direct Import | Confirmed · Contract 48/48 |
| Decision direct Import | Confirmed · Contract 24/24 |
| Execution direct Import | None · Not a direct Consumer |
| Legacy `utils.py` | Research imports `to_float` directly |
| Public API test | 4 tests exist against the installed Wheel |
| Package Version | `1.0.1` |
| Wheel structure | Required Member·prohibited path validation exists |
| CI·Publish method | GitHub Actions → CodeBuild, automatic Publish on main Push |

Do not finalize the entire Public API Signature set or the full Reason list without confirming the actual source.
Do not treat unconfirmed items as operational fact.

## 30. Documentation System

| Document | Role |
|---|---|
| `AGENTS.md` | Work·compatibility·purity·validation rules |
| `README.md` | Current structure and usage AS-IS |
| `CHANGELOG.md` | Actual change history by date |
| `docs/source-file-catalog.md` | File responsibility·Consumer·change impact |

- Record the current state in the README.
- Record past change facts in the CHANGELOG.
- Record per-file responsibilities and impact scope in the Source Catalog.
- Do not create new date-specific Worklogs.
- Do not repeat the same content at length across multiple documents.

## 31. Related Documents

- [AGENTS.md](AGENTS.md)
- [CHANGELOG.md](CHANGELOG.md)
- [Source File Catalog](docs/source-file-catalog.md)

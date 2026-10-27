# Source File Catalog

Organizes the responsibilities, Public API, Consumer impact, and change risk that the primary source
and documentation of `port_strategy_common` handle.

This document is not a full file Inventory but a file responsibility map needed for Common maintenance.

It is based on statically confirming the current files without running or importing the Common Source.

## 1. Documentation Usage Basis

| Item | Value |
|---|---|
| Target | The `port_strategy_common` Root and primary documents |
| Basis | Static confirmation of the current file structure and source |
| Primary perspective | Responsibility, input, output, Public API, Consumer impact, purity |
| Excluded | Cache, Build outputs, IDE temporary files |
| Execution | Do not run Python and Consumer Workflows during documentation work |
| Sensitive information | Actual values not recorded |
| Update timing | When file·API·Field·Enum·Reason·Config·Consumer relationships change |
| Current structure | `README.md` |
| Work rules | `AGENTS.md` |
| Change history | `CHANGELOG.md` |

## 2. Common Responsibility Map

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

| Layer | Common responsibility |
|---|---|
| Input contract | Market·Stock·Position Context |
| Result contract | Signal·Status·Reason·Numeric·Detail |
| Status contract | Market·Trade·Order·Decision·Position·Execution Enum |
| Market | Regime·Exposure·minimum-criterion decision |
| BUY | Filter·Guard·Sizing·Decision |
| SELL | Guard·Decision·Backtest compatibility |
| Block Watch | Block·Watch decision |
| Config | Strategy Default·Override·Snapshot |
| Version | Strategy·Engine Metadata |
| Utility | Pure conversion and Boundary Helper |

Common does not directly perform DB·HTTP·File IO·AWS·orders.

## 3. Root Documents

### `AGENTS.md`

| Item | Value |
|---|---|
| Responsibility | Common work·compatibility·purity·validation rules |
| Primary content | Public API, Context·Result, Enum·Reason, Config, Consumer |
| Usage timing | Before starting any Common code·documentation work |
| Change impact | The entire work scope and safety criteria |
| Caution | Does not replace the current structure or past change history |
| Update condition | When Public API·Consumer·purity·validation criteria change |

### `README.md`

| Item | Value |
|---|---|
| Responsibility | Describe the current Common structure and usage AS-IS |
| Primary content | Responsibility boundary, Consumer, decision flow, Config, safety |
| Usage timing | Understanding Common and confirming usage |
| Change impact | Consumer development and maintenance |
| Caution | Do not accumulate past change facts at length |
| Update condition | When the current file·API·Consumer·usage structure changes |

### `CHANGELOG.md`

| Item | Value |
|---|---|
| Responsibility | Preserve primary change facts by date |
| Primary content | Documentation·API·Config·strategy Rule·compatibility changes |
| Usage timing | Confirm change background and facts at the time |
| Change impact | Regression analysis and Consumer impact tracing |
| Caution | Do not repeat the current-state description |
| Update condition | When an actual primary change occurs |

### `docs/source-file-catalog.md`

| Item | Value |
|---|---|
| Responsibility | Per-file responsibility·Public API·Consumer impact map |
| Primary content | Context, Result, Types, Decision, Config, Utility |
| Usage timing | Confirm the modification target and related files |
| Change impact | Prevent missing impact scope |
| Caution | Do not list every trivial file unconditionally |
| Update condition | When file·responsibility·call·Export·Consumer change |

## 4. Package Export and Metadata

### `__init__.py`

| Item | Value |
|---|---|
| Responsibility | Package-level Metadata and Public Symbol Export |
| Input | Version·Metadata Symbols of the Common Module |
| Output | Consumer Package Import path |
| Side Effect | Must be absent |
| Public API | Export Symbol and Package Import Path |
| Consumer impact | `from port_strategy_common import ...` |
| Change risk | Import failure, Circular Import, Startup Side Effect |
| Confirmation target | The actual Export list and Consumer Import |
| Deletion·move | Prohibited unless all Consumers are modified together |

### `common_version.py`

| Item | Value |
|---|---|
| Responsibility | Provide Strategy·Engine Version Metadata |
| Input | Module constants |
| Output | Name·Version·Description·Metadata |
| Side Effect | Must be absent |
| Public API | Metadata Key and string format |
| Consumer impact | Identifying Backtest·Daily·Execution results |
| Change risk | Storing different strategy results under the same Version |
| Confirmation target | Whether Consumers store·Report it |
| Update basis | Linked to an actual strategy Rule·Config result change |

## 5. Context Contract

### `common_context.py`

| Item | Value |
|---|---|
| Responsibility | Define the Common input Context Dataclass |
| Primary structure | Market·Stock·Position Context |
| Input | Explicit values converted by the Consumer Adapter |
| Output | Common decision function input objects |
| Mutability | Confirm whether Frozen in the actual code |
| Public API | Class·Field·order·Type·Default·Optional |
| Consumer impact | Keyword·Positional construction and Serialization |
| Change risk | Consumer construction failure, unit·date meaning mismatch |
| Confirmation target | Use of `asdict`, JSON, DB Payload conversion |
| Purity | Prohibit data lookup·normalization·current-time use |

A Context is not a Consumer DB Row itself.

Per-Consumer Row and Feature conversion is the responsibility of the Consumer Adapter.

## 6. Result Contract

### `common_result.py`

| Item | Value |
|---|---|
| Responsibility | Define the common decision Result Dataclass |
| Primary structure | Market·Filter·Guard·Sizing·BUY·SELL Result |
| Input | Computation results of the decision stages |
| Output | Objects for Consumer branching·storage·display |
| Public API | Class·Field·Type·Default·Detail structure |
| Consumer impact | Attribute access, `asdict`, JSON, DB storage |
| Change risk | Branching failure, Result Serialization change |
| Confirmation target | Mutable Default and `default_factory` |
| Caution | Keep the meaning of `None`, 0, and Empty values |

In Result, distinguish machine-processing values from diagnostic Detail.

| Category | Use |
|---|---|
| Signal·Status | Consumer branching |
| Reason | Storage·aggregation·display |
| Numeric | Exposure·Weight·Amount·Quantity |
| Guard Flag | Risk limit |
| Detail | Diagnostic information |

## 7. Enum and Status Contract

### `common_types.py`

| Item | Value |
|---|---|
| Responsibility | Define Common Enums and status strings |
| Primary types | Market·Trade·Order·Decision·Position·Execution |
| Input | Code constant definitions |
| Output | Consumer comparison·storage·serialization values |
| Public API | Enum Class·Member·Value |
| Consumer impact | DB, Report, View, Execution branching |
| Change risk | String mismatch and status interpretation error |
| Confirmation target | Value case, Alias, Serialization |
| Caution | Do not add an Enum that is not in the code for documentation convenience |

Both the Enum Member name and Value have compatibility impact.

## 8. Config Contract

### `config.py`

| Item | Value |
|---|---|
| Responsibility | Provide the Strategy Default Config and Runtime Snapshot |
| Primary areas | Market·Filter·Guard·Sizing·BUY·SELL·Report |
| Input | Default and Optional Override |
| Output | Runtime Config and Snapshot Dictionary |
| Side Effect | Must have no Global Config Mutation |
| Public API | Key·Nested structure·Default·Type·unit |
| Consumer impact | Threshold·Rule·Sizing·Report results |
| Change risk | Strategy result change for all Consumers |
| Confirmation target | Copy·Deep Copy·Merge·Unknown Key handling |
| Security | Prohibit including Secret and Persistence Settings |

Do not Rename·Remove a Config Key unless all Consumers are modified together.

Even if a Caller modifies the returned Snapshot object, the original Config must not change.

## 9. Common Utility

### `common_utils.py`

| Item | Value |
|---|---|
| Responsibility | Common safe conversion and Boundary Helper |
| Primary functions | Null check, Float·Int·String·Boolean conversion, Clamp, Config lookup |
| Input | Primitive or Config values |
| Output | Converted values and Fallback |
| Side Effect | Must be absent |
| Public API | Function name·Fallback·exception handling |
| Consumer impact | Input defense of all decision Modules |
| Change risk | Change in the meaning of Missing·NaN·False·0 |
| Confirmation target | Pandas Optional use and Fallback |
| Caution | Does not modify the input object |

Confirm that it keeps a safe Fallback even when Pandas is absent or `pd.isna` fails.

### `utils.py`

| Item | Value |
|---|---|
| Responsibility | Legacy-compatible Helper |
| Primary function | `to_float` |
| Dependency | Uses pandas |
| Consumer | Research imports `to_float` directly |
| Current classification | Legacy preservation target |
| Public API | Module Path and function name |
| Change risk | Research Import failure |
| Confirmation target | Common internal·Consumer direct Import |
| Deletion basis | Consumer contract confirmation required before removal |

New code confirms the actual need and existing patterns, then prefers `common_utils.py`.

## 10. Market Decision

### `common_market.py`

| Item | Value |
|---|---|
| Responsibility | Convert a Market Context into a market decision result |
| Input | Regime·Breadth·Flow·Macro-related values |
| Output | Signal·Exposure·Max Positions·Minimum Score·Reason |
| Side Effect | Must be absent |
| Public API | Public function Signature and Result |
| Consumer impact | BUY allowance·Sizing·candidate criteria |
| Change risk | Change in Market Signal and Portfolio Exposure |
| Confirmation target | Threshold Boundary and Downgrade order |
| Numeric safety | None·NaN·Inf·negative·0 handling |

The Reason and Signal priority affect Backtest·Daily equivalence.

## 11. BUY Filter

### `common_buy_filter.py`

| Item | Value |
|---|---|
| Responsibility | BUY candidate base conditions and candidate sort·selection Helper |
| Input | Stock Context or convertible candidate values |
| Output | Filter Result and candidate list |
| Primary conditions | Score·Flow·Volatility·Intraday Range, etc. |
| Side Effect | Must be absent |
| Public API | Function·Sort Key·Filter Reason |
| Consumer impact | BUY candidate pass and priority |
| Change risk | Change in candidate count·order·Reason |
| Confirmation target | Context conversion, Strong·Normal classification, Cut criterion |
| Caution | Do not mix the Filter and Sizing responsibilities |

If this file converts a Dict·Object into a `CommonStockContext`,
confirm whether that behavior overlaps with the Consumer Adapter.

For candidate sorting, confirm the Tie-breaker for equal scores and input-order stability.

## 12. BUY Guard

### `common_buy_guard.py`

| Item | Value |
|---|---|
| Responsibility | Judge BUY Risk Flag and Haircut |
| Input | Market·Stock·Position·Config |
| Output | Guard Result, Flag, Reason, Detail |
| Primary conditions | Hot Chase·Stop Risk·Flow·Range·Soft Risk |
| Side Effect | Must be absent |
| Public API | Flag Name·Reason·Result Field |
| Consumer impact | Sizing Haircut and diagnostic Payload |
| Change risk | Change in BUY quantity and Risk display |
| Confirmation target | Flag priority and duplicate conditions |
| Caution | Distinguish BUY blocking and Haircut meaning in the actual code |

Confirm whether the Flag name is linked to the Consumer storage Payload.

## 13. BUY Sizing

### `common_buy_sizing.py`

| Item | Value |
|---|---|
| Responsibility | Single-stock Sizing and Backtest Allocation |
| Input | Cash·Score·Volatility·Guard Flag·Price·Config |
| Output | Weight·Amount·Quantity or Position Size |
| Calculation | Confirm the Float·Decimal use scope in the actual code |
| Side Effect | Must be absent |
| Public API | Function Signature·Return·Sort Key |
| Consumer impact | Order candidate amount and Backtest Position |
| Change risk | Change in strategy performance and actual candidate scale |
| Confirmation target | Haircut order, Cap, Minimum, Rounding |
| Determinism | Same Allocation order for the same candidate list |

Do not assume Daily·Execution single-stock Sizing and Backtest candidate Allocation
are the same computation.

When mixing Decimal and Float, confirm the conversion location and rounding basis.

## 14. BUY Decision

### `common_buy_decision.py`

| Item | Value |
|---|---|
| Responsibility | Final BUY·SKIP Orchestration |
| Input | Stock Context, Market Result, Cash, Config |
| Call | Filter·Guard·Sizing |
| Output | `CommonBuyDecision`-family Result |
| Side Effect | Must be absent |
| Public API | Call order, Signal, Reason, Detail |
| Consumer impact | Daily·Backtest final BUY result |
| Change risk | Change in Short-circuit and Reason priority |
| Confirmation target | Computation after failure, Detail Merge, Key conflict |
| Determinism | Same final result for the same input |

Confirm the actual Filter·Guard·Sizing call order in the code.

The sub-Results and the final Signal must not contradict each other.

## 15. SELL Guard

### `common_sell_guard.py`

| Item | Value |
|---|---|
| Responsibility | Compute SELL Risk Flag and Active Reason |
| Input | Position·Market·Stock Context and Config |
| Output | Guard Result, Flag, Reason, Detail |
| Primary conditions | Stop Loss·Profit Protect·Holding·Market Block·Flow·Score |
| Side Effect | Must be absent |
| Public API | Flag·Reason·Result Field |
| Consumer impact | Final SELL·HOLD decision |
| Change risk | Change in liquidation timing and Reason |
| Confirmation target | Condition priority, Missing Price, Holding Boundary |
| Caution | Separate responsibility from the final SELL·HOLD Orchestration |

The Guard does not modify the Position DB or create a SELL Order.

## 16. SELL Decision

### `common_sell_decision.py`

| Item | Value |
|---|---|
| Responsibility | Final SELL·HOLD and Backtest-compatible evaluation |
| Input | Position Context, Guard Result, Market·Stock Input |
| Output | `CommonSellDecision` and a Backtest-compatible Dictionary |
| Side Effect | Must be absent |
| Public API | Function Signature·Return Key·Reason |
| Consumer impact | Daily Position Decision and Backtest Exit |
| Change risk | Change in SELL timing·performance·storage Payload |
| Confirmation target | Reason priority and comparison operators |
| Special contract | `common_evaluate_backtest_sell` compatibility behavior |

When changing `common_evaluate_backtest_sell`, confirm the following.

- Parameter names and Default
- Return Dictionary Key
- Sell Reason strings
- Price comparison operators
- Holding Days
- Daily vs Backtest Adapter differences
- Look-ahead possibility

## 17. Block Watch

### `common_block_watch.py`

| Item | Value |
|---|---|
| Responsibility | Judge Watch candidates during a Market Block window |
| Input | Stock Context or compatible candidate values |
| Output | Whether Watch and the failure Reason |
| Side Effect | Must be absent |
| Public API | Function Signature·Reason·Return structure |
| Consumer impact | Daily Watch storage or diagnostics |
| Change risk | Change in the candidate scope during a Block window |
| Confirmation target | Score Field, Dict·Object handling, Threshold |
| Caution | Does not auto-promote to an actual BUY Signal or performance calculation |

Block and Watch are not the same state.

Confirm in the Consumer whether Watch is monitoring·penalizing·conditional allowance.

## 18. Public API Map

### 18.1 Functions

| File | Primary Public API |
|---|---|
| `common_market.py` | Market Decision function |
| `common_buy_filter.py` | BUY Filter·sort·selection Helper |
| `common_buy_guard.py` | BUY Guard |
| `common_buy_sizing.py` | BUY Sizing·Allocation |
| `common_buy_decision.py` | Final BUY Decision |
| `common_sell_guard.py` | SELL Guard |
| `common_sell_decision.py` | SELL Decision·Backtest evaluation |
| `common_block_watch.py` | Block Watch |
| `config.py` | Runtime Config·Snapshot |
| `common_version.py` | Metadata lookup |

Confirm the actual function names and Signatures in the source and Consumer Imports.

### 18.2 Data Structures

| File | Contract |
|---|---|
| `common_context.py` | Input Dataclass |
| `common_result.py` | Result Dataclass |
| `common_types.py` | Enum Value |
| `config.py` | Config Key and Nested structure |
| `common_version.py` | Metadata Key |
| `__init__.py` | Package Export |

## 19. Consumer Impact Map

### StrategyResearch

| Common file | Primary impact |
|---|---|
| Market | Backtest Market Regime |
| BUY Guard | Risk Flag and Haircut |
| BUY Sizing | Position Allocation |
| SELL Decision | Exit decision |
| Config | Backtest Rule |
| Version | Run Metadata |

### StrategyDecision

| Common file | Primary impact |
|---|---|
| Market | Daily Market Decision |
| BUY Filter | Candidate pass |
| BUY Guard | Risk limit |
| BUY Sizing | Target Weight·Amount |
| BUY Decision | Daily BUY·SKIP |
| SELL Decision | Position SELL·HOLD |
| Block Watch | Block-window Watch |
| Context·Result | Adapter and storage Payload |

### StrategyExecution

| Item | Value |
|---|---|
| Current state | No direct `port_strategy_common` Import |
| Source basis | Only a comment about Common Config non-use |
| Design purpose | Signal·Status·Mode meaning alignment target |
| Promotion condition | Record as a direct Consumer once a direct Import is added in the future |

Execution is not currently a direct Consumer and is not a Consumer Contract Test target.

### Other MS

| Item | Value |
|---|---|
| View·Crawler·Preprocessor·MarketConnector | No direct Import evidence |

Do not finalize items without confirmed actual Import as direct Consumer contracts.

## 20. Purity and Side Effect Map

| File group | Expected criterion |
|---|---|
| Context·Result·Types | Provide definitions only |
| Market·Filter·Guard | Perform input decisions only |
| Sizing | Perform numeric computation only |
| Decision | Orchestrate sub-decisions |
| Config | Copy·Override·Snapshot |
| Version | Return Metadata |
| Utility | Conversion and Boundary Helper |
| Package Export | Perform Symbol Export only |

If any of the following is found in a Common strategy file, re-review the responsibility boundary.

- SQL or DB Client
- HTTP·Broker Client
- AWS SDK
- File Read·Write
- Direct environment variable lookup
- Direct current-time lookup
- Random without a Seed
- Global Mutable State change
- Execution on Import
- Secret or Runtime Credential

## 21. Determinism and Reproducibility Map

| Risk | Related file |
|---|---|
| Global Config Mutation | `config.py` |
| Dictionary Mutation | Config·Decision·Utility |
| Unstable Sort | BUY Filter·Sizing |
| Current Time | Block Watch·SELL Holding |
| Random | All decision Modules |
| Float Exact Compare | Market·Sizing·SELL |
| NaN Silent Pass | Utility·Filter·Guard |
| Timezone | Context·Block Watch·SELL |
| Look-ahead | SELL Decision·Research Adapter |

Calling the same input repeatedly must produce the same Result.

## 22. Numeric·Date Impact Map

### Numeric

| Area | Confirmation target |
|---|---|
| Market | Threshold Boundary |
| BUY Filter | Score·Volatility·Range |
| BUY Guard | Risk Flag·Haircut |
| BUY Sizing | Decimal·Float·Rounding·Cap |
| SELL Guard | Stop·Profit·Score breakdown |
| SELL Decision | Price comparison and Holding Boundary |
| Utility | None·NaN·Inf·Fallback |

### Date

| Area | Confirmation target |
|---|---|
| Context | Trade·Feature·Evaluation Date |
| Block Watch | Application period and release date |
| SELL Guard | Entry Date and Holding Days |
| SELL Decision | Price Date and Exit timing |
| Backtest Helper | Same-day price use and Look-ahead |
| Consumer Adapter | Calendar Date and trading-day conversion |

## 23. Change Impact Relationships

| Change target | Files to confirm together |
|---|---|
| Context Field | Result consumers, BUY·SELL functions, Consumer Adapter |
| Result Field | Decision Module, Consumer storage·Report |
| Enum Value | All Consumer comparison·storage |
| Reason | Filter·Guard·Decision, Consumer aggregation |
| Config Key | Config call sites and Consumer Override |
| Market Rule | BUY Filter·Sizing·Decision |
| BUY Filter | BUY Decision and Candidate Sort |
| BUY Guard | BUY Sizing and BUY Decision |
| BUY Sizing | BUY Decision and Research Allocation |
| SELL Guard | SELL Decision and Backtest Helper |
| SELL Decision | Research·Decision Consumer |
| Block Watch | BUY Filter and Decision Consumer |
| Version | Package Export and Consumer Metadata |
| Package Export | All Package-level Imports |
| Utility | All calling Modules |
| Legacy file | Common and Consumer Import |
| File creation·deletion | README and Source Catalog |
| Public API change | AGENTS·README·CHANGELOG·Catalog |

## 24. Legacy and Deletion Judgment

Before cleaning up or deleting a file, confirm the following.

| Item | Confirmation content |
|---|---|
| Common Import | Root internal direct·dynamic Import |
| Consumer Import | Research·Decision·Execution |
| Export | `__init__.py` public Symbol |
| Test | Fixture·Monkeypatch·Import |
| Documentation | README·Catalog·examples |
| Git | Recent changes and the user's uncommitted work |
| Runtime | Installed Package and Deployment Copy |

If there is not enough evidence of non-use, do not delete; mark it only as a cleanup candidate.

Do not delete `utils.py` before confirming actual Consumer references.

## 25. AWS Operational Position

Common is not a standalone execution target.

| AWS component | Common position |
|---|---|
| ECS RunTask | Consumer Image Dependency |
| Lambda | Consumer Package Dependency |
| Step Functions | Not a direct Step |
| EventBridge | Not a direct Schedule |
| AWS Batch | Not a direct Job |

The Cluster, Task Definition, Image URI, Secret ARN, and Command ID are
managed in the Consumer operational documentation.

## 26. Sensitive Information

Do not add the following values to Common or record them in documentation.

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

Ensure no Secret is included in the Config Snapshot and Result Detail.

Use `[REDACTED]` or a generic Placeholder when needed.

## 27. Items Excluded from the Current Documentation

Date-specific `docs/worklog/*.md` files are excluded from the current file structure and Catalog list.

Past Worklog-creation facts are preserved only in `CHANGELOG.md`.
Do not create new Worklog files.

The following outputs are also excluded from the Catalog.

- `__pycache__/`
- `.pytest_cache/`
- `build/`
- `dist/`
- `*.egg-info/`
- IDE temporary files
- Coverage outputs
- One-time Log·Dump
- Secret verbatim files

## 28. Items Requiring Confirmation

| Item | Confirmation target |
|---|---|
| Public Function | Actual function name·Signature·Default |
| Context | Dataclass Field·order·Default·Frozen |
| Result | Field·Default·Detail structure |
| Enum | Member·Value·Alias |
| Reason | Actual strings and Consumer comparison |
| Config | Key·Default·Nested structure |
| Snapshot | Deep Copy·Override·Mutation |
| Export | `__init__.py` Public Symbol |
| Market | Threshold·Downgrade order |
| BUY Filter | Context conversion·Sort·Cut |
| BUY Guard | Flag meaning and Haircut |
| BUY Sizing | Decimal·Allocation·Rounding |
| BUY Decision | Actual call order and Detail Merge |
| SELL Guard | Flag·Reason priority |
| SELL Decision | SELL·HOLD and Backtest Return Key |
| Block Watch | Dict·Object input and Watch meaning |
| Determinism | Clock·Random·Global Mutation |
| Look-ahead | Price·Feature·Holding timing |
| Consumer | Research·Decision·Execution Import |
| Legacy | `utils.py` actual references |
| Tests | Test Runner and Consumer Contract Coverage |

Do not treat unconfirmed items as operational fact.

## 29. Catalog Update Conditions

When the following changes occur, confirm this document in the same task.

- File creation·deletion·Rename
- Public Function and Signature change
- Context·Result Dataclass change
- Enum Member·Value change
- Reason string change
- Config Key·Default·Nested structure change
- Snapshot·Override·Mutation policy change
- Package Export change
- Consumer Import and Adapter relationship change
- Market·BUY·SELL Rule change
- Filter·Guard·Sizing Orchestration change
- Block·Watch meaning change
- Version Metadata change
- Utility·Legacy classification change
- Purity or Import Side Effect change
- Test structure change
- Documentation structure and Worklog policy change

Do not mechanically update all unrelated files for a simple typo or description cleanup.

## 30. DevOps and Package Files

Organizes the responsibilities and change impact of Build·CI·deployment-related files.

Strategy decision logic is not included.

### `pyproject.toml`

| Item | Value |
|---|---|
| Responsibility | Package Metadata and Build definition |
| Package Name | `port-strategy-common` |
| Package Version | `1.0.1` |
| Version Source | Package Version Canonical Source |
| Python Version | `>=3.10` |
| Dependency declaration | Currently empty |
| Build Backend | setuptools |
| Change risk | Impact on Version·Package configuration and Wheel output |
| Confirmation target | Buildspec·verify_wheel·Public API tests follow this Version dynamically |

### `.github/workflows/common-codebuild.yml`

| Item | Value |
|---|---|
| Responsibility | GitHub OIDC authentication and CodeBuild start |
| Trigger | main Push + `workflow_dispatch` |
| main Push | Publish enabled |
| workflow_dispatch | Build-only |
| Execution | CodeBuild start·status wait·result judgment |
| Source SHA | Passes the Commit SHA as the Source Version |
| Change risk | Authentication boundary and Publish-enablement method |
| Confirmation target | No long-lived Access Key and Source SHA confirmation |

### `.devops/codebuild/buildspec.yml`

| Item | Value |
|---|---|
| Responsibility | Quality gates·Wheel Build·conditional Publish |
| Quality gates | Ruff, mypy, Wheel Build, Twine Check |
| Version Resolve | Derive the Package Version from `pyproject.toml` |
| Wheel validation | `verify_wheel.py` and Public API tests after installation |
| Build Failure Gate | Block Publish on a Build failure |
| Version Guard | Block Publish if the same Version exists |
| Publish | Conditional · CodeBuild default `false` |
| Change risk | Gate bypass and treating failure as success |
| Confirmation target | `PUBLISH_TO_CODEARTIFACT` default and Wheel path confirmation |

### `.devops/scripts/verify_wheel.py`

| Item | Value |
|---|---|
| Responsibility | Validate the Wheel name and internal structure |
| Wheel name | Dynamic validation based on the `pyproject.toml` Package Version |
| Required Member | Confirm inclusion of primary public Modules |
| Prohibited path | Exclude `__pycache__`·`.pyc`·`.git`·`docs` |
| Integrity | Output SHA-256 and Member count |
| Change risk | Mismatch between `pyproject.toml` and the Wheel output |
| Confirmation target | Follows `pyproject.toml` dynamically without hardcoding the Version |

### `tests/test_public_contract.py`

| Item | Value |
|---|---|
| Responsibility | Validate the Public API against the installed Wheel |
| Distribution Name | Confirm `port-strategy-common` |
| Package Version | Dynamic comparison with `pyproject.toml` |
| Strategy Version | Confirm `COMMON_STRATEGY_V1.0.0` |
| Public Symbols | Confirm import of 6 public Symbols |
| Installation source | Confirm installation in `site-packages` |
| Change risk | Mistaking a Repository Source Import for distribution validation |
| Confirmation target | Version·Symbol·installation-source alignment |

## 31. Related Documents

- [AGENTS.md](../AGENTS.md)
- [README.md](../README.md)
- [CHANGELOG.md](../CHANGELOG.md)

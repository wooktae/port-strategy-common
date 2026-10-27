# CHANGELOG

Records the primary change history of `port_strategy_common`.

Confirm the current structure and usage against `README.md`, the work rules against `AGENTS.md`,
and per-file responsibilities and impact against `docs/source-file-catalog.md`.

## 2026-08-12

### Completed Common main Push automatic Package Release

| Item | Value |
|---|---|
| Package Version | `1.0.1` |
| Work nature | Package Release automation improvement |
| Trigger | main Push automatic + `workflow_dispatch` retained |
| main Push | CodeArtifact Publish enabled |
| workflow_dispatch | Build-only |
| Canonical Version Source | `pyproject.toml` |
| Registry | AWS CodeArtifact |
| Strategy Version | `COMMON_STRATEGY_V1.0.0` retained |
| Strategy Rule·Config·API·Dataclass·Enum·Reason | No change |
| Consumer Repository | No change |

### Implementation Changes

| Item | Value |
|---|---|
| Package Version | `1.0.0` → `1.0.1` |
| `verify_wheel.py` | Removed Version hardcoding · dynamic validation from `pyproject.toml` |
| Public API test | Removed Package Version hardcoding · dynamic comparison with `pyproject.toml` |
| Version Guard | Added Publish block when the same Version exists |
| Build Gate | Block Publish on a Build failure |
| CodeBuild default Publish | `false` safeguard retained |
| Authentication·permission alignment | Complemented to run the automatic Release |

### Publish After-check

| Item | Result |
|---|---|
| main Push Workflow | Automatic run succeeded |
| GitHub Actions → CodeBuild | Succeeded |
| CodeBuild | SUCCEEDED |
| CodeArtifact Publish | Confirmed `1.0.1` INTERNAL Package Published |
| Wheel Asset | Confirmed `port_strategy_common-1.0.1-py3-none-any.whl` exists |

Detailed DevOps Architecture, IAM responsibility boundaries, OIDC Trust, and operational evidence are managed by port-devops.

## 2026-07-30

### Common DevOps and Version Package deployment configuration

| Item | Value |
|---|---|
| Change scope | DevOps configuration files and documentation |
| Work nature | Versioned Python Package Build·deployment configuration |
| Package Version | `1.0.0` |
| Strategy Version | `COMMON_STRATEGY_V1.0.0` |
| Artifact | Python Wheel |
| CI | GitHub Actions → AWS CodeBuild |
| Registry | AWS CodeArtifact |
| Consumer Contract | Research 48/48, Decision 24/24 |
| Release promotion | `1.0.0rc1` → `1.0.0` Publish |
| Rollback | Reinstall pinned to the previously published Version |
| Strategy decision change | None |
| Config change | None |
| Public function change | None |
| Dataclass·Enum·Reason change | None |
| DB·API·order execution | None |

There is no change to the strategy decision logic, Config, public functions, Dataclasses, Enums, and Reasons.

### CI and Wheel Build

| File | Role |
|---|---|
| `pyproject.toml` | Declares Package Metadata·Version·Dependency |
| `.github/workflows/common-codebuild.yml` | OIDC authentication and CodeBuild start·wait |
| `.devops/codebuild/buildspec.yml` | Quality gates·Wheel Build·conditional Publish |
| `.devops/scripts/verify_wheel.py` | Wheel name·required Member·SHA-256 validation |
| `tests/test_public_contract.py` | Public API test against the installed Wheel |

The quality gates are Ruff, mypy (`.devops/scripts` scope), Wheel Build,
Twine Check, Wheel structure validation, and 4 Public API tests.

### CodeArtifact Deployment

| Item | Value |
|---|---|
| RC Publish | `1.0.0rc1` deployed to CodeArtifact |
| RC validation | 4 installed-Wheel Public API tests passed |
| Release Publish | `1.0.0` deployed to CodeArtifact |
| Version preservation | RC and release Versions preserved simultaneously |
| Default Publish | Project default `false` |
| Release Publish | One-time Override only in an approved Release Build |

### Consumer Contract

| Consumer | Result |
|---|---|
| StrategyResearch | 48 passed |
| StrategyDecision | 24 passed |
| StrategyExecution | No direct Import · Not a target |
| Legacy `utils.to_float` | Research imports it directly · pandas required |
| pandas provision | Research's own Runtime Dependency |

### Release Promotion and Rollback

| Item | Value |
|---|---|
| Release installation validation | Validated after installing the `1.0.0` Wheel |
| Public Symbols | 6 confirmed |
| Public API test | 4 passed |
| Rollback reinstall | Reinstalled pinned to `1.0.0rc1` Version |
| Rollback validation | 4 Public API tests re-passed |
| Git Repository | No change |
| Method | Version Pin reinstall |

### Work Boundary

| Item | Result |
|---|---|
| Strategy Python logic change | None |
| DB DDL·DML | None |
| External API call | None |
| Order execution | None |
| Consumer Repository modification | None |
| Sensitive information in documentation | None |
| Deployment Slack notification linkage | None |

## 2026-07-23

### Common documentation baseline reorganization

| Item | Change content |
|---|---|
| Change scope | Baseline reorganization of `AGENTS.md`, `README.md`, `CHANGELOG.md`, `docs/source-file-catalog.md` documents |
| Work nature | Documentation improvement based on the current Common responsibilities and Public API |
| Functional change | None |
| Python code change | None |
| Config change | None |
| Enum change | None |
| Dataclass change | None |
| Reason change | None |
| Consumer change | None |
| Version change | None |
| External execution | None |

### AGENTS.md

| Item | Change content |
|---|---|
| Documentation readability | Added 2-column tables, long-cell splitting, and the 500-character line limit as highest-priority rules |
| Rule priority | Organized the relationship among user instructions, Workspace-common rules, and Common-specific rules |
| Project role | Clarified Common as a shared strategy Library rather than a standalone MS |
| Responsibility boundary | Separated roles from Research·Decision·Execution·MarketConnector |
| Consumer relationships | Added the Consumer Adapter and Common Context boundary |
| Work scope | Modify only the Common Root and limit Consumer repositories to read-only |
| Execution safety | Strengthened the prohibition on DB·API·AWS·order·File Write·Side Effect execution |
| Purity | Prohibit DB·HTTP·File IO·environment variables·Clock·Random·Global Mutation |
| Public API | Added Module·function·Parameter·Return·Export compatibility criteria |
| Context contract | Added Field·order·Default·Optional·unit·date·Serialization criteria |
| Result contract | Added Signal·Status·Reason·Numeric·Detail roles and Default criteria |
| Enum contract | Added Member·Value·case·serialization compatibility criteria |
| Reason contract | Added DB·Report·Slack·View·Test string impact |
| Config contract | Added Key·Default·unit·Override·Snapshot compatibility criteria |
| Config Mutation | Added Deep Copy·original preservation·call-order independence criteria |
| Market contract | Added Regime·Exposure·Threshold Boundary confirmation criteria |
| BUY contract | Separated Filter·Guard·Sizing·Decision responsibilities and Orchestration |
| SELL contract | Added Guard·Decision·Backtest-compatible evaluation criteria |
| Block Watch | Separated Block·Watch·release condition·date meaning |
| Determinism | Added the criterion of keeping the same result for the same input and Config |
| Look-ahead | Added Feature·Price·Trade Date and Holding Days safety criteria |
| Numeric safety | Added Float·Decimal·NaN·Inf·Rounding·unit criteria |
| Import contract | Added Package Export·Circular Import·Import Side Effect criteria |
| Version | Added the relationship between strategy result change and Version Metadata |
| Legacy | Prohibit deleting `utils.py` and similar before confirming actual references |
| Testing | Added Context·Enum·Config·Boundary·Consumer Contract validation criteria |
| Change classification | Distinguished documentation·refactoring·strategy change·Breaking Change |
| Documentation system | Separated AGENTS·README·CHANGELOG·Source Catalog roles |
| Worklog | Prohibited creating new date-specific Worklogs |
| Completion report | Added the criterion to report Public API·Consumer impact·whether strategy results changed |

### README.md

| Item | Change content |
|---|---|
| Service summary | Added input·output·Consumer·execution form·purity principles |
| Responsibility boundary | Separated the Common decision contract from the Consumer Persistence responsibility |
| Consumer structure | Added the Adapter → Context → Common → Result flow |
| Research | Distinguished Backtest decision reuse from the Look-ahead responsibility |
| Decision | Distinguished the Daily Adapter from the Persistence responsibility |
| Execution | Limited the actual Import scope to a code-confirmation target |
| Other MS | Organized to avoid concluding a Consumer without Import evidence |
| Pure functions | Explicitly stated the prohibition on DB·HTTP·File IO·Clock·Random·Global Mutation |
| Determinism | Added the principle of the same result for the same input·Config |
| Public API | Added the function·Field·Enum·Reason·Config·Export contract |
| Context | Added Field·Type·Default·Optional·unit·date criteria |
| Result | Separated the Signal·Status·Reason·Numeric·Detail roles |
| Enum | Organized to confirm the actual Class·Value in the code |
| Reason | Added storage·aggregation·display·Test impact |
| Config | Organized the impact of Threshold·Default·Weight·Key changes |
| Snapshot | Added Copy·Mutation·Override·Secret-exclusion criteria |
| Market | Added Regime·Exposure·Boundary confirmation criteria |
| BUY flow | Added the Filter → Guard → Sizing → Decision structure |
| SELL flow | Added the Guard → SELL·HOLD and Backtest compatibility structure |
| Block Watch | Separated the Block·Watch·Release meaning |
| Numeric safety | Added Float·Decimal·NaN·Inf·unit·Rounding criteria |
| Date safety | Added Trade·Feature·Price Date and Look-ahead criteria |
| Package | Separated the responsibilities of `__init__.py`, `common_utils.py`, and `utils.py` |
| Version | Added the relationship between result change and Metadata update |
| File structure | Reflected the current Root and `docs/source-file-catalog.md` structure |
| Worklog | Removed from the current file structure and reflected the prohibition on new creation |
| AWS | Clarified as a Consumer Dependency rather than a standalone execution target |
| Security | Added Secret exclusion from the Config Snapshot and Detail Payload |
| Validation | Separated the validation scope of documentation changes and code changes |
| Change impact | Added the documentation·refactoring·strategy result·Breaking Change classification |
| Confirmation items | Separated unconfirmed matters such as Public API·Consumer Import·Config·Determinism |

### CHANGELOG.md

| Item | Change content |
|---|---|
| Structure | Reorganized long-form Bullets and repeated Notes into per-date 2-column change summaries |
| Latest history | Added the 2026-07-23 Common documentation baseline reorganization entry |
| Change boundary | Separated documentation changes from code·Config·Enum·Dataclass changes |
| Past history | Preserved actual change facts from 2026-05-26 to 2026-07-01 |
| Language | Organized the 2026-05-28 English change sentences into Korean factual sentences |
| Worklog | Preserved past creation facts and distinguished them from the current no-new-creation policy |
| Sensitive information | Maintained the principle of not recording Credentials and AWS operational identifiers verbatim |

### docs/source-file-catalog.md

| Item | Change content |
|---|---|
| Structure | Reorganized the file description list into a responsibility·Public API·Consumer impact structure |
| Contract separation | Separated the responsibilities of the Context·Result·Enum·Config·Decision files |
| Consumer impact | Added the Research·Decision·Execution impact map |
| Purity | Added the purity and Import Side Effect map |
| Determinism | Added the determinism and reproducibility risk map |
| Numeric·date | Added the numeric·date·Look-ahead impact map |
| Change relationships | Added the file change impact relationship table |
| Worklog | Removed the Worklog from the current file structure and Catalog list |
| Update conditions | Added update conditions for Public API·Field·Enum·Reason·Config·Consumer changes |

### Public API Reinforcement

| Contract | Reinforcement content |
|---|---|
| Function | Treated public function names·Parameters·Return Types as Consumer contracts |
| Context | Classified Dataclass Field and Default changes as compatibility impact |
| Result | Added the criterion of keeping the Signal·Status·Reason·Detail structure |
| Enum | Treated Member and Value strings as an external contract |
| Reason | Stated that wording fixes may affect aggregation·View·Slack·Test |
| Config | Classified Key·Default·Threshold changes as strategy result impact |
| Export | Added the risk of `__init__.py` public Symbol changes |
| Version | Added the criterion for judging strategy Rule change and Metadata update |

### Purity and Reproducibility Reinforcement

| Item | Criterion |
|---|---|
| DB | Not accessed in Common strategy Modules |
| HTTP·API | Prohibit external Client calls |
| File IO | Prohibit reading·writing inside decision functions |
| Environment | Prohibit direct environment variable lookup inside functions |
| Clock | Prohibit direct use of the current time |
| Random | Prohibit random numbers without a Seed |
| Global State | Prohibit changing Mutable Global |
| Config | Caller Mutation does not affect the original |
| Determinism | Same result for the same input·Config |
| Look-ahead | Prohibit referencing future Feature·Price |

### Work Boundary

| Item | Result |
|---|---|
| Python execution | Not performed |
| Import Test | Not performed |
| Consumer execution | Not performed |
| Backtest·Daily execution | Not performed |
| DB DDL·DML | Not performed |
| External API·Crawler | Not performed |
| Order·Broker call | Not performed |
| AWS CLI·SDK | Not performed |
| Sensitive information query·recording | Not performed |
| Documentation static review | Performed |

## 2026-07-01

### Common operational documentation reinforcement

| Item | Change content |
|---|---|
| README | Added the Common responsibility boundary and Consumer dependencies |
| AWS | Stated its Dependency nature rather than as a directly executing MS |
| Compatibility | Added the criterion of keeping public functions·Dataclasses·Enums·Reasons·Config Keys |
| AGENTS | Organized the Worklog indentation format of the time to the ` 1)` basis |
| Status notation | Unified the Worklog status of the time to the `작업 명:완료` format |

### Documents Added at the Time

| Item | Change content |
|---|---|
| Worklog | Created `docs/worklog/2026-07-01.md` |
| Current policy | Preserve past creation facts but do not create new Worklogs |

### Work Boundary at the Time

| Item | Result |
|---|---|
| Functional change | None |
| Python code change | None |
| Config Key change | None |
| Enum change | None |
| Dataclass Field change | None |
| Reason change | None |
| Python execution | Not performed |
| DB DDL·DML | Not performed |
| External API·Crawler | Not performed |
| Order execution | Not performed |
| Sensitive information recording | Not done |

### Responsibility Boundary at the Time

At the time, only content directly related to Common was documented.

| Excluded area | Owner |
|---|---|
| View screens·approval UI | port-view |
| Broker·KIS API | MarketConnector |
| Source data collection | Crawler |
| Feature generation | Preprocessor |
| Daily storage | StrategyDecision |
| Backtest·Report storage | StrategyResearch |
| Execution Plan·Order | StrategyExecution |
| Scheduler·Lambda·Step Functions | The relevant operational configuration |

## 2026-05-28

### Source and documentation cleanup

| Item | Change content |
|---|---|
| Source Catalog | Added `docs/source-file-catalog.md` for the first time |
| Module Docstring | Added Korean descriptions to primary Python files |
| DB Dependency | Removed the DB dependency of the Common Core |
| Runtime Config | Limited the Snapshot scope to strategy settings |
| README | Reflected the file Catalog and description-comment state |
| Worklog | Created `docs/worklog/2026-05-28.md` |

### Change Nature at the Time

| Item | Result |
|---|---|
| Common DB Dependency | Removed |
| Runtime Config scope | Limited to strategy settings |
| External execution | Not performed |
| DB DDL·DML | Not performed |
| External API·Crawler | Not performed |
| Order execution | Not performed |
| Sensitive information recording | Not done |

The DB Dependency removal on this date is an actual code·structure change history.
Confirm whether it matches the current implementation in the latest source.

## 2026-05-26

### Initial documentation

| Item | Change content |
|---|---|
| AGENTS | Added the initial `AGENTS.md` |
| README | Added the initial `README.md` |
| Worklog | Created `docs/worklog/2026-05-26.md` |

### Work Basis at the Time

| Item | Criterion |
|---|---|
| Documentation basis | Confirmed the local file structure of the time and some core Modules |
| Python execution | Not performed |
| DB DDL·DML | Not performed |
| External API·Crawler | Not performed |
| Order execution | Not performed |
| Sensitive information | Actual values not recorded |

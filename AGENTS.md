# AGENTS.md - port_strategy_common

## 1. Highest-Priority Documentation Readability Rules

These rules apply with priority to all Markdown documentation authoring and modification for `port_strategy_common`.

- New standalone summary tables use two columns by default.
- The default columns are `Item / Value`, and depending on context `File / Role`, `Contract / Criterion`, and `Consumer / Impact` may be used.
- When adding a row to an existing table, preserve its existing column structure.
- Keep table cells to no more than two sentences where possible.
- Do not place three or more facts in a long sentence within one cell.
- Split three or more facts into multiple rows or a link to a detailed document.
- New table cells do not exceed 300 characters.
- A single line does not exceed 500 characters.
- Do not paste long file lists, complete logs, complete test output, and complete configuration Dumps into the document body.
- Do not repeat the same fact at length across `README.md`, `CHANGELOG.md`, and `docs/source-file-catalog.md`.
- Do not mix the current state and past change history in one paragraph.
- Preserve code notation for file names, function names, Class names, Enums, Config Keys, and Signal and Reason strings.
- Save Korean Markdown as UTF-8 without BOM.
- Do not create tab characters and trailing whitespace.

## 2. Rule Priority

| Scope | Priority basis |
|---|---|
| User's latest explicit request | Highest work instruction |
| Workspace-common safety·work method | Latest rules in `.kiro/AGENTS.md` if present |
| Common responsibility·compatibility·purity contract | This `AGENTS.md` |
| Direct conflict | The more restrictive and safer rule |

- If `.kiro/AGENTS.md` is absent, use this file as the basis for Common work.
- When the user specifies the target files and scope, do not exceed that scope.
- If the implementation fact is unclear, do not execute or assume; report the static confirmation result and its limitations.
- Do not proceed with a change requiring modification of all Consumers as a Common-only task.

## 3. Project Role

`port_strategy_common` is the Python strategy contract and decision core shared by
StrategyResearch, StrategyDecision, and StrategyExecution.

| Area | Responsibility |
|---|---|
| Context | Market·Stock·Position input contract |
| Result | Market·Filter·Guard·Sizing·BUY·SELL result contract |
| Types | Signal·Side·Status·Position·Execution Mode Enum |
| Market | Market Regime and Exposure decision |
| BUY Filter | Judge buy eligibility conditions |
| BUY Guard | Buy Risk Guard |
| BUY Sizing | Compute target weight·amount·quantity |
| BUY Decision | Filter·Guard·Sizing result Orchestration |
| SELL Guard | Sell Risk Flag and Guard |
| SELL Decision | SELL·HOLD decision and Backtest-compatible evaluation |
| Block Watch | Common Block·Watch decision |
| Config | Strategy constants and Runtime Config Snapshot |
| Version | Strategy Name·Engine Version Metadata |

Common is not an execution service but a shared library that consuming MS import and use.

## 4. Responsibility Boundary

The scope Common owns directly is as follows.

- Context Dataclass
- Result Dataclass
- Enums and public constants
- Pure strategy decision functions
- Strategy Config Key and Snapshot
- Version Metadata
- Decision compatibility across Consumers
- Diagnostic Reason and Detail Payload contract

The scope Common does not own directly is as follows.

| Area | Owner |
|---|---|
| Source data collection | Crawler |
| Raw preprocessing and Feature generation | Preprocessor |
| Daily Signal DB storage | StrategyDecision |
| Daily Position Decision DB storage | StrategyDecision |
| Backtest Run·Trade·Report storage | StrategyResearch |
| Execution Plan·Order·Position storage | StrategyExecution |
| Broker·KIS API | MarketConnector |
| Approval UI and screens | port-view |
| Daily Orchestration | Scheduler·Step Functions |
| DB Connection·Persistence | Each consuming MS |

- Do not add a DB Helper, HTTP Client, File Persistence, or AWS execution code to Common.
- Do not pull another MS's Adapter and Persistence responsibilities into Common.
- Do not replicate Consumer internal operational details in the Common documentation.

## 5. Consumer Relationships

| Consumer | Common usage scope |
|---|---|
| StrategyResearch | Direct Import · Market·BUY·SELL·Sizing·Config·Version contract |
| StrategyDecision | Direct Import · Daily Market·Filter·Guard·Sizing·BUY·SELL·Block Watch |
| StrategyExecution | No direct Import currently · Contract alignment target by design |
| Other MS | Record only when direct Import evidence is confirmed |

- Judge whether something is a direct Consumer by actual `port_strategy_common` Import.
- The current direct Consumers are Research and Decision.
- Execution currently has no direct Import and only has a comment that it does not use Common Config directly.
- Promote Execution to a Consumer once a Common Import is added in the future.
- Do not assume View·Crawler·Preprocessor·MarketConnector are Common Consumers.
- Per-Consumer input conversion is the responsibility of each Consumer Adapter.
- Do not make a Common function receive a specific Consumer DB Row structure directly.

## 6. Work Scope

- The default work scope is the `port_strategy_common` root and its subordinate files.
- Files outside the root are used only as read-only for confirming Consumer impact.
- Do not modify Consumer repository files without a user request.
- For a documentation work request, modify only the target Markdown files.
- For a code work request, modify only the specified Common Python·configuration·test files.
- Do not create a full repository scan, Sub-agent, Orchestrator, or new Scanner.
- Do not create nonexistent APIs, Tests, Consumers, or Config Keys for documentation convenience.
- Do not treat Generated Output, Cache, Dump, and temporary files as operational sources.

## 7. Static Confirmation Before Starting Work

Before modifying, confirm in the necessary scope in the following order.

1. User-specified target files
2. This `AGENTS.md`
3. The target Common Module
4. The Context·Result·Types·Config that the target Module imports
5. The Consumers that import the target public functions
6. Related tests
7. README·CHANGELOG·Source Catalog if affected by documentation changes

During static confirmation, distinguish the following.

| Category | Judgment basis |
|---|---|
| Current implementation | Confirmed directly in the actual code |
| Public API | Confirmed by Consumer Import and call method |
| Design principle | Rules stated in AGENTS and the current documents |
| Unverified | Content lacking evidence |
| No assumptions | Do not conclude Consumer·compatibility·Legacy status by name alone |

## 8. Execution Safety

Common is a pure library in principle, but do not run a Module before confirming its safety.

Do not perform the following without the user's approval.

- External API calls
- DB connection and DDL·DML
- File Write
- AWS CLI·SDK calls
- ECS·Lambda·Batch·Step Functions execution
- Order submission and Broker calls
- Crawling
- Git Commit·Push·Reset·Restore·Checkout
- Query or output of sensitive information

- First read to confirm there is no Side Effect on Import.
- Do not run a file that has `if __name__ == "__main__":`.
- Do not judge `utils.py` and Helpers as safe by name alone.
- For documentation work, do not perform Python execution and Import Tests by default.

## 9. Common Purity Contract

The `common_*` strategy Modules are kept centered on pure functions.

| Prohibited dependency | Criterion |
|---|---|
| DB | Prohibit Connection, Cursor, SQL, ORM |
| HTTP·API | Prohibit Requests, SDK, Broker Client |
| File IO | Prohibit reading·writing Config·Result files |
| Environment | Prohibit direct environment variable lookup inside decision functions |
| Clock | Prohibit direct current-time lookup inside functions |
| Random | Prohibit random numbers without a Seed |
| Global Mutation | Prohibit changing Module Global state |
| Logging Side Effect | Prohibit full output of a sensitive Payload |

The allowed inputs are explicit Arguments, a Context Dataclass, and a Config Dictionary.

The same input and the same Config must return the same result.

## 10. Public API Compatibility Contract

The following items are treated as Public API.

- Public Module paths
- Public function names
- Function Parameter names and order
- Default values
- Return Type
- Context Dataclass name and Fields
- Result Dataclass name and Fields
- Enum Class and Value
- Decision Reason strings
- Detail Dictionary Keys
- Config Dictionary Keys
- Version Metadata Keys
- Package Export

Before changing, confirm the following.

| Item | Confirmation target |
|---|---|
| Import | Consumer direct Import |
| Call | Positional·Keyword Argument |
| Return | Attribute access and Serialization |
| Enum | DB·Report·Slack·View string use |
| Reason | Comparison·aggregation·display logic |
| Config | Consumer Override and Snapshot |
| Export | `__init__.py` public Symbol |

Do not make a Breaking Change unless all Consumers are modified and validated together.

## 11. Context Dataclass Contract

When changing `common_context.py`, confirm the following.

- Class name
- Field name
- Field order
- Type Annotation
- Default value
- Whether Optional
- Unit
- Date representation
- Consumer construction method
- Use of `asdict` or Serialization
- Whether Frozen
- Backward compatibility of added Fields

A Context is not a Consumer DB Row itself.

- Do not force DB Column names as-is.
- The Consumer Adapter converts DB·Feature Rows into a Context.
- Do not perform data lookup or normalization inside a Context.
- Do not add duplicate date Fields with the same meaning.
- Clarify the units of price·quantity·ratio in documentation and tests.

## 12. Result Dataclass Contract

When changing `common_result.py`, confirm the following.

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
- Default value
- Serialization form

Result distinguishes machine-processing values from diagnostic information.

| Category | Use |
|---|---|
| Signal·Status | Consumer branching and storage |
| Reason | Aggregation·Report·Slack·View display |
| Numeric Result | Sizing·Execution candidate input |
| Detail | Diagnostics and explanation |

- When promoting a value that existed only in the Detail Dictionary to a public Field, confirm Consumer impact.
- Do not move an existing Field into Detail.
- Do not arbitrarily change the meaning of `None`, 0, and an Empty Dictionary.
- Use `default_factory` for a Mutable Default.

## 13. Enum and String Contract

The Enums and strings in `common_types.py` are treated as an external contract.

| Contract | Risk |
|---|---|
| Market Signal | Change in market exposure and BUY allowance |
| Trade Signal | Change in BUY·SELL·HOLD·SKIP branching |
| Order Side | Execution linkage error |
| Decision Status | DB·Report aggregation error |
| Position Status | Position status interpretation error |
| Execution Mode | Paper·Live boundary error |

- Do not arbitrarily change the case and string of an Enum Value.
- An Enum Member name change can also affect Consumer Imports.
- For an added Alias, confirm Serialization and comparison results.
- When changing a string comparison to an Enum comparison, confirm all Consumers.
- Do not add an Enum that is not in the code for documentation convenience.

## 14. Decision Reason Contract

A Decision Reason may be a Consumer contract rather than a mere descriptive phrase.

When changing it, confirm the following.

- Consumer string comparison
- Report aggregation
- Slack phrasing
- View display
- DB storage and analysis Query
- Test Fixture
- Backtest vs Daily result comparison

- Do not change an existing Reason for wording cleanup.
- Confirm Consumer comparison even for a typo fix.
- When adding a new Reason, clarify the occurrence condition and priority.
- Ensure a Reason does not change nondeterministically under the same conditions.
- If a Human-readable explanation is needed, prefer a separate Detail Field.

## 15. Config Contract

When changing `config.py` and the Runtime Config, confirm the following.

- Config Key name
- Default value
- Unit
- Type
- Nested structure
- Override Merge method
- Unknown Key handling
- Snapshot result
- Link with Version
- Per-Consumer Override use

Treat a Config change as a strategy result change.

| Change | Confirmation criterion |
|---|---|
| Threshold | Boundary result and signal change |
| Weight | Exposure·Sizing result |
| Max Positions | Portfolio limit |
| Minimum Score | Number of BUY candidates |
| Sell Rule | HOLD·SELL transition |
| Report Config | Consumer output impact |
| Default | All Consumers without an Override |

Do not Rename·Remove a Config Key unless all Consumers are modified together.

## 16. Config Snapshot and Mutation

If `get_runtime_config()` and `get_config_snapshot()` families exist, confirm the following.

- Whether the returned object is a new Copy
- Whether a Nested Dictionary is a Deep Copy
- Whether Caller Mutation affects the Global Config
- Whether an Override changes the original Config
- Whether any Consumer depends on the Snapshot Key order
- Whether it includes only Serializable values

- Do not return a Shared Mutable Dictionary as-is.
- A Config Merge does not change the input Dictionary.
- Tests must not produce different results depending on call order.

## 17. Market Decision Contract

When changing `common_market.py`, confirm the following.

- Input Context Fields
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

Confirm comparison operators at Boundary values.

- `<` and `<=`
- `>` and `>=`
- `None`
- NaN
- Inf
- Negatives and 0
- A value exactly equal to the Threshold

The Market result can affect the BUY Filter·Sizing and the Consumer Adapter.

## 18. BUY Filter Contract

When changing `common_buy_filter.py`, confirm the following.

- Whether the market allows BUY
- Stock Final Score
- Flow·Liquidity·Quality conditions
- Missing Input
- Block·Watch status
- Minimum score
- Filter priority
- Reason
- Detail

The Filter does not compute BUY quantity.
Do not mix in the Sizing and Guard responsibilities.

When multiple failure conditions occur simultaneously, maintain the returned Reason priority.

## 19. BUY Guard Contract

When changing `common_buy_guard.py`, confirm the following.

- Risk Flag
- Exposure limit
- Current Position
- Duplicate Holding
- Maximum Position
- Cash Guard
- Market Guard
- Haircut
- Reason priority

The Guard, in principle, validates input and limits Risk.

- The Guard does not query the Consumer DB.
- The Guard does not create an order.
- Confirm the application order of the Guard result and the Sizing result.
- Confirm with the actual Adapter whether the Guard application order must be the same in Research and Decision.

## 20. BUY Sizing Contract

When changing `common_buy_sizing.py`, confirm the following.

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
- 0-share handling

When changing numeric computation, confirm the following risks.

| Risk | Confirmation criterion |
|---|---|
| Float error | Decimal or a tolerance |
| Negative quantity | Prevent 0 or below |
| 0 Price | Skip or Error |
| Rounding | Floor·Round·Ceiling |
| Unit | Confusion of ratio 0~1 vs Percent |
| Cash | Whether it is shared across candidates |
| Maximum | Cap application order |

Common Sizing does not directly query the Broker tick size or the actual orderable quantity.

## 21. BUY Decision Orchestration

When changing `common_buy_decision.py`, confirm the following order in the actual code.

- Market result
- Filter
- Guard
- Sizing
- Final BUY·SKIP
- Reason
- Detail Merge

- Do not arbitrarily change the call order.
- Confirm whether unnecessary computation is performed after a prior failure.
- Confirm whether the same Key is overwritten in the Detail Merge.
- Ensure the final Signal and the sub-results do not contradict each other.
- Confirm whether the Daily and Backtest Adapters use the same Orchestration.

## 22. SELL Guard Contract

When changing `common_sell_guard.py`, confirm the following.

- Position status
- Holding Period
- Stop Loss
- Take Profit
- Risk Flag
- Market status
- Missing Price
- Reason priority

The SELL Guard does not modify the actual Position DB.
It does not create a SELL order or an Execution Order.

## 23. SELL Decision Contract

When changing `common_sell_decision.py`, confirm the following.

- Position Context
- Current Price
- Entry Price
- Highest Price
- Holding Period
- Stop·Take Profit
- Market·Stock Signal
- SELL·HOLD result
- Reason
- Detail

The compatibility behavior of `common_evaluate_backtest_sell` is a separate contract.

- Confirm whether the Adapter handles the input difference between Backtest and Daily.
- Confirm that the Backtest-specific price timing does not create Look-ahead.
- If the per-Consumer result differs for the same Context, clarify the Config and Adapter differences.
- Keep the SELL Reason strings and priority.

## 24. Block Watch Contract

When changing `common_block_watch.py`, confirm the following.

- Block status
- Watch status
- Application target
- Release condition
- Period or date
- Reason
- Linkage with the BUY Filter
- Per-Consumer use

Do not treat Block and Watch as the same state.

- Confirm whether Block prohibits BUY.
- Confirm the actual meaning of Watch among monitoring·penalizing·conditional allowance.
- For date comparison, distinguish the trading day from the Calendar Date.
- Do not link StrategyDecision-specific DB state directly into Common.

## 25. Determinism and Reproducibility

Common results must be reproducible from the same input and Config.

Prohibit or control the following.

- Direct use of the current time
- Timezone-dependent implicit conversion
- Dependence on the traversal result of an Unordered Collection
- Random without a Seed
- Global Mutable State
- Config Mutation depending on call order
- Locale-dependent string handling
- Exact comparison that ignores platform Float differences

In tests, call the same input multiple times and confirm the same result.

## 26. Date and Look-ahead Safety

Common does not look up input dates directly, but must maintain the date contract the Consumer provides.

- Trade Date
- Feature Date
- Price Date
- Position Evaluation Date
- Entry Date
- Exit Date
- Holding Days

- Do not add logic that references future Features or prices.
- In the Backtest Sell Helper, distinguish the same-day close use timing from the trade fill timing.
- Confirm explicit Date conversion instead of date string comparison.
- Do not mix Naive Datetime and Timezone-aware Datetime.
- Maintain the include·exclude criterion of the Holding Period calculation.

## 27. Numeric Safety

When changing strategy numeric computation, confirm the following.

- Mixing Float·Decimal
- NaN·Inf
- Division by 0
- Negative values
- Missing Value
- Clipping
- Min·Max Boundary
- Rounding
- Unit
- Overflow possibility

- Do not silently pass a NaN comparison result as a normal False.
- Do not handle `None`, NaN, and 0 with the same meaning.
- Confirm whether a ratio is 0~1 or 0~100.
- Confirm the Currency unit for price and amount.
- Confirm whether Quantity has an integer contract.

## 28. Import and Package Contract

Confirm the following.

- `__init__.py` public Export
- Relative Import vs absolute Import
- Circular Import
- Import Side Effect
- Consumer Module Path
- Installed Package name and Folder name
- Legacy `utils.py` reference

- Do not export all Symbols indiscriminately for Import convenience.
- Prohibit a Module Rename unless all Consumer Imports are modified together.
- Do not overuse Runtime Import to resolve a Circular Import.
- For Type Hint Import, consider using `TYPE_CHECKING`.
- Do not delete `utils.py` before confirming actual references.

## 29. Version Metadata Contract

When changing `common_version.py` and the Package Metadata, confirm the following.

- Strategy Name
- Engine Version
- Component Version
- Config Version
- Consumer storage·Report use
- Whether included in the Snapshot
- String format
- Backward compatibility

Update the Version in connection with an actual functional change.

- Do not bump the Version when only documentation is modified.
- If an internal function refactoring does not change results, judge per policy.
- For a Threshold·Rule change that alters results, report whether it affects the Version.
- Confirm whether a Consumer uses the Version as a DB Key.

## 30. Legacy and Cleanup Candidates

For files with Legacy potential such as `utils.py`, do not delete them before confirming the following.

| Item | Confirmation content |
|---|---|
| Import | Common internal direct·dynamic Import |
| Consumer | Research·Decision·Execution Import |
| Export | `__init__.py` public status |
| Test | Fixture and Patch targets |
| Documentation | Usage examples and operational documents |
| Git | Recent changes and the user's uncommitted work |

If there is not enough evidence of non-use, do not delete; record it only as a cleanup candidate.

## 31. Test Contract

For code changes, use the narrowest test that matches the impact scope first.

The test types to confirm first are as follows.

| Type | Validation |
|---|---|
| Context | Construction·Default·Serialization |
| Result | Field·Default·Detail Mutation |
| Enum | Value and Serialization |
| Config | Copy·Override·Mutation |
| Market | Threshold Boundary |
| BUY Filter | Failure Reason priority |
| BUY Guard | Risk Boundary |
| BUY Sizing | Cash·Price·Rounding Boundary |
| BUY Decision | Orchestration and Short-circuit |
| SELL Guard | Stop·Holding Boundary |
| SELL Decision | SELL·HOLD and Backtest compatibility |
| Determinism | Same result across repeated calls |
| Consumer Contract | Import·Signature·Field access |

Use the actual test commands after confirming the configuration that exists in the Repository.

- Do not assume a nonexistent Test Runner.
- Do not run tests during documentation work.
- Confirm whether running a test leads to an external API·DB·File Write.
- Do not approve a strategy numeric change based on a Snapshot Test alone.

## 32. Change Classification

Classify the impact level before changing.

| Level | Example |
|---|---|
| Documentation change | Explanation·links·readability |
| Internal refactoring | Public API and result unchanged |
| Compatible extension | Add an Optional Field·new Helper |
| Strategy result change | Threshold·Rule·Order change |
| Breaking Change | Function·Field·Enum·Config Key change |
| Consumer joint change | Requires simultaneous modification of the Adapter and call sites |

Report strategy result changes and Breaking Changes clearly to the user,
and do not expand scope without approval.

## 33. Security Rules

- Do not output the actual values of Password, Token, API Key, Account Number, Webhook URL, and ARN.
- Do not add Secrets and Runtime Credentials to the Common Source.
- Use only Placeholders in examples.
- Ensure no Secret is included in the Config Snapshot.
- Even if a Consumer Credential enters the Detail Payload, do not log it as-is.
- Use `[REDACTED]` when sensitive information must be mentioned.

## 34. Git Rules

- Confirm the change scope with `git status --short` before and after work.
- After work, confirm `git diff --stat` and the target file Diff.
- Because untracked files may not appear in `git diff --stat`, confirm Status together.
- Do not revert user changes.
- Do not Commit without an explicit request.
- Do not delete or Rename a file without the user's approval.

## 35. Documentation System

| Document | Role |
|---|---|
| `AGENTS.md` | Work·compatibility·purity·validation rules |
| `README.md` | Current structure and usage AS-IS |
| `CHANGELOG.md` | Actual change history by date |
| `docs/source-file-catalog.md` | File responsibility·Consumer·change impact |

- Do not create new date-specific `docs/worklog/*.md` files.
- Preserve past Worklog-creation facts only in the CHANGELOG.
- Record the current state in the README.
- Record past change facts in the CHANGELOG.
- Record file responsibilities and impact scope in the Source Catalog.
- Do not repeat the same content at length across the four documents.

## 36. Documentation Update Conditions

### 36.1 README.md

When the following change, confirm whether to update the README.

- Current file structure
- Common responsibility boundary
- Public API
- Consumer relationships
- Config structure
- Usage examples
- Installation·Import method
- Validation method

### 36.2 CHANGELOG.md

Record when the following actually change.

- Public functions
- Context·Result Field
- Enum·Reason
- Config Key·Default
- Decision Rules and Thresholds
- Version Metadata
- Consumer compatibility
- Documentation basis

### 36.3 docs/source-file-catalog.md

When the following change, confirm whether to update it in the same task.

- File creation·deletion·Rename
- File responsibility
- Public functions and Export
- Input·output contract
- Consumer Import
- Config·Version role
- Legacy classification
- Purity·Side Effect

Do not mechanically modify all unrelated documents for a simple typo fix.

## 37. Consistency Check Before Completion

Confirm the following before completing work.

### 37.1 Scope

- Were only the specified files modified?
- Was no Consumer repository modified?
- Were the user's existing changes preserved?
- Were no new Worklog·Scanner·temporary documents created?

### 37.2 Contract

- Are the public function Signatures preserved?
- Are the Context·Result Fields preserved?
- Are the Enum Values and Reasons preserved?
- Are the Config Keys and Defaults preserved as intended?
- Is the `__init__.py` Export preserved?
- Are Consumer Imports and call methods not broken?

### 37.3 Purity

- Was no DB·HTTP·File IO added?
- Was no Environment·Clock·Random dependency added?
- Was no Global Mutable State added?
- Is there no Import Side Effect?
- Is there no Config Mutation?

### 37.4 Strategy Result

- Is the Threshold Boundary preserved as intended?
- Is the Reason priority unchanged?
- Is the BUY·SELL Orchestration order preserved?
- Is the Backtest and Daily compatibility behavior preserved?
- Was no Look-ahead possibility added?
- Are the Numeric Unit and Rounding preserved?

### 37.5 Documentation

- Does the README match the current state?
- Does the CHANGELOG record only actual changes?
- Does the Source Catalog responsibility match?
- Is there no new Worklog-creation rule?
- Is it UTF-8 No BOM?
- Are there no lines over 500 characters, Tabs, or trailing whitespace?

## 38. Safe Validation

When only documentation is modified, confirm within the following scope.

```powershell
git status --short
git diff --stat
git diff -- AGENTS.md
```

Even for code changes, first confirm the static check and the existing test structure.

Acceptable validation candidates are as follows.

- Target Module Syntax confirmation
- Import confirmation without Side Effect
- Existing Unit Tests
- Direct Pure Function calls
- Consumer Contract Test

However, choose the actual command after confirming the user request and the Repository state.

The following validations are not performed.

- DB connection
- External API
- AWS
- Orders
- Entrypoints that cause a File Write
- Consumer Batch·Backtest·Daily operational execution

## 39. Completion Report

Write the completion report in the following order.

1. Changed files
2. Change summary
3. Public API impact
4. Consumer impact
5. Validation result
6. Validations not performed
7. Remaining risk or follow-up confirmation

- Distinguish documentation changes from functional changes.
- Do not report unconfirmed Consumer compatibility as complete.
- Clearly state whether strategy results changed.
- Do not report assumptions as if they were facts.

## 40. Package Release Rules

- The Canonical Source of the Package Version is `pyproject.toml`, a single location.
- Do not hardcode the Package Version in `verify_wheel.py` and the Public API tests.
- `verify_wheel.py` and the Public API tests follow the `pyproject.toml` Version dynamically.
- Do not treat the build outputs `build`, `dist`, `*.egg-info`, and `__pycache__` as Source changes.
- Do not commit Generated Output.
- Do not overwrite a release Version on top of an already existing identical Version.
- Preserve the RC and release Versions as separate Package Versions.

## 41. CI Quality Gate Rules

- Use Ruff, mypy, Wheel Build, Twine Check, Wheel structure validation, and the Public API tests as quality gates.
- Match the mypy scope to the current actual automation Script scope.
- Do not arbitrarily add a nonexistent Source scope to the mypy target.
- Run the Public API tests against the installed Wheel.
- Do not report a test that imports Repository Source as validation of the distributed Package.

## 42. Publish Safety Rules

- Keep the CodeBuild project's default `PUBLISH_TO_CODEARTIFACT` value as the `false` safeguard.
- Only the main Push Workflow enables the Publish Override.
- `workflow_dispatch` is a Build-only run that does not enable Publish.
- Publish only when the Wheel Build succeeds and the Wheel path is confirmed.
- Do not Publish on a Build failure or a missing Wheel.
- Block Publish if the same Version exists before publishing.
- Do not output or document an authentication Token or an Index URL containing authentication.
- Detailed DevOps policy (IAM, OIDC Trust, operational evidence) is managed by port-devops.

## 43. Consumer Contract Rules

- Judge whether something is a Consumer by actual `port_strategy_common` Import.
- Do not conclude a Consumer based on comments, DB strings, and indirect result use alone.
- The Consumer Contract Test cross-checks the actually imported Modules and Symbols against the installed Wheel.
- For a Module that requires a Consumer's own Runtime Dependency, validate it together with that Consumer's Dependency.
- The current direct Consumers are Research and Decision.
- Because Execution currently has no direct Import, do not record it as a direct Consumer.
- Once a Common Import is added in Execution in the future, include it in the Consumer Contract Test scope.

## 44. Promotion and Rollback Rules

- Promote the release Version after RC installation and Consumer Contract Test pass.
- Perform release promotion by building a new Version Wheel and publishing it to CodeArtifact.
- Validate Rollback by explicitly reinstalling the previously published Version, not by a Source Reset or Package deletion.
- After Rollback, re-confirm the Package Version, installation location, public Symbols, and the Public API tests.
- Do not change a Package Version to Archived or a deleted state without separate approval.

## 45. Documentation Work Safety

- In documentation modifications, do not run AWS CLI, CodeBuild, CodeArtifact Publish, or Package installation.
- When moving completion evidence into documentation, remove the actual Token, Account ID, ARN, Build ID, and authentication URL.
- Do not change the Package Version or Strategy Version through documentation work alone.

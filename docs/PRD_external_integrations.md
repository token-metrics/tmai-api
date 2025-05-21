# TOKEN METRICS API – EXTERNAL-INTEGRATION PRD

## 0 DOCUMENT META
• Title : TMAI API – External Integrations (Waves 1 & 2)
• Product owner : <mailto:product-lead@tokenmetrics.com|product-lead@tokenmetrics.com>
• Engineering lead: <mailto:eng-lead@tokenmetrics.com|eng-lead@tokenmetrics.com>
• Repo : <https://github.com/token-metrics/tmai-api>
• Public endpoint spec (OpenAPI 3.1): <https://developers.tokenmetrics.com/reference/tokens>

## 1 PROBLEM
External discovery is minimal and only ~10 % of paid traffic uses the TMAI token.
We must embed the API in high-reach ecosystems that auto-promote new listings and that enforce the 10 % pay-in / 2–25 % staking rebate.

## 2 OBJECTIVES (8 WEEK WINDOW AFTER WAVE-1 LAUNCH)
• ≥ 1 000 unique connector installs per week
• ≥ 3 000 real-time API calls per week
• ≥ 40 % of calls paid or discounted in TMAI
• Median "time-to-first-rating" ≤ 10 minutes for any connector

## 3 NON-GOALS
× Adding new metric or rating endpoints
× Enterprise Snowflake or bespoke deals
× Changes to the pricing-service internals

## 4 SYSTEM OVERVIEW (ALL CONNECTORS)
Client ⇢ Bearer JWT ⇢ API Gateway ⇢ /ratings | /metrics | /sentiment
└─⇢ /pricing svc ⇢ veTMAI staking contract
Required JWT claims: `plan`, `payment_method`, `stake_score`.
The gateway enforces per-plan QPS and monthly caps and logs usage.

## 5 ENGINEERING CONVENTIONS
• Each connector lives under `integrations/<platform>/`
• One PR per connector, branch name `feat/<platform>-v1`
• CI (GitHub Actions): `npm test`, `pytest`, `openapi-lint`, `eslint`, SLSA provenance
• Secrets pulled via GitHub OIDC → HashiCorp Vault — no plaintext keys in repo
• Add eng-lead + @security to `CODEOWNERS` for every new folder
• Release tags use SemVer: `v1.0.0-<platform>-<yyyymmdd>`

## 6 WAVE 1 — PR SPECIFICATION
### ELIZAOS PLUG-IN
• Docs : <https://docs.elizaos.com/plugins>
• Deliver: `integrations/elizaos/service.yaml` + demo GIF
• Must expose GET /ratings and POST /auth
• Acceptance: sandbox agent returns rating < 800 ms (95th pct.)

### QUICKNODE ADD-ON
• Docs : <https://docs.quicknode.com/marketplace/publish-add-ons>
• Deliver: Express proxy, provision / deprovision hooks, generated `pricing.json`
• Acceptance: QuickNode test invoice shows 10 % pay-in break + tier caps

### VIRTUALS TM-ORACLE
• Docs : <https://docs.virtuals.io/oracles>
• Deliver: `TMOracle.sol`, `oracle-keeper.ts`, Hardhat tests
• Must revert if `veTMAI.balanceOf(caller)==0`
• External audit (e.g., Code4rena) must show "no critical findings"

### CURSOR IDE CONNECTOR
• Docs : <https://docs.cursor.sh/marketplace>
• Deliver: `integrations/cursor/cursor.json`, OAuth→JWT flow
• Acceptance: IDE "Import API" wizard runs sample code with valid response

### RAPIDAPI HUB LISTING
• Docs : <https://docs.rapidapi.com/docs/publishing-your-api>
• Deliver: Upload `openapi.yaml`, enable sandbox 10 req / min, upgrade URL
• Acceptance: listing searchable under "crypto ratings"

### OPENAI AGENTS TOOL
• Docs : <https://platform.openai.com/docs/agents/tools>
• Deliver: `integrations/openai/tool.yaml`, helper lib `@tmai/openai` (PyPI + npm)
• Acceptance: tool installs in ChatGPT, fetches rating via JWT

## 7 WAVE 2 — PR SPECIFICATION (OVERVIEW)
Follow the same pattern as Wave 1.
• Chainlink Functions — <https://docs.chain.link/chainlink-functions>
• LangChain Tool — <https://python.langchain.com/docs/integrations>
• Coinbase AgentKit — <https://docs.base.org/agent-kit>
• Zapier App — <https://platform.zapier.com/docs>
• Windsurf MCP — <https://docs.windsurf.dev>
• Alchemy Add-On — <https://docs.alchemy.com/add-ons/publish>
Detailed checklists will be copied from the Wave-1 template into `docs/PRD_external_integrations.md`.

## 8 SUCCESS METRICS
• Grafana: `tm_api_calls_total{integration}`
• Grafana: `tm_tmai_spend_usd{payment_method}`
• Looker: `tm_accounts_by_plan` (upgrade funnel)

## 9 RELEASE / ROLLBACK FLOW
Merge PR → CI builds Docker image → auto-deploy to staging →
`/status` smoke test → Slack `/deploy promote <sha>` (requires @infra + @prod)
Rollback via `/deploy rollback <prev-sha>`; gateway drains 10 % traffic per minute.

## 10 SECURITY CHECKLIST (MUST PASS BEFORE MERGE)
:ballot_box_with_check: No plaintext secrets in repo
:ballot_box_with_check: `npm audit` and `pip audit` show zero critical issues
:ballot_box_with_check: External outbound calls only to <http://tokenmetrics.com|tokenmetrics.com> or approved RPC endpoints
:ballot_box_with_check: Solidity compiled with `0.8.21`, optimizer runs ≥ 1000

## 11 PRICING TIERS
• **Free — Staking Score 0**
  • 5 000 API calls per month, 1 req/min hard cap.
  • Endpoints: Token and OHLCV price data (hourly, daily, 10-min price feed), "Top Tokens by Market-Cap," plus live Trader Grades / Trading Signals.
  • Historical depth: three-month look-back for grades / signals / indices, but the most recent 30 days are pay-walled.
  • No charge; overage not available.
• **Advanced — Staking Scores 1-3**
  • 20 000 calls per month, 60 req/min.
  • Monthly fee USD 99.99 (10 % off when paid in TMAI).
  • Unlocks all Free endpoints plus Grades & Signals, Indices, Indicators, Token Reports & Metrics.
  • Historical depth: 12-month look-back on every unlocked category.
  • Overage: USD 0.010 per 1 000 calls.
• **Premium — Staking Scores 4-6**
  • 100 000 calls per month, 180 req/min.
  • Monthly fee USD 199.99 (10 % off in TMAI).
  • Adds AI-Agent endpoints and AI Reports on top of Advanced.
  • Historical depth: 36 months for every category.
  • Overage: USD 0.0075 per 1 000 calls.
• **VIP — Staking Scores 7-10**
  • 500 000 calls per month, 600 req/min.
  • Monthly fee USD 799.99 (10 % off in TMAI).
  • Everything in Premium, with unlimited historical look-back.
  • Overage: USD 0.0050 per 1 000 calls.

Overage is billed in blocks of 1 000 calls. Annual pre-pay still gives two months free, and paying the annual invoice in TMAI stacks the 10 % pay-in discount on top.

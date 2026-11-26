---
seo_title: "Kiwoom MCP prompt library — 19 questions to paste into Claude or Cursor"
description: "19 questions you can paste as-is into Claude or Cursor with kiwoom-client-mcp attached: account check, stock analysis, today's market, investor flow, condition search, live watch, rebalance math, open-order cleanup and porting OpenAPI+ code, each with the tools it uses and what comes back."
---

# Prompt library

Questions you can paste as-is into Claude or Cursor once the [MCP server](mcp.md) is attached. Each one lists the tools
the agent calls and what comes back, in one line. Name a stock by its name or code; no api_id or field names needed.

- Every question is a **lookup or a calculation**. None of them asks the agent to pick what to buy or sell. The person reading
  the result makes that call.
- Questions that involve an order stop at **a preview** (`order_preview`, nothing is sent). An order goes out only after the
  user has seen the preview and confirmed, and only when the order tools are registered. On a live account they do not exist
  until you set `KIWOOM_MCP_ALLOW_LIVE_ORDERS=true` (see "Live-order guard" in the [MCP server](mcp.md) page).
- Start with a paper-trading key (`KIWOOM_IS_MOCK=true`). The values you get depend on the quotes and balances at the time.
- The five prompts built into the server (`review_account`, `analyze_stock`, `market_today`, `rebalance`, `order_checklist`)
  give the same steps. Pick them from your client's prompt menu (see "Resources and prompts" in the [MCP server](mcp.md) page).

Stock names carry their Korean name in parentheses: the stock list (ka10099) is in Korean, so the Korean name finds the stock
on the first try. The agent understands the question itself in either language.

## Account

### 1. Account check

```text
Check my account. Show total valuation, profit and loss and return, plus each holding's weight and return as a table,
and tell me about any open orders left today. Do not place any orders.
```

- Tools: `get_portfolio` → `get_orders`
- You get: a table of each holding's quantity, average price, valuation, profit and loss and weight, cash (D+2) and total
  assets, and the open orders (account numbers masked).

### 2. How many shares I can buy

```text
At the current price, how many shares of Samsung Electronics (삼성전자) can I buy with my orderable cash? Do not place any orders.
```

- Tools: `get_buying_power`
- You get: orderable quantity and amount by margin rate at the current price (cash only).

### 3. Today's fills

```text
List my orders that filled today in time order: stock, buy/sell, quantity and fill price as a table.
```

- Tools: `get_orders`
- You get: today's fills (stock, side, quantity, fill price, time). Name a date to get that day instead.

## Stocks

### 4. A stock at a glance

```text
What's Samsung Electronics (삼성전자) trading at? Include change, volume, market cap, PER and PBR.
```

- Tools: `stock_snapshot`
- You get: price, change, volume, market cap, PER/PBR and more in one lookup.

### 5. Stock analysis

```text
Analyze SK hynix (SK하이닉스). Summarize the current quote and ratios, the trend over the last 60 daily bars
(5- and 20-day moving averages, period return, high and low), and foreign and institutional net buying over the same period.
Keep what the numbers show apart from your interpretation.
```

- Tools: `stock_snapshot` → `get_chart` → `investor_flow`
- You get: quote and ratios, a 60-day OHLCV summary (moving averages, return, high/low, average volume) and net buying totals
  by investor type. No buy or sell call.

### 6. Several stocks at once

```text
Show quotes for Samsung Electronics, SK hynix, NAVER, Kakao and Hyundai Motor (삼성전자, SK하이닉스, NAVER, 카카오, 현대차)
in one go, sorted by change.
```

- Tools: `get_quotes`
- You get: price, change, volume, traded value and market cap for up to 20 stocks in one request. Only stocks it cannot find
  come back as errors.

### 7. Find a stock code

```text
Find every stock whose name contains 에코프로 and give me its code and market.
```

- Tools: `stock_search`
- You get: code, name, market and sector of each match (KOSPI, KOSDAQ, ETF and so on).

### 8. Intraday bars

```text
Show today's 5-minute bars for Samsung Electronics (삼성전자) and point out the three busiest stretches by volume.
```

- Tools: `get_chart`
- You get: 5-minute OHLCV (oldest first) and the highest-volume stretches.

## Market

### 9. Today's market

```text
Summarize today's market. For KOSPI and KOSDAQ each, show the top 10 gainers, top 10 losers and top 10 by traded value as tables.
```

- Tools: `market_movers`
- You get: tables of top stocks by market and kind (price, change, volume, traded value).

### 10. Volume spikes

```text
Show 20 KOSDAQ stocks whose volume just jumped, and group the ones that are up today separately.
```

- Tools: `market_movers`
- You get: the volume-spike list and a table of only the rising ones.

### 11. Investor flow

```text
Show Samsung Electronics' (삼성전자) net buying by investor type (individuals, foreigners, institutions) over the last
20 trading days in won, and count the days foreigners were net buyers.
```

- Tools: `investor_flow`
- You get: daily net buying by investor type (million won), period totals and the count of net-buying days.

### 12. Flow for what I hold

```text
For each stock I hold, total the foreign and institutional net buying over the last 10 trading days as a table.
Do not place any orders.
```

- Tools: `get_portfolio` → `investor_flow`
- You get: a table of 10-day foreign and institutional net buying per holding.

## Condition search and real time

### 13. Run a condition search

```text
Run the "급등주" condition I saved in HTS (영웅문4) and show the matches sorted by change.
```

- Tools: `condition_search_run`
- You get: code, name, price, change and volume of every match. The condition must already be saved in HTS (영웅문4).

### 14. Watch live trades

```text
Watch trades in Samsung Electronics and SK hynix (삼성전자, SK하이닉스) for 30 seconds and tell me right away
if Samsung trades at 72,000 won or higher.
```

- Tools: `watch`
- You get: last price, high/low, buy/sell volume and tick count per stock. It returns as soon as the condition hits (at most
  60 seconds; trades arrive only during market hours).

## Rebalancing and orders

### 15. Rebalance math

```text
Work out what to buy and sell, in whole shares, to bring my account to Samsung Electronics 40%, SK hynix 20% and the rest
in cash. Keep at least 1,000,000 won in cash. Do not place any orders; just show a table.
```

- Tools: `get_portfolio` → `rebalance_plan`
- You get: a table of whole-share quantities at tick-rounded prices, sells first and buys only within cash. Nothing is sent;
  each row carries the arguments for a preview.

### 16. Clean up open orders

```text
Show all of today's open orders and make a cancel preview for each one. I will pick which ones to cancel;
do not send anything before that.
```

- Tools: `get_orders` → `order_preview` → (user confirms) → `cancel_order`
- You get: the open orders, a cancel preview and `confirm_token` for each. Only the orders the user picks are cancelled, and
  only with a matching token.

### 17. Order preview

```text
Make a preview for buying 10 shares of Samsung Electronics (삼성전자) at a 70,000 won limit. Check the price limits and
the orderable quantity too, and do not send it until I say "confirm".
```

- Tools: `order_preview` → (user confirms) → `place_order`
- You get: stock, quantity, price and estimated amount, price-limit and orderable-quantity checks (`errors`/`warnings`) and a
  single-use `confirm_token` valid for 120 seconds.

### 18. Are the order tools on?

```text
Check with a preview for buying 1 share of Samsung Electronics (삼성전자) whether this server has order tools turned on.
Do not place any orders.
```

- Tools: `order_preview`
- You get: `order_tools_enabled` (whether order tools are registered) in the preview and, when they are off, a warning saying
  why (read-only mode, or no live opt-in). With them off, no order can be sent.

## Porting code

### 19. OpenAPI+ code to REST

```text
The pykiwoom code below calls OpenAPI+ opt10081 (daily stock chart). Find the Kiwoom REST TR and the kiwoom-client method
that do the same thing, check the request fields, and rewrite it as code that runs with is_mock=True.

(paste your code here)
```

- Tools: `search_tools` → `describe_tool`
- You get: the matching REST TR (ka10081 here) and tool name, its request-field schema, and the rewritten code. Some TRs keep
  the number but change the name, so check against the table in [Moving from OpenAPI+](migration-from-openapi-plus.md).

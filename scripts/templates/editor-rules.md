# kiwoom-client

Python client for the Kiwoom Securities (키움증권) REST API and WebSocket (`import kiwoom_client`). It can place real
orders on a real brokerage account.

$usage_rules

Look up methods in `docs/endpoints.md` (api_id, Korean TR name), fields with `kiwoom_client.spec.get(api_id)`, and every
public signature in `llms-full.txt`. Inside this repository also follow `AGENTS.md`: unit tests mock HTTP with
`pytest-httpx` and never touch the live server, existing public behaviour is only added to, never changed, and generated
files are refreshed with `python scripts/gen_docs.py`.

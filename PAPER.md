# Paper trading notes

- No wallet, no live CLOB orders.
- Capital ledger: `paper_capital.reserve` / `release` on fill cost only.
- FAK ladder against in-memory book cache.
- `unfilled_cancel_seconds` (default 1800): zero-fill OPEN positions cancelled after timeout.

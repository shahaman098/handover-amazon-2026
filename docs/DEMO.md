# Demo script (< 3 minutes)

Show on screen: **Entrant-built Alexa+ simulation — not a production Alexa device.**

1. **Reset** — Click *Reset demo*. Show revision 0, assessments A1/A2/A3, identity unchanged.
2. **Adviser** — Role: Adviser. Click *Inspect A1* or type the payslip correction:
   `That is my old payslip. Use the September document instead.`
3. **Confirm card** — Show proposed income (£2450), affected A1/A2, proposal hash. Ledger unchanged until confirm.
4. **Applicant** — Click *Applicant confirms*. Show A1/A2 updated, identity assertion still Jordan Ellis, residency conflict still listed, A3 unresolved, ready_to_export = no.
5. **Receipt** — Export JSON handoff packet; open briefly to show ledger events.
6. **Persistence** — Restart API (`uvicorn`), reload page; state unchanged.
7. **Stale write** — Run `PYTHONPATH=. python scripts/run_verification.py` (or attempt duplicate confirm in UI) to show rejection without partial mutation.

Optional: run `scripts/mcp_smoke.py` to show MCP tools share the same ledger.

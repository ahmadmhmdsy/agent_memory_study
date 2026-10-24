# R-015 new advanced projects: A03–A16

Generator: `r015_advanced2.py`. Every project has 21 sessions and 4 modules, and FINISH falls in session 21. Each old value of a superseded fact has a `test_stale_*` test. `test_basic` uses no fact values.

Chain lengths count values, so 3 means the first value plus two replacements.

| id | domain | sessions | facts (sup / unf / con / dec) | superseded chains |
|---|---|---|---|---|
| A03 | car rental | 21 | 14 (5 / 3 / 3 / 3) | day_rate 3, free_km 4, young_surcharge 3, min_age 2, delimiter 3 |
| A04 | dental clinic appointments | 21 | 14 (5 / 3 / 4 / 2) | slot_len 3, last_start 3, filling_fee 3, kid_age 3, no_show_fee 2 |
| A05 | restaurant tabs | 21 | 13 (5 / 3 / 3 / 2) | service_pct 3, party_min 3, staff_pct 3, money_format 3, max_lines 2 |
| A06 | electricity billing | 21 | 13 (5 / 3 / 3 / 2) | standing 3, rate1 3, block 3, rate2 2, late 3 |
| A07 | airline bookings and baggage | 21 | 13 (5 / 3 / 3 / 2) | allowance 3, excess 3, child 3, max_bags 2, change_fee 3 |
| A08 | bike sharing | 21 | 13 (5 / 3 / 3 / 2) | unlock 3, rate 3, ebike 3, member_free 3, overtime_after 3 |
| A09 | pet kennel | 21 | 13 (5 / 3 / 3 / 2) | dog 3, cat 2, large_kg 3, meds 3, max_nights 3 |
| A10 | greenhouse plant care | 21 | 13 (5 / 3 / 3 / 2) | herb 2, cactus 3, fern 3, feed 3, alarm 3 |
| A11 | conference talks and tickets | 21 | 13 (5 / 3 / 3 / 2) | max_minutes 3, room_gap 3, per_speaker 2, ticket 3, student 2 |
| A12 | chess league standings | 21 | 13 (5 / 3 / 3 / 2) | win_pts 2, k_factor 3, rating_floor 3, provisional 3, entry_fee 3 |
| A13 | food delivery | 21 | 13 (5 / 3 / 3 / 2) | base_fee 3, per_km 3, min_order 3, free_over 2, service_pct 3 |
| A14 | print shop jobs | 21 | 14 (5 / 3 / 3 / 3) | bw_page 3, color_page 3, bulk_pages 3, binding_fee 3, rush_pct 2 |
| A15 | insurance claims | 21 | 13 (5 / 3 / 3 / 2) | deductible 3, payout_pct 3, claim_window 3, max_claims 3, cap 3 |
| A16 | cafe loyalty points | 21 | 13 (5 / 3 / 3 / 2) | signup_bonus 3, pts_per 3, reward_cost 3, gold_at 3, max_redeem 3 |

## Checks

- `python check_long.py A03 … A16`: every project shows "wrong with ref: none; pass on start repo: none". The reference passes everything except the stale tests, and the start repo passes nothing.
- `python check_facts.py A03 … A16`: 14 projects, 1 flag.

## Flags reviewed

- **A04 `name_required` flags `'Bob'`.** The test registers `"  Bob "` and expects the name to be stored as `"Bob"`. A prompt says names are stored without surrounding spaces, so the expected value follows from the input and the stated rule. The fact is stated; no change.
- **A13 `export_header` flagged `'Roma'` (fixed).** The restaurant name is test data and comes from the shared fixture. The test now compares against `o.get(1)[0]` instead of a literal, and the flag is gone.

Earlier flags (A03 delimiter, A07/A08 export order) were fixed in the generator by passing the test names as direct call arguments. Prompts that add a composed class now name the attribute the tests read, for example "works on a Players, kept as its attribute players".

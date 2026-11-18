## Rejected / disqualified (do not re-propose)

| What | Why rejected | Evidence |
|---|---|---|
| Nonstop TLV-DUB | Does not exist on these dates; every result has at least one stop | One-way captures for 4-7 Apr (127-142 itineraries each), all with stops |
| Flying home the same night after the show | Last departures from Dublin on Wed 7 Apr towards TLV are 20:30 (BA835) and 20:35 (EY48), before the show ends | `data/raw/ow_DUB_TLV_04-07_any.json` |
| Any return departing Dublin on Fri 9 Apr | **Friday rule FAIL.** Earliest possible landing is 15:25 (LH983 05:55 + LH686); next 16:40 (AF1017 + LY320), 16:50 (KL1134 + LY338), 19:10 (Lufthansa via FRA) | `data/raw/ow_DUB_TLV_04-09_any.json` |
| Thu 8 Apr evening departures landing Fri afternoon: LH981 + LH94 + LH680 (lands Fri 16:00), VL2519 + LH680 (16:00), LH981 + LH694 (19:10) and 14 similar | **Friday rule FAIL** (land after 12:00) | `data/raw/ow_DUB_TLV_04-08_any.json` (17 itineraries fail) |
| Etihad via Abu Dhabi, EY48 Thu 20:35 + EY593/EY607, lands Fri 11:10 / 11:20 | Passes the rule by under an hour, 12h35+, NIS 3,935-3,967 pp one way | same file |
| Saturday-night return (Sat 10 Apr) | Latest Dublin departures are 18:35-20:35, before nightfall in Dublin | `data/raw/ow_DUB_TLV_04-10_any.json` |
| Lufthansa LH687 + LH982 on Wed 7 Apr | Lands 22:15, after the show | round-trip capture for 7 Apr |
| KLM both ways (KL462 + KL1137 out 7h40, KL1142 + KL461 back) | Fastest outbound but NIS 3,258-3,920 pp | round-trip captures |
| SWISS via Zurich (LX257 + LX400 out; LX405 + LX256 back, 7h00, lands Fri 03:35) | NIS 2,493-2,753 pp as a round trip with a Lufthansa return; the 7h00 SWISS return one-way alone is 1,638 pp | round-trip and one-way captures |
| El Al + Air France / KLM mixes (LY339 + KL1145, LY327 + AF1816, LY221 + AF1116) | NIS 2,188-3,424 pp, no timing advantage | round-trip captures |
| Lufthansa return via Munich (LH2517 10:40 + LH682, lands Fri 00:35) | Friday rule OK, but 108 pp more than DUB-01, 5h45 in Munich, and leaves Dublin 2 hours earlier. NIS 1,668 pp (verified, booking page) | `data/raw/booking_LH_0406_retMUC.json` |
| Lufthansa return LH983 05:55 + LH690 (9h05 in Frankfurt, lands Thu 23:15) | Kayak's cheapest Lufthansa round trip ($450 pp = NIS 1,461), but not offered as a round-trip return by Google (one-way 2,743 for 3); 05:55 start for the same arrival time as DUB-01 | Kayak capture, one-way capture |
| ITA + Lufthansa two-stop outbound (AZ815 + VL1875 + VL2518, 10h55) | One-way 926 pp, no saving over Lufthansa direct via FRA (922 pp one-way) | `data/raw/ow_TLV_DUB_04-06_any.json` |
| Iberia Express via Madrid (IB1874 + IB1885 Tue, 14h10; return IB1882 + IB1873) | One-way 795 pp out but 1,748 pp back | one-way captures |
| TAP via Lisbon, return TP1327 + TP1603 | 20h45 with 12h25 in Lisbon, 1,624 pp one-way, lands Fri 04:15 | one-way capture |
| Self-transfer return via London Gatwick (Ryanair DUB-LGW morning + Wizz W95621 LGW 13:50 -> TLV 20:50) paired with the Athens outbound | Works (about 700 pp return, lands Thu 20:50, no Friday exposure) but needs a UK ETA; kept only as the return half of DUB-11 | London captures |
| Other Kayak "self-transfer hack" combinations (via Rome FCO, Budapest, Brussels, Milan MXP, Rhodes) | All $425-502 pp on Kayak, i.e. no cheaper than DUB-10; individual legs not verified | Kayak captures |
| Manchester / Edinburgh as a stopover | No nonstop TLV flight to MAN or EDI appeared for 6 Apr when searched together with the London airports (only LHR/LTN/LGW/STN results). Single query, not re-checked for other dates | Google Flights query 17 Nov 2026 (result not saved to `data/raw`) |
| Belfast + train | Not researched: no TLV-BFS nonstop is known and it adds a UK ETA plus a 2h+ train. Unverified | - |
| London one-ticket round trip as the base for a stopover | Round trip TLV-London 5 -> 8 Apr starts at 5,595 for 3 (Israir), dearer than two one-ways (2,783 + 1,625 = 4,408) | `data/raw/rt_TLV-LON_04-05_04-08_out_ns.json` |

## Cross-check log (second source: Kayak, 3 adults, USD)

Conversion: 1 USD = 3.2463 ILS, 1 GBP = 4.2823 ILS (Frankfurter API, ECB reference rates dated 2026-11-17).

| Itinerary | Google Flights (ILS pp) | Kayak (USD pp) | Kayak in NIS pp | Difference |
|---|---|---|---|---|
| DUB-01 LH Tue, return 12:40 | 1,560 | 461 | 1,497 | Google +4.2% |
| DUB-02 LH Mon, return 12:40 | 1,694 | 499 | 1,620 | Google +4.6% |
| DUB-03 LH Tue, return 05:55 -> 15:25 | 1,856 | 526 | 1,708 | Google +8.7% |
| LH Tue, return via MUC (rejected) | 1,668 | 489 | 1,587 | Google +5.1% |
| DUB-06 AF/KL Tue | 2,216 | 682 | 2,214 | match |
| DUB-10 pattern (self-transfer ATH / CLJ) | 1,212 (sum of airline-direct legs) | 434 (same outbound) / 423 (Aegean outbound) | 1,409 / 1,373 | Kayak +13-16% |

Flight times and connection airports matched between the two sources for every row. Kayak lists the Lufthansa fare brand as "Economy Light". Lufthansa options are consistently 4-9% cheaper on Kayak than the Lufthansa price Google shows in ILS; the airline site itself was not checked, so treat 1,500-1,560 pp as the range for DUB-01.

## Not verified

- No price was checked on an airline's own website or on an Israeli aggregator; "airline direct" prices are the ones Google's booking page attributes to the airline.
- Wizz Air cabin-trolley and checked-bag fees (Google shows only "available for a fee"). Aegean, Israir, Air France/KLM checked-bag fees.
- Lufthansa checked-bag fee beyond Google's range (NIS 0-553 per passenger per round trip).
- Whether an airside connection at Heathrow (DUB-07) requires a UK ETA.
- ETIAS status for Schengen entries (Greece, Romania) in April 2027.
- Sunset / nightfall time in Dublin on Sat 10 Apr 2027.
- DUB-13 was seen only on the search list; its booking page was not opened.
- Ryanair timetable times for flights not in the tables were not cross-checked.
- Airline schedules for April 2027 can still change; all times are as published on 17-18 Nov 2026.

## How this was collected

Scripts are in `scripts/` (Python + Playwright driving the installed Chrome; they load ordinary Google Flights URLs with `curr=ILS`, 3 adults, and read the result data the page itself fetches). Raw captures are in `data/raw/`, Kayak page text and screenshots in `data/crosscheck/`. `scripts/build_md.py` regenerates this file and `data/itineraries.json` from the raw captures. Google rate-limited the first sweep (its "unusual traffic" page); the sweep was stopped and resumed later at a slower pace, so the planned sweep of about 55 other European transfer airports was not run - Kayak's self-transfer results were used to cover that ground instead.

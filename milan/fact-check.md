# Fact-check - Milan flights (`flights.md`, `sources.md`)

Checked **2026-11-17 22:46-23:05 UTC** (= 18 Nov 2026 00:46-01:05 Israel time). All price checks: 3 adults, economy.
Verdicts: `confirmed`, `corrected` (flights.md edited), `could-not-verify`, `wrong`.

Summer-2027 timetables of ground operators and the El Al / Arkia websites could not be read, so "confirmed" for a schedule means: the flight is on sale for that date in the sources named, not that the airline cannot retime it.

## Sources used (label -> URL)

Independent of the author's Google/Kayak scripts:

- [WIZZ-TT] Wizz Air's own timetable/fare-chart endpoint, read from inside the loaded booking page https://wizzair.com/en-gb/booking/select-flight/TLV/MXP/2027-04-18/2027-04-20/3/0/0/null (calls `be.wizzair.com/29.25.0/Api/search/timetable` and `/asset/farechart`, 3 adults, EUR). Gives departure times per day and the day's lowest fare; no flight numbers. The flight-level `search/search` call still returns HTTP 429.
- [WIZZ-MAP] Wizz route map endpoint, same page (`/Api/asset/map`): TLV-MXP direct; TLV-BGY and TLV-VRN `isDirectFlight: false`.
- [WIZZ-CI] https://wizzair.com/en-gb/help-centre/check-in-and-boarding/check-in/check-in-and-baggage-drop-off-times and https://ssr-weu2.wizzair.com/en-gb/help-centre/check-in-and-boarding/check-in/check-in-process
- [ISRAIR] https://www.israir.co.il/reservation/search/flights-abroad/results?origin=VRN&destination=TLV&startDate=20/04/2027&adults=3&subject=ALL (same pattern for TLV-BGY, TLV-MXP)
- [ISRAIR-BAG] https://www.israir.co.il/Passengers_Info/Baggage_Policy.html
- [TRIP-RT] https://www.trip.com/flights/showfarefirst?dcity=tlv&acity=mil&ddate=2027-04-18&rdate=2027-04-20&triptype=rt&class=y&quantity=3&nonstoponly=on&locale=en-XX&curr=ILS
- [TRIP-OW20] https://www.trip.com/flights/showfarefirst?dcity=mil&acity=tlv&ddate=2027-04-20&triptype=ow&class=y&quantity=3&nonstoponly=on&locale=en-XX&curr=ILS
- [TRIP-OW17] https://www.trip.com/flights/showfarefirst?dcity=tlv&acity=mil&ddate=2027-04-17&triptype=ow&class=y&quantity=3&nonstoponly=on&locale=en-XX&curr=ILS
- [KIWI] https://www.kiwi.com/en/search/results/tel-aviv-israel/milan-italy/2027-04-18/2027-04-20?adults=3&stopNumber=0%7Etrue&currency=ils
- [HEBCAL-TLV] https://www.hebcal.com/zmanim?cfg=json&geonameid=293397&start=2027-04-16&end=2027-04-21 and https://www.hebcal.com/hebcal?v=1&cfg=json&maj=on&year=2027&month=4&geo=geoname&geonameid=293397&c=on&M=on
- [HEBCAL-MIL] https://www.hebcal.com/zmanim?cfg=json&geonameid=3173435&start=2027-04-16&end=2027-04-21
- [HEBCAL-ROM] https://www.hebcal.com/zmanim?cfg=json&geonameid=3169070&start=2027-04-16&end=2027-04-21
- [ECB] https://api.frankfurter.dev/v1/latest?base=EUR&symbols=ILS,USD (ECB reference 17 Nov 2026: 1 EUR = 3.5674 ILS; 1 USD = 3.2463 ILS)
- [ATM-M2] https://orari.atm.it/M2_694.pdf (Assago Milanofiori Forum), https://orari.atm.it/M2_685.pdf, https://orari.atm.it/M2_680.pdf (valid from 26 Oct 2026)
- [TRENORD] https://www.malpensaexpress.it/fileadmin/contenuti/TRENORD/2-Linee_e_orari/Orario_ferroviario/ORARIO_in_vigore/QMXP_giugno_2026.pdf and https://www.malpensaexpress.it/en/lines-and-timetable/most-searched-lines/milano-centrale-malpensa-aeroporto-t1-route
- [AUTOSTRADALE] https://autostradale.it/wp-content/uploads/2026/04/MalpensaAeroporto-MilanoCentrale.pdf
- [CARONTE] https://www.caronte.eu/wp-content/uploads/2026/11/Orari-sito-novembre-2026.pdf
- [MXP-SHUTTLE] https://www.malpensashuttle.it/uploads/c9c79a023333-050.-apt4-milano-centrale-malpensa-dal-9-ottobre-2026.pdf
- [SEA-COACH] https://www.milanomalpensa-airport.com/en/from-to/by-coach
- [TAXI-LOMB] https://www.regione.lombardia.it/infrastrutture-trasporti-e-mobilita/taxi-collegamenti-aeroportuali-e-noleggio/servizio-e-tariffe-taxi-nel-bacino-aeroportuale
- [TRANSFER] https://city-airport-taxis.com/airporttransfers/reservations/taxi-from-Assago-to-Milan-Malpensa-Airport (secondary quote page)
- [SLEEP-MXP] https://www.sleepinginairports.net/guides/milan-malpensa-airport-guide.htm (secondary)
- [FORUM-BAGS] https://www.mentelocale.it/milano/76479-brunori-sas-a-milano-orari-biglietti-e-scaletta-del-concerto-al-forum-di-assago.htm (secondary, Mar 2025) and https://www.unipolforum.it/it/regole/
- [TRENITALIA] https://www.lefrecce.it (booking engine, queried for 16 Dec 2026 and 18/20 Apr 2027)
- [ATV-VRN] https://www.atv.verona.it/Autobus_per_aeroporto_Catullo
- [ATVO] https://www.atvo.it/assets/bus_routes/035b_05.10.26-24.04.27.pdf
- [ETIAS] https://travel-europe.europa.eu/etias and https://travel-europe.europa.eu/etias/etias-timeline-explained
- [FC-MXP] https://www.flightconnections.com/flights-from-tlv-to-mxp ; [FC-BGY] https://www.flightconnections.com/flights-from-tlv-to-bgy ; [FC-LIN] https://www.flightconnections.com/flights-from-tlv-to-lin (secondary, updated 17 Nov 2026, winter schedule)
- [TRIP-STATUS] https://www.trip.com/flights/status-w46431 and https://www.trip.com/flights/status-w46405 (secondary)
- [WIZZ-PRIO] https://www.wizzair.com/en-gb/information-and-services/wizz-services/wizz-priority-old
- [ELAL-BAG] https://blog.wego.com/el-al-news/ and https://onemileatatime.com/news/el-al-carry-on-restriction-economy-lite-fares/ (secondary)
- [SKYEXP] https://www.skyexpress.gr/en/sky-experience/before-fly/fare-types

Same sources as the author (re-run today with the author's scripts, so not independent):

- [G-RT] https://www.google.com/travel/flights/search?tfs=GhwSCjIwMjctMDQtMTgoAGoFEgNUTFZyBRIDTVhQGhwSCjIwMjctMDQtMjAoAGoFEgNNWFByBRIDVExWQgMBAQFIAZgBAQ==&hl=en&curr=ILS
- [G-RT-W46434] https://www.google.com/travel/flights/search?tfs=Gj4SCjIwMjctMDQtMTgoAGoFEgNUTFZyBRIDTVhQIiAKA1RMVhIKMjAyNy0wNC0xOBoDTVhQKgJXNDIENjQzNBocEgoyMDI3LTA0LTIwKABqBRIDTVhQcgUSA1RMVkIDAQEBSAGYAQE=&hl=en&curr=ILS
- [G-RT-LY381] https://www.google.com/travel/flights/search?tfs=Gj0SCjIwMjctMDQtMTgoAGoFEgNUTFZyBRIDTVhQIh8KA1RMVhIKMjAyNy0wNC0xOBoDTVhQKgJMWTIDMzgxGhwSCjIwMjctMDQtMjAoAGoFEgNNWFByBRIDVExWQgMBAQFIAZgBAQ==&hl=en&curr=ILS
- [G-RT-21] https://www.google.com/travel/flights/search?tfs=Gj4SCjIwMjctMDQtMTgoAGoFEgNUTFZyBRIDTVhQIiAKA1RMVhIKMjAyNy0wNC0xOBoDTVhQKgJXNDIENjQzNBocEgoyMDI3LTA0LTIxKABqBRIDTVhQcgUSA1RMVkIDAQEBSAGYAQE=&hl=en&curr=ILS
- [G-RT-19] https://www.google.com/travel/flights/search?tfs=Gj0SCjIwMjctMDQtMTkoAGoFEgNUTFZyBRIDTVhQIh8KA1RMVhIKMjAyNy0wNC0xORoDTVhQKgJMWTIDMzgxGhwSCjIwMjctMDQtMjAoAGoFEgNNWFByBRIDVExWQgMBAQFIAZgBAQ==&hl=en&curr=ILS
- [G-RT-15] https://www.google.com/travel/flights/search?tfs=Gj4SCjIwMjctMDQtMTUoAGoFEgNUTFZyBRIDTVhQIiAKA1RMVhIKMjAyNy0wNC0xNRoDTVhQKgJXNDIENjQzMhocEgoyMDI3LTA0LTIwKABqBRIDTVhQcgUSA1RMVkIDAQEBSAGYAQE=&hl=en&curr=ILS
- [G-OW-MXPTLV20] https://www.google.com/travel/flights/search?tfs=GhwSCjIwMjctMDQtMjAoAGoFEgNNWFByBRIDVExWQgMBAQFIAZgBAg==&hl=en&curr=ILS
- [G-OW-MXPTLV20-ALL] https://www.google.com/travel/flights/search?tfs=GhoSCjIwMjctMDQtMjBqBRIDTVhQcgUSA1RMVkIDAQEBSAGYAQI=&hl=en&curr=ILS
- [G-OW-SAT17] https://www.google.com/travel/flights/search?tfs=GhwSCjIwMjctMDQtMTcoAGoFEgNUTFZyBRIDTVhQQgMBAQFIAZgBAg==&hl=en&curr=ILS
- [G-OW-FCO17] https://www.google.com/travel/flights/search?tfs=GhwSCjIwMjctMDQtMTcoAGoFEgNUTFZyBRIDRkNPQgMBAQFIAZgBAg==&hl=en&curr=ILS
- [G-OW-VRN] https://www.google.com/travel/flights/search?tfs=GhwSCjIwMjctMDQtMjAoAGoFEgNWUk5yBRIDVExWQgMBAQFIAZgBAg==&hl=en&curr=ILS
- [G-OW-VCE21] https://www.google.com/travel/flights/search?tfs=GhwSCjIwMjctMDQtMjEoAGoFEgNWQ0VyBRIDVExWQgMBAQFIAZgBAg==&hl=en&curr=ILS
- [K-RT] https://www.il.kayak.com/flights/TLV-MXP/2027-04-18/2027-04-20/3adults?sort=price_a&fs=stops=0
- [K-OW18] https://www.il.kayak.com/flights/TLV-MXP/2027-04-18/3adults?sort=price_a&fs=stops=0
- [K-OW21] https://www.il.kayak.com/flights/MXP-TLV/2027-04-21/3adults?sort=price_a&fs=stops=0
- [K-FCO17] https://www.il.kayak.com/flights/TLV-FCO/2027-04-17/3adults?sort=price_a&fs=stops=0
- [K-VRN] https://www.il.kayak.com/flights/VRN-TLV/2027-04-20/3adults?sort=price_a&fs=stops=0
- [K-VCE] https://www.il.kayak.com/flights/VCE-TLV/2027-04-21/3adults?sort=price_a&fs=stops=0
- [K-SAT17] https://www.il.kayak.com/flights/TLV-MIL/2027-04-17/3adults?sort=depart_b&fs=stops=0

## Facts shared by several itineraries

| Claim | Verdict | Evidence | Date |
|---|---|---|---|
| W4 6431 MXP 05:00 -> TLV 09:55 operates Tue 20 Apr and Wed 21 Apr 2027 (daily) | confirmed for the 05:00 departure; flight number could-not-verify on Wizz | [WIZZ-TT] lists MXP -> TLV departures 05:00 and 13:05 every day 12-25 Apr, plus 16:15 on Mon/Wed/Fri. Number 6431 appears on Google [G-OW-MXPTLV20] and in Kayak's result data [K-OW21]. Caveat: the winter-2026 flights at the same times are numbered W4 6405/6403/6406/6404 ([FC-MXP]) and [TRIP-STATUS] shows "W4 6431 cancelled" today, so book by time, not number | 17 Nov 2026 |
| W4 6432 10:50 and W4 6434 18:55 TLV -> MXP daily; W4 6436 22:05 Mon/Wed/Fri only | confirmed (times/days) | [WIZZ-TT]: 10:50 and 18:55 daily; 22:05 on 12, 14, 16, 19, 21, 23 Apr only. [TRIP-RT] shows 18:55 and 10:50 Wizz Air Malta to MXP T1 | 17 Nov 2026 |
| Wizz fares EUR 225 pp (18 Apr out) and EUR 200 pp (20 Apr 05:00 back) | confirmed first-hand | [WIZZ-TT]: TLV-MXP 18 Apr lowest EUR 224.99; MXP-TLV 20 Apr lowest EUR 199.99 (3 adults). At [ECB] 3.5674 = NIS 803 + 713 = 1,516 pp / 4,548 total | 17 Nov 2026 |
| LY 381 07:35 -> 10:45, LY 387 18:30 -> 21:40, LY 382 11:55 -> 16:40, LY 388 22:55 -> 03:40+1 on 18 / 20 Apr | confirmed on four aggregators; El Al site could-not-verify (booking.elal.com needs interactive input) | Same times on Google [G-RT-LY381], Kayak [K-RT], [TRIP-RT] / [TRIP-OW20] and [KIWI]. Numbers 381/387/382 in Kayak data. Current winter times differ ([FC-MXP]), so re-check after booking | 17 Nov 2026 |
| LY 388 does not operate Wed 21 Apr (holiday eve) | confirmed (Google only) | [G-RT-21] lists no 22:55 on 21 Apr | 17 Nov 2026 |
| Durations with time zones | confirmed | Recomputed with Israel UTC+3, Italy UTC+2, Greece UTC+3: all 15 itineraries match (e.g. 05:00 CEST = 03:00 UTC, 09:55 IDT = 06:55 UTC, 3h55). Overnight arrival dates (LY 388, 6H 352, W4 6036, LY 290) correct | - |
| per-person x 3 = total, add-on sums, ratios, Kayak percentages | confirmed | Recomputed every figure in flights.md; no arithmetic error found | - |
| Passover eve is Wed 21 Apr 2027 | confirmed | [HEBCAL-TLV]: "Erev Pesach 2027-04-21", Pesach I 22 Apr | 17 Nov 2026 |
| Sunset TLV Wed 21 Apr ~19:12; 12:00 cutoff | corrected (19:14; 7 h before = 12:14, so 12:00 holds) | [HEBCAL-TLV] sunset 19:14, candle lighting 18:54 | 17 Nov 2026 |
| Shabbat ends ~20:00 on Sat 17 Apr in Tel Aviv | corrected (Havdalah 19:49; 72-min opinion 20:23) | [HEBCAL-TLV] sunset 19:11, tzeit 8.5 deg 19:49, 72 min 20:23 | 17 Nov 2026 |
| No nonstop TLV -> Milan after nightfall on Sat 17 Apr | confirmed | [WIZZ-TT] Sat 17: 10:50 and 18:55 only; [G-OW-SAT17], [K-SAT17] (all Milan airports), [TRIP-OW17] show the same two Wizz flights and nothing else | 17 Nov 2026 |
| No TLV nonstop to BGY or LIN | confirmed for the trip dates | [WIZZ-MAP] BGY not direct; [ISRAIR] returns no TLV-BGY on 15, 16, 18, 19 Apr and no BGY-TLV on 20, 21 Apr; Google BGY/LIN nonstop queries empty. Note: [FC-BGY] lists a once-weekly Israir 6H 301 TLV-BGY from Jan 2027 (day of week not shown); it is not on sale for these dates. [FC-LIN]: no nonstop | 17 Nov 2026 |
| Neos and Bluebird absent | confirmed for the dates checked; April 2027 intentions could-not-verify | Not on Google, Kayak, Trip.com or Kiwi for 18-20 Apr; [FC-MXP] does not list them in Nov 2026. Their own sites were not readable | 17 Nov 2026 |
| Arkia only on Kayak; number not seen | corrected: IZ 337 (TLV 06:05 -> MXP 09:15, Sun 18 Apr) and IZ 338 (MXP 10:45 -> TLV 15:30, Wed 21 Apr) | Flight numbers read from Kayak's result data [K-OW18], [K-OW21]. arkia.co.il is behind a Cloudflare challenge: days of week and fare rules could-not-verify on Arkia's site. [FC-MXP] says Arkia TLV-MXP "starts in December" | 17 Nov 2026 |
| Pre-Passover Tuesday daytime returns cost 2-2.7x a normal week | confirmed (Google); consistent elsewhere | Google today: W4 6433 Tue 13 Apr 1,611 vs Tue 20 Apr 4,296 (2.67x); LY 382 2,328 vs 4,701 (2.02x) ([G-OW-MXPTLV20] and same query for 13 Apr). [TRIP-OW20]: 13:05 Wizz NIS 1,736 pp vs 05:00 Wizz 781 pp on 20 Apr | 17 Nov 2026 |
| Kayak is 7-9% lower because of currency conversion | corrected | Google matches the airlines' own prices: Wizz [WIZZ-TT] EUR 424.98 pp = NIS 1,516 vs Google 1,521; El Al's own price shown on [K-RT] NIS 2,928 pp vs Google 2,954; Israir's own USD 237 = NIS 769 vs Google 772. Kayak's lower rows are third-party agency prices. Other agencies are higher: [TRIP-RT] NIS 1,748 pp and [KIWI] NIS 4,886 for 3 for MIL-01 | 17 Nov 2026 |
| Google links open the right search | confirmed | Opened four link types in Chrome (round trip, round trip with W4 6434 selected, with LY 381 selected, one-way VRN): each showed the right route, dates, "3", nonstop and the same prices as the script. One load returned "No results" and worked on reload | 17 Nov 2026 |
| Wizz deep links | confirmed (page), flight list not shown | Link opens "18 APR 2027 - 20 APR 2027, 3 PASSENGERS, Tel-Aviv -> Milan Malpensa"; the flight list stays empty for an automated browser (HTTP 429 on search) | 17 Nov 2026 |
| Kayak links | confirmed | [K-RT] and the one-way links open the right route, date and 3 travellers | 17 Nov 2026 |

## Per itinerary

Google totals are today's re-run with the author's script (3 adults, ILS). "Was" = figure in flights.md.

### MIL-01

| Claim | Verdict | Evidence | Date |
|---|---|---|---|
| W4 6434 Sun 18:55 -> 22:10 and W4 6431 Tue 05:00 -> 09:55 exist | confirmed (times/days on Wizz; numbers on Google + Kayak) | [WIZZ-TT], [G-RT-W46434], [K-RT], [TRIP-RT], [KIWI] | 17 Nov 2026 |
| NIS 4,567 total / 1,522 pp | confirmed (now 4,564 / 1,521) | [G-RT-W46434] 4,564. Wizz direct EUR 424.98 pp = NIS 4,548 total ([WIZZ-TT], [ECB]). Kayak 4,162 / 1,388 [K-RT]; Kiwi 4,886 for 3 [KIWI]; Trip.com 1,748 pp [TRIP-RT] | 17 Nov 2026 22:46-22:50 UTC |
| Rules: Sunday out, lands Tue 09:55 | confirmed | - | - |
| Red-eye is reachable after the show | corrected (see "Resolved open items" 1-3): coach from Centrale works, the train only if the 22:45 metro is caught | [ATM-M2], [TRENORD], [CARONTE], [AUTOSTRADALE], [MXP-SHUTTLE], [WIZZ-CI] | Nov 2026 timetables |

### MIL-02

| Claim | Verdict | Evidence | Date |
|---|---|---|---|
| W4 6432 Sun 10:50 -> 14:05, W4 6431 back | confirmed | [WIZZ-TT], [G-RT], [K-RT], [TRIP-RT] | 17 Nov 2026 |
| NIS 5,373 / 1,791 pp | confirmed (now 5,370 / 1,790) | [G-RT] 5,370. Kayak 4,937 / 1,646 (was 4,917 / 1,639) [K-RT]; Kiwi 5,698 for 3; Trip.com 1,951 pp. Wizz's own price for the 10:50 flight could-not-verify (only the day's lowest fare is exposed) | 17 Nov 2026 |
| Rules | confirmed | - | - |

### MIL-03

| Claim | Verdict | Evidence | Date |
|---|---|---|---|
| LY 388 Tue 22:55 -> Wed 03:40 | confirmed on aggregators | [G-RT-W46434], [K-RT], [TRIP-OW20], [KIWI] | 17 Nov 2026 |
| NIS 7,122 / 2,374 pp | confirmed (now 7,117 / 2,372) | [G-RT-W46434]. Kayak 6,065 [K-RT]; Kiwi 6,750. Trip.com LY 388 one-way 5,001 for 3 vs Google 4,701 | 17 Nov 2026 |
| "home 15 h before the Passover-eve cutoff" (picks table) | corrected: 15.5 h before sunset, 8 h 20 before the 12:00 cutoff | [HEBCAL-TLV] sunset 19:14 | 17 Nov 2026 |
| Rules | confirmed (lands Wed 03:40) | - | - |

### MIL-04

| Claim | Verdict | Evidence | Date |
|---|---|---|---|
| LY 382 Tue 11:55 -> 16:40 | confirmed on aggregators | [G-RT-W46434], [K-RT], [TRIP-OW20] | 17 Nov 2026 |
| NIS 7,122 / 2,374 pp | confirmed (now 7,117) | [G-RT-W46434]; Kayak 6,717 / 2,239 (was 6,727) [K-RT]; Trip.com LY 382 one-way 4,866 for 3 | 17 Nov 2026 |

### MIL-05

| Claim | Verdict | Evidence | Date |
|---|---|---|---|
| W4 6433 Tue 13:05 -> 18:00 | confirmed | [WIZZ-TT] 13:05 daily; [G-RT-W46434]; [TRIP-OW20] | 17 Nov 2026 |
| NIS 6,716 / 2,239 pp | confirmed (now 6,712) | [G-RT-W46434]; Kayak now 6,088 / 2,030 (was 6,269 / 2,090) [K-RT]; Kiwi 6,813; Trip.com one-way 5,208 for 3 | 17 Nov 2026 |

### MIL-06

| Claim | Verdict | Evidence | Date |
|---|---|---|---|
| LY 381 / LY 382 (and LY 387 / LY 388 variants) | confirmed on aggregators; El Al site could-not-verify | [G-RT-LY381], [K-RT], [TRIP-RT] | 17 Nov 2026 |
| NIS 8,862 / 2,954 pp | confirmed (now 8,861) | [G-RT-LY381]; El Al's own price as displayed on Kayak NIS 2,928 pp [K-RT]; Kayak agencies 8,061 | 17 Nov 2026 |
| Trolley included on El Al Lite | could-not-verify on elal.com; secondary sources say the 8 kg trolley is taken at counter/gate and carried free in the hold on Europe routes | [ELAL-BAG]; [TRIP-RT] labels El Al "Carry-on baggage included" | 17 Nov 2026 |

### MIL-07

| Claim | Verdict | Evidence | Date |
|---|---|---|---|
| LY 381 out, W4 6431 back; NIS 6,579 / 2,193 pp | confirmed (now 6,578) | [G-RT-LY381]; Kayak 6,087 [K-RT]; Kiwi 6,900 | 17 Nov 2026 |

### MIL-08

| Claim | Verdict | Evidence | Date |
|---|---|---|---|
| Arkia Sun 06:05 -> 09:15, number not seen | corrected: IZ 337 | Kayak result data [K-OW18] | 17 Nov 2026 22:51 UTC |
| NIS 5,624 / 1,875 pp (Kayak) | confirmed on Kayak only | [K-RT] 5,624; Arkia one-way 3,792 [K-OW18]. Arkia's own site could-not-verify (Cloudflare) | 17 Nov 2026 |
| Arkia bag rules | could-not-verify | arkia.co.il not readable | 17 Nov 2026 |

### MIL-09

| Claim | Verdict | Evidence | Date |
|---|---|---|---|
| W4 6431 Wed 21 Apr 05:00 -> 09:55 | confirmed | [WIZZ-TT] 05:00 on 21 Apr; [G-RT-21]; [K-OW21] | 17 Nov 2026 |
| NIS 4,567 / 1,522 pp | confirmed (now 4,564) | [G-RT-21]; Kayak one-way 668 pp [K-OW21] | 17 Nov 2026 |
| Lands 09:55 on Passover eve, inside cutoff, flagged | confirmed (9 h 19 before sunset 19:14) | [HEBCAL-TLV] | 17 Nov 2026 |

### MIL-10

| Claim | Verdict | Evidence | Date |
|---|---|---|---|
| W4 6036 Sat 17 Apr 21:55 -> FCO 00:45 | confirmed (time/day on Wizz; number on Google + Kayak) | [WIZZ-TT] TLV-FCO 21:55 daily incl. Sat 17; [G-OW-FCO17]; [K-FCO17] | 17 Nov 2026 |
| NIS 4,084 flights (1,935 + 2,149) | confirmed (now 1,933 + 2,148 = 4,081) | [G-OW-FCO17], [G-OW-MXPTLV20]; Wizz own lowest 17 Apr EUR 179.99 = NIS 1,926 for 3; Kayak 1,762 | 17 Nov 2026 |
| "Shabbat ends ~20:00; leaves ~25 min" | corrected: Havdalah 19:49. Wizz airport check-in at TLV closes 70 min before departure (20:45); online check-in closes 3 h before (18:55, still Shabbat) and without a paid seat opens only 24 h before (Fri 21:55, already Shabbat). So: buy seats and check in online before Friday sunset, or reach the counter between 19:49 and 20:45 | [HEBCAL-TLV], [WIZZ-CI] | 17 Nov 2026 |
| Rome local time rule | confirmed | Departure 21:55 Israel = 20:55 Rome; Rome nightfall Sat 17 Apr 20:36 [HEBCAL-ROM] | 17 Nov 2026 |
| Train promo EUR 19.90-29.90, average 42-92 | corrected: Frecciarossa Roma Termini -> Milano Centrale Base EUR 95, Economy 74.90, Super Economy from 44.90, FrecciaDAYS 37.90; 2h59-3h16. April 2027 is on sale but only partly loaded. Italo could-not-verify | [TRENITALIA] | 17 Nov 2026 |
| Taxi from FCO needed, fare not sourced | corrected: fixed fare EUR 55 to central Rome (secondary); Leonardo Express last departures 23:23 and 23:53 (Dec 2026 timetable) | https://www.hemenhesap.com (secondary; exact page not recorded, Roma Capitale tariff page not read), [TRENITALIA] | 17 Nov 2026 |

### MIL-11

| Claim | Verdict | Evidence | Date |
|---|---|---|---|
| 6H 352 VRN Tue 20 Apr 21:35 -> TLV Wed 02:05 | confirmed on the airline's site | [ISRAIR] shows "[6H352] 21:35 -> 02:05 +1, direct, 3:30" | 17 Nov 2026 22:55 UTC |
| NIS 2,313 for 3 (771 pp) | confirmed | [ISRAIR] USD 237 pp = NIS 769 pp / 2,308 at [ECB]; Google 2,315 [G-OW-VRN]; Kayak 1,964 [K-VRN] | 17 Nov 2026 |
| Israir trolley USD 30 pre-booked | confirmed, plus: EUR 35 if bought at a station abroad (Verona); checked 23 kg USD 65 | [ISRAIR-BAG] | 17 Nov 2026 |
| Train from EUR 13, average 22, 1h13 / 1h52 | confirmed: regional EUR 12.75 fixed (1h53), Frecciarossa Base 33 / Super Economy 15.90-23.90 (1h14) | [TRENITALIA] | 17 Nov 2026 |
| Verona station -> airport not researched | corrected: Airlink bus EUR 7, every 20 min, 15 min ride; last departure could-not-verify | [ATV-VRN] | 17 Nov 2026 |
| Rules (lands Wed 02:05) | confirmed | - | - |

### MIL-12

| Claim | Verdict | Evidence | Date |
|---|---|---|---|
| W4 6717 VCE Wed 21 Apr 05:30 -> 10:05; not Tue/Thu | confirmed (time/day on Wizz; number on Google + Kayak) | [WIZZ-TT] VCE-TLV 05:30 on 16, 19, 21, 23 Apr only; [G-OW-VCE21]; [K-VCE]. Winter number is W4 6735 (https://www.flightconnections.com, secondary), so book by time | 17 Nov 2026 |
| NIS 817 for 3 (272 pp) | confirmed | [WIZZ-TT] EUR 75.99 = NIS 813 for 3; Google 817; Kayak 746 | 17 Nov 2026 |
| Lands Wed 10:05 on Passover eve: flagged? | confirmed: flagged as "OK (flagged)", "highest-risk option", "under 2 h of slack" (1 h 55 to the 12:00 cutoff; 9 h 09 before sunset). Not in the recommended picks | [HEBCAL-TLV] | 17 Nov 2026 |
| Milan -> Venice fare budget EUR 20-50 | confirmed: Frecciarossa Base EUR 49, Economy 37.90, Super Economy 22.90, FrecciaDAYS 19.90, 2h28-2h30; regional 22.40 (3h28) | [TRENITALIA] | 17 Nov 2026 |
| VCE transfer for 05:30 not researched | corrected: first ATVO buses from Mestre station 04:20 and 05:00 (20 min); the 04:20 leaves ~50 min before departure. Taxi from Mestre EUR 35-40 (secondary) | [ATVO] | timetable valid to 24 Apr 2027 |
| LY 290 VCE Tue 22:05 -> Wed 02:25, 3,553 | confirmed (Google only; now 3,551) | https://www.google.com/travel/flights/search?tfs=GhwSCjIwMjctMDQtMjAoAGoFEgNWQ0VyBRIDVExWQgMBAQFIAZgBAg==&hl=en&curr=ILS | 17 Nov 2026 |

### MIL-13

| Claim | Verdict | Evidence | Date |
|---|---|---|---|
| A3 661 MXP 10:15 -> ATH 13:40, A3 926 ATH 17:00 -> TLV 19:00; 2,413 for 3 | confirmed (Google only; now 2,411). Aegean site could-not-verify (HTTP 403) | [G-OW-MXPTLV20-ALL] | 17 Nov 2026 |
| Sky Express GQ 831 / GQ 720, 1,842 for 3 | confirmed (now 1,841; Kayak 1,752) | [G-OW-MXPTLV20-ALL]; Kayak https://www.il.kayak.com/flights/MXP-TLV/2027-04-20/3adults?sort=price_a | 17 Nov 2026 |
| Aegean is the cheapest sensible Tuesday 1-stop | corrected: a cheaper Aegean option was missed: A3 665 MXP 19:25 -> ATH 22:50, A3 928 ATH 00:40 -> TLV Wed 02:45, NIS 2,121 for 3 (707 pp), 6h20, lands before the Passover-eve cutoff | [G-OW-MXPTLV20-ALL] | 17 Nov 2026 22:47 UTC |
| Aegean / Sky Express cabin bag | Sky Express confirmed (8 kg 55x40x23 + personal item on the cheapest fares); Aegean Light could-not-verify | [SKYEXP] | 17 Nov 2026 |

### MIL-14

| Claim | Verdict | Evidence | Date |
|---|---|---|---|
| LY 381 Mon 19 Apr 07:35 -> 10:45; 7,409 with W4 6431 | confirmed (Google only; now 7,408) | [G-RT-19] | 17 Nov 2026 |
| Arkia Mon 19 Apr 06:05 variant | could-not-verify today (not re-queried; Arkia site unreadable) | [K-OW18] covers Sun 18 only | 17 Nov 2026 |

### MIL-15

| Claim | Verdict | Evidence | Date |
|---|---|---|---|
| W4 6432 Thu 15 Apr 10:50 -> 14:05; 5,051 with W4 6431 | schedule confirmed; price confirmed on Google (now 5,048) but Wizz's own lowest fare that day is higher | [G-RT-15] 5,048 (outbound 2,900 = EUR 270 pp). [WIZZ-TT] shows EUR 299.99 pp as the lowest TLV-MXP fare on 15 Apr for 3 adults (= NIS 3,211 for 3, +11% on that leg, about +6% on the total). Expect up to ~NIS 5,360 | 17 Nov 2026 |
| Friday W4 6432 variant lands 14:05, "well before sunset" | wrong under the trip rule: Milan sunset Fri 16 Apr is 20:10, so 14:05 is 6 h 05 before sunset, less than the ~7 h required for a Friday landing (cutoff ~13:10). LY 381 Fri (10:05) and Arkia Fri (08:00 / 09:15) pass | [HEBCAL-MIL] | 17 Nov 2026 |
| Milan sunset ~20:05 (author's estimate) | corrected: 20:10 | [HEBCAL-MIL] | 17 Nov 2026 |

## Resolved open items

1. **M2 after the show.** Mon-Fri departures from Assago Milanofiori Forum towards the city: 22:15, 22:45, 23:15, 23:39, 00:09, last 00:17; about 15 min to Cadorna and 24 min to Centrale ([ATM-M2], timetable valid from 26 Oct 2026). Extra post-concert trains: could-not-verify.
2. **Last Malpensa Express.** Centrale 23:25 (T1 00:18), Cadorna 23:26 (T1 00:04); EUR 15 ([TRENORD], June 2026 timetable). The ~01:00 Cadorna trains are seasonal (Mondays/holidays until late September). Only the 22:45 metro connects (Cadorna 23:00 / Centrale 23:09); the 23:15 metro misses both.
3. **Night coaches Centrale -> MXP T1 (70 min).** Caronte 22:05, 23:05, 00:05, 01:05, 03:05, EUR 10 ([CARONTE], valid from 16 Nov 2026). Autostradale 22:20, 22:50, 23:20, then 00:50, then 03:20, EUR 4.99 online ([AUTOSTRADALE]); the author's "every 30 min until 00:50" (from [SEA-COACH]) is wrong between 23:20 and 00:50. Malpensa Shuttle 23:10, 23:40, 02:10, 03:40, EUR 10 ([MXP-SHUTTLE]). Terravision night times could-not-verify. Usable: 00:05, 00:50, 01:05 (arrive 01:15-02:15) and 02:10 (arrives 03:20, 40 min before check-in closes). The 03:05 / 03:20 buses arrive after check-in closes.
4. **Wizz check-in at MXP.** Opens 180 min, closes 60 min before departure: 02:00-04:00 for the 05:00 flight; online check-in closes 3 h before ([WIZZ-CI]). An extra Israel-specific security lead time could-not-verify.
5. **Terminal.** Wizz uses MXP Terminal 1 ([TRIP-RT] / [TRIP-OW20] show "MXP T1"); coaches stop at T1 ([SEA-COACH]).
6. **MXP overnight.** Open 24 h landside per [SLEEP-MXP] (secondary); no official SEA statement found.
7. **Taxi.** Fixed fare EUR 114 is official for Malpensa <-> any street in the City of Milan ([TAXI-LOMB], since 1 Jul 2024). Assago is not on the fixed-fare list, so the ride is metered; no sourced metered total. Pre-booked private sedan Assago -> MXP for 3: EUR 125 = about NIS 448 total / 149 pp ([TRANSFER], secondary, not date-specific). Uber / Welcome Pickups could-not-verify.
8. **Arena bags.** Secondary report for a 2025 Forum concert: suitcases, trolleys and backpacks not admitted, bags up to 15 litres allowed ([FORUM-BAGS]); the venue's own page defers to the organiser. Plan luggage storage for Monday.
9. **Wizz own prices.** Confirmed through Wizz's timetable endpoint ([WIZZ-TT]); see shared facts.
10. **WIZZ Priority.** Official range EUR 10-60 online, EUR 65-75 at the airport confirmed ([WIZZ-PRIO]). The price on TLV-MXP for these dates could-not-verify (it is only shown after flight selection, which is blocked). All-in MIL-01 with one trolley each stays NIS 1,594-1,952 pp; the NIS 1,736 planning figure remains an assumption.
11. **Israir bags.** Confirmed on israir.co.il ([ISRAIR-BAG]).
12. **Train fares.** Trenitalia fares read from the booking engine ([TRENITALIA]); see MIL-10/11/12.
13. **ETIAS.** Official site: "ETIAS is currently not in operation"; no start date published; fee EUR 20; Israel is a visa-exempt country that will need it once live; after launch there is a transitional period of at least six months in which travellers without ETIAS are not refused entry ([ETIAS], page updated 21 Oct 2026). So nothing can be applied for today and it is not expected to block an April 2027 trip, but re-check in March 2027. EES (biometric registration at the border) is in operation (secondary: https://www.connexionfrance.com).
14. **Tel Aviv nightfall, Passover eve, sunsets.** See shared facts ([HEBCAL-TLV], [HEBCAL-MIL], [HEBCAL-ROM]).

## Remaining unknowns

- Flight-level Wizz prices other than each day's lowest fare, and the Priority/trolley price for these flights (Wizz search API returns HTTP 429).
- Wizz flight numbers for summer 2027 on Wizz's own site (times and days are confirmed; numbers come from Google and Kayak only, and differ from the numbers flying this winter).
- El Al: own-site schedule and fare brand for April 2027; Lite bag rules from elal.com (site not readable by script).
- Arkia: own-site schedule, days of operation, fares and bag rules (Cloudflare block). IZ 337 / IZ 338 come from Kayak's data only.
- Neos and Bluebird plans for April 2027 (own sites not readable).
- All ground timetables are the ones valid in Nov 2026; April 2027 editions are not published. Whether ATM runs extra M2 trains after Forum concerts.
- Metered taxi fare Assago -> MXP; Uber price; whether MXP applies an earlier cut-off for Tel Aviv flights.
- Official statement that MXP T1 stays open landside overnight.
- Luggage storage on show day (arena policy for this event, and opening hours of storage at Centrale late at night).
- Italo fares; Aegean Light cabin-bag allowance; El Al checked-bag price; last Verona Airlink departure; FCO taxi tariff on Roma Capitale's own page; night bus from FCO.
- Seat availability beyond "3 seats priced".

## Changes applied

`flights.md`:

1. Header: added the fact-check date line.
2. "How to read the prices": replaced the currency-conversion explanation of the Kayak gap with the agency-price explanation; noted Wizz's own EUR fares are confirmed.
3. Recommended picks: MIL-03 wording ("15 h before the cutoff" -> 15.5 h before sunset / 8 h 20 before cutoff); MIL-10 row now warns about check-in and gives the Trenitalia fare range; trolley sentence notes the route price is still unverified.
4. Constraint summary: nightfall Sat 17 Apr 19:49 (20:23 by the 72-minute opinion); sunset Wed 21 Apr 19:14.
5. Schedule table: Arkia flight numbers IZ 337 / IZ 338; added a note that Wizz times/days are confirmed on Wizz and that winter flight numbers differ.
6. BGY bullet: added the Israir and Wizz checks and the 6H 301 note.
7. Bags table: Wizz, El Al, Israir, Aegean rows updated with what was verified.
8. Arena -> Malpensa section: sourced check-in window, corrected metro, train, coach and taxi rows, added bag-policy note.
9. Every itinerary MIL-01..MIL-15: added a `fact_check` line under `verification` with today's result (the original `verification` text is unchanged, except MIL-08 where the Arkia flight number was filled in).
10. MIL-10: train fares, FCO taxi, all-in range and the Saturday-night check-in constraint.
11. MIL-11: train fares, Airlink bus, Israir trolley price at Verona, all-in range.
12. MIL-12: train fares and Venice airport transfer.
13. MIL-13: added the missed A3 665 / A3 928 option.
14. MIL-15: Friday W4 6432 variant marked FAIL (lands 6 h 05 before Milan sunset); Thursday fare caveat (Wizz shows EUR 299.99).
15. Cross-check section: Kayak-gap bullet and wizzair.com bullet rewritten.
16. Open items: resolved items struck from the list, pointer to this file, Milan sunset corrected.

`sources.md`: added a "Fact-check sources (2026-11-17/18)" section with the new URLs; noted that the scripts now live in `milan/scripts/`.

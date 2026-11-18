# Lisbon flights - sources

All checked 17 Nov 2026 23:52 to 18 Nov 2026 00:22 (Israel time). Every search used 3 adults, economy.

## Method

- **Google Flights** was read by requesting the public results page (`/travel/flights/search?tfs=...&hl=en&curr=ILS`) and parsing the itinerary data embedded in it: flight numbers, airports, local times, layovers and the price for 3 adults in ILS. Round-trip prices for a specific pair of flights were read by pinning the outbound flight in the URL and reading the list of returns. The embedded data holds only the first batch of results per search (about 5-16), so searches were narrowed with stops, departure-hour and airline filters to bring specific flights into view.
- **Kayak Israel** (il.kayak.com) pages were loaded in headless Chrome and each result card expanded to read flight numbers, per-person and total NIS price, fare name and the carry-on / checked-bag counts. Bag cost was tested by adding Kayak's "1 carry-on bag" filter (`cfc=1`) and comparing prices.
- Scripts and raw captures are in `a temporary scratch folder (lisbon/)` (`gf.py`, `rt.py`, `kayak.py`, `ksum.py`; captures in `cache/` and `web/`). That folder is temporary.
- No personal details were sent to any site. Nothing was booked or held.

## Google Flights searches

| URL | Supported | Checked |
|---|---|---|
| https://www.google.com/travel/flights/search?tfs=GhoSCjIwMjctMDQtMTNqBRIDVExWcgUSA0xJU0IDAQEBSAGYAQI=&hl=en&curr=ILS | TLV -> LIS Tue 13 Apr one-way list and prices | 17 Nov 23:57, 18 Nov 00:01 |
| https://www.google.com/travel/flights/search?tfs=GhoSCjIwMjctMDQtMTRqBRIDVExWcgUSA0xJU0IDAQEBSAGYAQI=&hl=en&curr=ILS | TLV -> LIS Wed 14 Apr one-way list | 17 Nov 23:57 |
| https://www.google.com/travel/flights/search?tfs=GhoSCjIwMjctMDQtMTJqBRIDVExWcgUSA0xJU0IDAQEBSAGYAQI=&hl=en&curr=ILS | TLV -> LIS Mon 12 Apr one-way list | 17 Nov 23:58 |
| https://www.google.com/travel/flights/search?tfs=GhoSCjIwMjctMDQtMTVqBRIDVExWcgUSA0xJU0IDAQEBSAGYAQI=&hl=en&curr=ILS | TLV -> LIS Thu 15 Apr (show-day arrivals) | 17 Nov 23:58 |
| Same search for Sun 11 Apr, and nonstop-only variants for 11-15 Apr | Operating days and times of TP1604, LY375, LY371 | 17 Nov 23:56 |
| https://www.google.com/travel/flights/search?tfs=Gh4SCjIwMjctMDQtMTVAFkgXagUSA0xJU3IFEgNUTFZCAwEBAUgBmAEC&hl=en&curr=ILS | LIS -> TLV Thu 15 Apr departing 22:00-23:59: LY376, A3723 + A3924, TP1040, TP1938 | 17 Nov 23:53 |
| https://www.google.com/travel/flights/search?tfs=GhoSCjIwMjctMDQtMTVqBRIDTElTcgUSA1RMVkIDAQEBSAGYAQI=&hl=en&curr=ILS | LIS -> TLV Thu 15 Apr, all departures (TP1603 20:50, LY376 22:15) | 17 Nov 23:53 |
| https://www.google.com/travel/flights/search?tfs=Gh4SCjIwMjctMDQtMTZAAEgJagUSA0xJU3IFEgNUTFZCAwEBAUgBmAEC&hl=en&curr=ILS | LIS -> TLV Fri 16 Apr departing 00:00-09:59: 16 itineraries, earliest TLV arrival 15:25 | 17 Nov 23:53 |
| https://www.google.com/travel/flights/search?tfs=GhoSCjIwMjctMDQtMTZqBRIDTElTcgUSA1RMVkIDAQEBSAGYAQI=&hl=en&curr=ILS | LIS -> TLV Fri 16 Apr, default list | 17 Nov 23:52 |
| LIS -> X one-way Thu 15 Apr, nonstop, departing 22:00-23:59, for X = ATH, IST, SAW, BEG, SOF, OTP, LCA, PFO, BUD, VIE, WAW, KRK, FCO, MXP, BCN, MAD, FRA, MUC, ZRH, CDG, AMS, LHR, SKG, HER, RHO, TBS, BUS, PRG, BER, MLA, TIA, IAS, CLJ | Late-night departures from Lisbon: only ATH 23:40, BEG 23:00, BCN 22:40, MAD 22:00 returned flights. KRK and SKG hit a bot check and were not retried | 17 Nov 23:54 |
| https://www.google.com/travel/flights/search?tfs=GiASCjIwMjctMDQtMTUoAEAXSBdqBRIDTElTcgUSA0FUSEIDAQEBSAFqBBABGACYAQI=&hl=en&curr=ILS | LIS -> ATH Thu 15 Apr, A3723 23:40 -> 05:35, ₪1,417 x3 | 17 Nov 23:53, 18 Nov 00:00 |
| https://www.google.com/travel/flights/search?tfs=GhoSCjIwMjctMDQtMTZqBRIDQVRIcgUSA1RMVkIDAQEBSAGYAQI=&hl=en&curr=ILS | ATH -> TLV Fri 16 Apr: 6H564, A3928, GQ720, W4 8402, LY542, A3924, 6H562 | 17 Nov 23:55 |
| BEG -> TLV, BCN -> TLV, LCA -> TLV, MAD -> TLV, OPO -> TLV one-way Fri 16 Apr | Onward options from other late-night destinations; none lands by 12:00 except from Athens | 17 Nov 23:55, 18 Nov 00:10 |
| https://www.google.com/travel/flights/search?tfs=GhoSCjIwMjctMDQtMTdqBRIDTElTcgUSA1RMVkIDAQEBSAGYAQI=&hl=en&curr=ILS | LIS -> TLV Sat 17 Apr, incl. departures 21:00-23:59 (FB564, 5F5812, TP1938) | 17 Nov 23:56 |
| OPO, MAD, BCN, FAO, SVQ -> TLV Sat 17 Apr departing 21:00-23:59; OPO -> TLV nonstop 15-18 Apr; TLV -> OPO nonstop 12-14 Apr | Nearby-airport options; TP1607 / TP1608 / LY373 days | 17 Nov 23:58 |
| https://www.google.com/travel/flights/search?tfs=Gh4SCjIwMjctMDQtMThAAEgMagUSA0xJU3IFEgNUTFZCAwEBAUgBmAEC&hl=en&curr=ILS | LIS -> TLV Sun 18 Apr departing 00:00-12:59 (A3723 00:40, Lufthansa, Iberia) | 17 Nov 23:56 |
| https://www.google.com/travel/flights/search?tfs=Gh4SCjIwMjctMDQtMThACUgXagUSA0xJU3IFEgNUTFZCAwEBAUgBmAEC&hl=en&curr=ILS | LIS -> TLV Sun 18 Apr departing 09:00-23:59 (TP1603, LY376, UX, GQ) | 18 Nov 00:00 |
| https://www.google.com/travel/flights/search?tfs=Gh4SCjIwMjctMDQtMTlAAEgLagUSA0xJU3IFEgNUTFZCAwEBAUgBmAEC&hl=en&curr=ILS | LIS -> TLV Mon 19 Apr departing 00:00-11:59 | 17 Nov 23:56 |
| https://www.google.com/travel/flights/search?tfs=GlwSCjIwMjctMDQtMTNqBRIDVExWcgUSA0xJUyIfCgNUTFYSCjIwMjctMDQtMTMaA0FUSCoCQTMyAzkyNSIfCgNBVEgSCjIwMjctMDQtMTMaA0xJUyoCQTMyAzcyMhoaEgoyMDI3LTA0LTE4agUSA0xJU3IFEgNUTFZCAwEBAUgBmAEB&hl=en&curr=ILS | Round trip, Aegean out Tue 13 pinned, returns Sun 18: ₪4,973 with A3723 + A3924 (LIS-01) | 18 Nov 00:02 |
| https://www.google.com/travel/flights/search?tfs=GlwSCjIwMjctMDQtMTJqBRIDVExWcgUSA0xJUyIfCgNUTFYSCjIwMjctMDQtMTIaA0FUSCoCQTMyAzkyNSIfCgNBVEgSCjIwMjctMDQtMTIaA0xJUyoCQTMyAzcyMhoaEgoyMDI3LTA0LTE4agUSA0xJU3IFEgNUTFZCAwEBAUgBmAEB&hl=en&curr=ILS | Round trip, Aegean out Mon 12 pinned: ₪4,640 (LIS-02) | 18 Nov 00:15 |
| https://www.google.com/travel/flights/search?tfs=GlwSCjIwMjctMDQtMTNqBRIDVExWcgUSA0xJUyIfCgNUTFYSCjIwMjctMDQtMTMaA0FUSCoCQTMyAzkyNSIfCgNBVEgSCjIwMjctMDQtMTMaA0xJUyoCQTMyAzcyMhoaEgoyMDI3LTA0LTE5agUSA0xJU3IFEgNUTFZCAwEBAUgBmAEB&hl=en&curr=ILS | Round trip, Aegean out Tue 13 pinned, return Mon 19 00:40: ₪5,381 (LIS-13) | 18 Nov 00:15 |
| https://www.google.com/travel/flights/search?tfs=GlwSCjIwMjctMDQtMTNqBRIDVExWcgUSA0xJUyIfCgNUTFYSCjIwMjctMDQtMTMaA0FUSCoCQTMyAzkyNSIfCgNBVEgSCjIwMjctMDQtMTMaA0xJUyoCQTMyAzcyMhoaEgoyMDI3LTA0LTE1agUSA0xJU3IFEgNUTFZCAwEBAUgBmAEB&hl=en&curr=ILS | Round trip, Aegean out Tue 13 pinned, return Thu 15 23:40 through ticket: ₪4,640 (rejected, lands 12:50) | 18 Nov 00:02 |
| https://www.google.com/travel/flights/search?tfs=GjsSCjIwMjctMDQtMTNqBRIDVExWcgUSA0xJUyIfCgNUTFYSCjIwMjctMDQtMTMaA0xJUyoCTFkyAzM3NRoaEgoyMDI3LTA0LTE4agUSA0xJU3IFEgNUTFZCAwEBAUgBmAEB&hl=en&curr=ILS | Round trip, LY375 Tue 13 pinned: TP1603 ₪8,388, LY376 ₪9,081 (LIS-03, LIS-06) | 18 Nov 00:02, 00:15 |
| https://www.google.com/travel/flights/search?tfs=GjsSCjIwMjctMDQtMTRqBRIDVExWcgUSA0xJUyIfCgNUTFYSCjIwMjctMDQtMTQaA0xJUyoCTFkyAzM3NRoaEgoyMDI3LTA0LTE4agUSA0xJU3IFEgNUTFZCAwEBAUgBmAEB&hl=en&curr=ILS | Round trip, LY375 Wed 14 pinned: TP1603 ₪9,667, LY376 ₪10,351 (LIS-09) | 18 Nov 00:02 |
| https://www.google.com/travel/flights/search?tfs=GjwSCjIwMjctMDQtMTNqBRIDVExWcgUSA0xJUyIgCgNUTFYSCjIwMjctMDQtMTMaA0xJUyoCVFAyBDE2MDQaGhIKMjAyNy0wNC0xOGoFEgNMSVNyBRIDVExWQgMBAQFIAZgBAQ==&hl=en&curr=ILS | Round trip, TP1604 Tue 13 pinned: TP1603 ₪9,950 (LIS-05). Same check for Thu 15 (LIS-15) | 18 Nov 00:02, 00:14 |
| https://www.google.com/travel/flights/search?tfs=GjwSCjIwMjctMDQtMTJqBRIDVExWcgUSA0xJUyIgCgNUTFYSCjIwMjctMDQtMTIaA0xJUyoCVFAyBDE2MDQaGhIKMjAyNy0wNC0xOGoFEgNMSVNyBRIDVExWQgMBAQFIAZgBAQ==&hl=en&curr=ILS | Round trip, TP1604 Mon 12 pinned: TP1603 ₪8,183 (LIS-14) | 18 Nov 00:14 |
| https://www.google.com/travel/flights/search?tfs=Gl0SCjIwMjctMDQtMTRqBRIDVExWcgUSA0xJUyIfCgNUTFYSCjIwMjctMDQtMTQaA0ZSQSoCTEgyAzY4NyIgCgNGUkESCjIwMjctMDQtMTQaA0xJUyoCTEgyBDExNzIaGhIKMjAyNy0wNC0xOGoFEgNMSVNyBRIDVExWQgMBAQFIAZgBAQ==&hl=en&curr=ILS | Round trip, Lufthansa Wed 14 pinned: returns Sun 18 ₪6,081 (05:05) and ₪6,337 (06:15) (LIS-08) | 18 Nov 00:02 |
| https://www.google.com/travel/flights/search?tfs=Gl0SCjIwMjctMDQtMTRqBRIDVExWcgUSA0xJUyIgCgNUTFYSCjIwMjctMDQtMTQaA01BRCoCSUIyBDE4NzIiHwoDTUFEEgoyMDI3LTA0LTE1GgNMSVMqAklCMgM1MjkaGhIKMjAyNy0wNC0xOGoFEgNMSVNyBRIDVExWQgMBAQFIAZgBAQ==&hl=en&curr=ILS | Round trip, Iberia Wed 14 pinned: ₪6,879 with IB532 + IB1873 (rejected) | 18 Nov 00:02 |
| https://www.google.com/travel/flights/search?tfs=Gh4SCjIwMjctMDQtMTQyAkEzagUSA1RMVnIFEgNMSVMaIhIKMjAyNy0wNC0xODICQTNAAEgBagUSA0xJU3IFEgNUTFZCAwEBAUgBmAEB&hl=en&curr=ILS | Round trip filtered to Aegean, Wed 14 out, return 00:00-01:59 Sun 18: ₪5,106 for A3929 + A3722 (LIS-10) | 17 Nov 23:59 |
| https://www.google.com/travel/flights/search?tfs=GhwSCjIwMjctMDQtMTMoAGoFEgNUTFZyBRIDT1BPQgMBAQFIAZgBAg==&hl=en&curr=ILS | TLV -> OPO Tue 13 nonstop, TP1608 ₪5,455 x3 (LIS-12) | 17 Nov 23:58 |

Not obtained from Google: multi-city (open-jaw) prices returned no data; one pinned round-trip check (Aegean Wed 14) was blocked by a bot check; Google's bag filters did not change the embedded prices, so they were not used for bag costs.

## Kayak Israel searches

| URL | Supported | Checked |
|---|---|---|
| https://www.il.kayak.com/flights/ATH-TLV/2027-04-16/3adults?sort=depart_a&fs=stops=0 | ATH -> TLV Fri 16 nonstops incl. Arkia 09:40 -> 11:35 and Israir, which Google omits | 18 Nov 00:05 |
| https://www.il.kayak.com/flights/ATH-TLV/2027-04-16/3adults?sort=depart_a&fs=stops=0;takeoff=0900,1100 | Flight numbers: Arkia 212 (operated by Bul Air) ₪664 pp; Wizz Air 8402 ₪265 pp; El Al 542 ₪923 pp; Aegean 924 ₪441 pp | 18 Nov 00:06 |
| https://www.il.kayak.com/flights/ATH-TLV/2027-04-16/3adults?sort=depart_a&fs=stops=0;takeoff=0900,1100;cfc=1 | Same with a carry-on included: Arkia ₪734, Wizz ₪419, El Al and Aegean unchanged | 18 Nov 00:20 |
| https://www.il.kayak.com/flights/LIS-TLV/2027-04-15/3adults?sort=arrive_a&fs=takeoff=2230,2359 | LIS -> TLV Thu 15 after 22:30 sorted by arrival: 12:00 (A3723 + W4 8402, ₪870 pp), 12:45, 12:50, then 15:50 and later | 18 Nov 00:07 |
| https://www.il.kayak.com/flights/LIS-ATH/2027-04-15/3adults?sort=depart_b&fs=stops=0 | LIS -> ATH Thu 15: Aegean 723 23:40 -> 05:35, ₪450 pp (also https://www.kayak.com/flights/LIS-ATH/2027-04-15/3adults?sort=depart_b&fs=stops=0 in USD: $119 pp) | 18 Nov 00:04, 00:19 |
| https://www.il.kayak.com/flights/LIS-TLV/2027-04-18/3adults?sort=depart_a&fs=takeoff=0000,0200 | LIS -> TLV Sun 18 00:40: Aegean 723 + 924 ₪774 pp | 18 Nov 00:09 |
| https://www.il.kayak.com/flights/LIS-TLV/2027-04-18/3adults?sort=depart_a&fs=stops=0 (and with `;cfc=1`) | Sun 18 nonstops: TAP 1603 ₪1,410 pp, El Al 376 ₪2,172 pp, codeshare prices; unchanged with carry-on | 18 Nov 00:08, 00:22 |
| https://www.il.kayak.com/flights/LIS-TLV/2027-04-17/3adults?sort=depart_a&fs=takeoff=2100,2359 | Sat 17 departures after 21:00: 50 self-transfer combinations, none better than Aegean 00:40 | 18 Nov 00:11 |
| https://www.il.kayak.com/flights/TLV-LIS/2027-04-13/3adults?sort=depart_a&fs=stops=0 (and with `;cfc=1`) | Tue 13 nonstops: TAP 1604 ₪1,868 pp, El Al 371 ₪2,048, El Al 375 ₪1,523; no Arkia; unchanged with carry-on | 18 Nov 00:12, 00:21 |
| https://www.il.kayak.com/flights/TLV-LIS/2027-04-13/3adults?sort=price_a | Tue 13 cheapest: Aegean 925 + 722 ₪784 pp; Aegean 929 + 720 ₪817 pp | 18 Nov 00:14 |
| https://www.il.kayak.com/flights/TLV-LIS/2027-04-14/3adults?sort=depart_a&fs=stops=0 | Wed 14 nonstops: TAP 1604 ₪2,487 pp, El Al 375 ₪2,048; no Arkia | 18 Nov 00:14 |
| https://www.il.kayak.com/flights/TLV-LIS/2027-04-14/3adults?sort=price_a | Wed 14 cheapest: Smartwings 1287 + 1176 ₪879 pp; Aegean 929 + 722 ₪904 pp | 18 Nov 00:16 |
| https://www.il.kayak.com/flights/TLV-LIS/2027-04-13/2027-04-18/3adults?sort=price_a | Round trips 13 -> 18: Lufthansa ₪2,023 / ₪2,098 pp; El Al + TAP nonstop ₪2,552; El Al + Aegean ₪2,303; Aegean + TAP ₪2,245 | 18 Nov 00:18 |

## Other pages

| URL | Supported | Checked |
|---|---|---|
| https://www.flightconnections.com/flights-from-lis-to-ath | Confirms Aegean, Sky Express and TAP operate LIS -> ATH nonstop; April day-by-day schedule not readable | 18 Nov 00:03 |
| https://www.flightsfrom.com/TLV-LIS, /LIS-ATH, /ATH-TLV | Returned HTTP 403; nothing obtained | 18 Nov 00:03 |
| https://www.kayak.com/flights/LIS-TLV/2027-04-15/3adults | Plain fetch returned no results (needs a browser); superseded by the il.kayak.com captures | 18 Nov 00:03 |
| https://www.wizzair.com/static_fe/metadata.json | Returned 404; Wizz's own timetable not obtained | 18 Nov 00:04 |
| https://www.aegeanhub.com/en/passenger-services-and-procedures/baggage/baggage-policy | Aegean Light: no free checked bag (via web search summary) | 18 Nov 00:17 |
| https://ssr-weu2.wizzair.com/en-gb/information-and-services/prices-discounts/fares-bundles | Wizz Basic: one free under-seat bag 40 x 30 x 20 cm (via web search summary) | 18 Nov 00:17 |
| https://loudavymkrokem.cz/en/wizz-air-luggage/ · https://airadvisor.com/en-us/baggage-allowance/wizz-air | WIZZ Priority (trolley) price is dynamic, roughly EUR 5-60; secondary sources | 18 Nov 00:17 |
| https://www.flytap.com/en-us/baggage/hold-baggage · https://aifly.one/guides/tap-air-portugal-baggage-allowance/ | TAP: cabin bag plus personal item on all fares; checked-bag inclusion varies by fare; secondary and conflicting | 18 Nov 00:17 |
| https://onemileatatime.com/news/el-al-carry-on-restriction-economy-lite-fares/ · https://www.israelhayom.com/2025/05/20/el-al-changes-policy-angers-passengers/ | El Al Lite on Europe routes: cabin bag may have to be checked at the counter or gate | 18 Nov 00:17 |
| README.md | Starting point: show times, earlier Friday list (15:25 earliest), nonstop operators | 17 Nov 23:50 |

## Given by the requester, not checked here

- Sunset in Tel Aviv on Fri 16 Apr 2027 about 19:08; Saturday nightfall about 20:00 Israel time and about 20:40 in Lisbon. **Checked in the fact-check:** sunset 19:10; nightfall 19:49 Tel Aviv, 20:56 Lisbon, 20:43 Athens.
- Show ends about 22:00; arena about 10 minutes from LIS airport. **Checked in the fact-check:** likely end 22:35-22:45; arena about 4 km from the airport.
- Passover 2027 begins the evening of Wed 21 Apr. **Checked in the fact-check:** confirmed.

## Fact-check sources (18 Nov 2026, 00:45 to 01:15 Israel time)

Full verdicts are in `fact-check.md`. Method: the Google Flights searches were re-run from an empty cache with the scripts in `scripts/`; Kayak Israel pages were re-loaded; Trip.com was added as a third aggregator (loaded in headless Chrome with `scripts/br.py`, 3 adults, ILS).

| URL | Supported | Checked |
|---|---|---|
| https://www.trip.com/flights/showfarefirst?dcity=ath&acity=tlv&ddate=2027-04-16&triptype=ow&class=y&quantity=3&nonstoponly=on&locale=en-IL&curr=ILS | ATH -> TLV Fri 16 nonstops: Arkia 09:40 -> 11:35 (₪834 pp, "Operated by Electra"), Wizz 09:55 -> 12:00 (₪330), El Al 10:30, Aegean 10:50, Israir 12:15; nothing earlier after 03:30 | 18 Nov 00:52 |
| https://www.trip.com/flights/showfarefirst?dcity=lis&acity=ath&ddate=2027-04-15&triptype=ow&class=y&quantity=3&nonstoponly=on&locale=en-IL&curr=ILS | LIS -> ATH Thu 15: Aegean 23:40 -> 05:35 +1, ₪500 pp | 18 Nov 00:54 |
| https://www.trip.com/flights/showfarefirst?dcity=lis&acity=tlv&ddate=2027-04-18&triptype=ow&class=y&quantity=3&locale=en-IL&curr=ILS (also `&nonstoponly=on`; also `ddate` 15, 16, 19) | LIS -> TLV: Aegean 00:40 -> 12:50 (₪812 pp Sun, ₪946 Mon); TAP 20:40 -> 04:05; El Al 22:15 -> 05:25; codeshare prices; Arkia Mon 19 20:00 -> 03:15 | 18 Nov 00:54-01:09 |
| https://www.trip.com/flights/showfarefirst?dcity=tlv&acity=lis&ddate=2027-04-13&triptype=ow&class=y&quantity=3&locale=en-IL&curr=ILS (also `&nonstoponly=on`; also `ddate` 12, 14) | TLV -> LIS: Aegean, Lufthansa, Smartwings, El Al and TAP times for 12-14 Apr; Arkia Mon 12 arriving 18:10 | 18 Nov 00:55-01:07 |
| https://www.trip.com/flights/showfarefirst?dcity=tlv&acity=opo&ddate=2027-04-13&triptype=ow&class=y&quantity=3&nonstoponly=on&locale=en-IL&curr=ILS | TLV -> OPO Tue 13: TAP 06:30 -> 10:30, ₪2,943 pp | 18 Nov 01:08 |
| https://www.il.kayak.com/flights/LIS-TLV/2027-04-16/3adults?sort=depart_a&fs=stops=0 | Fri 16 nonstops: Arkia 254 10:15 -> 17:30 ₪891 pp; TAP 1603 19:50 | 18 Nov 01:04 |
| https://www.il.kayak.com/flights/LIS-TLV/2027-04-19/3adults?sort=depart_a&fs=stops=0 | Mon 19 nonstops: Arkia 254 20:00 -> 03:15 ₪1,078 pp; TAP 1603 ₪1,410; TAP 8913 ₪1,700; El Al 376 ₪1,894 | 18 Nov 01:03 |
| https://www.il.kayak.com/flights/TLV-LIS/2027-04-12/3adults?sort=depart_a&fs=stops=0 | Mon 12 nonstops: TAP 1604 ₪1,449 pp; Arkia 253 14:25 -> 18:10 ₪1,406; El Al 375 ₪1,517 | 18 Nov 01:04 |
| https://www.google.com/travel/flights/search?tfs=GlwSCjIwMjctMDQtMTRqBRIDVExWcgUSA0xJUyIfCgNUTFYSCjIwMjctMDQtMTQaA0FUSCoCQTMyAzkyOSIfCgNBVEgSCjIwMjctMDQtMTQaA0xJUyoCQTMyAzcyMhoaEgoyMDI3LTA0LTE4agUSA0xJU3IFEgNUTFZCAwEBAUgBmAEB&hl=en&curr=ILS | Round trip, Aegean A3929 + A3722 Wed 14 pinned: ₪5,136 with A3723 + A3924 (LIS-10) | 18 Nov 00:47 |
| https://www.google.com/travel/flights/search?tfs=GhwSCjIwMjctMDQtMTMoAGoFEgNUTFZyBRIDTElTQgMBAQFIAZgBAg==&hl=en&curr=ILS (and the same search for 16 and 17 Apr) | TP1604 Fri 16 08:00 -> 12:10 and Sat 17 05:05 -> 09:15; LY375 not on Fri or Sat | 18 Nov 00:48 |
| https://www.flightradar24.com/data/flights/iz212 | IZ212 is ATH -> TLV, flies Fridays, scheduled time varies daily, recent delays -5 to +51 min | 18 Nov 00:50 |
| https://www.flightradar24.com/data/flights/a3723 | A3723 is LIS -> ATH (winter times); recent delays 0 to +58 min | 18 Nov 00:50 |
| https://www.flightradar24.com/data/flights/iz253 · https://www.flightradar24.com/data/flights/iz254 | Arkia TLV <-> LIS nonstop operating Mondays and Fridays in Nov 2026 | 18 Nov 01:03 |
| https://www.hebcal.com/shabbat?cfg=json&geonameid=293397&M=on&gy=2027&gm=4&gd=16 (Lisbon `geonameid=2267057`, Athens `geonameid=264371`) | Candle lighting and havdalah 16-17 Apr 2027; Erev Pesach Wed 21 Apr 2027 | 18 Nov 00:45 |
| https://www.hebcal.com/zmanim?cfg=json&geonameid=2267057&date=2027-04-17 (same for 293397, 264371) | Sunset and nightfall (8.5 degrees, 72 min) | 18 Nov 00:45 |
| https://www.timeanddate.com/sun/israel/tel-aviv?month=4&year=2027 · https://www.timeanddate.com/sun/portugal/lisbon?month=4&year=2027 | Sunset Tel Aviv 16 Apr 19:10; Lisbon 17 Apr 20:15, civil twilight ends 20:42 | 18 Nov 01:10 |
| https://arena.meo.pt/en/agenda/sabaton_en/16249 | Venue: "15 April 20h30", duration 90 minutes, opened by The Legendary Orchestra, promoter Malpevent | 18 Nov 00:58 |
| https://www.bol.pt/Comprar/Bilhetes/179858-sabaton_the_legendary_tour_2027-meo_arena/?lang=en-US | Seller: session 19:00, doors 17:30, no break, promoter "Rua Atlântica" | 18 Nov 00:58 |
| https://www.sabaton.net/tour/ | No times published for any date | 18 Nov 00:58 |
| https://www.setlist.fm/setlist/sabaton/2025/lanxess-arena-cologne-germany-6b5efa02.html | Cologne 14 Nov 2025: doors 17:30, orchestra 18:30, Sabaton 20:00-22:05 | 18 Nov 00:51 |
| https://www.setlist.fm/setlist/sabaton/2025/3arena-stockholm-sweden-2358288b.html | Stockholm 13 Dec 2025: doors 18:00, orchestra 19:00, Sabaton 20:35-22:45 | 18 Nov 00:51 |
| https://www.setlist.fm/stats/average-setlist/sabaton-13d6d1c5.html?tour=1bdc79c0 | Tour average: 18 live songs + outro over 22 shows | 18 Nov 00:51 |
| https://en.aegeanair.com/travel-info/travelling-with-aegean/check-in/airport-check-in/ | Gate closes at least 30 min before departure (15 min at Athens only); Light-fare cabin bags gate-checked when bins are full | 18 Nov 00:59 |
| https://en.aegeanair.com/travel-info/travelling-with-aegean/baggage/baggage-allowance-v1/ | Aegean Light: 1 carry-on up to 8 kg; no fixed checked-bag price published | 18 Nov 00:59 |
| https://www.flytap.com/en-il/baggage/hand-baggage | TAP Economy: hand bag 10 kg, 55 x 40 x 25 cm, plus personal item 2 kg | 18 Nov 00:58 |
| https://travel-europe.europa.eu/etias_en · https://travel-europe.europa.eu/etias/who-should-apply_en | ETIAS not in operation, no start date; Israel on the list; fee EUR 20 | 18 Nov 00:59 |
| https://www.visitportugal.com/en/node/139876 | MEO Arena about 4 km from the airport (via web search summary) | 18 Nov 01:00 |
| https://thebulkheadseat.com/tap-air-portugal-to-resume-flights-between-lisbon-and-tel-aviv-in-march/ · https://www.aeroroutes.com/eng/250902-iznw25lis | Background: TAP TLV-LIS 05:05 departure pattern; Arkia TLV-LIS launched Oct 2025 (via web search summary) | 18 Nov 00:50, 01:00 |
| https://www.arkia.co.il/ · https://www.arkia.com/ · https://www.skyscanner.co.il/transport/flights/ath/tlv/270416/ · https://www.flightsfrom.com/ATH-TLV | Blocked (Cloudflare 403 / captcha); nothing obtained | 18 Nov 00:50-00:53 |

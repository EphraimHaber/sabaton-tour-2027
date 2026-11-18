# Sources - Milan flights research

All checked **2026-11-17 21:53-22:20 UTC** (17 Nov 23:53 - 18 Nov 00:20 Israel time) unless noted.
Method column: `script` = Python query of the Google Flights results page (3 adults, economy, `curr=ILS`, flight numbers read from the page data); `browser` = page loaded in headless Chrome and its visible text read; `fetch` = plain HTTP fetch; `search` = web-search result summary (secondary).

## Flight prices and schedules (primary)

| URL | Method | What it supported |
|---|---|---|
| https://www.google.com/travel/flights/search?tfs=GhwSCjIwMjctMDQtMTgoAGoFEgNUTFZyBRIDTVhQQgMBAQFIAZgBAg==&hl=en&curr=ILS | script | TLV -> MXP Sun 18 Apr nonstops: W4 6434, W4 6432, LY 381, LY 387 with prices. Same query pattern repeated for every day 12-22 Apr in both directions (schedule table, pre-Passover comparison) |
| https://www.google.com/travel/flights/search?tfs=GhwSCjIwMjctMDQtMTcoAGoFEgNUTFZyBRIDTVhQQgMBAQFIAZgBAg==&hl=en&curr=ILS | script | Sat 17 Apr: only W4 6432 10:50 and W4 6434 18:55; no late-night nonstop, no El Al |
| https://www.google.com/travel/flights/search?tfs=GhwSCjIwMjctMDQtMTdAFGoFEgNUTFZyBRIDTVhQQgMBAQFIAZgBAg==&hl=en&curr=ILS | script | Sat 17 Apr departures after 20:00 to MXP, any stops: only Etihad via AUH |
| https://www.google.com/travel/flights/search?tfs=GhwSCjIwMjctMDQtMjAoAGoFEgNNWFByBRIDVExWQgMBAQFIAZgBAg==&hl=en&curr=ILS | script | MXP -> TLV Tue 20 Apr nonstops: W4 6431, W4 6433, LY 382, LY 388 |
| https://www.google.com/travel/flights/search?tfs=GhoSCjIwMjctMDQtMjBqBRIDTVhQcgUSA1RMVkIDAQEBSAGYAQI=&hl=en&curr=ILS | script | MXP -> TLV Tue 20 Apr incl. 1-stop: Aegean A3 661/926, Sky Express GQ 831/720, Lufthansa, LOT, Swiss |
| https://www.google.com/travel/flights/search?tfs=GhwSCjIwMjctMDQtMjEoAGoFEgNNWFByBRIDVExWQgMBAQFIAZgBAg==&hl=en&curr=ILS | script | MXP -> TLV Wed 21 Apr nonstops and which pass the 12:00 cutoff |
| https://www.google.com/travel/flights/search?tfs=GhwSCjIwMjctMDQtMTgoAGoFEgNUTFZyBRIDTVhQGhwSCjIwMjctMDQtMjAoAGoFEgNNWFByBRIDVExWQgMBAQFIAZgBAQ==&hl=en&curr=ILS | script | Round trip 18 -> 20 Apr, outbound list with "from" prices (4,567 / 5,373 / 6,579) |
| https://www.google.com/travel/flights/search?tfs=Gj4SCjIwMjctMDQtMTgoAGoFEgNUTFZyBRIDTVhQIiAKA1RMVhIKMjAyNy0wNC0xOBoDTVhQKgJXNDIENjQzNBocEgoyMDI3LTA0LTIwKABqBRIDTVhQcgUSA1RMVkIDAQEBSAGYAQE=&hl=en&curr=ILS | script | Round trip 18 -> 20 Apr with W4 6434 selected: return options and totals (MIL-01, 03, 04, 05) |
| https://www.google.com/travel/flights/search?tfs=Gj0SCjIwMjctMDQtMTgoAGoFEgNUTFZyBRIDTVhQIh8KA1RMVhIKMjAyNy0wNC0xOBoDTVhQKgJMWTIDMzgxGhwSCjIwMjctMDQtMjAoAGoFEgNNWFByBRIDVExWQgMBAQFIAZgBAQ==&hl=en&curr=ILS | script | Round trip 18 -> 20 Apr with LY 381 selected (MIL-06, MIL-07) |
| https://www.google.com/travel/flights/search?tfs=Gj0SCjIwMjctMDQtMTgoAGoFEgNUTFZyBRIDTVhQIh8KA1RMVhIKMjAyNy0wNC0xOBoDTVhQKgJMWTIDMzg3GhwSCjIwMjctMDQtMjAoAGoFEgNNWFByBRIDVExWQgMBAQFIAZgBAQ==&hl=en&curr=ILS | script | Round trip 18 -> 20 Apr with LY 387 selected (MIL-06 variant) |
| https://www.google.com/travel/flights/search?tfs=Gj4SCjIwMjctMDQtMTgoAGoFEgNUTFZyBRIDTVhQIiAKA1RMVhIKMjAyNy0wNC0xOBoDTVhQKgJXNDIENjQzNBocEgoyMDI3LTA0LTIxKABqBRIDTVhQcgUSA1RMVkIDAQEBSAGYAQE=&hl=en&curr=ILS | script | Round trip 18 -> 21 Apr with W4 6434 selected (MIL-09) |
| https://www.google.com/travel/flights/search?tfs=Gj0SCjIwMjctMDQtMTkoAGoFEgNUTFZyBRIDTVhQIh8KA1RMVhIKMjAyNy0wNC0xORoDTVhQKgJMWTIDMzgxGhwSCjIwMjctMDQtMjAoAGoFEgNNWFByBRIDVExWQgMBAQFIAZgBAQ==&hl=en&curr=ILS | script | Round trip 19 -> 20 Apr with LY 381 selected (MIL-14) |
| https://www.google.com/travel/flights/search?tfs=Gj4SCjIwMjctMDQtMTUoAGoFEgNUTFZyBRIDTVhQIiAKA1RMVhIKMjAyNy0wNC0xNRoDTVhQKgJXNDIENjQzMhocEgoyMDI3LTA0LTIwKABqBRIDTVhQcgUSA1RMVkIDAQEBSAGYAQE=&hl=en&curr=ILS | script | Round trip 15 -> 20 Apr with W4 6432 selected (MIL-15) |
| https://www.google.com/travel/flights/search?tfs=Gj4SCjIwMjctMDQtMTYoAGoFEgNUTFZyBRIDTVhQIiAKA1RMVhIKMjAyNy0wNC0xNhoDTVhQKgJXNDIENjQzMhocEgoyMDI3LTA0LTIwKABqBRIDTVhQcgUSA1RMVkIDAQEBSAGYAQE=&hl=en&curr=ILS | script | Round trip 16 -> 20 Apr with W4 6432 selected (MIL-15 Friday variant) |
| https://www.google.com/travel/flights/search?tfs=GhwSCjIwMjctMDQtMTcoAGoFEgNUTFZyBRIDRkNPQgMBAQFIAZgBAg==&hl=en&curr=ILS | script | TLV -> FCO Sat 17 Apr nonstops incl. W4 6036 21:55 (MIL-10) |
| https://www.google.com/travel/flights/search?tfs=GhwSCjIwMjctMDQtMjAoAGoFEgNGQ09yBRIDVExWQgMBAQFIAZgBAg==&hl=en&curr=ILS | script | FCO -> TLV Tue 20 Apr nonstops (Rome return alternative) |
| https://www.google.com/travel/flights/search?tfs=GhwSCjIwMjctMDQtMjAoAGoFEgNWUk5yBRIDVExWQgMBAQFIAZgBAg==&hl=en&curr=ILS | script | VRN -> TLV Tue 20 Apr: Israir 6H 352 (MIL-11). Same pattern for 13, 14, 19, 22 Apr and TLV -> VRN |
| https://www.google.com/travel/flights/search?tfs=GhwSCjIwMjctMDQtMjEoAGoFEgNWQ0VyBRIDVExWQgMBAQFIAZgBAg==&hl=en&curr=ILS | script | VCE -> TLV Wed 21 Apr: W4 6717 (MIL-12). Same pattern for 19, 20, 22 Apr (LY 290) |
| https://www.google.com/travel/flights/search?tfs=GhoSCjIwMjctMDQtMThqBRIDVExWcgUSA0xJTkIDAQEBSAGYAQI=&hl=en&curr=ILS | script | TLV -> LIN Sun 18 Apr: 1-stop only. Same pattern for 17 Apr and LIN -> TLV 20, 21 Apr |
| https://www.google.com/travel/flights/search?tfs=GhoSCjIwMjctMDQtMThqBRIDVExWcgUSA0JHWUIDAQEBSAGYAQI=&hl=en&curr=ILS | script | TLV -> BGY: zero results (also 15-17 Apr and BGY -> TLV 20, 21 Apr) |
| Google Flights, same pattern, airports FCO VCE VRN BLQ TRN NAP GOA PSA FLR ZRH GVA NCE TSF, dates 15-18 Apr out and 20-21 Apr back, nonstop | script | Deviation scan; rejected list |
| Google Flights, TLV -> MXP 18 Apr and MXP -> TLV 20 Apr with `curr=EUR` and `curr=USD` | script | Native Wizz fares (EUR 225 / 200 / 400 pp) and Google's implied rates 1 EUR = 3.582 NIS, 1 USD = 3.254 NIS |
| Google Flights, same two queries with the "1 carry-on bag" filter | script | Prices unchanged; filter gives no bag-fee data here |

## Second source (cross-check)

| URL | Method | What it supported |
|---|---|---|
| https://www.il.kayak.com/flights/TLV-MXP/2027-04-18/2027-04-20/3adults?sort=price_a&fs=stops=0 | browser | Round-trip prices in ILS for all nonstop combinations 18 -> 20 Apr; Arkia 06:05 -> 09:15 |
| https://www.il.kayak.com/flights/TLV-MIL/2027-04-18/2027-04-20/3adults?sort=price_a&fs=stops=0 | browser | Same for all Milan airports (only MXP has nonstops) |
| https://www.il.kayak.com/flights/TLV-MXP/2027-04-18/3adults?sort=price_a&fs=stops=0 | browser | One-way Sun 18 Apr. Same pattern for 15, 16, 17, 19 Apr |
| https://www.il.kayak.com/flights/MXP-TLV/2027-04-20/3adults?sort=price_a&fs=stops=0 | browser | One-way Tue 20 Apr nonstop. Same pattern for 21 Apr (Arkia 10:45 -> 15:30) |
| https://www.il.kayak.com/flights/MXP-TLV/2027-04-20/3adults?sort=price_a | browser | Tue 20 Apr with stops: Aegean, Sky Express, self-transfer combinations |
| https://www.il.kayak.com/flights/TLV-FCO/2027-04-17/3adults?sort=price_a&fs=stops=0 | browser | Sat 17 Apr to Rome: Arkia 19:20, Israir 19:00, Wizz 19:40 and 21:55 |
| https://www.il.kayak.com/flights/FCO-TLV/2027-04-20/3adults?sort=price_a&fs=stops=0 | browser | Rome returns Tue 20 Apr |
| https://www.il.kayak.com/flights/VRN-TLV/2027-04-20/3adults?sort=price_a&fs=stops=0 | browser | Israir Verona 21:35 -> 02:05, NIS 655 pp |
| https://www.il.kayak.com/flights/VCE-TLV/2027-04-20/3adults?sort=price_a&fs=stops=0 and .../VCE-TLV/2027-04-21/... | browser | El Al Venice 22:05 (NIS 1,078 pp); Wizz Venice 05:30 (NIS 249 pp) |
| https://www.il.kayak.com/flights/TLV-BGY/2027-04-18/3adults?sort=price_a | browser | Bergamo: self-transfer combinations only, no nonstop |
| https://www.kayak.com/flights/TLV-MXP/2027-04-18/2027-04-20/3adults?sort=price_a&fs=stops=0 | browser | Same round trip in USD (USD 455 pp for MIL-01), used to explain the ILS gap |

## Airline sites

| URL | Method | What it supported |
|---|---|---|
| https://wizzair.com/en-gb/booking/select-flight/TLV/MXP/2027-04-18/2027-04-20/3/0/0/null | browser | Deep link opens the Wizz booking page with the right route, dates and 3 passengers, but it displayed "No flights on this date" (headless and visible browser). Treated as bot blocking; Wizz's own price NOT confirmed |
| https://be.wizzair.com (search API) | script | HTTP 429, blocked. No data |
| https://www.wizzair.com/en-gb/information-and-services/wizz-services/wizz-priority | browser | WIZZ Priority EUR 10-60 online, EUR 65-75 at airport; trolley 55x40x23 cm 10 kg; free bag 40x30x20 cm |
| https://www.wizzair.com/en-gb/information-and-services/prices-discounts/fares-bundles | browser | Basic fare includes only the 40x30x20 bag; bundle contents |
| https://www.ryanair.com/api/farfnd/v4/oneWayFares?departureAirportIataCode=TLV&outboundDepartureDateFrom=2027-04-10&outboundDepartureDateTo=2027-04-22&currency=EUR | fetch | Zero fares from TLV (also zero for Nov 2026 - Mar 2027, and zero BGY -> TLV) |
| https://www.ryanair.com/api/farfnd/v4/oneWayFares?departureAirportIataCode=BGY&outboundDepartureDateFrom=2027-04-18&outboundDepartureDateTo=2027-04-21&currency=EUR | fetch | Returns other BGY fares for those dates, so the April 2027 schedule is loaded and TLV is simply not sold |

## Ground transport

| URL | Method | What it supported |
|---|---|---|
| https://www.malpensaexpress.it/en/lines-and-timetable/most-searched-lines/milano-malpensa-airport-t1-route/ | browser | Last train Milano Centrale -> Malpensa T1 23:25, first 05:25; 51 min; EUR 15 |
| https://www.milanomalpensa-airport.com/en/from-to/by-coach | browser | Coach times Centrale -> MXP: Autostradale 03:20-00:50, Caronte until 01:05 then 03:05, Malpensa Shuttle extra 02:10, Terravision 03:30-23:30 |
| https://www.milanomalpensa-airport.com/en/from-to/by-taxi | fetch | Official page lists no taxi fares (so the EUR 114 figure stays secondary) |
| https://www.hemenhesap.com/en/milan-airport-taxi-fare ; https://www.sicurauto.it/news/traffico-e-viabilita/taxi-milano-per-malpensa-linate-e-orio-quanto-costa/ | search | Fixed taxi fare Milan <-> Malpensa EUR 114 (secondary) |
| https://trenord.it/en/routes-and-timetables/services/airport-routes-mxp ; https://www.malpensaexpress.it/en/trenord-information/news/service-enhancement/ | search | Conflicting last-train times from Cadorna (23:27 vs ~01:00, summer weekend extras); not relied on |
| https://www.flibco.com/en/news/how-to-get-to-unipol-forum-milan ; https://www.flibco.com/it/news/come-raggiungere-il-forum-di-assago | search | M2 may run extended service after concerts; no confirmed last departure |
| https://artofthetravel.com/posts/rome-to-milan-train ; https://www.omio.co.uk/trains/milan-centrale/rome-termini-xiahg ; https://au.trip.com/trains/italy/route/milan-to-rome | search | Rome <-> Milan high-speed fares: promo from EUR 19.90-29.90, averages EUR 42-92, ~2h55 |
| https://www.omio.ie/trains/milan-centrale/verona-porta-nuova-ymbln ; https://www.omio.com/trains/milan/verona | search | Milan -> Verona from EUR 13, average EUR 22, 1h13 fast / 1h52 regional |
| https://heymondo.com/blog/fiumicino-airport-to-rome-city-center ; https://bluekeys.it/blog/fiumicino-rome-transfer-leonardo-express-train | search | Leonardo Express EUR 14, last departure from FCO ~23:23-23:27 |

## Bag rules (secondary)

| URL | Method | What it supported |
|---|---|---|
| https://onemileatatime.com/news/el-al-carry-on-restriction-economy-lite-fares/ ; https://aifly.one/guides/el-al-baggage-allowance/ | search | El Al Lite: 8 kg cabin bag, no checked bag, cabin bag handed in at counter/gate on Europe routes; checked bag ~USD 90 |
| https://www.ynetnews.com/travel/article/ryx1krnaze | search | Israir: trolley USD 30 pre-booked / USD 40 at airport; first checked bag USD 65 pre-booked (bookings from 1 May 2026) |
| https://airadvisor.com/en/baggage-allowance/wizz-air | search | Wizz ranges, consistent with the official page |

## Schedule context (secondary, not relied on for April 2027)

| URL | Method | What it supported |
|---|---|---|
| https://www.flightconnections.com/flights-from-tlv-to-mxp | search | Lists Arkia, El Al, Neos, Wizz Air Malta as nonstop carriers as of April 2026 |
| https://aviability.com/en/flight/iz337-arkia/tlv-mxp | search | Arkia TLV -> MXP was IZ337 in 2026 (not confirmed for 2027) |
| https://www.flightsfrom.com/TLV-MXP | fetch | HTTP 403, not readable |

## Not reachable / no data

- kayak.com and skyscanner.co.il via plain fetch returned no results (JavaScript pages); Kayak worked through a browser, Skyscanner was not retried.
- El Al, Arkia, Israir, Neos, Bluebird, Aegean, Trenitalia and ATM websites were not read.

## Fact-check sources (2026-11-17 22:46-23:05 UTC)

Added by the independent fact-check; verdicts are in `fact-check.md`. Method `page-api` = JSON calls made by the airline's own page, read in a browser session.

| URL | Method | What it supported |
|---|---|---|
| https://wizzair.com/en-gb/booking/select-flight/TLV/MXP/2027-04-18/2027-04-20/3/0/0/null (calls be.wizzair.com/29.25.0/Api/search/timetable, /asset/farechart, /asset/map) | page-api | Wizz's own departure times and operating days 12-25 Apr 2027 for TLV-MXP, MXP-TLV, TLV-FCO, FCO-TLV, VCE-TLV; day's lowest fare for 3 adults in EUR (224.99 / 199.99 / 179.99 / 75.99; 299.99 on Thu 15 Apr); TLV-BGY and TLV-VRN not direct. Flight-level search still HTTP 429 |
| https://wizzair.com/en-gb/help-centre/check-in-and-boarding/check-in/check-in-and-baggage-drop-off-times ; https://ssr-weu2.wizzair.com/en-gb/help-centre/check-in-and-boarding/check-in/check-in-process | browser / search | MXP check-in opens 180 and closes 60 min before departure; TLV closes 70 min before; online check-in 30 days (with seat) or 24 h (without) until 3 h before |
| https://www.wizzair.com/en-gb/information-and-services/wizz-services/wizz-priority-old | fetch | WIZZ Priority EUR 10-60 online, EUR 65-75 at the airport |
| https://www.israir.co.il/reservation/search/flights-abroad/results?origin=VRN&destination=TLV&startDate=20/04/2027&adults=3&subject=ALL | browser | Israir's own result: 6H352 VRN 21:35 -> TLV 02:05+1, USD 237 pp. Same pattern: no TLV-BGY on 15, 16, 18, 19 Apr, no BGY-TLV on 20, 21 Apr, no TLV-MXP on 18 Apr |
| https://www.israir.co.il/Passengers_Info/Baggage_Policy.html | fetch | Israir trolley USD 30 / USD 40 at TLV / EUR 35 abroad; 23 kg bag USD 65 |
| https://www.trip.com/flights/showfarefirst?dcity=tlv&acity=mil&ddate=2027-04-18&rdate=2027-04-20&triptype=rt&class=y&quantity=3&nonstoponly=on&locale=en-XX&curr=ILS | browser | Third price source: same four nonstops and times, MXP T1; Wizz round trip NIS 1,748 pp. One-way variants for MXP-TLV 20 Apr and TLV-MIL 17 Apr |
| https://www.kiwi.com/en/search/results/tel-aviv-israel/milan-italy/2027-04-18/2027-04-20?adults=3&stopNumber=0%7Etrue&currency=ils | browser | Fourth price source: MIL-01 NIS 4,886 for 3; MIL-02 5,698; MIL-03 6,750; MIL-05 6,813; MIL-07 6,900 |
| https://www.il.kayak.com/flights/TLV-MXP/2027-04-18/3adults?sort=price_a&fs=stops=0 and https://www.il.kayak.com/flights/MXP-TLV/2027-04-21/3adults?sort=price_a&fs=stops=0 (result data behind the page) | browser | Arkia flight numbers IZ 337 / IZ 338; El Al's own price shown as a paid placement |
| https://www.il.kayak.com/flights/TLV-MIL/2027-04-17/3adults?sort=depart_b&fs=stops=0 | browser | Sat 17 Apr, all Milan airports: only W4 6432 and W4 6434 |
| https://www.hebcal.com/zmanim?cfg=json&geonameid=293397&start=2027-04-16&end=2027-04-21 ; same with geonameid=3173435 (Milan) and 3169070 (Rome) | fetch | Tel Aviv sunset 19:11 / Havdalah 19:49 on 17 Apr, sunset 19:14 on 21 Apr; Milan sunset 20:10 on 16 Apr; Rome nightfall 20:36 on 17 Apr |
| https://www.hebcal.com/hebcal?v=1&cfg=json&maj=on&year=2027&month=4&geo=geoname&geonameid=293397&c=on&M=on | fetch | Erev Pesach = Wed 21 Apr 2027 |
| https://api.frankfurter.dev/v1/latest?base=EUR&symbols=ILS,USD | fetch | ECB reference rates 17 Nov 2026: 1 EUR = 3.5674 ILS, 1 USD = 3.2463 ILS |
| https://orari.atm.it/M2_694.pdf ; https://orari.atm.it/M2_685.pdf ; https://orari.atm.it/M2_680.pdf | fetch | M2 departures from Assago Milanofiori Forum (last 00:17 Mon-Fri) and running times to Cadorna / Centrale |
| https://www.malpensaexpress.it/fileadmin/contenuti/TRENORD/2-Linee_e_orari/Orario_ferroviario/ORARIO_in_vigore/QMXP_giugno_2026.pdf | fetch | Last Malpensa Express: Centrale 23:25, Cadorna 23:26; later Cadorna trains are seasonal |
| https://autostradale.it/wp-content/uploads/2026/04/MalpensaAeroporto-MilanoCentrale.pdf | fetch | Autostradale night departures 22:20, 22:50, 23:20, 00:50, 03:20; EUR 4.99 online |
| https://www.caronte.eu/wp-content/uploads/2026/11/Orari-sito-novembre-2026.pdf | fetch | Caronte 22:05, 23:05, 00:05, 01:05, 03:05; EUR 10 |
| https://www.malpensashuttle.it/uploads/c9c79a023333-050.-apt4-milano-centrale-malpensa-dal-9-ottobre-2026.pdf | fetch | Malpensa Shuttle 23:10, 23:40, 02:10, 03:40; EUR 10 |
| https://www.regione.lombardia.it/infrastrutture-trasporti-e-mobilita/taxi-collegamenti-aeroportuali-e-noleggio/servizio-e-tariffe-taxi-nel-bacino-aeroportuale | fetch | Official fixed taxi fare Malpensa <-> City of Milan EUR 114; Assago not on the fixed-fare list |
| https://city-airport-taxis.com/airporttransfers/reservations/taxi-from-Assago-to-Milan-Malpensa-Airport | fetch | Private transfer quote Assago -> MXP, sedan for 3, EUR 125 (secondary) |
| https://www.sleepinginairports.net/guides/milan-malpensa-airport-guide.htm | fetch | MXP open 24 h landside (secondary) |
| https://www.mentelocale.it/milano/76479-brunori-sas-a-milano-orari-biglietti-e-scaletta-del-concerto-al-forum-di-assago.htm ; https://www.unipolforum.it/it/regole/ | fetch | Forum bag restrictions (secondary; venue page defers to organiser) |
| https://www.lefrecce.it | browser | Trenitalia fares Rome-Milan, Milan-Verona, Milan-Venice; Leonardo Express last departures 23:23 / 23:53 |
| https://www.atv.verona.it/Autobus_per_aeroporto_Catullo | fetch | Verona Airlink EUR 7, every 20 min |
| https://www.atvo.it/assets/bus_routes/035b_05.10.26-24.04.27.pdf | fetch | First Mestre -> VCE buses 04:20, 05:00 |
| https://travel-europe.europa.eu/etias ; https://travel-europe.europa.eu/etias/etias-timeline-explained | fetch | ETIAS not in operation, no start date, EUR 20, transitional period after launch |
| https://www.flightconnections.com/flights-from-tlv-to-mxp ; https://www.flightconnections.com/flights-from-tlv-to-bgy ; https://www.flightconnections.com/flights-from-tlv-to-lin | fetch | Winter-2026 flight numbers (W4 6405/6403/6406/6404), Israir 6H 301 TLV-BGY weekly from Jan 2027, no LIN nonstop (secondary) |
| https://www.trip.com/flights/status-w46431 ; https://www.trip.com/flights/status-w46405 | fetch | W4 6431 shown cancelled today; W4 6405 operating daily at 05:00 (secondary) |
| https://blog.wego.com/el-al-news/ ; https://www.skyexpress.gr/en/sky-experience/before-fly/fare-types | fetch | El Al Lite cabin-bag rule (secondary); Sky Express cabin allowance |

Blocked during the fact-check: skyscanner.co.il (captcha), arkia.co.il (Cloudflare), booking.elal.com (no deep link), en.aegeanair.com (403), Wizz flight-level search (429).

## Scripts and raw captures

The author's scripts are now kept in `milan/scripts/` (`gf.py`, `gf2.py`, `kayak.py`, `browse.py`, `wizz.py`). The note below describes the original temporary location of the raw captures.


Kept in `a temporary scratch folder (milan/)` (temporary directory, may be cleared): `gf.py`, `gf2.py` (Google Flights queries), `kayak.py`, `browse.py` (browser captures), `raw/*.rows.json` (parsed Google results with timestamps and URLs), `pages/*.txt` (page text captures), `out_*.txt` (run logs).

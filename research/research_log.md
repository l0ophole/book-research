# Research log

### 1. 2026-11-15 — Document inventory
- Reason: Establish scope
- Tool: Bash (wc, ls), Grep
- Query/target: headings ^#{1,3}
- Result: 1 file, 24,202 lines, 222,696 words; 31 chapters + appendices + 358 references; headings mapped (secmap.json).
- Limitations: OCR artifacts present (e.g., "Keyhole" for Keyhoe; "lmage")

### 2. 2026-11-15 — Reading: front matter, methods, Ch1 framing, Ch2 (through Sandia), Ch3 (Webb + early fallout cases), Ch6, Ch9 (opening, George, date, final thoughts), Ch10 opening, Ch11 (Echo/Oscar), Ch18 NORAD logs, Ch21 Bentwaters opening
- Reason: Core claims & incidents
- Tool: Read tool
- Query/target: offsets 1-940,1354-2003,2424-2755,5059-5355,7416-7830,8076-8200,8399-8480,8657-8850,9863-10282,13993-14252,15923-16060
- Result: 3,853 of 24,203 lines (15.9%) read verbatim.
- Limitations: Remaining ~84% only pattern-scanned or unread

### 3. 2026-11-15 — Pattern scan
- Reason: Index remaining text
- Tool: Python regex
- Query/target: date+facility keywords in unread paragraphs
- Result: 296 candidate paragraphs; top 6/section kept (194) as LEAD records.
- Limitations: Heuristic; false positives/negatives likely

### 4. 2026-11-15 — Reference parse
- Reason: Build References table
- Tool: Python regex
- Query/target: Bibliography lines 23548-24185
- Result: 358 references parsed; type classification heuristic.
- Limitations: Some merged/mis-split entries (e.g., Ch4 ref 17/18)

### 5. 2026-11-15 — WebSearch
- Reason: Verify Echo/Malmstrom 1967
- Tool: WebSearch standard
- Query/target: Malmstrom Echo Flight March 16 1967 ...
- Result: Found NICAP, Skeptoid, RR0 (wing history excerpt), Metabunk.
- Limitations: Search summaries are not primary sources

### 6. 2026-11-15 — WebSearch
- Reason: Verify Chadwell memo
- Tool: WebSearch standard
- Query/target: Chadwell memorandum December 2 1952 ...
- Result: Found memo listings; quote only in curated excerpt; CIA RR item dated 9 Dec 1952 distinct.
- Limitations: Original PDF not opened

### 7. 2026-11-15 — HTTP fetch
- Reason: Read primary excerpts
- Tool: curl via proxy
- Query/target: nicap malmstrom67-2; rr0 Malmstrom; ufopedia Chadwell; cia.gov node 415717
- Result: NICAP and RR0 opened and quoted (SRC001, SRC002); CIA node was landing page.
- Limitations: —

### 8. 2026-11-15 — WebSearch+fetch
- Reason: Verify Big Sur launch dates
- Tool: WebSearch; curl
- Query/target: Atlas D Sept 1964; SI George 1993
- Result: SI PDF opened (SRC004); Wikipedia Atlas list opened (SRC005); outrocket blocked (SRC006).
- Limitations: EA page not retrieved; Jacobs MUFON article not retrieved

### 9. 2026-11-15 — WebSearch+fetch
- Reason: Verify 1975 NORAD / Loring
- Tool: WebSearch; curl
- Query/target: Loring 27 Oct 1975 NMCC NORAD
- Result: NICAP chronology, TWZ, Wikipedia opened (SRC009-011).
- Limitations: Original NORAD/NMCC messages not obtained

### 10. 2026-11-15 — WebSearch+fetch
- Reason: Verify FBI 1949 memo
- Tool: WebSearch; curl
- Query/target: FBI Protection of Vital Installations 1949
- Result: Black Vault page, ufopedia page opened (SRC008); PDF not opened.
- Limitations: —

### 11. 2026-11-15 — Fetch
- Reason: Check Rendlesham dates
- Tool: curl
- Query/target: Wikipedia Rendlesham
- Result: Confirmed Halt memo date error and lighthouse/fireball explanations (SRC014).
- Limitations: —

### 12. 2026-11-15 — Attempted
- Reason: Fetch outrocket LORV-3 page
- Tool: curl
- Query/target: outrocket.com atlas-abres-lorv-3
- Result: HTTP 429 bot-checkpoint; unsuccessful.
- Limitations: Retry with different source (Encyclopedia Astronautica / Space Launch Report)

### 13. 2026-11-15 — Reading (follow-up): Ch7 (5356-6120), Ch12 (11026-11307), Ch13 (11308-12551), Ch14 (12552-12770), Ch15 (12771-12986)
- Reason: User requested full read + extraction + verification of these chapters
- Tool: Read tool
- Query/target: offsets as listed
- Result: All lines of these chapters read verbatim (2,585 lines).
- Limitations: Ch15 ends at line 12986; chapter 16 begins 12987 (not read)

### 14. 2026-11-15 — WebSearch: Minot 24 Oct 1968 / Krause letter / Cox column / Condon / Frazier-Oberg
- Reason: Verify claims in newly read chapters
- Tool: WebSearch standard
- Query/target: 5 parallel queries
- Result: Found Tulien report, Cox column copy, Condon & Frazier pages; Krause letter not found.
- Limitations: Search summaries are discovery only

### 15. 2026-11-15 — Fetch + read: minotb52ufo.com investigation; Patrick Gross Cox column; Wikipedia Condon, Frazier, SM-65 Atlas, Walker AFB
- Reason: Primary/secondary checking
- Tool: curl via proxy
- Query/target: see SRC017-SRC021
- Result: Quintanilla text and Oscar-7 break-in confirmed; Cox column matches; Atlas deployment partly differs; Frazier Sandia 1983-2006.
- Limitations: Original Blue Book PDFs not opened

### 16. 2026-11-15 — Unsuccessful search: Krause letter NICAP 20 Dec 1964
- Reason: Locate the letter
- Tool: WebSearch
- Query/target: Barry Krause letter NICAP ...
- Result: Not found.
- Limitations: Absence of search hit is not evidence of absence; try CUFOS/NICAP archive

### 17. 2026-11-16 — Fetch minotb52ufo.com documentation index, Shough and Poher reports, Blue Book Final Case Report, dispatcher log, radarscope scans
- Reason: Follow-up question 1: recompute radar speed from frames and dispatcher log
- Tool: curl via proxy; pdftotext; pdftoppm
- Query/target: pdf/Blue-Book-Final-Case-Report.pdf; shough/pdf/SHOUGH_Report.pdf; poher/pdf/POHER_Report.pdf; pdf/Base-Operations-Dispatcher-Log.pdf; pdf/All-Radarscope-Photographs.pdf
- Result: All downloaded and text-extracted; frame 771 viewed; 13 other documents listed but not read.
- Limitations: NARA microfilm T1206 not accessed; original negatives not located

### 18. 2026-11-16 — Analyst calculation: echo displacement/speed from Shough positions
- Reason: Test the book/Clark 3,900 mph figure
- Tool: Python (analysis/minot_speed.py)
- Query/target: positions 771-773
- Result: Naive 3.0 s: ~2,500 kt; paint-time corrected: 2,020 and 5,710 kt; simple mean 3,865 kt; time-weighted mean ~2,960 kt.
- Limitations: Uses Shough measurements; I did not measure the photographs myself

### 19. 2026-11-16 — Analyst calculation: Sirius/Vega azimuth-altitude over Minot, 0800-1010Z 24 Oct 1968
- Reason: Test Blue Book star explanation against dispatcher log directions
- Tool: Python (analysis/minot_sirius.py)
- Query/target: Minot AFB coordinates; precession-corrected coordinates
- Result: Sirius SE-SSE alt 11-23 deg; Vega NW-NNW low, setting ~0940Z.
- Limitations: No refraction; approximate coordinates

### 20. 2026-11-16 — Read transcript (doc 17), viewed Partin, Bond, Smith, Isley, O'Connor AF 117s; built unified timeline
- Reason: Follow-up question 1 (settle Shough vs Poher timeline)
- Tool: pdftotext, pdftoppm, image viewing, Python
- Query/target: pdf/0017.pdf; pdf/AF-117-*.pdf
- Result: Timeline reconciled to the transcript Zulu clock; analysts agree on altitude; offset 5-9 min; Partin form differs from later account; Vega fails brightness test.
- Limitations: Handwriting resolution limited; Adams/Jablonski not viewed; no NARA originals

### 21. 2026-11-16 — Analyst calculation: Vega bearing, altitude and extinction at 0906-0935Z
- Reason: Test Blue Book Vega explanation
- Tool: Python
- Query/target: Minot coordinates; Kasten-Young airmass
- Result: Bearing consistent; brightness inconsistent (mag ~5-7).
- Limitations: Extinction coefficients assumed; refraction/ducting not modelled

### 22. 2026-11-16 — Downloaded and read Blue Book docs 3, 5-7, 9-13, 15, 25-27, 29; viewed Adams and Jablonski AF 117s
- Reason: Follow-up question 1 (read remaining case-file documents)
- Tool: curl, pdftotext, image viewing
- Query/target: minotb52ufo.com/pdf/00xx.pdf
- Result: Found Werlich 80% B-52 opinion, SAC play-down request, Smith note, Oscar-7 prior cases, weather-radar gap; origin of 3,000 mph.
- Limitations: No OCR tool available, so scanned-only documents (AF 117s, docs 1, 2, 4, 14, 30, 31) were viewed or skipped; docs 14, 30, 31 (upper-air data, overlay map, area map) not read

### 23. 2026-11-16 — Independent image measurement of radarscope frames 771-773
- Reason: Measure echoes rather than rely on Shough
- Tool: Python/numpy/PIL on pdfimages output
- Query/target: analysis/minot_frame_measure.py
- Result: Echoes recovered in 772 and 773; 771 not recovered; displacement 2.14 NM; calibration sensitivity ~30%.
- Limitations: Heading-up/constant-orientation assumption; JPEG print scans

### 24. 2026-11-16 — Read book lines 8851-9481 (rest of Ch.10 Warren material through "Hynek Opens the Door") and Chapter 16 (12987-13288)
- Reason: Follow-up question 1: check the 1 Aug 1965 Warren log vs "stars", then read Ch.16
- Tool: Read tool
- Query/target: offsets 8851-9481; 12987-13288
- Result: Extracted Warren witness accounts (Tashner, Earnshaw, Stuck, Thompson), Hynek/Fowler 1966 Minot summary, Ch.16 claims.
- Limitations: —

### 25. 2026-11-16 — Fetched ufohastings.com Warren page, UFOScans Blue Book Cheyenne PDF, SUNlite 14-3, NICAP Bolender page; searched for the original Anspaugh log
- Reason: Verify Warren 1965 claims and Bolender quote
- Tool: curl; pdftotext; WebSearch
- Query/target: multiple
- Result: Found 90th SMW counts/descriptions, Blue Book addendum, Printy review, Bolender quote; original Anspaugh log NOT found.
- Limitations: OCR of Blue Book PDF poor; original log and time zone unresolved

### 26. 2026-11-16 — Sky computation for Cheyenne, 1 Aug 1965, 2200-0430 MDT
- Reason: Test "stars" explanation
- Tool: Python/PyEphem 4.2.1
- Query/target: analysis/warren_sky_1965.py
- Result: Jupiter/Aldebaran/Capella east-NE at 0317-0340 MDT; 70-deg azimuth match for Jupiter at 0340 only if log is Mountain time.
- Limitations: Log time zone unknown; satellites not modelled

### 27. 2026-11-16 — Located Hynek (1972) printing of the Warren log on archive.org (full text) and read pp.233-236
- Reason: Fix the log time zone (follow-up question 1)
- Tool: curl; archive.org full text
- Query/target: the-ufo-experience-j.-allen-hynek
- Result: Log is the Blue Book call log (Eastern clock inferred); book matches Hynek; Hynek also argues a lack-of-interest reading.
- Limitations: Original Blue Book memo not seen; EST vs EDT unresolved

### 28. 2026-11-16 — Per-entry sky test under three clock hypotheses incl. the Pleiades
- Reason: Redo star-by-star test
- Tool: Python/PyEphem 4.2.1
- Query/target: analysis/warren_sky_by_entry.py
- Result: Overhead=Deneb, east=Pleiades, NE=Capella plausible; unexplained: 3:17 flashing-red oval, az-120 entry, passing-through motions, four NW.
- Limitations: No satellites or aircraft modelled; EVD055 corrected

### 29. 2026-11-16 — Located SAO Special Report 289 (NTRS 19700026243) with Echo 1/Echo 2 mean elements for July-Dec 1965
- Reason: Follow-up question 1 (satellite test) — no user-supplied elements needed
- Tool: curl; pdftotext; image reading
- Query/target: ntrs.nasa.gov/api/citations/19700026243
- Result: Echo 2 smoothed elements for 16 Jul-16 Aug 1965 and Echo 1 daily elements for 1 Aug obtained; first search used wrong NORAD number (614 vs 740) but did not affect the SAO data.
- Limitations: OCR of polynomial elements imperfect; consistency-checked

### 30. 2026-11-16 — Propagated Echo 1 and Echo 2; listed visible passes over Cheyenne; tested coincidence with log times against chance
- Reason: Test satellite explanation for Warren entries
- Tool: Python/PyEphem/numpy
- Query/target: analysis/warren_echo2_passes.py; warren_echo1_passes.py; warren_echo2_coincidence.py
- Result: Echo 2: three visible passes; matches to log entries at chance; Echo 1: none. First run had a date-conversion bug (found and fixed).
- Limitations: Brightness not computed; other satellites untested

### 31. 2026-11-16 — Parsed 1964-5A (Saturn stage) mean elements from SAO SR-289 p.81 image; propagated; checked fainter stars near azimuths 70/120; searched for Pegasus 3 elements
- Reason: Follow-up question 1: other satellites and aircraft/meteor candidates
- Tool: Python/PyEphem; image reading; WebSearch
- Query/target: analysis/warren_s5_passes.py; warren_az120_check.py
- Result: 1964-5A not visible that night; az-120 entry has fainter-star candidates; Pegasus 3 elements not found (launched 30 Jul 1965).
- Limitations: Pegasus series, aircraft and meteors untested

### 32. 2026-11-16 — Read book lines 13289-13992 (Ch.17), 14894-15330 (Ch.19), 15331-15922 (Ch.20)
- Reason: Follow-up question 1: Chapters 17 and 19-20 in full
- Tool: Read tool
- Query/target: offsets as listed
- Result: Extracted INC055-INC068, CLM108-CLM131, witnesses WIT071-WIT084.
- Limitations: —

### 33. 2026-11-16 — Checks: moon/sky for Grand Forks 1974 and Wall SD winter 1978-79; Wikipedia pages for Greenham Common and Cattle mutilation; searches for Rommel report, Ellsworth commander/weather
- Reason: Verify Ch.17/19/20 claims
- Tool: PyEphem; curl; WebSearch
- Query/target: analysis/grandforks_moon_1974.py; mills_ellsworth_sky_1979.py
- Result: Moon claim for Grand Forks contradicted; Greenham F-111 statement wrong; Rommel/CBI outline consistent; commander and weather not found.
- Limitations: Spraker/Stone/Fenimore, Jan 1979 weather not verified; Fischbach and Safeguard pages not retrievable

### 34. 2026-11-16 — Compared public versions of Salas account: Carlson critique, Klotz/Salas 1996, Skeptoid, Wikipedia, Metabunk, CBS, 2010 affidavit image, book text lines 9926-10034
- Reason: Follow-up 2
- Tool: curl; image view; Read; WebSearch
- Query/target: n/a
- Result: Built version matrix EVD077; assessment EVD078; added SRC042-044
- Limitations: Affidavit page 2 not legible; Carlson letter quotes not checked against original; 1995 Tribune/MUFON originals not obtained; Metabunk/CBS read only for context

### 35. 2026-11-16 — Computed Mars/Moon/Venus/Jupiter/Saturn positions for Malmstrom 15-25 Mar 1967
- Reason: Follow-up 1: test Sheaffer Mars hypothesis
- Tool: PyEphem
- Query/target: analysis/salas_mars_1967.py
- Result: Mars bright (-0.7 to -1.1) and up ~2130-0730 on the Oscar window, below horizon at Echo time 0845; near-full Moon also up; inconclusive without Oscar sighting time
- Limitations: Time of the Oscar sighting not in sources read; elevation 1100 m assumed; no refraction


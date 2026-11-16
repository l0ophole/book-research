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


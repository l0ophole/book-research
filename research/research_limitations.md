# Limitations and requirements

## What was and was not done
| Task | Status |
|---|---|
| Identify and inventory the document | **Completed** |
| Read every chapter in full | **NOT completed** — 6,579 of 24,203 lines (27.2%) read verbatim after follow-up 1 (see `documents/coverage_matrix.md`). 41 sections FULL_READ, 9 PARTIAL_READ, 56 PATTERN_SCAN_ONLY, 1 PARSED (references) |
| Extract every incident, witness and claim | **Partially completed** — records cover the read portions only (54 incidents, 86 claims, 65 witnesses). Unread chapters are represented by 160 machine-extracted leads and 196 auto-extracted name mentions, which are **unreviewed** |
| Independent verification | **Partially completed** — 22 external sources recorded (17 examined, 5 discovered only); original PDFs for FBI/CIA/NORAD documents were **not** obtained |
| Chapter-by-chapter evidence database | **Partially completed** (schema complete; coverage as above) |
| SQLite/CSV/JSON/Markdown exports | **Completed** (all generated from the same SQLite file) |

## Why
The book is ~330–430K tokens of text, larger than the working context; reading it all requires multiple further passes. This pass prioritised the best-documented incidents (Echo/Oscar, Big Sur, 1975 NORAD, Bentwaters, early FBI/CIA documents).

## Tool/access limits
- Web access worked through a proxy; some sites blocked (outrocket.com bot checkpoint; CIA Reading Room returned landing page only). No access to restricted archives; no FOIA requests submitted; no witnesses contacted; no original radar/telemetry data examined.
- Search-engine summaries were treated as *discovery only*, not as examination.
- Encyclopedia Astronautica, Jacobs’s 1989 MUFON article, *Faded Giant*, the Black Vault PDFs, NARA Blue Book files, and AFHRA holdings were not examined.
- The markdown has OCR errors (e.g., “Keyhole” for Keyhoe, “lmage”), no pagination, and no images; line numbers are the provenance anchor.
- Reference parsing is heuristic (358 entries; some merged); reference types are approximate.

## What you can do to help
1. Tell me which chapters to read next (Ch.7 and Ch.12–15 are now done; recommended next: Ch.16–17, 19–20, 22–23, 26–27, 29–30).
2. Provide (or point me to) PDFs: *Faded Giant* (Salas/Klotz), Jacobs’s MUFON UFO Journal Jan 1989 article, Klotz’s FOIA response PDFs, NORAD/NMCC 1975 messages, Halt’s tape transcript.
3. If you have a FOIA/Mandatory Declassification Review route, the highest-value requests are listed in `missing_records/INDEX.md` (MIS009–MIS012, MIS014, MIS017–MIS020).
4. If you can run a browser session through an institutional login (CIA CREST, NARA catalog, newspaper archives), say so and I will extract exact records.

## Never claimed
No witnesses were contacted, no FOIA requests were filed, no restricted archive was accessed.

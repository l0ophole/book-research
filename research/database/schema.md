# Database schema (version 1.0.0, generated 2026-11-15)

SQLite file `evidence.sqlite` is authoritative; CSV and JSON files in sibling folders are exported from it.

**Confidence scale (integer 0–5):** 0 not investigated · 1 unsupported/unverified · 2 disputed or conflicting · 3 partially verified (secondary or transcribed support) · 4 verified against an original primary record · 5 independently corroborated by multiple primary records. *Limitation:* confidence rates documentary support for an account, not witness sincerity; repetition by secondary sources does not raise it.

**Verification statuses:** VERIFIED, PARTIALLY_VERIFIED, CORROBORATED, CONTRADICTED, UNVERIFIED, DISPUTED, INSUFFICIENT_EVIDENCE, NOT_YET_INVESTIGATED, SOURCE_UNAVAILABLE. **Source classes:** PRIMARY, SECONDARY, TERTIARY, UNKNOWN. **Priorities:** CRITICAL, HIGH, MEDIUM, LOW.

**ID prefixes:** DOC document · SEC section · INC incident · CLM claim · WIT witness · GOV government document · TEC technical evidence · SRC external source · REF book reference · EXP competing explanation · EVD evidence record · MIS missing record · RQ research question · LEAD pattern-scan lead · NM name mention.

**Provenance:** every record carrying `line_ref` points to a line number in the supplied markdown file (`f3ff02a2-hastings-2008-ufos-and-nukes.md`); the markdown has no page numbers. `section_id` joins to Document_Sections.

## Claims
Rows: 107

| name | type | pk |
|---|---|---|
| claim_id | TEXT | 1 |
| claim_text | TEXT | 0 |
| attribution | TEXT | 0 |
| claim_type | TEXT | 0 |
| importance | TEXT | 0 |
| verification_status | TEXT | 0 |
| confidence | INT | 0 |
| quotation | TEXT | 0 |
| section_id | TEXT | 0 |
| line_ref | INT | 0 |

Foreign keys: section_id → Document_Sections

## Competing_Explanations
Rows: 32

| name | type | pk |
|---|---|---|
| explanation_id | TEXT | 1 |
| target_entities | TEXT | 0 |
| explanation | TEXT | 0 |
| supporting_evidence | TEXT | 0 |
| contradicting_evidence | TEXT | 0 |
| evaluation_status | TEXT | 0 |
| section_id | TEXT | 0 |
| line_ref | INT | 0 |

Foreign keys: section_id → Document_Sections

## Document_Claim_Links
Rows: 107

| name | type | pk |
|---|---|---|
| link_id | INTEGER | 1 |
| claim_id | TEXT | 0 |
| document_id | TEXT | 0 |
| section_id | TEXT | 0 |
| line_ref | INT | 0 |

Foreign keys: section_id → Document_Sections; document_id → Documents; claim_id → Claims

## Document_Sections
Rows: 107

| name | type | pk |
|---|---|---|
| section_id | TEXT | 1 |
| document_id | TEXT | 0 |
| chapter_label | TEXT | 0 |
| heading_level | INT | 0 |
| title | TEXT | 0 |
| line_start | INT | 0 |
| line_end | INT | 0 |
| word_count | INT | 0 |
| footnote_markers | INT | 0 |
| pct_lines_read | REAL | 0 |
| coverage_status | TEXT | 0 |
| notes | TEXT | 0 |

Foreign keys: document_id → Documents

## Documents
Rows: 1

| name | type | pk |
|---|---|---|
| document_id | TEXT | 1 |
| filename | TEXT | 0 |
| title | TEXT | 0 |
| author | TEXT | 0 |
| publication_year | INT | 0 |
| format | TEXT | 0 |
| total_lines | INT | 0 |
| total_words | INT | 0 |
| sha256 | TEXT | 0 |
| description | TEXT | 0 |
| access_limitations | TEXT | 0 |

## Evidence_Records
Rows: 70

| name | type | pk |
|---|---|---|
| evidence_id | TEXT | 1 |
| description | TEXT | 0 |
| evidence_type | TEXT | 0 |
| provenance | TEXT | 0 |
| related_entities | TEXT | 0 |
| significance | TEXT | 0 |
| verification_status | TEXT | 0 |
| confidence | INT | 0 |
| section_id | TEXT | 0 |
| line_ref | INT | 0 |

Foreign keys: section_id → Document_Sections

## Government_Documents
Rows: 17

| name | type | pk |
|---|---|---|
| gov_doc_id | TEXT | 1 |
| title | TEXT | 0 |
| agency | TEXT | 0 |
| doc_date | TEXT | 0 |
| document_number | TEXT | 0 |
| repository | TEXT | 0 |
| availability | TEXT | 0 |
| verification_status | TEXT | 0 |
| notes | TEXT | 0 |
| section_id | TEXT | 0 |
| line_ref | INT | 0 |

Foreign keys: section_id → Document_Sections

## Incidents
Rows: 55

| name | type | pk |
|---|---|---|
| incident_id | TEXT | 1 |
| date_text | TEXT | 0 |
| location | TEXT | 0 |
| description | TEXT | 0 |
| significance | TEXT | 0 |
| verification_status | TEXT | 0 |
| confidence | INT | 0 |
| evidence_basis | TEXT | 0 |
| section_id | TEXT | 0 |
| line_ref | INT | 0 |
| notes | TEXT | 0 |

Foreign keys: section_id → Document_Sections

## Missing_Records
Rows: 42

| name | type | pk |
|---|---|---|
| missing_id | TEXT | 1 |
| description | TEXT | 0 |
| existence_status | TEXT | 0 |
| potential_repository | TEXT | 0 |
| acquisition_method | TEXT | 0 |
| status | TEXT | 0 |
| section_id | TEXT | 0 |
| line_ref | INT | 0 |

Foreign keys: section_id → Document_Sections

## Name_Mentions
Rows: 196

| name | type | pk |
|---|---|---|
| mention_id | TEXT | 1 |
| normalized_name | TEXT | 0 |
| rank_or_title | TEXT | 0 |
| mention_count | INT | 0 |
| first_line | INT | 0 |
| last_line | INT | 0 |
| first_section_id | TEXT | 0 |
| status | TEXT | 0 |

Foreign keys: first_section_id → Document_Sections

## Pattern_Scan_Leads
Rows: 143

| name | type | pk |
|---|---|---|
| lead_id | TEXT | 1 |
| section_id | TEXT | 0 |
| line_ref | INT | 0 |
| matched_date | TEXT | 0 |
| score | INT | 0 |
| verbatim_excerpt | TEXT | 0 |
| status | TEXT | 0 |

Foreign keys: section_id → Document_Sections

## References
Rows: 358

| name | type | pk |
|---|---|---|
| reference_id | TEXT | 1 |
| chapter_label | TEXT | 0 |
| note_number | INT | 0 |
| citation | TEXT | 0 |
| reference_type | TEXT | 0 |
| section_id | TEXT | 0 |
| line_ref | INT | 0 |
| parse_note | TEXT | 0 |

Foreign keys: section_id → Document_Sections

## Relationships
Rows: 521

| name | type | pk |
|---|---|---|
| relationship_id | INTEGER | 1 |
| from_id | TEXT | 0 |
| to_id | TEXT | 0 |
| relationship_type | TEXT | 0 |
| note | TEXT | 0 |

## Research_Log
Rows: 31

| name | type | pk |
|---|---|---|
| log_id | INTEGER | 1 |
| log_date | TEXT | 0 |
| action | TEXT | 0 |
| reason | TEXT | 0 |
| tool | TEXT | 0 |
| query | TEXT | 0 |
| result | TEXT | 0 |
| limitations | TEXT | 0 |

## Research_Questions
Rows: 17

| name | type | pk |
|---|---|---|
| question_id | TEXT | 1 |
| question | TEXT | 0 |
| priority | TEXT | 0 |
| related_entities | TEXT | 0 |
| existing_evidence | TEXT | 0 |
| missing_evidence | TEXT | 0 |
| potential_sources | TEXT | 0 |
| recommended_methods | TEXT | 0 |
| verification_criteria | TEXT | 0 |
| status | TEXT | 0 |
| next_action | TEXT | 0 |

## Schema_Info
Rows: 4

| name | type | pk |
|---|---|---|
| key | TEXT | 1 |
| value | TEXT | 0 |

## Sources
Rows: 38

| name | type | pk |
|---|---|---|
| source_id | TEXT | 1 |
| title | TEXT | 0 |
| author | TEXT | 0 |
| organization | TEXT | 0 |
| pub_date | TEXT | 0 |
| source_type | TEXT | 0 |
| classification | TEXT | 0 |
| url | TEXT | 0 |
| document_identifier | TEXT | 0 |
| pages_sections | TEXT | 0 |
| access_date | TEXT | 0 |
| related_entities | TEXT | 0 |
| extracted_information | TEXT | 0 |
| reliability_notes | TEXT | 0 |
| verification_status | TEXT | 0 |
| examination_level | TEXT | 0 |

## Technical_Evidence
Rows: 9

| name | type | pk |
|---|---|---|
| tech_id | TEXT | 1 |
| evidence_type | TEXT | 0 |
| originating_system | TEXT | 0 |
| evidence_date | TEXT | 0 |
| raw_data_availability | TEXT | 0 |
| notes | TEXT | 0 |
| section_id | TEXT | 0 |
| line_ref | INT | 0 |

Foreign keys: section_id → Document_Sections

## Witness_Incidents
Rows: 74

| name | type | pk |
|---|---|---|
| witness_id | TEXT | 1 |
| incident_id | TEXT | 2 |

Foreign keys: incident_id → Incidents; witness_id → Witnesses

## Witnesses
Rows: 71

| name | type | pk |
|---|---|---|
| witness_id | TEXT | 1 |
| name | TEXT | 0 |
| role | TEXT | 0 |
| firsthand_status | TEXT | 0 |
| identity_status | TEXT | 0 |
| notes | TEXT | 0 |
| section_id | TEXT | 0 |
| line_ref | INT | 0 |

Foreign keys: section_id → Document_Sections

## Indexes
- ix_inc_date
- ix_inc_loc
- ix_inc_vs
- ix_clm_vs
- ix_clm_imp
- ix_clm_sec
- ix_wit_name
- ix_src_cls
- ix_ref_ch
- ix_rel_from
- ix_rel_to
- ix_nm_name
- ix_lead_sec

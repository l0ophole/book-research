import sqlite3,json,os,re
OUT='/home/user/book-research/research'
con=sqlite3.connect(f'{OUT}/database/evidence.sqlite');con.row_factory=sqlite3.Row;c=con.cursor()
qa=json.load(open('qa.json'));cnt=qa['counts']
def rows(q,*a): return [dict(r) for r in c.execute(q,a)]
def w(path,txt): open(f'{OUT}/{path}','w',encoding='utf-8').write(txt)
def esc(x): return str(x if x is not None else '').replace('|','\\|').replace('\n',' ')
def table(cols,rs):
    out='| '+' | '.join(cols)+' |\n|'+'---|'*len(cols)+'\n'
    for r in rs: out+='| '+' | '.join(esc(r[k]) for k in cols)+' |\n'
    return out
BOOKLN='book line %s'
# ---- schema.md
tabs=[r['name'] for r in rows("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
s='# Database schema (version 1.0.0, generated 2026-11-15)\n\nSQLite file `evidence.sqlite` is authoritative; CSV and JSON files in sibling folders are exported from it.\n\n**Confidence scale (integer 0–5):** 0 not investigated · 1 unsupported/unverified · 2 disputed or conflicting · 3 partially verified (secondary or transcribed support) · 4 verified against an original primary record · 5 independently corroborated by multiple primary records. *Limitation:* confidence rates documentary support for an account, not witness sincerity; repetition by secondary sources does not raise it.\n\n**Verification statuses:** VERIFIED, PARTIALLY_VERIFIED, CORROBORATED, CONTRADICTED, UNVERIFIED, DISPUTED, INSUFFICIENT_EVIDENCE, NOT_YET_INVESTIGATED, SOURCE_UNAVAILABLE. **Source classes:** PRIMARY, SECONDARY, TERTIARY, UNKNOWN. **Priorities:** CRITICAL, HIGH, MEDIUM, LOW.\n\n**ID prefixes:** DOC document · SEC section · INC incident · CLM claim · WIT witness · GOV government document · TEC technical evidence · SRC external source · REF book reference · EXP competing explanation · EVD evidence record · MIS missing record · RQ research question · LEAD pattern-scan lead · NM name mention.\n\n**Provenance:** every record carrying `line_ref` points to a line number in the supplied markdown file (`f3ff02a2-hastings-2008-ufos-and-nukes.md`); the markdown has no page numbers. `section_id` joins to Document_Sections.\n\n'
for t in tabs:
    s+=f'## {t}\n'+f'Rows: {cnt.get(t)}\n\n'+table(['name','type','pk'],[dict(name=r['name'],type=r['type'],pk=r['pk']) for r in rows(f'PRAGMA table_info("{t}")')])+'\n'
    fk=rows(f'PRAGMA foreign_key_list("{t}")')
    if fk: s+='Foreign keys: '+'; '.join(f"{f['from']} → {f['table']}" for f in fk)+'\n\n'
s+='## Indexes\n'+'\n'.join('- '+r['name'] for r in rows("SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'ix_%'"))+'\n'
w('database/schema.md',s)
# ---- coverage matrix & inventory
secs=rows('SELECT * FROM Document_Sections ORDER BY line_start')
m='# Coverage matrix\n\nStatus definitions: **FULL_READ** ≥90% of the section’s lines read verbatim by the analyst; **PARTIAL_READ** some lines read; **PATTERN_SCAN_ONLY** not read verbatim — only machine-scanned for date/facility paragraphs (leads) and mention indexes; **PARSED_PROGRAMMATICALLY** (References).\n\n'
m+=table(['section_id','chapter_label','title','line_start','line_end','word_count','pct_lines_read','coverage_status'],secs)
w('documents/coverage_matrix.md',m)
st=rows('SELECT coverage_status,COUNT(*) n,SUM(word_count) words FROM Document_Sections GROUP BY 1')
d=rows('SELECT * FROM Documents')[0]
inv=f"# Document inventory\n\n| Field | Value |\n|---|---|\n| ID | {d['document_id']} |\n| File | {d['filename']} |\n| Title | {d['title']} |\n| Author | {d['author']} ({d['publication_year']}) |\n| Format | {d['format']} |\n| Size | {d['total_lines']} lines, {d['total_words']} words |\n| SHA-256 | `{d['sha256']}` |\n| Access limitations | {d['access_limitations']} |\n\n## Section coverage summary\n"+table(['coverage_status','n','words'],st)+f"\nLines read verbatim: **{qa['qa'][[x[0] for x in qa['qa']].index('lines_read_pct')][1]}%** of 24,203.\n"
w('documents/document_inventory.md',inv)
# ---- per-record pages
def secname(sid):
    r=rows('SELECT title,chapter_label FROM Document_Sections WHERE section_id=?',sid)
    return f"{r[0]['chapter_label']} — {r[0]['title']} ({sid})" if r else ''
incs=rows('SELECT * FROM Incidents ORDER BY incident_id')
for i in incs:
    rel=rows("SELECT * FROM Relationships WHERE from_id=? OR to_id=?",i['incident_id'],i['incident_id'])
    wits=rows("SELECT w.* FROM Witnesses w JOIN Witness_Incidents x ON x.witness_id=w.witness_id WHERE x.incident_id=?",i['incident_id'])
    ex=rows("SELECT e.* FROM Competing_Explanations e JOIN Relationships r ON r.from_id=e.explanation_id AND r.to_id=? AND r.relationship_type='EXPLAINS'",i['incident_id'])
    t=f"# {i['incident_id']} — {i['location']}\n\n- **Date:** {i['date_text']}\n- **Significance:** {i['significance']} · **Status:** {i['verification_status']} (confidence {i['confidence']}/5) · **Basis:** {i['evidence_basis']}\n- **Provenance:** {secname(i['section_id'])}, book line {i['line_ref']}\n\n## Description (as presented in the book; paraphrase)\n{i['description']}\n\n## Witnesses\n"+('\n'.join(f"- [{x['witness_id']}](../witnesses/{x['witness_id']}.md) {x['name']} — {x['firsthand_status']}" for x in wits) or '- none recorded')+'\n\n## Competing explanations\n'+('\n'.join(f"- [{x['explanation_id']}](../competing_explanations/{x['explanation_id']}.md) {x['explanation']}" for x in ex) or '- none recorded yet')+'\n\n## Linked records\n'+('\n'.join(f"- {r['from_id']} —{r['relationship_type']}→ {r['to_id']}" for r in rel) or '- none')+'\n'
    w(f"incidents/{i['incident_id']}.md",t)
w('incidents/INDEX.md','# Incidents\n\n'+table(['incident_id','date_text','location','significance','verification_status','confidence','line_ref'],incs))
for x in rows('SELECT * FROM Witnesses ORDER BY witness_id'):
    inc=rows("SELECT incident_id FROM Witness_Incidents WHERE witness_id=?",x['witness_id'])
    w(f"witnesses/{x['witness_id']}.md",f"# {x['witness_id']} — {x['name']}\n\n- **Role:** {x['role']}\n- **First-hand status:** {x['firsthand_status']}\n- **Identity:** {x['identity_status']}\n- **Incidents:** {', '.join(i['incident_id'] for i in inc) or '—'}\n- **Provenance:** {secname(x['section_id'])}, book line {x['line_ref']}\n\n## Notes\n{x['notes']}\n\n*Privacy:* only names published in the book are recorded; no contact information is stored.\n")
w('witnesses/INDEX.md','# Witnesses and investigators\n\n'+table(['witness_id','name','role','firsthand_status','identity_status'],rows('SELECT * FROM Witnesses')))
cl=rows('SELECT * FROM Claims ORDER BY claim_id')
w('claims/INDEX.md','# Claims\n\n'+table(['claim_id','claim_text','attribution','importance','verification_status','confidence','line_ref'],cl))
for x in rows('SELECT * FROM Government_Documents ORDER BY gov_doc_id'): w(f"government_documents/{x['gov_doc_id']}.md",f"# {x['gov_doc_id']} — {x['title']}\n\n- **Agency:** {x['agency']}\n- **Date:** {x['doc_date']}\n- **Number:** {x['document_number'] or '—'}\n- **Repository / where to look:** {x['repository']}\n- **Availability:** {x['availability']}\n- **Status:** {x['verification_status']}\n- **Provenance:** book line {x['line_ref']}\n\n{x['notes']}\n")
w('government_documents/INDEX.md','# Government documents\n\n'+table(['gov_doc_id','title','agency','doc_date','availability','verification_status'],rows('SELECT * FROM Government_Documents')))
w('technical_evidence/INDEX.md','# Technical evidence\n\n'+table(['tech_id','evidence_type','originating_system','evidence_date','raw_data_availability','notes'],rows('SELECT * FROM Technical_Evidence')))
for x in rows('SELECT * FROM Sources ORDER BY source_id'): w(f"sources/{x['source_id']}.md",f"# {x['source_id']} — {x['title']}\n\n- **Author / org:** {x['author']} / {x['organization']}\n- **Date:** {x['pub_date']} · **Type:** {x['source_type']} · **Class:** {x['classification']}\n- **URL:** {x['url']}\n- **Identifier:** {x['document_identifier'] or '—'} · **Pages:** {x['pages_sections'] or '—'}\n- **Accessed:** {x['access_date']} · **Examination level:** {x['examination_level']} · **Status:** {x['verification_status']}\n- **Related:** {x['related_entities']}\n\n## Extracted information\n{x['extracted_information']}\n\n## Reliability considerations\n{x['reliability_notes']}\n")
w('sources/INDEX.md','# External sources\n\n'+table(['source_id','title','classification','examination_level','verification_status','url'],rows('SELECT * FROM Sources')))
for x in rows('SELECT * FROM Competing_Explanations'): w(f"competing_explanations/{x['explanation_id']}.md",f"# {x['explanation_id']} — explanation for {x['target_entities']}\n\n**Explanation:** {x['explanation']}\n\n**Supporting evidence:** {x['supporting_evidence']}\n\n**Contradicting evidence / problems:** {x['contradicting_evidence']}\n\n**Status:** {x['evaluation_status']} (assumption: none of these has been independently tested in this project)\n")
w('competing_explanations/INDEX.md','# Competing explanations\n\n'+table(['explanation_id','target_entities','explanation','evaluation_status'],rows('SELECT * FROM Competing_Explanations')))
w('missing_records/INDEX.md','# Missing and unobtained records\n\nExistence terms: KNOWN = confirmed to exist (cited or seen) but not yet obtained here; REFERENCED = cited by the book or other sources, not located; SUSPECTED = plausible but unconfirmed; never presumed to exist.\n\n'+table(['missing_id','description','existence_status','potential_repository','acquisition_method','status'],rows('SELECT * FROM Missing_Records')))
w('evidence_records/INDEX.md','# Independent evidence records\n\n'+table(['evidence_id','description','evidence_type','provenance','verification_status','confidence'],rows('SELECT * FROM Evidence_Records')))
rq=rows('SELECT * FROM Research_Questions ORDER BY question_id')
w('unresolved_questions/INDEX.md','# Research questions\n\n'+table(['question_id','question','priority','status','next_action'],rq))
plan='# Research plan\n\n'
for x in rq: plan+=f"## {x['question_id']} [{x['priority']}] — {x['question']}\n- **Related:** {x['related_entities']}\n- **Existing evidence:** {x['existing_evidence']}\n- **Missing evidence:** {x['missing_evidence']}\n- **Potential sources:** {x['potential_sources']}\n- **Methods:** {x['recommended_methods']}\n- **Verification criteria:** {x['verification_criteria']}\n- **Status:** {x['status']}\n- **Next action:** {x['next_action']}\n\n"
w('research_plan.md',plan)
lg='# Research log\n\n'
for x in rows('SELECT * FROM Research_Log ORDER BY log_id'): lg+=f"### {x['log_id']}. {x['log_date']} — {x['action']}\n- Reason: {x['reason']}\n- Tool: {x['tool']}\n- Query/target: {x['query']}\n- Result: {x['result']}\n- Limitations: {x['limitations'] or '—'}\n\n"
w('research_log.md',lg)
w('database/leads_pattern_scan.md','# Pattern-scan leads (unreviewed, machine-extracted)\n\nThese are paragraphs from sections NOT read verbatim, selected by date + facility keywords. They are *leads*, not extracted facts.\n\n'+table(['lead_id','section_id','line_ref','matched_date','score','verbatim_excerpt'],rows('SELECT * FROM Pattern_Scan_Leads')))
w('database/name_mentions.md','# Auto-extracted ranked-name mentions (unverified)\n\n'+table(['normalized_name','rank_or_title','mention_count','first_line','last_line'],rows('SELECT * FROM Name_Mentions ORDER BY mention_count DESC LIMIT 100'))+'\n\n*(Top 100 shown; all rows in Name_Mentions.)*\n')
import shutil;shutil.copy('/tmp/claude-0/-home-user-book-research/0041f4a6-627b-57d1-a860-4a04cf581a1e/scratchpad/timeline_minot.md',f'{OUT}/documents/minot_1968_timeline.md')
print('md ok')

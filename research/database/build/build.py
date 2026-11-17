import sqlite3,json,csv,os,re,shutil,datetime,hashlib
import b01,b02,b03,b04,b05,b06,b07,b08,b09,b10,b11,b12,b13,b14,b15,b16,b17,b18,b19,b20,b21,b22,b23,b24,b25,b26,b27,b28,b29,b30,b31
from kb import T,SM,sec
BOOK='/root/.claude/uploads/0041f4a6-627b-57d1-a860-4a04cf581a1e/f3ff02a2-hastings-2008-ufos-and-nukes.md'
OUT='/home/user/book-research/research'
SCHEMA_VERSION='1.23.0'; GEN=datetime.date(2026,11,15).isoformat()
for _d in ['database','documents','incidents','witnesses','claims','government_documents','technical_evidence','sources','competing_explanations','missing_records','unresolved_questions','evidence_records']:
    if _d=='database':
        for _s in ['csv','json']: shutil.rmtree(f'{OUT}/database/{_s}',ignore_errors=True)
        if os.path.exists(f'{OUT}/database/evidence.sqlite'): os.remove(f'{OUT}/database/evidence.sqlite')
    else: shutil.rmtree(f'{OUT}/{_d}',ignore_errors=True)
for d in ['database/csv','database/json','documents','incidents','witnesses','claims','government_documents','technical_evidence','sources','competing_explanations','missing_records','unresolved_questions','evidence_records']: os.makedirs(f'{OUT}/{d}',exist_ok=True)
DB=f'{OUT}/database/evidence.sqlite'
con=sqlite3.connect(DB);con.execute('PRAGMA foreign_keys=ON');cur=con.cursor()
L=open(BOOK,encoding='utf-8').read().split('\n')
VS={'VERIFIED','PARTIALLY_VERIFIED','CORROBORATED','CONTRADICTED','UNVERIFIED','DISPUTED','INSUFFICIENT_EVIDENCE','NOT_YET_INVESTIGATED','SOURCE_UNAVAILABLE'}
def vs(x):
    x=(x or '').replace('?','').strip()
    return x if x in VS else 'NOT_YET_INVESTIGATED'
CONF={'VERIFIED':4,'CORROBORATED':3,'PARTIALLY_VERIFIED':3,'DISPUTED':2,'CONTRADICTED':1,'UNVERIFIED':1,'INSUFFICIENT_EVIDENCE':1,'NOT_YET_INVESTIGATED':0,'SOURCE_UNAVAILABLE':0}
# overrides after independent research
OV={'INC019':'PARTIALLY_VERIFIED','INC020':'DISPUTED','INC029':'DISPUTED','INC034':'PARTIALLY_VERIFIED','CLM032':'DISPUTED','CLM033':'PARTIALLY_VERIFIED','CLM036':'DISPUTED','CLM043':'PARTIALLY_VERIFIED','CLM034':'UNVERIFIED','CLM054':'PARTIALLY_VERIFIED','INC052':'PARTIALLY_VERIFIED','INC042':'UNVERIFIED','CLM088':'PARTIALLY_VERIFIED','CLM090':'DISPUTED','CLM094':'DISPUTED','CLM101':'DISPUTED','CLM096':'PARTIALLY_VERIFIED','CLM100':'PARTIALLY_VERIFIED','CLM113':'CONTRADICTED','CLM116':'DISPUTED','CLM118':'DISPUTED','CLM120':'PARTIALLY_VERIFIED','CLM123':'PARTIALLY_VERIFIED','CLM098':'DISPUTED','CLM099':'PARTIALLY_VERIFIED','CLM066':'DISPUTED','CLM170':'VERIFIED','CLM068':'PARTIALLY_VERIFIED','CLM067':'PARTIALLY_VERIFIED'}
cur.executescript(f'''
CREATE TABLE Schema_Info(key TEXT PRIMARY KEY,value TEXT);
CREATE TABLE Documents(document_id TEXT PRIMARY KEY,filename TEXT,title TEXT,author TEXT,publication_year INT,format TEXT,total_lines INT,total_words INT,sha256 TEXT,description TEXT,access_limitations TEXT);
CREATE TABLE Document_Sections(section_id TEXT PRIMARY KEY,document_id TEXT REFERENCES Documents,chapter_label TEXT,heading_level INT,title TEXT,line_start INT,line_end INT,word_count INT,footnote_markers INT,pct_lines_read REAL,coverage_status TEXT CHECK(coverage_status IN ('FULL_READ','PARTIAL_READ','PATTERN_SCAN_ONLY','PARSED_PROGRAMMATICALLY','NOT_PROCESSED')),notes TEXT);
CREATE TABLE Incidents(incident_id TEXT PRIMARY KEY,date_text TEXT,location TEXT,description TEXT,significance TEXT,verification_status TEXT,confidence INT,evidence_basis TEXT,section_id TEXT REFERENCES Document_Sections,line_ref INT,notes TEXT);
CREATE TABLE Claims(claim_id TEXT PRIMARY KEY,claim_text TEXT,attribution TEXT,claim_type TEXT,importance TEXT,verification_status TEXT,confidence INT,quotation TEXT,section_id TEXT REFERENCES Document_Sections,line_ref INT);
CREATE TABLE Witnesses(witness_id TEXT PRIMARY KEY,name TEXT,role TEXT,firsthand_status TEXT,identity_status TEXT,notes TEXT,section_id TEXT REFERENCES Document_Sections,line_ref INT);
CREATE TABLE Witness_Incidents(witness_id TEXT REFERENCES Witnesses,incident_id TEXT REFERENCES Incidents,PRIMARY KEY(witness_id,incident_id));
CREATE TABLE Government_Documents(gov_doc_id TEXT PRIMARY KEY,title TEXT,agency TEXT,doc_date TEXT,document_number TEXT,repository TEXT,availability TEXT,verification_status TEXT,notes TEXT,section_id TEXT REFERENCES Document_Sections,line_ref INT);
CREATE TABLE Technical_Evidence(tech_id TEXT PRIMARY KEY,evidence_type TEXT,originating_system TEXT,evidence_date TEXT,raw_data_availability TEXT,notes TEXT,section_id TEXT REFERENCES Document_Sections,line_ref INT);
CREATE TABLE Sources(source_id TEXT PRIMARY KEY,title TEXT,author TEXT,organization TEXT,pub_date TEXT,source_type TEXT,classification TEXT CHECK(classification IN ('PRIMARY','SECONDARY','TERTIARY','UNKNOWN')),url TEXT,document_identifier TEXT,pages_sections TEXT,access_date TEXT,related_entities TEXT,extracted_information TEXT,reliability_notes TEXT,verification_status TEXT,examination_level TEXT CHECK(examination_level IN ('DISCOVERED','OPENED','EXAMINED','INDEPENDENTLY_VERIFIED')));
CREATE TABLE "References"(reference_id TEXT PRIMARY KEY,chapter_label TEXT,note_number INT,citation TEXT,reference_type TEXT,section_id TEXT REFERENCES Document_Sections,line_ref INT,parse_note TEXT);
CREATE TABLE Competing_Explanations(explanation_id TEXT PRIMARY KEY,target_entities TEXT,explanation TEXT,supporting_evidence TEXT,contradicting_evidence TEXT,evaluation_status TEXT,section_id TEXT REFERENCES Document_Sections,line_ref INT);
CREATE TABLE Evidence_Records(evidence_id TEXT PRIMARY KEY,description TEXT,evidence_type TEXT,provenance TEXT,related_entities TEXT,significance TEXT,verification_status TEXT,confidence INT,section_id TEXT REFERENCES Document_Sections,line_ref INT);
CREATE TABLE Missing_Records(missing_id TEXT PRIMARY KEY,description TEXT,existence_status TEXT,potential_repository TEXT,acquisition_method TEXT,status TEXT,section_id TEXT REFERENCES Document_Sections,line_ref INT);
CREATE TABLE Research_Questions(question_id TEXT PRIMARY KEY,question TEXT,priority TEXT CHECK(priority IN ('CRITICAL','HIGH','MEDIUM','LOW')),related_entities TEXT,existing_evidence TEXT,missing_evidence TEXT,potential_sources TEXT,recommended_methods TEXT,verification_criteria TEXT,status TEXT,next_action TEXT);
CREATE TABLE Relationships(relationship_id INTEGER PRIMARY KEY AUTOINCREMENT,from_id TEXT,to_id TEXT,relationship_type TEXT,note TEXT);
CREATE TABLE Document_Claim_Links(link_id INTEGER PRIMARY KEY AUTOINCREMENT,claim_id TEXT REFERENCES Claims,document_id TEXT REFERENCES Documents,section_id TEXT REFERENCES Document_Sections,line_ref INT);
CREATE TABLE Research_Log(log_id INTEGER PRIMARY KEY AUTOINCREMENT,log_date TEXT,action TEXT,reason TEXT,tool TEXT,query TEXT,result TEXT,limitations TEXT);
CREATE TABLE Pattern_Scan_Leads(lead_id TEXT PRIMARY KEY,section_id TEXT REFERENCES Document_Sections,line_ref INT,matched_date TEXT,score INT,verbatim_excerpt TEXT,status TEXT);
CREATE TABLE Name_Mentions(mention_id TEXT PRIMARY KEY,normalized_name TEXT,rank_or_title TEXT,mention_count INT,first_line INT,last_line INT,first_section_id TEXT REFERENCES Document_Sections,status TEXT);
CREATE INDEX ix_inc_date ON Incidents(date_text);CREATE INDEX ix_inc_loc ON Incidents(location);CREATE INDEX ix_inc_vs ON Incidents(verification_status);
CREATE INDEX ix_clm_vs ON Claims(verification_status);CREATE INDEX ix_clm_imp ON Claims(importance);CREATE INDEX ix_clm_sec ON Claims(section_id);
CREATE INDEX ix_wit_name ON Witnesses(name);CREATE INDEX ix_src_cls ON Sources(classification);CREATE INDEX ix_ref_ch ON "References"(chapter_label);
CREATE INDEX ix_rel_from ON Relationships(from_id);CREATE INDEX ix_rel_to ON Relationships(to_id);CREATE INDEX ix_nm_name ON Name_Mentions(normalized_name);
CREATE INDEX ix_lead_sec ON Pattern_Scan_Leads(section_id);
''')
for k,v in {'schema_version':SCHEMA_VERSION,'generated':GEN,'confidence_scale':'0=not investigated;1=single/unsupported or unverified;2=disputed or conflicting;3=partially verified (secondary/transcribed support);4=verified against original primary record;5=independently corroborated by multiple primary records. Confidence is about documentary support for the account, not witness sincerity.','authoritative_store':'SQLite; CSV/JSON/Markdown generated from it'}.items(): cur.execute('INSERT INTO Schema_Info VALUES(?,?)',(k,v))
sha=hashlib.sha256(open(BOOK,'rb').read()).hexdigest()
cur.execute('INSERT INTO Documents VALUES(?,?,?,?,?,?,?,?,?,?,?)',('DOC001','f3ff02a2-hastings-2008-ufos-and-nukes.md','UFOs and Nukes: Extraordinary Encounters at Nuclear Weapons Sites','Robert L. Hastings',2008,'Markdown (OCR-converted book)',len(L),sum(len(x.split()) for x in L),sha,'Author-published book arguing for a UFO-nuclear weapons connection; 31 chapters, 2 appendices, references.','Only ~16% of lines read verbatim in this pass; no page numbers or images present in the markdown; OCR artifacts; figures/photos not available.'))
cov=json.load(open('cov.json'));READ=json.load(open('read_ranges.json'))
chap=''
secrows=[]
for i,s in enumerate(SM):
    sid='SEC%03d'%(i+1)
    m=re.match(r'^(\d+)\.\s',s['title'])
    if m: chap='Chapter '+m.group(1)
    elif s['title'] in('Introduction',): chap='Introduction'
    elif s['title'].startswith('Appendix'): chap=s['title'].split(':')[0]
    elif s['title']=='References': chap='References'
    elif i<14: chap='Front matter'
    label=chap
    c=cov[i]
    if s['line_start']>=23380: st='PARSED_PROGRAMMATICALLY' if s['title']=='References' else 'PATTERN_SCAN_ONLY'
    elif c>=0.9: st='FULL_READ'
    elif c>0: st='PARTIAL_READ'
    else: st='PATTERN_SCAN_ONLY'
    secrows.append((sid,'DOC001',label,s['level'],s['title'],s['line_start'],s['line_end'],s['words'],s['fn'],round(100*c,1),st,''))
cur.executemany('INSERT INTO Document_Sections VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',secrows)
def S(ln): return sec(ln) if ln and ln>0 else None
for r in T['incidents']:
    v=vs(OV.get(r['id'],r['status']));cur.execute('INSERT INTO Incidents VALUES(?,?,?,?,?,?,?,?,?,?,?)',(r['id'],r['date'],r['location'],r['description'],r['significance'],v,CONF[v],r['basis'],S(r['ln']),r['ln'],r['notes']))
for r in T['claims']:
    v=vs(OV.get(r['id'],r['status']));cur.execute('INSERT INTO Claims VALUES(?,?,?,?,?,?,?,?,?,?)',(r['id'],r['text'],r['attribution'],r['claim_type'],r['importance'],v,CONF[v],r['quote'],S(r['ln']),r['ln']))
    cur.execute('INSERT INTO Document_Claim_Links(claim_id,document_id,section_id,line_ref) VALUES(?,?,?,?)',(r['id'],'DOC001',S(r['ln']),r['ln']))
incids={r['id'] for r in T['incidents']}
for r in T['witnesses']:
    cur.execute('INSERT INTO Witnesses VALUES(?,?,?,?,?,?,?,?)',(r['id'],r['name'],r['role'],r['firsthand'],r['identity'],r['notes'],S(r['ln']),r['ln']))
    for i in r['incidents']:
        if i in incids: cur.execute('INSERT OR IGNORE INTO Witness_Incidents VALUES(?,?)',(r['id'],i))
for r in T['govdocs']: cur.execute('INSERT INTO Government_Documents VALUES(?,?,?,?,?,?,?,?,?,?,?)',(r['id'],r['title'],r['agency'],r['date'],r['doc_no'],r['repository'],r['availability'],vs(r['status']),r['notes'],S(r['ln']),r['ln']))
for r in T['tech']: cur.execute('INSERT INTO Technical_Evidence VALUES(?,?,?,?,?,?,?,?)',(r['id'],r['evidence_type'],r['system'],r['date'],r['raw_data_availability'],r['notes'],S(r['ln']),r['ln']))
for r in T['sources']:
    cls=r['classification'].split(' ')[0]
    cur.execute('INSERT INTO Sources VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(r['id'],r['title'],r['author'],r['organization'],r['date'],r['source_type'],cls if cls in('PRIMARY','SECONDARY','TERTIARY') else 'UNKNOWN',r['url'],r['doc_id'],r['pages'],r['access_date'],r['related'],r['extract'],r['reliability'],vs(r['verification']),r['examined']))
refs=json.load(open('refs.json'))
for n,r in enumerate(refs,1):
    ch=r['chapter']; 
    cur.execute('INSERT INTO "References" VALUES(?,?,?,?,?,?,?,?)',('REF%03d'%n,ch,r['num'],r['citation'],r['reference_type'],S(r['ln']),r['ln'],'heuristic parse; type classification approximate'))
for r in T['expl']: cur.execute('INSERT INTO Competing_Explanations VALUES(?,?,?,?,?,?,?,?)',(r['id'],r['target'],r['explanation'],r['supporting'],r['contradicting'],r['evaluation'],S(r['ln']),r['ln']))
for r in T['evidence']:
    v=vs(r['status']);cur.execute('INSERT INTO Evidence_Records VALUES(?,?,?,?,?,?,?,?,?,?)',(r['id'],r['description'],r['evidence_type'],r['provenance'],r['related'],r['significance'],v,CONF[v],S(r['ln']),r['ln']))
for r in T['missing']: cur.execute('INSERT INTO Missing_Records VALUES(?,?,?,?,?,?,?,?)',(r['id'],r['description'],r['existence'],r['repository'],r['acquisition'],r['status'],S(r['ln']),r['ln']))
for r in T['rq']: cur.execute('INSERT INTO Research_Questions VALUES(?,?,?,?,?,?,?,?,?,?,?)',(r['id'],r['question'],r['priority'],r['related'],r['existing'],r['missing'],r['sources'],r['methods'],r['criteria'],r['status'],r['next_action']))
for r in T['log']: cur.execute('INSERT INTO Research_Log(log_date,action,reason,tool,query,result,limitations) VALUES(?,?,?,?,?,?,?)',(r['ts'],r['action'],r['reason'],r['tool'],r['query'],r['result'],r['limits']))
leads=json.load(open('leads_keep.json'))
for n,l in enumerate(leads,1): cur.execute('INSERT INTO Pattern_Scan_Leads VALUES(?,?,?,?,?,?,?)',('LEAD%03d'%n,S(l['ln']),l['ln'],l['date'],l['score'],l['text'],'UNREVIEWED_AUTOMATED_LEAD'))
# name mentions (auto)
NM=re.compile(r'\b(Col\.|Colonel|Lt\. Col\.|Lt\. Colonel|Capt\.|Captain|Maj\.|Major|Lt\.|Lieutenant|Sgt\.|SSgt\.?|MSgt\.?|TSgt\.?|Airman|Gen\.|General|Dr\.|Mr\.|Sheriff)\s+((?:[A-Z][a-z]+\.?|[A-Z]\.)(?:\s+(?:[A-Z][a-z]+|[A-Z]\.)){0,2})')
mm={}
for i,l in enumerate(L,1):
    if i>=23380: break
    for m in NM.finditer(l):
        nm=m.group(2).strip().rstrip('.')
        if len(nm)<4 or nm.split()[0] in('Force','Air','Base','Strategic','Command','Weapons','Missile','Security','Police','Group','Wing','Squadron'): continue
        key=nm;d=mm.setdefault(key,dict(t=m.group(1),c=0,f=i,l=i));d['c']+=1;d['l']=i
for n,(k,d) in enumerate(sorted(mm.items(),key=lambda x:-x[1]['c']),1):
    cur.execute('INSERT INTO Name_Mentions VALUES(?,?,?,?,?,?,?,?)',('NM%04d'%n,k,d['t'],d['c'],d['f'],d['l'],S(d['f']),'AUTO_EXTRACTED_UNVERIFIED'))
# relationships
import re as _r
def expand(tok):
    out=[]
    for m in _r.finditer(r'(INC|CLM|GOV|SRC|WIT|EXP|MIS|EVD)(\d{3})(?:\s*-\s*(?:INC|CLM|GOV)?(\d{3}))?',tok):
        p,a,b=m.group(1),int(m.group(2)),m.group(3)
        out+=[f'{p}{x:03d}' for x in (range(a,int(b)+1) if b else [a])]
    return out
valid=set()
for t in ['incidents','claims','witnesses','govdocs','tech','sources','expl','evidence','missing','rq']:
    for r in T[t]: valid.add(r['id'])
R=set()
for r in T['witnesses']:
    for i in r['incidents']: R.add((r['id'],i,'WITNESS_TO',''))
for r in T['expl']:
    for t in expand(r['target']): R.add((r['id'],t,'EXPLAINS',''))
for r in T['evidence']:
    for t in expand(r['related']): R.add((r['id'],t,'RELATES_TO',''))
for r in T['sources']:
    for t in expand(r['related']): R.add((r['id'],t,'INFORMS',''))
for r in T['rq']:
    for t in expand(r['related']): R.add((r['id'],t,'INVESTIGATES',''))
# claim->incident manual map
CI={'CLM081':['INC052'],'CLM108':['INC055'],'CLM109':['INC056'],'CLM110':['INC056'],'CLM111':['INC059'],'CLM112':['INC060'],'CLM113':['INC060'],'CLM114':['INC061'],'CLM115':['INC062'],'CLM116':['INC062'],'CLM117':['INC063'],'CLM119':['INC064'],'CLM120':['INC064'],'CLM121':['INC064'],'CLM125':['INC067'],'CLM126':['INC067'],'CLM127':['INC067'],'CLM129':['INC068'],'CLM131':['INC068'],'CLM106':['INC033'],'CLM107':['INC033'],'CLM101':['INC033'],'CLM100':['INC033'],'CLM102':['INC033'],'CLM103':['INC033'],'CLM104':['INC033'],'CLM105':['INC054'],'CLM092':['INC052'],'CLM093':['INC052'],'CLM094':['INC052'],'CLM090':['INC052'],'CLM091':['INC052'],'CLM087':['INC052'],'CLM088':['INC052'],'CLM089':['INC052'],'CLM082':['INC052'],'CLM083':['INC052'],'CLM084':['INC052'],'CLM085':['INC052'],'CLM077':['INC050'],'CLM078':['INC050'],'CLM079':['INC050'],'CLM059':['INC037','INC038','INC039','INC040','INC041','INC042'],'CLM062':['INC045','INC048','INC049'],'CLM086':['INC033','INC052'],'CLM032':['INC019','INC020'],'CLM033':['INC019'],'CLM034':['INC019'],'CLM035':['INC019'],'CLM036':['INC019'],'CLM037':['INC020'],'CLM038':['INC019','INC020'],'CLM039':['INC020'],'CLM040':['INC025'],'CLM041':['INC025'],'CLM042':['INC025'],'CLM043':['INC025'],'CLM044':['INC025'],'CLM045':['INC025'],'CLM048':['INC027'],'CLM049':['INC027'],'CLM050':['INC027'],'CLM016':['INC001','INC012'],'CLM017':['INC001'],'CLM021':['INC001'],'CLM023':['INC013'],'CLM024':['INC013'],'CLM025':['INC014','INC015','INC016','INC017'],'CLM029':['INC018'],'CLM030':['INC018'],'CLM052':['INC033'],'CLM054':['INC034'],'CLM055':['INC034'],'CLM056':['INC035']}
for c,ii in CI.items():
    for i in ii: R.add((c,i,'CLAIM_ABOUT',''))
GI={'GOV013':['INC042'],'GOV014':['INC052'],'GOV015':['INC052'],'GOV016':['INC052'],'GOV001':['INC001'],'GOV002':['INC001','INC012'],'GOV003':['INC008'],'GOV004':['INC001'],'GOV005':['INC019'],'GOV006':['INC019'],'GOV007':['INC022'],'GOV008':['INC027'],'GOV009':['INC027','INC029'],'GOV010':['INC029'],'GOV011':['INC033'],'GOV012':['INC034']}
for g,ii in GI.items():
    for i in ii: R.add((g,i,'DOCUMENTS',''))
for r in T['missing']:
    pass
R={x for x in R if x[0] in valid and x[1] in valid}
for a,b,t,n in sorted(R): cur.execute('INSERT INTO Relationships(from_id,to_id,relationship_type,note) VALUES(?,?,?,?)',(a,b,t,n))
con.commit()
# ---- QA
qa=[]
fk=cur.execute('PRAGMA foreign_key_check').fetchall();qa.append(('foreign_key_violations',len(fk)))
qa.append(('integrity_check',cur.execute('PRAGMA integrity_check').fetchone()[0]))
cnt={t:cur.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0] for t in [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]}
qa.append(('sections_total',cnt['Document_Sections']))
for st,n in cur.execute('SELECT coverage_status,COUNT(*) FROM Document_Sections GROUP BY 1'): qa.append((f'sections_{st}',n))
qa.append(('lines_read_pct',round(100*sum(b-a+1 for a,b in READ)/len(L),1)))
dups=cur.execute('SELECT name,COUNT(*) FROM Witnesses GROUP BY name HAVING COUNT(*)>1').fetchall();qa.append(('duplicate_witness_names',len(dups)))
qa.append(('claims_without_section',cur.execute('SELECT COUNT(*) FROM Claims WHERE section_id IS NULL').fetchone()[0]))
qa.append(('incidents_without_section',cur.execute('SELECT COUNT(*) FROM Incidents WHERE section_id IS NULL').fetchone()[0]))
qa.append(('witnesses_without_incident',cur.execute('SELECT COUNT(*) FROM Witnesses w WHERE NOT EXISTS(SELECT 1 FROM Witness_Incidents wi WHERE wi.witness_id=w.witness_id)').fetchone()[0]))
qa.append(('incidents_without_witness',cur.execute('SELECT COUNT(*) FROM Incidents i WHERE NOT EXISTS(SELECT 1 FROM Witness_Incidents wi WHERE wi.incident_id=i.incident_id)').fetchone()[0]))
qa.append(('incidents_without_competing_explanation',cur.execute("SELECT COUNT(*) FROM Incidents i WHERE NOT EXISTS(SELECT 1 FROM Relationships r WHERE r.to_id=i.incident_id AND r.relationship_type='EXPLAINS')").fetchone()[0]))
# unresolved relationship ids check (all inserted are valid by construction)
qa.append(('relationships',cnt['Relationships']))
json.dump(dict(qa=qa,counts=cnt),open('qa.json','w'),indent=1)
# ---- exports
tables=[r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
full={}
for t in tables:
    cols=[c[1] for c in cur.execute(f'PRAGMA table_info("{t}")')];rows=cur.execute(f'SELECT * FROM "{t}"').fetchall()
    with open(f'{OUT}/database/csv/{t}.csv','w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(cols);w.writerows(rows)
    recs=[dict(zip(cols,r)) for r in rows];full[t]=recs
    json.dump(recs,open(f'{OUT}/database/json/{t}.json','w',encoding='utf-8'),indent=1,ensure_ascii=False)
json.dump(dict(schema_version=SCHEMA_VERSION,generated=GEN,tables=full),open(f'{OUT}/database/json/_complete_export.json','w',encoding='utf-8'),indent=1,ensure_ascii=False)
json.dump(dict(counts=cnt,qa=qa),open(f'{OUT}/database/json/_qa_report.json','w'),indent=1)
con.close()
print(qa);print(cnt)

import re,json
from kb import SM,sec
p='/root/.claude/uploads/0041f4a6-627b-57d1-a860-4a04cf581a1e/f3ff02a2-hastings-2008-ufos-and-nukes.md'
L=open(p,encoding='utf-8').read().split('\n')
READ=[(1,940),(13289,13992),(14894,15922),(8851,9481),(12987,13288),(5356,6120),(11026,12986),(1354,2003),(2424,2755),(5059,5355),(7416,7830),(8076,8200),(8399,8480),(8657,8850),(9863,10282),(13993,14252),(15923,16060),(17363,17824),(17825,19398)]
def isread(n): return any(a<=n<=b for a,b in READ)
json.dump(READ,open('read_ranges.json','w'))
# coverage per section
cov=[]
for s in SM:
    a,b=s['line_start'],s['line_end'];tot=max(1,b-a+1)
    r=sum(1 for n in range(a,b+1) if isread(n))
    cov.append(r/tot)
json.dump(cov,open('cov.json','w'))
MONTH=r'(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)'
DATE=re.compile(MONTH+r'\.?\s+(\d{1,2}(?:st|nd|rd|th)?,?\s+)?(19[4-9]\d|200\d)|\b(19[4-9]\d|200\d)\b')
KEY=re.compile(r'(AFB|Air Force Base|missile|ICBM|nuclear|atomic|weapons storage|WSA|launch (?:control|facility)|Minuteman|SAC|NORAD|radar|Blue Book|FBI|CIA|NSA|DIA|OSI|Los Alamos|Hanford|Oak Ridge|Savannah|Pantex|Bomb|B-52|Titan|Atlas|test shot|Pacific|Kwajalein|Eniwetok|Bikini)',re.I)
DOC=re.compile(r'(memorandum|memo|declassified|FOIA|teletype|telex|message|report|log|letter|affidavit|testimony|Blue Book)',re.I)
WIT=re.compile(r'(told me|interview|recalled|he said|she said|according to|witness|stationed)',re.I)
paras=[];cur=[];start=None
for i,l in enumerate(L,1):
    if l.strip()=='' :
        if cur: paras.append((start,' '.join(x.strip() for x in cur)));cur=[];start=None
    else:
        if start is None:start=i
        cur.append(l)
if cur: paras.append((start,' '.join(x.strip() for x in cur)))
leads=[]
for st,t in paras:
    if isread(st): continue
    if st>=23380: continue  # appendix/refs handled separately
    if len(t)<120 or t.startswith('#'): continue
    d=DATE.search(t);k=KEY.findall(t)
    if d and len(k)>=2:
        score=len(k)+(2 if DOC.search(t) else 0)+(1 if WIT.search(t) else 0)
        leads.append(dict(ln=st,score=score,date=d.group(0),text=t[:420]))
print(len(paras),len(leads))
from collections import Counter
c=Counter(sec(l['ln']) for l in leads)
json.dump(leads,open('leads_all.json','w'),indent=1,ensure_ascii=False)
print(c.most_common(10))
# per-section cap: keep top 6 by score
by={}
for l in leads: by.setdefault(sec(l['ln']),[]).append(l)
keep=[]
for s,v in by.items():
    v.sort(key=lambda x:-x['score']);keep+=v[:6]
keep.sort(key=lambda x:x['ln'])
json.dump(keep,open('leads_keep.json','w'),indent=1,ensure_ascii=False)
print(len(keep))
for l in keep[:5]: print(l['ln'],l['score'],l['date'],l['text'][:160])
# coverage summary
tr=sum(1 for n in range(1,len(L)+1) if isread(n));print('lines read',tr,len(L),round(100*tr/len(L),1))

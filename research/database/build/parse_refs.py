import re,json
from kb import SM,sec
p='/root/.claude/uploads/0041f4a6-627b-57d1-a860-4a04cf581a1e/f3ff02a2-hastings-2008-ufos-and-nukes.md'
L=open(p,encoding='utf-8').read().split('\n')
start=23548-1; end=24185-1
chap=None;cur=None;refs=[]
def flush():
    global cur
    if cur: refs.append(cur);cur=None
for i in range(start,end):
    l=L[i].rstrip()
    m=re.match(r'^\*\*(.+?)\*\*\s*$',l)
    if m: flush();chap=m.group(1).strip();continue
    m=re.match(r'^(\d{1,3})\.\s+(.*)',l)
    if m and chap:
        flush();cur=dict(chapter=chap,num=int(m.group(1)),citation=m.group(2).strip(),ln=i+1);continue
    if cur and l.strip() and not l.startswith('#'):
        cur['citation']+=' '+l.strip()
flush()
def rtype(c):
    cl=c.lower()
    if re.search(r'\b(fbi|usaf|air force|army|navy|cia|dia|nsa|norad|dod|memorandum|memo|letter|teletype|message|report|telex|afosi|osi|nmcc|jcs|aec|document|history)\b',cl) and not re.search(r'\bpress|inc\.|books?\b',cl): return 'GOVERNMENT_DOCUMENT_OR_REPORT'
    if re.search(r'(interview|e-?mail|correspondence|telephone|phone|conversation)',cl): return 'AUTHOR_INTERVIEW_OR_CORRESPONDENCE'
    if re.search(r'(newspaper|times|post|tribune|herald|journal|magazine|news|inquirer)',cl): return 'PERIODICAL_OR_NEWSPAPER'
    if re.search(r'(press|inc\.|publish|books)',cl): return 'BOOK'
    if re.search(r'(http|www\.|\.com|\.org|\.net)',cl): return 'WEB'
    return 'OTHER'
for r in refs: r['reference_type']=rtype(r['citation'])
json.dump(refs,open('refs.json','w'),indent=1,ensure_ascii=False)
from collections import Counter
print(len(refs),Counter(r['reference_type'] for r in refs).most_common())
print(Counter(r['chapter'] for r in refs).most_common(40))
for r in refs[100:106]: print(r)

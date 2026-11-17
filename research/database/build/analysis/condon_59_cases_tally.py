# Tally of my own reading of the stated conclusions of the 59 Condon Report case studies.
# Usage: python3 -I condon_59_cases_tally.py <dir-with-s4chap0N.html-lists> <out.csv>
# Categories are the analyst's judgement from the conclusion text; they are NOT the Report's own classification.
import re,sys,html,csv,collections
d,out=sys.argv[1],sys.argv[2]
titles={}
for p in ['s4chap01','s4chap02','s4chap03']:
    t=open(f'{d}/{p}.html',errors='ignore').read()
    for h,l in re.findall(r'href="([^"#]+)"[^>]*>\s*(Case\s*(\d+):[^<]*)',t,flags=re.S) and [(a,b) for a,b,c in re.findall(r'href="([^"#]+)"[^>]*>\s*(Case\s*(\d+):[^<]*)',t,flags=re.S)]:
        n=int(re.match(r'Case\s*(\d+)',l).group(1)); titles[n]=re.sub(r'\s+',' ',html.unescape(l)).strip()
E,U,I,H='EXPLAINED','UNEXPLAINED','INCONCLUSIVE','HOAX_NOEVENT_OR_PSYCH'
cat={1:(I,'altitude unknowable; debris possible'),2:(U,'genuine UFO probability "fairly high"'),3:(E,'radar chaff'),4:(I,'sample; no evidence of origin'),5:(I,'no record; recollection only'),
6:(E,'Jupiter; close-encounter part not explained'),7:(E,'ordinary object thrown'),8:(I,'single witness; cannot verify or refute'),9:(E,'Capella probable; not definite'),
10:(U,'titled No Explanation'),11:(E,'Agena reentry'),12:(U,'"interesting but unexplained"'),13:(U,'"unexplained for lack of knowledge of context"'),
14:(U,'six sightings; 3 identified; 1 strong unidentified'),15:(E,'planet'),16:(E,'commonplace phenomena'),17:(I,'impossible to say if real'),18:(E,'plastic-bag hot-air balloons'),
19:(H,'predicted event did not occur'),20:(E,'saw-whet owl'),21:(U,'"not satisfactorily explained"; radar artifact favoured'),22:(I,'not probative'),23:(E,'airplane'),24:(I,'photos not worth analysis'),
25:(E,'power-line arcs'),26:(H,'fabricated by witness'),27:(I,'instruments found nothing'),28:(E,'USAF aerial refueling'),29:(E,'flare drop'),30:(I,'rumor; could not confirm or deny'),
31:(U,'tower "not a fully satisfactory explanation"'),32:(H,'no evidence of abnormal cause of horse death'),33:(I,'serious doubts; unverifiable'),34:(I,'no further investigation'),
35:(E,'anomalous radar conditions; interpretation issue'),36:(E,'fireball'),37:(E,'Venus'),38:(E,'airplanes and stars'),39:(I,'vague; not pursued'),40:(E,'headlights/hunters'),
41:(E,'weather balloon'),42:(H,'psychological assessment; no confidence in reality'),43:(U,'"left as unidentified"'),44:(H,'witness under severe stress'),45:(E,'balloon'),
46:(U,'McMinnville: all factors consistent with extraordinary object; cannot rule out fabrication'),47:(U,'Great Falls film: airplanes "strains credibility" but not entirely ruled out'),
48:(H,'internal inconsistency in photographs'),49:(E,'probably gulls'),50:(E,'atomic-bomb simulation'),51:(E,'Venus'),52:(I,'evidence not probative'),53:(I,'little value'),
54:(E,'sub-sun hypothesis'),55:(E,'man-made flare test'),56:(I,'inconsistency impairs usefulness'),57:(I,'consistent with testimony but hand-thrown model not excluded'),
58:(I,'real objects; low information'),59:(I,'little basis for identification')}
assert len(cat)==59
cnt=collections.Counter(v[0] for v in cat.values())
with open(out,'w',newline='') as f:
    w=csv.writer(f); w.writerow(['case','title','category','basis'])
    for n in range(1,60): w.writerow([n,titles.get(n,''),cat[n][0],cat[n][1]])
print(dict(cnt),{k:round(100*v/59,1) for k,v in cnt.items()})

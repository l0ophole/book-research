import re,json,sys
p='/root/.claude/uploads/0041f4a6-627b-57d1-a860-4a04cf581a1e/f3ff02a2-hastings-2008-ufos-and-nukes.md'
L=open(p,encoding='utf-8').read().split('\n')
heads=[(i+1,len(m.group(1)),m.group(2).strip()) for i,l in enumerate(L) for m in [re.match(r'^(#{1,3}) (.*)',l)] if m]
out=[]
for k,(ln,lv,t) in enumerate(heads):
    end=(heads[k+1][0]-1) if k+1<len(heads) else len(L)
    txt='\n'.join(L[ln-1:end])
    out.append(dict(line_start=ln,line_end=end,level=lv,title=t,words=len(txt.split()),fn=len(re.findall(r'\^\d+',txt))))
json.dump(out,open('secmap.json','w'),indent=1)
for o in out: print(o['line_start'],o['line_end'],o['level'],o['words'],o['fn'],o['title'][:50])

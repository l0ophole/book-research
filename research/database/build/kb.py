import json,bisect
SM=json.load(open('/tmp/claude-0/-home-user-book-research/0041f4a6-627b-57d1-a860-4a04cf581a1e/scratchpad/secmap.json'))
STARTS=[s['line_start'] for s in SM]
def sec(ln):
    i=bisect.bisect_right(STARTS,ln)-1
    return 'SEC%03d'%(i+1)
T={k:[] for k in 'incidents claims witnesses govdocs tech sources refs expl evidence missing rq rels log'.split()}
def add(t,**kw):
    if 'ln' in kw:
        try: kw['ln']=int(kw['ln'])
        except: kw['ln']=0
        if 'sec' not in kw: kw['sec']=sec(kw['ln']) if kw['ln']>0 else None
    T[t].append(kw)
def inc(id,date,loc,desc,ln,sig='MEDIUM',status='NOT_YET_INVESTIGATED',src_type='DOCUMENT_BASED',expl=''):
    add('incidents',id=id,date=date,location=loc,description=desc,ln=ln,significance=sig,status=status,basis=src_type,notes=expl)
def clm(id,text,attrib,ctype,imp,ln,status='NOT_YET_INVESTIGATED',quote=''):
    add('claims',id=id,text=text,attribution=attrib,claim_type=ctype,importance=imp,ln=ln,status=status,quote=quote)
def wit(id,name,role,firsthand,incs,ln,notes='',identity='NAMED'):
    add('witnesses',id=id,name=name,role=role,firsthand=firsthand,incidents=incs,ln=ln,notes=notes,identity=identity)
def gov(id,title,agency,date,docno,repo,avail,ln,status='NOT_YET_INVESTIGATED',notes=''):
    add('govdocs',id=id,title=title,agency=agency,date=date,doc_no=docno,repository=repo,availability=avail,ln=ln,status=status,notes=notes)
def tech(id,etype,system,date,raw,ln,notes=''):
    add('tech',id=id,evidence_type=etype,system=system,date=date,raw_data_availability=raw,ln=ln,notes=notes)
def expl(id,target,text,support,contra,status,ln=0):
    add('expl',id=id,target=target,explanation=text,supporting=support,contradicting=contra,evaluation=status,ln=ln)
def miss(id,desc,existence,repo,method,ln,status='OPEN'):
    add('missing',id=id,description=desc,existence=existence,repository=repo,acquisition=method,ln=ln,status=status)
def rq(id,q,prio,related,have,need,sources,method,crit,status,nxt):
    add('rq',id=id,question=q,priority=prio,related=related,existing=have,missing=need,sources=sources,methods=method,criteria=crit,status=status,next_action=nxt)
def src(id,title,author,org,date,stype,cls,url,docid,pages,access,related,extract,reliab,vstatus,examined='DISCOVERED'):
    add('sources',id=id,title=title,author=author,organization=org,date=date,source_type=stype,classification=cls,url=url,doc_id=docid,pages=pages,access_date=access,related=related,extract=extract,reliability=reliab,verification=vstatus,examined=examined)
def rel(a,b,t,note=''): add('rels',frm=a,to=b,rel_type=t,note=note)
def log(ts,action,reason,tool,query,result,limits=''): add('log',ts=ts,action=action,reason=reason,tool=tool,query=query,result=result,limits=limits)
def ev(id,desc,etype,prov,related,ln,sig,status): add('evidence',id=id,description=desc,evidence_type=etype,provenance=prov,related=related,ln=ln,significance=sig,status=status)
def dump(path): json.dump(T,open(path,'w'),indent=1,ensure_ascii=False)

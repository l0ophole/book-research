"""Redo the sky test for each Anspaugh-log entry under three clock hypotheses (PyEphem; Cheyenne 41.15N 104.82W, 1 Aug 1965).
Hynek (1972) prints the entries as calls "received at the Blue Book offices" (Dayton, Ohio). Hypotheses for the printed times:
  H0 = Mountain Daylight (UTC-6, Warren local); H1 = Eastern Standard (UTC-5); H2 = Eastern Daylight (UTC-4).
Output: bright objects (mag<=1.6 stars/planets, plus the Pleiades) above 3 deg near the described direction. No satellites/aircraft."""
import ephem, math
obs=ephem.Observer();obs.lat='41.15';obs.lon='-104.82';obs.elevation=1900;obs.pressure=0
B={}
for n in ['Capella','Aldebaran','Rigel','Betelgeuse','Sirius','Vega','Deneb','Altair','Arcturus','Fomalhaut','Bellatrix','Alnilam','Mintaka','Alnitak','Menkar','Hamal','Pollux','Procyon','Antares','Spica']:
    B[n]=ephem.star(n)
pl=ephem.FixedBody();pl._ra=ephem.hours('3:47:00');pl._dec=ephem.degrees('24:07:00');pl._epoch='2000';B['Pleiades']=pl
for P in (ephem.Venus,ephem.Mars,ephem.Jupiter,ephem.Saturn): p=P();B[p.name]=p
def up(utc):
    obs.date=ephem.Date(utc);out=[]
    for n,b in B.items():
        b.compute(obs);alt=math.degrees(b.alt);az=math.degrees(b.az)
        mag=getattr(b,'mag',None) if n!='Pleiades' else 1.6
        if alt>3 and (mag is None or mag<=1.6): out.append((n,alt,az,mag))
    return out
def fmt(o,lo,hi): return ', '.join(f"{n} {a:.0f}/{z:.0f}" for n,a,z,m in o if lo<=z<=hi) or '-'
OFF={'H0 Mountain':6,'H1 EST':5,'H2 EDT':4}   # printed local clock -> UTC = printed + offset
ENT=[('0300 H-2 "white oval directly overhead"','03:00',None,'overhead'),
     ('0317 B-4 "90 mi east, descending, oval white, flashing red light, moving east"','03:17',(45,135),'east'),
     ('0320 "seven UFOs east of the site"','03:20',(45,135),'east'),
     ('0325 E site "six UFOs stacked vertically"','03:25',(30,150),'east/NE-SE'),
     ('0340 G site "one at 70 deg azimuth and one at 120"','03:40',(60,130),'az 70-120'),
     ('0400 Q flight "four NW, three NE"','04:00',(20,80),'NE (and NW below)')]
for lab,t,rng,w in ENT:
    h,m=map(int,t.split(':'))
    print(lab)
    for hn,off in OFF.items():
        o=up('1965/8/1 %02d:%02d'%(h+off,m))
        if w=='overhead': s=', '.join(f"{n} {a:.0f}/{z:.0f}" for n,a,z,_ in o if a>70) or '-'
        else: s=fmt(o,*rng)
        extra=''
        if t=='04:00': extra=' | NW: '+fmt(o,270,340)
        print(f"   {hn:12s}: {s}{extra}")

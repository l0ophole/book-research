"""Which stars/planets (mag<=2.6, alt>3 deg) lie within +-15 deg of azimuth 70 and 120 at the 3:40 log entry, under H0/H1/H2? PyEphem star list, Cheyenne, 1 Aug 1965."""
import ephem, math
obs=ephem.Observer();obs.lat='41.15';obs.lon='-104.82';obs.elevation=1900;obs.pressure=0
import ephem.stars as ST
names=[l.split(',')[0] for l in ST.db.strip().split('\n')]
bodies=[]
for n in names:
    try:
        s=ephem.star(n);bodies.append((n,s))
    except Exception: pass
for P in (ephem.Venus,ephem.Mars,ephem.Jupiter,ephem.Saturn): p=P();bodies.append((p.name,p))
for hn,off in (('H0 Mountain',6),('H1 EST',5),('H2 EDT',4)):
    obs.date=ephem.Date('1965/8/1 %02d:40'%(3+off))
    print(hn,'(3:40 printed clock)')
    for target in (70,120):
        c=[]
        for n,b in bodies:
            b.compute(obs);alt=math.degrees(b.alt);az=math.degrees(b.az)
            mag=b.mag
            if alt>3 and mag<=2.6 and abs(((az-target+180)%360)-180)<=15: c.append(f"{n} {mag:.1f} alt{alt:.0f} az{az:.0f}")
        print(f"   az {target}+-15: ",', '.join(c) or '-')

import ephem,math
d=math.degrees
o=ephem.Observer();o.lat='52.09';o.lon='1.44';o.elevation=20;o.pressure=0   # Rendlesham Forest / RAF Woodbridge
STARS=['Sirius','Procyon','Pollux','Castor','Capella','Vega','Arcturus','Spica','Regulus','Betelgeuse','Rigel','Aldebaran','Altair','Deneb']
def show(date,h,lab):  # h in UT (GMT)
    o.date=ephem.Date(date+' 00:00')+h/24.;out=[lab]
    for n,c in [('Moon',ephem.Moon),('Ven',ephem.Venus),('Mar',ephem.Mars),('Jup',ephem.Jupiter),('Sat',ephem.Saturn)]:
        b=c(o);s='%s %5.1f/%5.1f'%(n,d(b.alt),d(b.az))
        if n=='Moon': s+=' ph%2.0f%%'%b.phase
        else: s+=' m%.1f'%b.mag
        out.append(s)
    print(' | '.join(out))
    st=[]
    for n in STARS:
        b=ephem.star(n);b.compute(o)
        if 0<d(b.alt)<30: st.append('%s %.0f/%.0f'%(n,d(b.alt),d(b.az)))
    print('   low stars (<30 deg alt/az):',', '.join(st))
for dd,h,l in [('1980/12/26',2.9,'26 Dec 0250 GMT (Penniston/Burroughs start)'),('1980/12/28',0.8,'28 Dec 0050 GMT (Halt team enters ~0030)'),('1980/12/28',2.0,'28 Dec 0200 GMT (objects seen)'),('1980/12/28',3.0,'28 Dec 0300 GMT'),('1980/12/28',3.4,'28 Dec 0325 GMT (Eastern Radar log)')]:
    show(dd,h,l)

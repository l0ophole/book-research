import ephem,math
d=math.degrees
def ob(lat,lon,el=50):
    o=ephem.Observer();o.lat=str(lat);o.lon=str(lon);o.elevation=el;o.pressure=0;return o
BR=[('Sun',ephem.Sun),('Moon',ephem.Moon),('Ven',ephem.Venus),('Mar',ephem.Mars),('Jup',ephem.Jupiter),('Sat',ephem.Saturn)]
STARS=['Sirius','Arcturus','Vega','Capella','Spica','Antares','Altair','Regulus','Deneb','Fomalhaut','Procyon','Pollux','Betelgeuse','Rigel']
def show(o,utc,label):
    o.date=utc;out=[label]
    for n,c in BR:
        b=c(o);s='%s %5.1f/%5.1f'%(n,d(b.alt),d(b.az))
        if n=='Moon': s+=' ph%2.0f%%'%b.phase
        if n in('Ven','Mar','Jup','Sat'): s+=' m%.1f'%b.mag
        out.append(s)
    print(' | '.join(out))
    st=[]
    for n in STARS:
        b=ephem.star(n);b.compute(o)
        if d(b.alt)>5 and ((b.mag if hasattr(b,'mag') else 0)<=1.3): st.append('%s %.0f/%.0f'%(n,d(b.alt),d(b.az)))
    print('   stars >5deg alt (alt/az):',', '.join(st))
def L(date,h,off): return ephem.Date(date+' 00:00')+(h+off)/24.
print('Swanson, Bangor 22 Apr 1998 2122 PDT (UTC-7)')
o=ob(47.7,-122.7); show(o,L('1998/4/22',21.37,7),'21:22'); 
print('Junkin, Poulsbo 16 Sep 2004 2100 PDT')
o=ob(47.73,-122.65); show(o,L('2004/9/16',21.0,7),'21:00')
print('Fernandina Beach 23 Jun 2001 2145 EDT (UTC-4)')
o=ob(30.67,-81.45); show(o,L('2001/6/23',21.75,4),'21:45')
print('Palo Verde 20 Jul 2004 2215 MST (UTC-7)')
o=ob(33.39,-112.86); show(o,L('2004/7/20',22.25,7),'22:15')
print('Indian Point 24 Jun 1984 2230 EDT')
o=ob(41.27,-73.95); show(o,L('1984/6/24',22.5,4),'22:30')
print('Kingsland GA 14 Dec 2007 1845 EST (UTC-5)')
o=ob(30.8,-81.69); show(o,L('2007/12/14',18.75,5),'18:45')
print('Chernobyl 26 Apr 1986 ~0425 MSD (UTC+4), 3 h after explosion')
o=ob(51.39,30.10,110); show(o,L('1986/4/26',4.42,-4),'04:25')
print('Yankee Atomic, Haddam Neck CT 13 Sep 1967 2300 EDT')
o=ob(41.48,-72.50,20); show(o,L('1967/9/13',23.0,4),'23:00')

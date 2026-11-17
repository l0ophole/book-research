import ephem,math
d=math.degrees
o=ephem.Observer();o.lat='11.5';o.lon='165.4';o.elevation=3;o.pressure=0
# deck log 2305 local; Marshall Islands time UTC+12 (assumed; log may use zone -12 'M')
for off,lab in [(12,'UTC+12'),(11,'UTC+11')]:
    o.date=ephem.Date('1954/4/7 00:00')+(23.083-off)/24.
    out=[lab]
    for n,c in [('Sun',ephem.Sun),('Moon',ephem.Moon),('Ven',ephem.Venus),('Mar',ephem.Mars),('Jup',ephem.Jupiter),('Sat',ephem.Saturn)]:
        b=c(o);s='%s %5.1f/%5.1f'%(n,d(b.alt),d(b.az))
        if n=='Moon': s+=' ph%2.0f%%'%b.phase
        if n in('Ven','Mar','Jup','Sat'): s+=' m%.1f'%b.mag
        out.append(s)
    print(' | '.join(out))

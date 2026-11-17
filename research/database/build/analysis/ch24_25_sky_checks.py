import ephem,math
d=math.degrees
def ob(lat,lon,el):
    o=ephem.Observer();o.lat=str(lat);o.lon=str(lon);o.elevation=el;o.pressure=0;return o
BR=[('Sun',ephem.Sun),('Moon',ephem.Moon),('Ven',ephem.Venus),('Mar',ephem.Mars),('Jup',ephem.Jupiter),('Sat',ephem.Saturn)]
def show(o,utc,label,bodies=BR):
    o.date=utc;out=[label]
    for n,c in bodies:
        b=c(o)
        s='%s alt %5.1f az %5.1f'%(n,d(b.alt),d(b.az))
        if n=='Moon': s+=' ph%2.0f%%'%b.phase
        if n in('Ven','Mar','Jup','Sat'): s+=' m%.1f'%b.mag
        out.append(s)
    print(' | '.join(out))
print('Brown, Monarch MT (47.0N 110.9W), pre-dawn spring 1992 (MST=UTC-7; DST starts Apr 5)')
o=ob(47.0,-110.9,1300)
for date in ['1992/3/15','1992/3/28','1992/4/10','1992/4/25']:
    for h,u in [(4.5,'04:30'),(6.5,'06:30')]:
        off=7 if date<'1992/4/5' else 6
        show(o,ephem.Date(date+' 00:00')+(h+off)/24.,'%s %s'%(date,u))
print('Reager/Berrier, Ellsworth (44.15N 103.1W), 27 Oct 1992 2350 MST')
show(ob(44.15,-103.1,1000),ephem.Date('1992/10/27 00:00')+(23.83+7)/24.,'1992-10-27 23:50')
print('Goodrich, Great Falls, 2 Feb 1996 1045 MST')
show(ob(47.5,-111.3,1100),ephem.Date('1996/2/2 00:00')+(10.75+7)/24.,'1996-02-02 10:45')
print('Los Alamos area 20-21 Jul 1996 (MDT=UTC-6)')
o=ob(35.9,-106.3,2200)
for h in [21.5,22.5,27.0]:
    show(o,ephem.Date('1996/7/20 00:00')+(h+6)/24.,'1996-07-20 +%.1fh'%h)
print('Conrad MT (48.17N 111.95W) Dec 2006 (MST)')
o=ob(48.17,-111.95,1050)
for dt,h in [('2006/12/7',22.5),('2006/12/11',17.0),('2006/12/11',18.0),('2006/12/11',19.0)]:
    show(o,ephem.Date(dt+' 00:00')+(h+7)/24.,'%s %04.1fh'%(dt,h))
    # bright stars
    o.date=ephem.Date(dt+' 00:00')+(h+7)/24.
    st=[]
    for n in ['Sirius','Capella','Procyon','Betelgeuse','Rigel','Aldebaran','Arcturus','Pollux']:
        b=ephem.star(n);b.compute(o)
        if d(b.alt)>0: st.append('%s %.0f/%.0f'%(n,d(b.alt),d(b.az)))
    print('    stars up (alt/az):',', '.join(st))
print('Conrad 11 Dec 2006 late evening, rising objects')
o=ob(48.17,-111.95,1050)
for h in [21.0,22.0,23.0,24.0]:
    show(o,ephem.Date('2006/12/11 00:00')+(h+7)/24.,'2006-12-11 %04.1fh'%h,[('Moon',ephem.Moon),('Sat',ephem.Saturn)])
    o.date=ephem.Date('2006/12/11 00:00')+(h+7)/24.
    st=[]
    for n in ['Sirius','Capella','Procyon','Betelgeuse','Rigel','Aldebaran','Pollux','Regulus']:
        b=ephem.star(n);b.compute(o)
        if d(b.alt)>0: st.append('%s %.0f/%.0f'%(n,d(b.alt),d(b.az)))
    print('    stars up (alt/az):',', '.join(st))

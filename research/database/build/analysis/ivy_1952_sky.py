import ephem,math
d=math.degrees
o=ephem.Observer();o.lat='11.5';o.lon='162.3';o.elevation=3;o.pressure=0   # Eniwetok/Bikini area
STARS=['Sirius','Canopus','Arcturus','Vega','Capella','Rigel','Procyon','Betelgeuse','Achernar','Altair','Aldebaran','Spica','Antares','Fomalhaut','Pollux','Regulus','Deneb']
def show(date,h,label):
    o.date=ephem.Date(date+' 00:00')+(h-12)/24.
    out=[label]
    for n,c in [('Moon',ephem.Moon),('Ven',ephem.Venus),('Mar',ephem.Mars),('Jup',ephem.Jupiter),('Sat',ephem.Saturn)]:
        b=c(o);s='%s %5.1f/%5.1f'%(n,d(b.alt),d(b.az))
        if n=='Moon': s+=' ph%2.0f%%'%b.phase
        if n!='Moon': s+=' m%.1f'%b.mag
        out.append(s)
    print(' | '.join(out))
    st=[]
    for n in STARS:
        b=ephem.star(n);b.compute(o)
        if d(b.alt)>20: st.append('%s %.0f/%.0f'%(n,d(b.alt),d(b.az)))
    print('   stars >20 deg (alt/az):',', '.join(st))
print('Marquez (Fletcher), lookout 0345-0415 local (UTC+12), 5-7 days before Mike (1 Nov 1952): 25-27 Oct 1952')
for dd in ['1952/10/25','1952/10/26','1952/10/27']:
    show(dd,4.0,dd+' 04:00')
print('Kramer (Curtiss), evening after a movie ~2100 local, ~a week before Mike')
for dd in ['1952/10/24','1952/10/25','1952/10/26']:
    show(dd,21.0,dd+' 21:00')
print('Pantex, Amarillo (35.2N 101.8W) 7 Nov 1957 1946-2034 CST (UTC-6)')
o=ephem.Observer();o.lat='35.2';o.lon='-101.8';o.elevation=1100;o.pressure=0
for h in [19.77,20.25,20.57]:
    o.date=ephem.Date('1957/11/7 00:00')+(h+6)/24.
    out=['%.2fh'%h]
    for n,c in [('Moon',ephem.Moon),('Ven',ephem.Venus),('Mar',ephem.Mars),('Jup',ephem.Jupiter),('Sat',ephem.Saturn)]:
        b=c(o);s='%s %5.1f/%5.1f'%(n,d(b.alt),d(b.az))
        if n=='Moon': s+=' ph%2.0f%%'%b.phase
        out.append(s)
    print(' | '.join(out))
    st=[]
    for n in ['Capella','Vega','Arcturus','Altair','Fomalhaut','Deneb','Aldebaran','Antares']:
        b=ephem.star(n);b.compute(o)
        if d(b.alt)>0: st.append('%s %.0f/%.0f'%(n,d(b.alt),d(b.az)))
    print('   ',', '.join(st))

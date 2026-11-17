import ephem,math
def o(lat,lon,el):
    x=ephem.Observer(); x.lat=str(lat); x.lon=str(lon); x.elevation=el; x.pressure=0; return x
def row(ob,utc,label):
    ob.date=utc; d=math.degrees
    s=ephem.Sun(ob);m=ephem.Moon(ob)
    out=[label,'Sun %5.1f'%d(s.alt),'Moon %5.1f az %5.1f ph %2.0f%%'%(d(m.alt),d(m.az),m.phase)]
    for n,b in [('Ve',ephem.Venus(ob)),('Ma',ephem.Mars(ob)),('Ju',ephem.Jupiter(ob)),('Sa',ephem.Saturn(ob))]:
        b.compute(ob); out.append('%s %5.1f az %5.1f m%.1f'%(n,d(b.alt),d(b.az),b.mag))
    print(' | '.join(out))
print('Byelokoroviche 4 Oct 1982, MSK=UTC+3')
ob=o(51.17,28.05,150)
for h in [17,18,19,20,21,22,23]:
    row(ob,ephem.Date('1982/10/4 00:00')+(h-3)/24.,'%02d:00 MSK'%h)
print('Kapustin Yar 28-29 Jul 1989, local=UTC+4')
ob=o(48.6,46.3,50)
for h in [22.2,23,24,25,26,25.5+0]:
    row(ob,ephem.Date('1989/7/28 00:00')+(h-4)/24.,'%5.1f h'%h)
print('Manzano 8 Aug 1980 2350 MDT (UTC-6)')
ob=o(35.0,-106.5,1900)
for h in [23.0,23.83,24.5,25.5]:
    row(ob,ephem.Date('1980/8/8 00:00')+(h+6)/24.,'%5.2f h'%h)
print('Katta-Kurgan Oct 1984 2345 local (UTC+5): Moon by date')
ob=o(39.64,65.98,500)
for dday in range(1,32,3):
    row(ob,ephem.Date('1984/10/%d 00:00'%dday)+(23.75-5)/24.,'Oct %2d 2345'%dday)

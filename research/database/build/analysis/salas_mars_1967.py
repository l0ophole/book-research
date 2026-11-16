import ephem,math
# Malmstrom AFB approx 47.505N 111.183W, elev ~1100 m; MST = UTC-7 (no DST in March)
def obs(dt):
    o=ephem.Observer(); o.lat='47.505'; o.lon='-111.183'; o.elevation=1100; o.pressure=0; o.date=dt; return o
for day in ['1967/3/15','1967/3/16','1967/3/23','1967/3/24','1967/3/25']:
    o=obs(day+' 00:00')
    print(day,'(local midnight start)')
    for h in range(0,25,2):
        # local hour h on 'day' -> UTC +7
        t=ephem.Date(ephem.Date(day+' 00:00')+(h+7)/24.)
        o.date=t
        m=ephem.Mars(o); s=ephem.Sun(o); mo=ephem.Moon(o); v=ephem.Venus(o); j=ephem.Jupiter(o); sa=ephem.Saturn(o)
        print('  %02d:00 MST Mars alt %6.1f az %5.1f mag %.1f | Sun alt %6.1f | Moon alt %6.1f ph %2.0f%% | Venus alt %5.1f mag %.1f | Jup alt %5.1f | Sat alt %5.1f'%(h,math.degrees(m.alt),math.degrees(m.az),m.mag,math.degrees(s.alt),math.degrees(mo.alt),mo.phase,math.degrees(v.alt),v.mag,math.degrees(j.alt),math.degrees(sa.alt)))

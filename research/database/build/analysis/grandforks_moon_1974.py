"""Moon and bright-object check for the Grand Forks AFB bomber-alert-area sighting, reported as 9:09 pm on 14 Oct 1974 (CDT = UTC-5).
The book (via the witness's report to Hynek) says a last-quarter moon had risen in the east. PyEphem; observer 47.96N 97.40W."""
import ephem, math
o=ephem.Observer();o.lat='47.96';o.lon='-97.40';o.elevation=270;o.pressure=0
o.date=ephem.Date('1974/10/15 02:09')
m=ephem.Moon(o);print('Moon at 21:09 CDT 14 Oct 1974: alt %.0f az %.0f illuminated %.0f%%'%(math.degrees(m.alt),math.degrees(m.az),m.phase))
print('last quarter nearest before:',ephem.previous_last_quarter_moon('1974/10/15'),'| new moon after:',ephem.next_new_moon('1974/10/10'))
o.date=ephem.Date('1974/10/15 00:00');print('next moonrise after 19:00 CDT 14 Oct:',o.next_rising(ephem.Moon()),'UTC')
# when was the Moon ~last quarter and risen in the east around 21:00 CDT?
for d in range(1,16):
    o.date=ephem.Date('1974/10/%d 02:09'%(d+1));m=ephem.Moon(o);m.compute(o)
    print('  evening of Oct %2d 21:09 CDT: alt %4.0f az %3.0f illum %3.0f%%'%(d,math.degrees(m.alt),math.degrees(m.az),m.phase))

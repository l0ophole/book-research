"""Moon phase/position at ~18:15 MST (01:15Z next day) near Wall SD (Delta-3) for 28 Dec 1978 - 10 Jan 1979, for the Mills (Ellsworth) account of a pitch-black sky,
and bright stars that would be overhead (Capella near zenith in early January). PyEphem; 43.99N 102.24W."""
import ephem, math
w=ephem.Observer();w.lat='43.99';w.lon='-102.24';w.pressure=0
for d in range(28,32):
    w.date=ephem.Date('1978/12/%d 01:15'%d)+1;m=ephem.Moon(w);m.compute(w);print('1978-12-%d 18:15 MST moon alt %3.0f az %3.0f illum %3.0f%%'%(d,math.degrees(m.alt),math.degrees(m.az),m.phase))
for d in range(1,11):
    w.date=ephem.Date('1979/1/%d 01:15'%d)+1;m=ephem.Moon(w);m.compute(w);print('1979-01-%02d 18:15 MST moon alt %3.0f az %3.0f illum %3.0f%%'%(d,math.degrees(m.alt),math.degrees(m.az),m.phase))
w.date=ephem.Date('1979/1/3 01:15')
for n in ['Capella','Vega','Rigel','Aldebaran','Sirius']:
    s=ephem.star(n);s.compute(w);print(' ',n,'alt %.0f az %.0f'%(math.degrees(s.alt),math.degrees(s.az)))

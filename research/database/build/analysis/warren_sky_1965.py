"""Sky over F.E. Warren AFB (Cheyenne WY) on 1 Aug 1965, 0100-0440 MDT, using PyEphem (pip install ephem).
Lists bright stars/planets above 3 deg and the Moon; key log times 0317, 0320, 0325, 0327-0340, 0400 MDT."""
import ephem, math
obs=ephem.Observer();obs.lat='41.15';obs.lon='-104.82';obs.elevation=1900;obs.pressure=0   # no refraction
bodies=[ephem.Venus(),ephem.Mars(),ephem.Jupiter(),ephem.Saturn(),ephem.Moon()]
stars={n:ephem.star(n) for n in ['Capella','Aldebaran','Rigel','Betelgeuse','Sirius','Pollux','Procyon','Vega','Deneb','Altair','Arcturus','Fomalhaut','Alnilam','Mintaka','Alnitak','Bellatrix','Menkar','Hamal']}
def line(t):
    obs.date=ephem.Date(t)   # t given as UTC string
    out=[]
    for b in bodies:
        b.compute(obs)
        if math.degrees(b.alt)>3: out.append(f"{b.name} {math.degrees(b.alt):.0f}/{math.degrees(b.az):.0f} m{b.mag:.1f}")
    for n,s in stars.items():
        s.compute(obs)
        if math.degrees(s.alt)>3 and s.mag<1.8 or (n in('Alnilam','Mintaka','Alnitak') and math.degrees(s.alt)>1):
            out.append(f"{n} {math.degrees(s.alt):.0f}/{math.degrees(s.az):.0f} m{s.mag:.1f}")
    return out
for lab,t in (('0130 MDT','1965/8/1 07:30'),('0230','1965/8/1 08:30'),('0317','1965/8/1 09:17'),('0325','1965/8/1 09:25'),('0340','1965/8/1 09:40'),('0400','1965/8/1 10:00'),('0430','1965/8/1 10:30')):
    print(lab,'|',', '.join(line(t)))
sun=ephem.Sun();obs.date=ephem.Date('1965/8/1 10:30');obs.pressure=1013;sun.compute(obs);print('Sun alt at 0430 MDT %.0f deg; moon phase %.0f%%'%(math.degrees(sun.alt),(lambda m:(m.compute(obs),m.phase)[1])(ephem.Moon())))

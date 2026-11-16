"""1964-5A (Saturn SA-5 S-IV stage, 'Saturn 5' in SAO SR-289) visible passes over Cheyenne, 31 Jul-1 Aug 1965, from SAO daily mean elements.
Row MJD 38973.0 (1 Aug 1965 0h UT): w=57.41, Om=96.011, i=31.4594, e=0.02197, M=0.7585 rev, n=15.568706 rev/d, n'/2=5.28e-4, a=6.772939 (x1000 km).
Row MJD 38974.0: w=67.9, Om=89.11, M=0.3280 (check: 0.3272). Rates: w +10.5 deg/d, Om -6.90 deg/d.
Window widened to 0000-1200Z to include evening and dawn passes. Visibility: sat sunlit, observer sun alt < -6, sat elevation > 5."""
import sys,ephem;sys.path.insert(0,'.')
import warren_echo2_passes as E
E.SETS['S5']=dict(T0=38973.0,w=(57.41,10.5,0.0),Om=(96.011,-6.90,0.0),i=31.4594,e=(0.02197,-2e-5,0.0),M=(0.7585,15.568706,5.28e-4,0.0,0.0))
res=E.run('S5',38973.0,38973.0+12/24)
def hhmm(m,off): d=ephem.Date(m-15019.5-off/24).tuple();return '%02d:%02d'%(d[3],d[4])
P=E.passes(res)
print('1964-5A visible passes (Z):',len(P))
for p in P:
    pk=max(p,key=lambda r:r[1]);t0=p[0][0];t1=p[-1][0]
    print(f"  Z {E.utc(t0)}-{E.utc(t1)} el_max {pk[1]:.0f} az {p[0][2]:.0f}->{pk[2]:.0f}->{p[-1][2]:.0f} | MDT {hhmm(t0,6)}-{hhmm(t1,6)} EST {hhmm(t0,5)}-{hhmm(t1,5)} EDT {hhmm(t0,4)}-{hhmm(t1,4)}")
# geometry-only passes for context
cur=[];print('geometric passes (el>5, any illumination) with sunlit fraction:')
for m,el,az,rg,salt,lit in res:
    if el>5: cur.append((m,el,az,salt,lit))
    elif cur:
        print(f"  Z {E.utc(cur[0][0])}-{E.utc(cur[-1][0])} sunlit {sum(c[4] for c in cur)/len(cur):.0%} sun_alt {cur[0][3]:.0f}");cur=[]

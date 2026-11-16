"""Echo 1 (1960 Iota 1) visible passes over Cheyenne, night of 31 Jul-1 Aug 1965, from SAO daily MEAN elements
(SAO Special Report 289, 'SAO mean elements - Satellite 1960 Iota 1, August 1-31, 1965', NTRS 19700026243 p.22).
Row MJD 38973.0 (1 Aug 1965 0h UT): w=18.82 deg, Om=77.931, i=47.271, e=0.05201, M=0.5062 rev, n=12.69403 rev/day, a=7.761971 (x1000 km).
Row MJD 38974.0: w=22.5, Om=74.537, M=0.1991 (consistency check: M(38974) from n = 0.2002). Rates: w +3.68 deg/d, Om -3.394 deg/d.
Uses the propagation/visibility machinery of warren_echo2_passes.py."""
import math,sys
sys.path.insert(0,'.')
import warren_echo2_passes as E
E.SETS['E1']=dict(T0=38973.0,w=(18.82,3.68,0.0),Om=(77.931,-3.394,0.0),i=47.271,e=(0.05201,-3.7e-3,0.0),M=(0.5062,12.69403,0.0,0.0,0.0))
# e rate: 0.05201 -> 0.05174 per day => -0.00027/d ; fix
E.SETS['E1']['e']=(0.05201,-0.00027,0.0)
res=E.run('E1',38973.0+4/24,38973.0+11/24)
print('Echo 1 (mean elements, epoch 1 Aug 0h UT):')
for p in E.passes(res):
    peak=max(p,key=lambda r:r[1]);t0=p[0][0];t1=p[-1][0]
    import ephem
    def hhmm(m,off): d=ephem.Date(m-15019.5-off/24).tuple();return '%02d:%02d'%(d[3],d[4])
    print(f"  Z {E.utc(t0)}-{E.utc(t1)} (peak {E.utc(peak[0])}) el_max {peak[1]:.0f} az {p[0][2]:.0f}->{peak[2]:.0f}->{p[-1][2]:.0f} | H0 MDT {hhmm(t0,6)}-{hhmm(t1,6)}, H1 EST {hhmm(t0,5)}-{hhmm(t1,5)}, H2 EDT {hhmm(t0,4)}-{hhmm(t1,4)}")

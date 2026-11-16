"""Echo 2 (1964-004A) visible passes over Cheyenne WY, 31 Jul-1 Aug 1965, from SAO smoothed MEAN elements
(SAO Special Report 289, Orbital Elements No. 0-19, 24 Dec 1968; NTRS 19700026243; Echo 2 sets for 16 Jul-1 Aug [T0=MJD 38965] and 1-16 Aug [T0=MJD 38981]).
Elements (OCR-read; cross-checked: Omega, omega and M advance consistently between the two sets):
  set B (T0=38965.0): w=176.07-1.7767t+2.5586cos w ; Om=312.4476-0.8313t ; i=81.447 ; e=0.02593+7.0e-5t+0.0010928 sin w ; M(rev)=0.4402+13.30358t+9.91e-5 t^2-1.09e-6 t^3-0.0070988 cos w
  set C (T0=38981.0): w=146.89-1.897t+2.097cos w ; Om=299.1665-0.8326t ; i=81.454 ; e=0.02582-1.17e-4 t+0.0010931 sin w ; M(rev)=0.32041+13.30620t+4.3e-5 t^2-1.48e-6 t^3-0.0066847 cos w
Keplerian propagation of mean elements (no short-period J2 terms) -> positions good to ~10s of km. Visibility: sat sunlit, observer sun alt < -6 deg, sat elevation > 5 deg.
Brightness not computed (Echo 2 is a 41-m balloon, typically about mag +1 to +2.5 in a good pass)."""
import math, numpy as np, ephem
MU=398600.4418;RE=6378.137
SETS={'B':dict(T0=38965.0,w=(176.07,-1.7767,2.5586),Om=(312.4476,-0.8313,0.0),i=81.447,e=(0.02593,7.0e-5,0.0010928),M=(0.4402,13.30358,9.91e-5,-1.09e-6,-0.0070988)),
      'C':dict(T0=38981.0,w=(146.89,-1.897,2.097),Om=(299.1665,-0.8326,0.0),i=81.454,e=(0.02582,-1.17e-4,0.0010931),M=(0.32041,13.30620,4.3e-5,-1.48e-6,-0.0066847))}
def mjd(y,mo,d,h):  # UTC
    return ephem.Date('%d/%d/%d %02d:%02d:%02d'%(y,mo,d,int(h),int((h%1)*60),int(((h*60)%1)*60)))+0 + 15019.5
def prop(S,mj):
    t=mj-S['T0'];w0,w1,w2=S['w'];cw=math.cos(math.radians(w0))
    for _ in range(3):
        w=w0+w1*t+w2*math.cos(math.radians(w0+w1*t))
    Om=S['Om'][0]+S['Om'][1]*t;i=S['i'];e=S['e'][0]+S['e'][1]*t+S['e'][2]*math.sin(math.radians(w))
    M0,n,m2,m3,mc=S['M'];M=(M0+n*t+m2*t*t+m3*t**3+mc*math.cos(math.radians(w)))*2*math.pi
    nn=n*2*math.pi/86400.0;a=(MU/nn**2)**(1/3.)
    E=M
    for _ in range(12): E=M+e*math.sin(E)
    nu=2*math.atan2(math.sqrt(1+e)*math.sin(E/2),math.sqrt(1-e)*math.cos(E/2));r=a*(1-e*math.cos(E))
    u=math.radians(w)+nu;O=math.radians(Om);ii=math.radians(i)
    x=r*(math.cos(O)*math.cos(u)-math.sin(O)*math.sin(u)*math.cos(ii));y=r*(math.sin(O)*math.cos(u)+math.cos(O)*math.sin(u)*math.cos(ii));z=r*math.sin(u)*math.sin(ii)
    return np.array([x,y,z])
def gmst(mj):  # radians
    jd=mj+2400000.5;T=(jd-2451545.0)/36525
    g=280.46061837+360.98564736629*(jd-2451545.0)+0.000387933*T*T
    return math.radians(g%360)
lat=math.radians(41.15);lon=math.radians(-104.82);h=1.9
def site_ecef():
    f=1/298.257;e2=2*f-f*f;N=RE/math.sqrt(1-e2*math.sin(lat)**2)
    return np.array([(N+h)*math.cos(lat)*math.cos(lon),(N+h)*math.cos(lat)*math.sin(lon),(N*(1-e2)+h)*math.sin(lat)])
S0=site_ecef()
obs=ephem.Observer();obs.lat='41.15';obs.lon='-104.82';obs.pressure=0
def look(Seteci,mj):
    g=gmst(mj);c,s=math.cos(g),math.sin(g)
    # ECI->ECEF
    xe=c*Seteci[0]+s*Seteci[1];ye=-s*Seteci[0]+c*Seteci[1];ze=Seteci[2]
    d=np.array([xe,ye,ze])-S0
    up=np.array([math.cos(lat)*math.cos(lon),math.cos(lat)*math.sin(lon),math.sin(lat)])
    east=np.array([-math.sin(lon),math.cos(lon),0]);north=np.cross(up,east)
    el=math.degrees(math.asin(d@up/np.linalg.norm(d)));az=math.degrees(math.atan2(d@east,d@north))%360
    return el,az,np.linalg.norm(d)
sun=ephem.Sun()
def sunstate(mj,Seteci):
    obs.date=ephem.Date(mj-15019.5);sun.compute(obs);salt=math.degrees(sun.alt)
    # sun ECI direction
    ra,dec=sun.g_ra,sun.g_dec;sv=np.array([math.cos(dec)*math.cos(ra),math.cos(dec)*math.sin(ra),math.sin(dec)])
    dot=Seteci@sv;perp=np.linalg.norm(Seteci-dot*sv)
    lit=not(dot<0 and perp<RE)
    return salt,lit
def run(setname,t0,t1,step=10):
    S=SETS[setname];res=[];m=t0
    while m<t1:
        P=prop(S,m);el,az,rg=look(P,m);salt,lit=sunstate(m,P)
        res.append((m,el,az,rg,salt,lit));m+=step/86400.0
    return res
def passes(res):
    out=[];cur=None
    for m,el,az,rg,salt,lit in res:
        vis=(el>5 and lit and salt<-6)
        if vis:
            if cur is None: cur=[]
            cur.append((m,el,az,rg))
        elif cur: out.append(cur);cur=None
    if cur: out.append(cur)
    return out
def utc(m):
    d=ephem.Date(m-15019.5).tuple();return '%02d:%02d:%02d'%(d[3],d[4],int(d[5]))
if __name__=='__main__':
    # Aug 1 1965 UTC: 0400-1100Z (22h MDT Jul31 - 05h MDT) ; MJD of 1965-08-01 = 38973
    base=38973.0
    for name in ('C','B'):
        print('=== element set',name)
        res=run(name,base+4/24,base+11/24)
        for p in passes(res):
            peak=max(p,key=lambda r:r[1]);t0=p[0][0];t1=p[-1][0]
            def hhmm(m,off): 
                d=ephem.Date(m-15019.5-off/24).tuple();return '%02d:%02d'%(d[3],d[4])
            print(f"  Z {utc(t0)}-{utc(t1)} (peak {utc(peak[0])}) el_max {peak[1]:.0f} az {p[0][2]:.0f}->{peak[2]:.0f}->{p[-1][2]:.0f} | printed-clock if H0 MDT {hhmm(t0,6)}-{hhmm(t1,6)}, H1 EST {hhmm(t0,5)}-{hhmm(t1,5)}, H2 EDT {hhmm(t0,4)}-{hhmm(t1,4)}")

import math
R=3958.8
def hav(a,b):
    la1,lo1,la2,lo2=map(math.radians,(*a,*b))
    h=math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(math.sqrt(h))
def brg(a,b):
    la1,lo1,la2,lo2=map(math.radians,(*a,*b))
    y=math.sin(lo2-lo1)*math.cos(la2);x=math.cos(la1)*math.sin(la2)-math.sin(la1)*math.cos(la2)*math.cos(lo2-lo1)
    return (math.degrees(math.atan2(y,x))+360)%360
def xtrack(p,a,b):
    d13=hav(a,p)/R;t13=math.radians(brg(a,p));t12=math.radians(brg(a,b))
    return math.asin(math.sin(d13)*math.sin(t13-t12))*R, math.acos(math.cos(d13)/math.cos(math.asin(math.sin(d13)*math.sin(t13-t12))))*R
T=(33.6773,-106.4752)   # Trinity Site
RAAF=(33.301,-104.531)  # Roswell AAF / Walker AFB
RTOWN=(33.3943,-104.5230)
CAP=(33.5,-105.57)      # Capitan, approx
D={'BLM point (33.952,-105.331)':(33.952189,-105.331214),'Wikipedia (33.968,-105.243)':(33+58.1/60,-(105+14.6/60)),'Wikipedia deg (33.9503,-105.3142)':(33+57/60+1/3600,-(105+18/60+51/3600))}
print('Trinity-RAAF distance mi %.1f ; bearing %.0f'%(hav(T,RAAF),brg(T,RAAF)))
mid=((T[0]+RAAF[0])/2,(T[1]+RAAF[1])/2); print('midpoint approx',mid,'Capitan to midpoint %.1f mi'%hav(CAP,mid))
for k,p in D.items():
    xt,at=xtrack(p,T,RAAF)
    print(k,'| to Trinity %.1f mi | to RAAF %.1f mi (brg from RAAF %.0f) | offset from straight line %.1f mi | along-track from Trinity %.1f of %.1f'%(hav(p,T),hav(p,RAAF),brg(RAAF,p),abs(xt),at,hav(T,RAAF)))
print('Capitan to RAAF %.1f mi bearing %.0f'%(hav(CAP,RAAF),brg(RAAF,CAP)))

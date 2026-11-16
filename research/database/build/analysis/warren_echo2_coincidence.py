"""How many Anspaugh-log times fall inside Echo 2 visible-pass windows, versus chance?
Pass windows (UTC, 1 Aug 1965, from warren_echo2_passes.py): P1 05:02-05:08, P2 06:50-06:59.5, P3 08:38.8-08:48.
Log times (printed clock, minutes after 00:00): calls and event times in Hynek's printing."""
import random
passes=[(5*60+2,5*60+8),(6*60+50,6*60+59.5),(8*60+38.8,8*60+48)]
times={'1:30':90,'1:45':105,'1:48':108,'1:49':109,'2:20':140,'2:50':170,'3:00':180,'3:17':197,'3:20':200,'3:25':205,'3:27':207,'3:28':208,'3:32':212,'3:35':215,'3:40':220,'4:00':240,'4:05':245,'4:40':280}
def hits(offset_min, slack=0):
    h=[k for k,t in times.items() if any(a-slack<=t+offset_min<=b+slack for a,b in passes)]
    return h
for lab,off in (('H0 Mountain (UTC=local+6h)',6*60),('H1 EST (+5h)',5*60),('H2 EDT (+4h)',4*60)):
    print(lab,'-> entries inside a pass window:',hits(off),'| within +-3 min:',hits(off,3))
random.seed(1);N=20000;cnt={}
for _ in range(N):
    off=random.uniform(3*60,8*60);k=len(hits(off,3));cnt[k]=cnt.get(k,0)+1
print('chance (random clock offset 3-8 h, +-3 min slack): P(k entries matched) =',{k:round(v/N,3) for k,v in sorted(cnt.items())})
mean=sum(k*v for k,v in cnt.items())/N;print('mean matched entries by chance: %.1f of %d'%(mean,len(times)))

# Base rate: fraction of days in 1951-1955 that fall within N days after a Nevada atmospheric test shot.
# Shot dates are from my memory of the published DOE/NNSA list (not re-verified this session).
import datetime as dt
D=dt.date
shots=[ # Ranger 1951
D(1951,1,27),D(1951,1,28),D(1951,2,1),D(1951,2,2),D(1951,2,6),
# Buster-Jangle
D(1951,10,22),D(1951,10,28),D(1951,10,30),D(1951,11,1),D(1951,11,5),D(1951,11,19),D(1951,11,29),
# Tumbler-Snapper
D(1952,4,1),D(1952,4,15),D(1952,4,22),D(1952,5,1),D(1952,5,7),D(1952,5,25),D(1952,6,1),D(1952,6,5),
# Upshot-Knothole
D(1953,3,17),D(1953,3,24),D(1953,3,31),D(1953,4,6),D(1953,4,11),D(1953,4,18),D(1953,4,25),D(1953,5,8),D(1953,5,19),D(1953,5,25),D(1953,6,4),
# Teapot
D(1955,2,18),D(1955,2,22),D(1955,3,1),D(1955,3,7),D(1955,3,12),D(1955,3,22),D(1955,3,23),D(1955,3,29),D(1955,4,6),D(1955,4,9),D(1955,4,15),D(1955,5,5),D(1955,5,15)]
start,end=D(1951,1,1),D(1955,12,31)
n=(end-start).days+1
for N in (3,5,7,10):
    covered=set()
    for s in shots:
        for k in range(0,N+1):
            d=s+dt.timedelta(days=k)
            if start<=d<=end: covered.add(d)
    print('within 0-%d days after any shot: %d of %d days = %.1f%%'%(N,len(covered),n,100*len(covered)/n))
# also fraction within the active test-series windows themselves
wins=[(D(1951,1,27),D(1951,2,6)),(D(1951,10,22),D(1951,11,29)),(D(1952,4,1),D(1952,6,5)),(D(1953,3,17),D(1953,6,4)),(D(1955,2,18),D(1955,5,15))]
w=set()
for a,b in wins:
    d=a
    while d<=b: w.add(d); d+=dt.timedelta(days=1)
print('days inside a series window: %d = %.1f%%'%(len(w),100*len(w)/n))

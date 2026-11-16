"""Recompute relative echo speeds for Minot B-52 radarscope frames 771-773.
Inputs are Shough's measured positions (azimuth from nose, slant range NM). Co-altitude, single-target assumptions."""
import math
F={771:(138,1.62),772:(242,1.05),773:(40,1.05)}
xy=lambda az,r:(r*math.sin(math.radians(az)),r*math.cos(math.radians(az)))
P={k:xy(*v) for k,v in F.items()}
d=lambda a,b:math.hypot(P[a][0]-P[b][0],P[a][1]-P[b][1])
d1,d2=d(771,772),d(772,773)
print(f"displacements NM {d1:.2f} {d2:.2f}")
for lab,dd,t in(('naive771-772',d1,3.0),('naive772-773',d2,3.0),('Shough771-772',d1,3.8),('Shough772-773',d2,1.3)):
    kt=dd/t*3600;print(f"{lab}: {kt:,.0f} kt = {kt*1.1508:,.0f} mph")
print("simple mean of the two corrected rates (kt):",round((d1/3.8+d2/1.3)/2*3600))
print("time-weighted mean over 5.1 s (kt):",round((d1+d2)/5.1*3600))

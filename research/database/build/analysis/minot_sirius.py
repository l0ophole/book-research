"""Approximate Sirius/Vega altitude-azimuth over Minot AFB, 24 Oct 1968 (UTC). Simple GMST + precession; no refraction."""
import math
def jd(y,m,d,h):
    if m<=2:y-=1;m+=12
    A=y//100;B=2-A+A//4
    return int(365.25*(y+4716))+int(30.6001*(m+1))+d+B-1524.5+h/24
gmst=lambda J:(280.46061837+360.98564736629*(J-2451545.0)+0.000387933*((J-2451545.0)/36525)**2)%360
def altaz(ra_h,dec,lat,lon,J):
    H=math.radians((gmst(J)+lon)%360-ra_h*15);d=math.radians(dec);p=math.radians(lat)
    alt=math.degrees(math.asin(math.sin(d)*math.sin(p)+math.cos(d)*math.cos(p)*math.cos(H)))
    az=math.degrees(math.atan2(-math.sin(H)*math.cos(d),math.sin(d)*math.cos(p)-math.cos(d)*math.sin(p)*math.cos(H)))%360
    return alt,az
def prec(ra_h,dec,yrs):
    a=math.radians(ra_h*15);d=math.radians(dec)
    return (ra_h*15-(3.07+1.336*math.sin(a)*math.tan(d))*yrs/3600*15)/15,dec-20.04*math.cos(a)*yrs/3600
sir=prec(6+45/60+8.9/3600,-16.7161,31.2);veg=prec(18+36/60+56.3/3600,38.7837,31.2)
for hh,mm in[(8,0),(8,30),(8,58),(9,6),(9,26),(9,40),(10,4),(10,10)]:
    J=jd(1968,10,24,hh+mm/60);print(f"{hh:02d}{mm:02d}Z Sirius {altaz(*sir,48.4155,-101.3577,J)} Vega {altaz(*veg,48.4155,-101.3577,J)}")

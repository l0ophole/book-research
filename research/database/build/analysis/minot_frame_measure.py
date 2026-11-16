"""Independent measurement of echoes in Minot B-52 radarscope frames 772 and 773.
Usage: python3 minot_frame_measure.py All-Radarscope-Photographs.pdf
Method: extract the 300-ppi scans (pdfimages), locate the scope centre spot, calibrate the range rings from
the radial profile (frame 771: rings at 60/134/208 px, hole edge 266 px), find the strongest local-contrast blob
inside the 'altitude hole' (difference of 9-px and 71-px box filters), and convert to slant range with
  slant_NM = r_px/148 + 0.345   (rings assumed at 0.75/1.25/1.75 NM per Shough; offset = short-range TR hole)
Screen orientation assumed heading-up and constant between frames (Shough: no evidence of a turn).
Limitations: frame 771's echo overlaps the third range ring and was NOT independently recovered.
"""
import sys,subprocess,tempfile,os,math,numpy as np
from PIL import Image
pdf=sys.argv[1];tmp=tempfile.mkdtemp();subprocess.run(['pdfimages','-png','-f','1','-l','3',pdf,tmp+'/s'],check=True)
def box(a,k):
    c=np.cumsum(np.cumsum(np.pad(a,((1,0),(1,0))),0),1);h,w=a.shape;r=k//2
    ys=np.arange(h);xs=np.arange(w);y0=np.clip(ys-r,0,h);y1=np.clip(ys+r+1,0,h);x0=np.clip(xs-r,0,w);x1=np.clip(xs+r+1,0,w)
    return (c[np.ix_(y1,x1)]-c[np.ix_(y0,x1)]-c[np.ix_(y1,x0)]+c[np.ix_(y0,x0)])/((y1-y0)[:,None]*(x1-x0)[None,:])
PX=148.0
CENT={772:(877.4,1131.8,212),773:(890.9,1084.3,206)}   # centre x,y and hole-edge radius (px), measured as described
RES={}
for n,f in((772,'s-001.png'),(773,'s-002.png')):
    im=np.asarray(Image.open(f'{tmp}/{f}').convert('L')).astype(float);cx,cy,he=CENT[n]
    H,W=im.shape;Y,X=np.mgrid[0:H,0:W];R=np.hypot(X-cx,Y-cy);A=np.degrees(np.arctan2(X-cx,-(Y-cy)))%360
    dog=box(im,9)-box(im,71);m=(R>80)&(R<he-12)&(np.abs(R-134)>7)   # exclude centre smudge zone and ring 2
    c=np.where(m,dog,-999);iy,ix=np.unravel_index(c.argmax(),c.shape)
    RES[n]=(R[iy,ix],A[iy,ix],c[iy,ix]);print(n,'blob r_px=%.0f screen_angle=%.0f dog=%.0f'%RES[n])
def xy(r,a,off):
    s=r/PX+off;return s*math.sin(math.radians(a)),s*math.cos(math.radians(a)),s
for off,lab in((0.345,'rings at 0.75/1.25/1.75 NM (Shough)'),(0.0,'linear from centre (no TR-hole offset)')):
    p772=xy(RES[772][0],RES[772][1],off);p773=xy(RES[773][0],RES[773][1],off)
    dd=math.hypot(p772[0]-p773[0],p772[1]-p773[1])
    print(f'{lab}: ranges {p772[2]:.2f},{p773[2]:.2f} NM; displacement {dd:.2f} NM; naive 3.0 s -> {dd/3*3600:,.0f} kt; Shough 1.3 s -> {dd/1.3*3600:,.0f} kt')

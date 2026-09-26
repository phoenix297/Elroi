"""Traces the client logo (logo-source.jpg) into SVG paths in logo_paths.json. Run once when the logo changes."""
import numpy as np
from PIL import Image, ImageFilter
from skimage import measure
import os
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'logo-source.jpg')
g=Image.open(SRC).convert('L')
a=np.asarray(g).astype(float)
lab=measure.label(a<110,connectivity=2)
def trace(labels, scale=4, tol=0.35):
    keep=np.isin(lab,labels)
    # grow mask a little so antialiased edges stay, blank everything else
    from scipy import ndimage
    grow=ndimage.binary_dilation(keep,iterations=3)
    b=np.where(grow,a,255.0)
    im=Image.fromarray(b.astype('uint8')).resize((b.shape[1]*scale,b.shape[0]*scale),Image.BICUBIC).filter(ImageFilter.GaussianBlur(scale*0.6))
    c=np.asarray(im).astype(float)
    paths=[]
    for ct in measure.find_contours(c,128):
        ct=measure.approximate_polygon(ct,tol*scale)
        if len(ct)<4: continue
        pts=' '.join(f'{x/scale:.1f} {y/scale:.1f}' for y,x in ct)
        paths.append('M'+pts+'Z')
    return ''.join(paths)
import json
E=trace([1])
letters=[l for l in range(2,lab.max()+1)]
top=[r.label for r in measure.regionprops(lab) if r.label!=1 and r.bbox[0]<400]
bottom=[r.label for r in measure.regionprops(lab) if r.bbox[0]>=400]
json.dump({'E':E,'elroi':trace(top),'ship':trace(bottom)},open(os.path.join(HERE, 'logo_paths.json'), 'w'))
print(len(E),len(trace(top)),len(trace(bottom)))

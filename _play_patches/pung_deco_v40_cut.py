from PIL import Image
import numpy as np, base64, io, json
from scipy import ndimage as nd
im=Image.open('/mnt/user-data/uploads/0a13117c-image.png').convert('RGB')
B={'beanie':(690,18,169,166),'flower':(987,59,180,97),'bow':(153,108,110,148),'scarf':(307,122,256,133),'crown':(134,306,92,87),'glasses':(400,376,170,79),
   'bowtie':(713,385,143,135),'cape':(905,407,243,145),'santa':(31,603,224,138),'raincoat':(378,628,195,204),'band':(1007,651,143,79),'backpack':(653,703,135,132)}
HOLE={'scarf','bowtie','cape','backpack'}
out={}
for k,(x,y,w,h) in B.items():
    a=np.array(im.crop((x-4,y-4,x+w+4,y+h+4))).astype(int)
    white=a.min(2)>242; lab,n=nd.label(white); sizes=nd.sum(white,lab,range(1,n+1))
    rm=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])).tolist())-{0}
    if k in HOLE: rm|={i+1 for i,s in enumerate(sizes) if s>300}
    bg=np.isin(lab,list(rm))
    if k=='raincoat':
        r,g,b=a[...,0],a[...,1],a[...,2]; inner=(r<215)&(r>90)&(g<170)&(b<90)&(r-g>25)
        lab2,n2=nd.label(inner); sz=nd.sum(inner,lab2,range(1,n2+1)); big=np.argmax(sz)+1
        bg|=nd.binary_fill_holes(lab2==big)
    if k=='beanie':
        r,g,b=a[...,0],a[...,1],a[...,2]; lum=(r*0.3+g*0.59+b*0.11); dk=(lum<112)&(b>r+15)
        dk[:a.shape[0]//2]=False; lab2,n2=nd.label(dk); sz=nd.sum(dk,lab2,range(1,n2+1)); big=np.argmax(sz)+1
        bg|=nd.binary_fill_holes(lab2==big)
        keep=~bg; l3,n3=nd.label(keep); sz3=nd.sum(keep,l3,range(1,n3+1)); bg|=np.isin(l3,[i+1 for i,v in enumerate(sz3) if v<300])
    al=nd.grey_erosion(np.where(bg,0,255).astype(np.uint8),size=2)
    o=Image.fromarray(np.dstack([a.astype(np.uint8),al]),'RGBA'); o=o.crop(o.getbbox())
    s=min(1,180/max(o.size)); o=o.resize((round(o.width*s),round(o.height*s)),Image.LANCZOS)
    bb=io.BytesIO(); o.save(bb,'WEBP',quality=88); out['d_'+k]={'src':'data:image/webp;base64,'+base64.b64encode(bb.getvalue()).decode(),'w':o.width,'h':o.height}
    o.save(f'd_{k}.png')
json.dump(out,open('deco.json','w'))
ims=[Image.open(f'd_{k}.png') for k in B]; c=Image.new('RGBA',(1800,220),(120,160,200,255)); xx=5
for i in ims: c.paste(i,(xx,5),i); xx+=i.width+5
c.crop((0,0,xx,220)).save('dchk.png')

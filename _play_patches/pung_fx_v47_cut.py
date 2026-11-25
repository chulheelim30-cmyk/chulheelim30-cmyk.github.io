from PIL import Image
import numpy as np, base64, io, json
from scipy import ndimage as nd
im=Image.open('/mnt/user-data/uploads/d469142c-image.png').convert('RGB'); A=np.array(im).astype(float)
B={1:(1286,18,217,200),2:(559,38,153,168),3:(314,44,161,140),4:(82,46,150,153),5:(812,47,140,150),6:(1028,63,192,113),7:(160,219,179,173),8:(1135,221,207,169),9:(884,225,166,158),11:(417,235,155,144),12:(226,392,207,203),13:(531,417,176,171),14:(811,432,140,134),15:(1061,464,97,95),18:(519,618,177,149),20:(81,783,1395,203)}
NAMES={4:'fx_p0',3:'fx_p1',2:'fx_p2',5:'fx_p3',6:'fx_p4',1:'fx_p5',7:'fx_s0',11:'fx_s1',10:'fx_s2',9:'fx_s3',8:'fx_s4',12:'fx_b0',13:'fx_b1',14:'fx_b2',15:'fx_b3',18:'fx_paw',20:'fx_rb'}
SIZE={'p':72,'s':72,'b':80,'paw':64,'rb':420}
out={}
for i,(x,y,w,h) in B.items():
    k=NAMES[i]; a=A[y-6:y+h+6, x-6:x+w+6]
    if k.startswith('fx_p') or k=='fx_paw':
        white=a.min(2)>240; lab,n=nd.label(white); edge=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])).tolist())-{0}
        al=np.where(np.isin(lab,list(edge)),0,255).astype(np.uint8); al=nd.grey_erosion(al,size=2); rgb=a
    else: # 바깥 흰 배경만 투명으로, 빛 번짐은 반투명으로 (안쪽 흰 부분은 그대로)
        white=a.min(2)>200; lab,n=nd.label(white); edge=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])).tolist())-{0}
        bg=np.isin(lab,list(edge))
        ca=np.clip((255-a).max(2)/255,0,1); safe=np.maximum(ca,1e-3)[...,None]
        crgb=np.clip((a-255*(1-safe))/safe,0,255)
        sat=a.max(2)-a.min(2); ca=np.where(sat<14,0,ca); al=np.where(bg,np.clip(ca*1.25,0,1),1.0); rgb=np.where(bg[...,None],crgb,a); al=(al*255).astype(np.uint8)
    if k=='fx_rb':
        W=al.shape[1]; x=np.arange(W)/W; ramp=np.clip(np.minimum(x-0.04,0.96-x)/0.14,0,1); al=(al*ramp[None,:]).astype(np.uint8)
    o=Image.fromarray(np.dstack([rgb.astype(np.uint8),al]),'RGBA'); o=o.crop(o.getbbox())
    t=SIZE['rb'] if k=='fx_rb' else SIZE['paw'] if k=='fx_paw' else SIZE[k[3]]
    s=t/max(o.size); o=o.resize((round(o.width*s),round(o.height*s)),Image.LANCZOS)
    b=io.BytesIO(); o.save(b,'WEBP',quality=88); out[k]={'src':'data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode(),'w':o.width,'h':o.height}
    o.save(k+'.png')
im2=np.array(Image.open('/mnt/user-data/uploads/6c0489bb-image.png').convert('RGB')).astype(float)
for n,(x,y,w,h) in enumerate([(58,794,222,194),(367,789,207,184),(647,793,200,173),(943,807,203,153)]):
    a=im2[y-6:y+h+6, x-6:x+w+6]; white=a.min(2)>240; lab,nn=nd.label(white); edge=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])).tolist())-{0}
    al=nd.grey_erosion(np.where(np.isin(lab,list(edge)),0,255).astype(np.uint8),size=2)
    o=Image.fromarray(np.dstack([a.astype(np.uint8),al]),'RGBA'); o=o.crop(o.getbbox()); s2=64/max(o.size); o=o.resize((round(o.width*s2),round(o.height*s2)),Image.LANCZOS)
    b=io.BytesIO(); o.save(b,'WEBP',quality=88); out[f'fx_w{n}']={'src':'data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode(),'w':o.width,'h':o.height}; o.save(f'fx_w{n}.png')
out.pop('fx_paw',None)
json.dump(out,open('fx.json','w')); print(sum(len(v['src']) for v in out.values())//1024,'KB')
ks=[k for k in out if k!='fx_rb']+['fx_rb']; c=Image.new('RGBA',(1400,260),(60,40,80,255)); xx=5
for k in ks[:-1]: i=Image.open(k+'.png'); c.paste(i,(xx,10),i); xx+=i.width+6
r=Image.open('fx_rb.png'); c.paste(r,(5,120),r); c.save('chk.png')

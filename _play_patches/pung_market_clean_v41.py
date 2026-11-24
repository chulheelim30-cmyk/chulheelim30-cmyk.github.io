import cv2, numpy as np
im=cv2.imread('/mnt/user-data/uploads/d54a65e5-image.png'); out=im.copy().astype(np.float32)
P=[[(124,20),(270,93),(252,153),(104,82)],[(304,110),(365,109),(365,233),(305,233)],[(409,202),(483,233),(473,263),(399,230)],
 [(529,268),(586,296),(578,320),(522,294)],[(988,214),(1056,186),(1057,232),(991,257)],[(820,290),(867,264),(872,283),(823,307)],
 [(620,366),(655,366),(655,390),(620,390)],[(1143,388),(1164,388),(1164,428),(1143,428)],[(12,420),(62,420),(62,440),(12,440)],[(142,414),(184,414),(184,433),(142,433)],[(257,506),(293,506),(293,527),(257,527)]]
rng=np.random.default_rng(1)
for p in P:
    pm=np.zeros(im.shape[:2],np.uint8); cv2.fillPoly(pm,[np.array(p)],255); pm=cv2.erode(pm,np.ones((3,3),np.uint8))
    px=im[pm>0].astype(np.float32); lum=px.mean(1); col=np.median(px[lum>=np.percentile(lum,60)],0)
    fill=np.ones_like(out)*col; fill+=rng.normal(0,3,fill.shape).astype(np.float32); fill=cv2.GaussianBlur(fill,(3,3),0)
    # 가장자리 쪽은 살짝 어둡게(원래 그림처럼)
    dist=cv2.distanceTransform(pm,cv2.DIST_L2,3); shade=np.clip(dist/6,0,1)[...,None]; fill=fill*(0.9+0.1*shade)
    a=cv2.GaussianBlur(pm.astype(np.float32)/255,(5,5),0)[...,None]
    out=out*(1-a)+fill*a
out=np.clip(out,0,255).astype(np.uint8); cv2.imwrite('/tmp/market_clean.png',out)
cv2.imwrite('/tmp/mcmp.png',np.vstack([np.hstack([im[20:330,80:600],out[20:330,80:600]]),np.hstack([im[170:480,700:1220],out[170:480,700:1220]])]))

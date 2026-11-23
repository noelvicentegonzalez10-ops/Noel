from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os, subprocess
W,H,FPS=1080,1920,30
FB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def font(s): return ImageFont.truetype(FB,s)
ORANGE=(215,134,80); CREAM=(242,211,181); BROWN=(93,43,9); DARK=(40,26,18); WHITE=(255,255,255)
FUR=(226,160,96); FUR2=(190,120,66); EAR=(150,88,45); NOSE=(45,30,25)
import json, sys
HERE=os.path.dirname(os.path.abspath(__file__))
V=os.path.join(HERE,"assets")+"/"

def dog(expr="happy", talk=0.0, blink=False, tail=0.0, mud=False, shades=False, bounce=0, S=2):
    # draw at 2x on 900x1000 canvas, return downscaled RGBA 450x500
    w,h=900*S//2*2//2*2//2, 1000
    w,h=900*S,1000*S
    im=Image.new("RGBA",(w,h),(0,0,0,0)); d=ImageDraw.Draw(im)
    s=S
    oy=int(bounce*s)
    # tail
    cx,cy=620*s,700*s+oy
    ang=math.radians(-40+25*math.sin(tail))
    tx,ty=cx+int(170*s*math.cos(ang)), cy-int(170*s*math.sin(ang)+60*s)
    d.line([cx,cy,tx,ty],fill=FUR2,width=44*s); d.ellipse([tx-26*s,ty-26*s,tx+26*s,ty+26*s],fill=FUR2)
    # body
    d.ellipse([230*s,560*s+oy,670*s,960*s+oy],fill=FUR)
    d.ellipse([340*s,650*s+oy,560*s,930*s+oy],fill=CREAM)
    # legs
    for x in (300,520):
        d.rounded_rectangle([x*s,860*s+oy,(x+90)*s,975*s+oy],radius=40*s,fill=FUR)
        d.ellipse([(x-10)*s,930*s+oy,(x+100)*s,990*s+oy],fill=CREAM)
    # collar
    d.rounded_rectangle([300*s,560*s+oy,600*s,610*s+oy],radius=25*s,fill=(200,40,40))
    d.ellipse([430*s,590*s+oy,480*s,640*s+oy],fill=(240,200,60))
    # ears
    hy=oy
    d.ellipse([130*s,170*s+hy,300*s,470*s+hy],fill=EAR)
    d.ellipse([600*s,170*s+hy,770*s,470*s+hy],fill=EAR)
    # head
    d.ellipse([200*s,110*s+hy,700*s,590*s+hy],fill=FUR)
    d.ellipse([310*s,330*s+hy,590*s,580*s+hy],fill=CREAM)
    # eyes
    ey=290*s+hy
    for ex in (350*s,550*s):
        if shades: continue
        if blink or (expr=="wink" and ex>450*s):
            d.arc([ex-40*s,ey-20*s,ex+40*s,ey+30*s],200,340,fill=DARK,width=10*s)
        elif expr=="sad":
            d.ellipse([ex-34*s,ey-24*s,ex+34*s,ey+44*s],fill=DARK)
            d.ellipse([ex-14*s,ey-12*s,ex+6*s,ey+8*s],fill=WHITE)
            d.line([ex-45*s,ey-50*s+(15*s if ex<450*s else -15*s),ex+45*s,ey-50*s+(-15*s if ex<450*s else 15*s)],fill=EAR,width=12*s)
        else:
            d.ellipse([ex-38*s,ey-38*s,ex+38*s,ey+44*s],fill=DARK)
            d.ellipse([ex-16*s,ey-22*s,ex+8*s,ey+2*s],fill=WHITE)
            d.ellipse([ex+10*s,ey+10*s,ex+20*s,ey+20*s],fill=WHITE)
    if shades:
        d.rounded_rectangle([290*s,250*s+hy,610*s,340*s+hy],radius=30*s,fill=(20,20,20))
        d.line([300*s,260*s+hy,600*s,260*s+hy],fill=(90,90,90),width=6*s)
        d.polygon([(330*s,270*s+hy),(360*s,270*s+hy),(335*s,320*s+hy)],fill=(255,255,255,120))
    # blush
    if expr in("happy","wink","cool"):
        for bx in (285*s,615*s):
            d.ellipse([bx-35*s,380*s+hy,bx+35*s,415*s+hy],fill=(240,130,120,140))
    # nose
    d.ellipse([405*s,370*s+hy,495*s,430*s+hy],fill=NOSE)
    d.ellipse([425*s,380*s+hy,450*s,395*s+hy],fill=(110,90,85))
    # mouth
    my=440*s+hy
    d.line([450*s,430*s+hy,450*s,my],fill=NOSE,width=8*s)
    if expr=="sad" and talk<0.15:
        d.arc([390*s,my+10*s,510*s,my+70*s],200,340,fill=NOSE,width=8*s)
    else:
        op=int((20+70*talk)*s)
        d.chord([385*s,my-20*s,515*s,my+op+30*s],0,180,fill=(120,30,40))
        d.ellipse([420*s,my+op-5*s,480*s,my+op+30*s],fill=(240,110,120))
        d.arc([380*s,my-40*s,450*s,my+20*s],0,150,fill=NOSE,width=8*s)
        d.arc([450*s,my-40*s,520*s,my+20*s],30,180,fill=NOSE,width=8*s)
    if mud:
        for (x,y,r) in [(260,700,55),(600,780,50),(420,880,45),(250,300,45),(640,520,40),(330,950,40),(560,250,35)]:
            d.ellipse([(x-r)*s,(y-r)*s+oy,(x+r)*s,(y+r)*s+oy],fill=(110,75,40,220))
    if expr=="sad":
        # tear
        d.ellipse([320*s,340*s+hy,345*s,380*s+hy],fill=(120,180,240))
    return im.resize((450,500),Image.LANCZOS)

def bg(c1,c2,t):
    g=Image.new("RGB",(W,H),c1); d=ImageDraw.Draw(g)
    for y in range(0,H,8):
        a=y/H; col=tuple(int(c1[i]*(1-a)+c2[i]*a) for i in range(3)); d.rectangle([0,y,W,y+8],fill=col)
    # floating paw prints
    for i in range(9):
        x=(i*157+int(t*40))%W; y=(i*263+int(t*25*(1+i%3)))%H
        c=tuple(min(255,v+25) for v in c1)
        d.ellipse([x,y,x+50,y+42],fill=c)
        for dx,dy in((-18,-28),(4,-40),(28,-40),(48,-28)):
            d.ellipse([x+dx,y+dy,x+dx+22,y+dy+22],fill=c)
    return g

def wrap(d,txt,f,maxw):
    out=[];cur=""
    for wd in txt.split():
        t=(cur+" "+wd).strip()
        if d.textlength(t,font=f)<=maxw: cur=t
        else: out.append(cur); cur=wd
    out.append(cur); return out

def bubble(img,txt,y,progress):
    d=ImageDraw.Draw(img); f=font(62)
    lines=wrap(d,txt,f,880)
    n=max(1,int(len(txt)*min(1,progress*1.6)))  # typewriter
    shown=txt[:n]
    sl=wrap(d,shown,f,880) if shown else [""]
    hgt=len(lines)*76+60
    d.rounded_rectangle([60,y,W-60,y+hgt],radius=50,fill=WHITE,outline=DARK,width=6)
    d.polygon([(420,y+hgt-3),(520,y+hgt-3),(450,y+hgt+60)],fill=WHITE,outline=DARK)
    d.line([(423,y+hgt-3),(517,y+hgt-3)],fill=WHITE,width=8)
    yy=y+30
    for ln in sl:
        d.text(((W-d.textlength(ln,font=f))/2,yy),ln,font=f,fill=DARK); yy+=76

def card(img,src,label,t,cx,cy,maxw=620,maxh=560):
    if t<0: return
    p=Image.open(V+src).convert("RGB")
    sc=min(maxw/p.width,maxh/p.height)
    # pop-in spring
    k=min(1,t/0.35); s=sc*(1.0+0.15*math.sin(k*math.pi))*k if k<1 else sc
    if s<=0.02: return
    pw,ph=int(p.width*s),int(p.height*s)
    p=p.resize((pw,ph),Image.LANCZOS)
    m=Image.new("L",(pw,ph),0); ImageDraw.Draw(m).rounded_rectangle([0,0,pw,ph],radius=30,fill=255)
    fr=Image.new("RGBA",(pw+20,ph+20),(255,255,255,255)); 
    fm=Image.new("L",(pw+20,ph+20),0); ImageDraw.Draw(fm).rounded_rectangle([0,0,pw+20,ph+20],radius=38,fill=255)
    img.paste(fr,(cx-(pw+20)//2,cy-(ph+20)//2),fm)
    img.paste(p,(cx-pw//2,cy-ph//2),m)
    if label and k>=1:
        d=ImageDraw.Draw(img); f=font(50); tw=d.textlength(label,font=f)
        x=cx-tw/2; y=cy+ph//2+30
        d.rounded_rectangle([x-30,y-14,x+tw+30,y+64],radius=36,fill=ORANGE)
        d.text((x,y),label,font=f,fill=WHITE)


def main(cfg_path,out_path):
    cfg=json.load(open(cfg_path))
    scenes=[]
    for s in cfg["escenas"]:
        scenes.append((s.get("duracion",4.2),(tuple(s["fondo"][0]),tuple(s["fondo"][1])),s.get("perro",{}),s["texto"],s.get("imagen"),s.get("etiqueta"),s.get("final",False)))
    tmp=out_path+".frames"; os.makedirs(tmp,exist_ok=True)
    N=0; T=0.0
    for si,(dur,(c1,c2),kw,txt,prod,label,final) in enumerate(scenes):
        n=int(dur*FPS)
        for k in range(n):
            t=k/FPS; T+=1/FPS
            img=bg(c1,c2,T)
            talking=0.0 if t>len(txt)/16+0.3 else abs(math.sin(t*14))*(0.6 if kw.get("expr")=="sad" else 1)
            blink=(int(T*FPS)%95)<4
            dg=dog(talk=talking,blink=blink,tail=T*(3 if kw.get("expr")=="sad" else 12),bounce=(0 if kw.get("expr")=="sad" else 12*abs(math.sin(T*6))),**kw)
            if prod:
                card(img,prod,label,t-0.6,W//2,720,maxw=600,maxh=440)
                dsz=(440,489); dx,dy=(W-440)//2,1080
            elif final:
                dsz=(560,622); dx,dy=(W-560)//2,880
            else:
                dsz=(620,689); dx,dy=(W-620)//2,820
            dimg=dg.resize(dsz,Image.LANCZOS)
            img.paste(dimg,(dx,dy),dimg)
            bubble(img,txt,200 if not prod else 150,t/dur*1.3)
            d=ImageDraw.Draw(img)
            if final:
                code=cfg.get("codigo","-10 % BIENVENIDA10")
                pulse=1+0.04*math.sin(T*8)
                f2=font(int(70*pulse)); tw=d.textlength(code,font=f2)
                d.rounded_rectangle([(W-tw)/2-40,1530,(W+tw)/2+40,1640],radius=50,fill=WHITE)
                d.text(((W-tw)/2,1548),code,font=f2,fill=BROWN)
                f3=font(54); tw=d.textlength("Link en la bio",font=f3)
                d.text(((W-tw)/2,1680),"Link en la bio",font=f3,fill=WHITE,stroke_width=5,stroke_fill=DARK)
            f=font(34); tw=d.textlength("@mimopata",font=f)
            d.text(((W-tw)/2,70),"@mimopata",font=f,fill=WHITE,stroke_width=3,stroke_fill=DARK)
            img.save(f"{tmp}/{N:05d}.jpg",quality=90); N+=1
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",f"{tmp}/%05d.jpg","-c:v","libx264","-pix_fmt","yuv420p","-crf","21","-movflags","+faststart",out_path],check=True)
    subprocess.run(["rm","-rf",tmp])
    print("OK",out_path,round(T,1),"s")

if __name__=="__main__":
    if len(sys.argv)!=3: sys.exit("uso: python3 pata.py guion.json salida.mp4")
    main(sys.argv[1],sys.argv[2])

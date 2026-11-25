"""Vídeo viral: "6 cosas que NUNCA debes dar a tu perro" -> snacks naturales Mimopata.
Uso: python3 viral_alimentos.py [salida.mp4]   |   --frame escena t salida.png"""
import math, os, sys, subprocess
from PIL import Image, ImageDraw, ImageFilter
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from pata import font, W, H, FPS, WHITE, DARK, BROWN, ORANGE, CREAM
from sin_sonido import gradient, caption, chip, card, progress, tag, img, ease, endcard
from personajes import dog_sprite

RED=(230,55,60); GREEN=(60,170,90)

# ---------- iconos dibujados ----------
def ic_chocolate(d,cx,cy,s):
    d.rounded_rectangle([cx-150*s,cy-100*s,cx+150*s,cy+100*s],radius=18*s,fill=(110,60,35),outline=(60,30,15),width=int(8*s))
    for i in range(3):
        for j in range(2):
            x=cx-150*s+18*s+i*94*s; y=cy-100*s+18*s+j*92*s
            d.rounded_rectangle([x,y,x+80*s,y+74*s],radius=10*s,fill=(135,78,45))
    d.polygon([(cx+60*s,cy-100*s),(cx+150*s,cy-100*s),(cx+150*s,cy-10*s)],fill=(230,230,240))
def ic_uvas(d,cx,cy,s):
    d.line([cx,cy-150*s,cx+20*s,cy-200*s],fill=(110,80,40),width=int(14*s))
    d.ellipse([cx+15*s,cy-200*s,cx+90*s,cy-160*s],fill=(90,160,70))
    rows=[4,3,3,2,1]; y=cy-120*s
    for r in rows:
        for k in range(r):
            x=cx-(r-1)*35*s+k*70*s
            d.ellipse([x-38*s,y-38*s,x+38*s,y+38*s],fill=(120,55,150),outline=(70,25,95),width=int(5*s))
            d.ellipse([x-20*s,y-24*s,x-6*s,y-10*s],fill=(200,160,220))
        y+=60*s
def ic_cebolla(d,cx,cy,s):
    d.ellipse([cx-120*s,cy-90*s,cx+120*s,cy+130*s],fill=(200,150,190),outline=(130,80,120),width=int(8*s))
    d.polygon([(cx-30*s,cy-80*s),(cx+30*s,cy-80*s),(cx,cy-190*s)],fill=(200,150,190),outline=(130,80,120))
    for k in (-60,0,60): d.arc([cx-100*s+k*s*0.3,cy-80*s,cx+100*s+k*s*0.3,cy+120*s],250,290,fill=(150,95,140),width=int(6*s))
    d.ellipse([cx+110*s,cy-10*s,cx+210*s,cy+110*s],fill=(245,240,225),outline=(170,160,140),width=int(6*s))
def ic_chicle(d,cx,cy,s):
    d.rounded_rectangle([cx-170*s,cy-80*s,cx+170*s,cy+80*s],radius=20*s,fill=(90,200,210),outline=(40,120,130),width=int(8*s))
    d.text((cx-130*s,cy-45*s),"SIN AZÚCAR",font=font(int(38*s)),fill=WHITE)
    d.text((cx-130*s,cy+10*s),"xilitol",font=font(int(34*s)),fill=(30,90,100))
    for i in range(3): d.rounded_rectangle([cx-150*s+i*110*s,cy+95*s,cx-60*s+i*110*s,cy+140*s],radius=12*s,fill=WHITE,outline=(170,170,170))
def ic_hueso(d,cx,cy,s):
    d.rounded_rectangle([cx-140*s,cy-35*s,cx+140*s,cy+35*s],radius=20*s,fill=(245,235,210),outline=(150,130,100),width=int(7*s))
    for dx in (-160,160):
        for dy in (-35,35): d.ellipse([cx+dx*s-50*s,cy+dy*s-50*s,cx+dx*s+50*s,cy+dy*s+50*s],fill=(245,235,210),outline=(150,130,100),width=int(7*s))
    d.rounded_rectangle([cx-140*s,cy-28*s,cx+140*s,cy+28*s],radius=18*s,fill=(245,235,210))
    for k in range(3): d.line([cx-60*s+k*50*s,cy-25*s,cx-40*s+k*50*s,cy+20*s],fill=(180,140,90),width=int(6*s))
    d.text((cx-70*s,cy+70*s),"cocinado",font=font(int(40*s)),fill=(120,90,60))
def ic_macadamia(d,cx,cy,s):
    for (dx,dy) in [(-90,0),(30,-40),(100,50),(-20,80)]:
        x,y=cx+dx*s,cy+dy*s
        d.ellipse([x-60*s,y-60*s,x+60*s,y+60*s],fill=(235,210,160),outline=(160,120,70),width=int(7*s))
        d.ellipse([x-25*s,y-35*s,x+5*s,y-10*s],fill=(250,235,200))

def prohibido(d,cx,cy,r,k):
    r=int(r*(0.6+0.4*k))
    d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=RED,width=26)
    a=math.radians(45); d.line([cx-r*math.cos(a)+10,cy-r*math.sin(a)+10,cx+r*math.cos(a)-10,cy+r*math.sin(a)-10],fill=RED,width=26)

ITEMS=[("Chocolate","Tóxico para su corazón y su sistema nervioso",ic_chocolate,((255,240,225),(240,205,175))),
       ("Uvas y pasas","Pueden dañar gravemente sus riñones",ic_uvas,((245,235,255),(220,200,240))),
       ("Cebolla y ajo","Dañan sus glóbulos rojos (también cocinados)",ic_cebolla,((250,240,245),(235,210,225))),
       ("Chicle sin azúcar","Lleva xilitol: muy poca cantidad ya es peligrosa",ic_chicle,((225,248,250),(190,230,235))),
       ("Huesos cocinados","Se astillan y pueden dañar su estómago",ic_hueso,((250,245,232),(232,220,195))),
       ("Nueces de macadamia","Pueden causar debilidad y temblores",ic_macadamia,((252,246,232),(238,225,195)))]

def dog_corner(b,T,expr="shock",x=880,y=1840,sz=0.33,shades=False):
    sp=dog_sprite(expr,talk=abs(math.sin(T*10))*0.5 if expr!="sad" else 0,tail=T*14,tilt=6*math.sin(T*4),shades=shades)
    w=int(sp.width*sz); sp=sp.resize((w,w),Image.LANCZOS); b.paste(sp,(int(x-w/2),int(y-w)),sp)

def s_hook(t,T):
    b=gradient((30,30,40),(10,10,15)); d=ImageDraw.Draw(b)
    shake=6*math.sin(T*60) if t<0.4 else 0
    f=font(int(118+8*math.sin(T*6))); s="6 cosas que"; tw=d.textlength(s,font=f); d.text(((W-tw)/2+shake,300),s,font=f,fill=WHITE,stroke_width=10,stroke_fill=DARK)
    f=font(150); s="NUNCA"; tw=d.textlength(s,font=f); d.text(((W-tw)/2,450),s,font=f,fill=RED,stroke_width=12,stroke_fill=DARK)
    caption(b,"debes dar a tu perro",650,t*2,size=96)
    if t>0.9:
        chip(b,"La nº 4 casi nadie la conoce",960,58,(255,210,60),DARK,t-0.9,0.05*math.sin(T*10))
    dog_corner(b,T,"shock",540,1700,0.62)
    return b

def s_item(i,t,T):
    name,why,icon,bg=ITEMS[i]; b=gradient(*bg); d=ImageDraw.Draw(b)
    k=ease(t/0.35); bounce=1+0.06*math.sin(min(1,t/0.35)*math.pi)
    f=font(190); s=str(i+1); tw=d.textlength(s,font=f); d.text(((W-tw)/2,110),s,font=f,fill=RED,stroke_width=12,stroke_fill=DARK)
    caption(b,name,340,t*1.5,size=92,color=WHITE)
    icon(d,W/2,900,max(0.08,1.25*k*bounce))
    if t>0.45: prohibido(d,W/2,900,330,ease((t-0.45)/0.25))
    if t>0.7: caption(b,why,1320,(t-0.7)*1.6,size=62)
    dog_corner(b,T,"sad" if i%2 else "shock",900,1860,0.3)
    return b

def s_turn(t,T):
    b=gradient((60,170,90),(30,110,60)); d=ImageDraw.Draw(b)
    caption(b,"¿Entonces qué premio le doy?",380,t*1.5,size=100)
    dog_corner(b,T,"happy",540,1650,0.6)
    return b

def s_answer(t,T):
    b=img("lab_bolsa_hd.jpg");
    from sin_sonido import cover
    b=cover(b,0.55,0.45,1.0+0.12*ease(t/3))
    caption(b,"Snacks 100 % naturales",230,t*1.5,size=88)
    if t>0.6: chip(b,"Sin conservantes ni colorantes",1430,56,GREEN,WHITE,t-0.6)
    return b

def s_end(t,T):
    b=endcard(t,T,"mixpack_hd.jpg","Pack Degustación","23,17 €","-10 % con BIENVENIDA10")
    d=ImageDraw.Draw(b); f=font(40); s="Guárdalo y compártelo con quien tenga perro"; tw=d.textlength(s,font=f)
    d.text(((W-tw)/2,1680),s,font=f,fill=WHITE,stroke_width=4,stroke_fill=DARK)
    f=font(30); s="Ante cualquier duda, consulta a tu veterinario."; tw=d.textlength(s,font=f)
    d.text(((W-tw)/2,1760),s,font=f,fill=(255,235,210))
    return b

SCENES=[(2.8,s_hook)]+[(2.6,(lambda i: (lambda t,T: s_item(i,t,T)))(i)) for i in range(6)]+[(1.8,s_turn),(2.4,s_answer),(4.2,s_end)]

def main(out):
    total=sum(d for d,_ in SCENES); tmp=out+".frames"; os.makedirs(tmp,exist_ok=True); N=0; T=0.0; prev=None; X=4
    for dur,fn in SCENES:
        for k in range(int(dur*FPS)):
            t=k/FPS; T+=1/FPS; b=fn(t,T); progress(b,T/total); tag(b)
            if prev is not None and k<X: b=Image.blend(prev,b,(k+1)/(X+1))
            b.save(f"{tmp}/{N:05d}.jpg",quality=90); N+=1
        prev=b
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",f"{tmp}/%05d.jpg","-c:v","libx264","-pix_fmt","yuv420p","-crf","20","-movflags","+faststart",out],check=True)
    subprocess.run(["rm","-rf",tmp]); print("OK",out,round(N/FPS,1),"s",flush=True)

if __name__=="__main__":
    if len(sys.argv)>1 and sys.argv[1]=="--frame":
        i=int(sys.argv[2]); t=float(sys.argv[3]); b=SCENES[i][1](t,t); progress(b,0.4); tag(b); b.save(sys.argv[4]); sys.exit()
    main(sys.argv[1] if len(sys.argv)>1 else os.path.join(HERE,"..","videos","viral-6-cosas-nunca-perro.mp4"))

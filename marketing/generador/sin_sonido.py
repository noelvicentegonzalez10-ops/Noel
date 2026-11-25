"""Vídeos pensados para verse SIN SONIDO: textos grandes, fotos reales y cierre con precio.
Uso: python3 sin_sonido.py <1|2|3|4|todos>"""
import math, os, sys, subprocess, random
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
HERE=os.path.dirname(os.path.abspath(__file__)); A=os.path.join(HERE,"assets")+"/"
OUTDIR=os.path.join(HERE,"..","videos")
sys.path.insert(0,HERE)
from pata import font, wrap, W, H, FPS, WHITE, DARK, BROWN, ORANGE, CREAM
_cache={}
def img(n):
    if n not in _cache: _cache[n]=Image.open(A+n).convert("RGB")
    return _cache[n]
def ease(k): k=max(0,min(1,k)); return k*k*(3-2*k)

def cover(src,cx,cy,zoom):
    sw,sh=src.size; s=max(W/sw,H/sh)*zoom; vw,vh=W/s,H/s
    x=max(0,min(sw-vw,cx*sw-vw/2)); y=max(0,min(sh-vh,cy*sh-vh/2))
    return src.crop((int(x),int(y),int(x+vw),int(y+vh))).resize((W,H),Image.LANCZOS)

def gradient(c1,c2):
    g=Image.new("RGB",(W,H)); d=ImageDraw.Draw(g)
    for y in range(0,H,8):
        k=y/H; d.rectangle([0,y,W,y+8],fill=tuple(int(c1[i]*(1-k)+c2[i]*k) for i in range(3)))
    return g

def card(base,src,cx,cy,w,t,r=40):
    k=ease(t/0.35); w=max(2,int(w*(0.85+0.15*k)))
    h=int(w*src.height/src.width); p=src.resize((w,h),Image.LANCZOS)
    sh=Image.new("RGBA",(w+80,h+80),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([40,50,w+40,h+50],radius=r,fill=(0,0,0,110))
    sh=sh.filter(ImageFilter.GaussianBlur(20)); base.paste(sh,(int(cx-w/2-40),int(cy-h/2-40)),sh)
    m=Image.new("L",(w,h),0); ImageDraw.Draw(m).rounded_rectangle([0,0,w,h],radius=r,fill=255)
    base.paste(p,(int(cx-w/2),int(cy-h/2)),m)

def caption(base,txt,y,t,size=82,box=False,color=WHITE):
    """Texto grande tipo subtítulo con aparición palabra a palabra."""
    d=ImageDraw.Draw(base); f=font(size); lines=wrap(d,txt,f,940)
    words_total=len(txt.split()); shown=max(1,int(words_total*min(1,t/0.6)))
    count=0; yy=y
    if box:
        hgt=len(lines)*int(size*1.2)+50
        d.rounded_rectangle([50,y-25,W-50,y-25+hgt],radius=40,fill=(0,0,0,0),outline=None)
    for ln in lines:
        ws=ln.split(); vis=[]
        for w_ in ws:
            if count<shown: vis.append(w_)
            count+=1
        s=" ".join(vis); full=d.textlength(ln,font=f); x=(W-full)/2
        if s: d.text((x,yy),s,font=f,fill=color,stroke_width=max(6,size//10),stroke_fill=(0,0,0))
        yy+=int(size*1.2)
    return yy

def chip(base,txt,y,size,bg,fg,t=1.0,pulse=0.0):
    d=ImageDraw.Draw(base); sz=int(size*(1+pulse)); f=font(sz); tw=d.textlength(txt,font=f)
    k=ease(t/0.3);
    if k<=0: return
    d.rounded_rectangle([(W-tw)/2-38,y-16,(W+tw)/2+38,y+sz+28],radius=50,fill=bg)
    d.text(((W-tw)/2,y),txt,font=f,fill=fg)

def progress(base,frac):
    d=ImageDraw.Draw(base); d.rectangle([0,0,W,10],fill=(0,0,0)); d.rectangle([0,0,int(W*frac),10],fill=ORANGE)

def tag(base):
    d=ImageDraw.Draw(base); f=font(34); s="@mimopata"; tw=d.textlength(s,font=f)
    d.text(((W-tw)/2,40),s,font=f,fill=WHITE,stroke_width=3,stroke_fill=DARK)

def endcard(t,T,prod,name,price,extra,bg=((215,134,80),(150,70,35))):
    b=gradient(*bg); card(b,img(prod),W/2,760,640,t)
    caption(b,name,1130,t,size=64)
    chip(b,price,1290,64,CREAM,BROWN,t)
    chip(b,extra,1420,56,WHITE,BROWN,t-0.2,0.04*math.sin(T*8))
    if t>0.5:
        d=ImageDraw.Draw(b); f=font(60); s="Link en la bio ↑"; tw=d.textlength(s,font=f)
        d.text(((W-tw)/2,1560),s,font=f,fill=WHITE,stroke_width=6,stroke_fill=DARK)
    return b

def fireworks(base,T,seed=1):
    d=ImageDraw.Draw(base); rnd=random.Random(seed)
    for i in range(6):
        period=1.6+rnd.random(); ph=(T+rnd.random()*period)%period; cx=rnd.randint(120,960); cy=rnd.randint(200,900)
        col=rnd.choice([(255,210,80),(255,90,120),(120,200,255),(180,255,140)]); r=ph/period*260
        if ph/period<0.8:
            for k in range(16):
                a=k*math.pi/8; x,y=cx+r*math.cos(a),cy+r*math.sin(a)+30*(ph/period)**2
                d.ellipse([x-7,y-7,x+7,y+7],fill=col)

# ---------- guiones ----------
def v1(t,T,i):   # Pack Degustación
    if i==0: b=cover(img("lab_bolsa_hd.jpg"),0.58,0.45,1.0+0.12*ease(t/3)); caption(b,"¿Tu perro se aburre de sus premios?",260,t)
    elif i==1: b=cover(img("doodle_bolsas_hd.jpg"),0.25+0.5*ease(t/3),0.55,1.05); caption(b,"Dale 8 sabores para elegir",260,t)
    elif i==2: b=cover(img("mixpack_hd.jpg"),0.5,0.5,1.0+0.08*ease(t/3)); caption(b,"4 blanditos + 4 galletas",250,t); chip(b,"680 g de snacks",1450,58,ORANGE,WHITE,t-0.4)
    elif i==3: b=cover(img("mujer_perro_hd.jpg"),0.45,0.5,1.0+0.1*ease(t/3)); caption(b,"100 % naturales. Sin conservantes ni colorantes.",260,t)
    else: b=endcard(t,T,"mixpack_hd.jpg","Pack Degustación Floopp","23,17 €","-10 % con BIENVENIDA10")
    return b
def v2(t,T,i):   # Arnés GripPro
    if i==0:
        b=gradient((170,200,150),(90,120,80)); card(b,img("harness_bully.png"),W/2,1000,820,t); caption(b,"¿Tu perro te pasea a ti?",230,t,size=90)
    elif i==1:
        b=gradient((235,238,242),(190,198,210)); card(b,img("arnes_negro.jpg"),W/2,980,800,t); caption(b,"Asa para sujetarlo al momento",230,t)
    elif i==2:
        b=gradient((235,238,242),(190,198,210)); card(b,img("arnes_rojo.jpg"),W/2,980,800,t); caption(b,"Cierre rápido: puesto en 2 segundos",230,t)
    elif i==3:
        b=gradient((235,238,242),(190,198,210));
        for j,(n,x,y) in enumerate([("arnes_azul.jpg",300,820),("arnes_caqui.jpg",780,820),("arnes_rojo.jpg",300,1260),("arnes_negro.jpg",780,1260)]):
            card(b,img(n),x,y,420,t-0.12*j,r=30)
        caption(b,"4 colores · tallas M a XXL",230,t)
    else: b=endcard(t,T,"arnes_negro.jpg","Arnés GripPro antitirones","110 €","Compra 2 y ahorra 10 %",bg=((120,150,110),(60,85,55)))
    return b
def v3(t,T,i):   # Petardos + Sweet Dreams
    if i==0:
        b=gradient((25,20,60),(5,5,20)); fireworks(b,T); caption(b,"Nochevieja: tu perro lo pasa fatal",980,t,size=88)
    elif i in (1,2,3):
        tips=["Prepárale un refugio tranquilo","Paseo largo ANTES de los petardos","Dale algo para masticar: le calma"]
        b=gradient((45,40,95),(15,12,40)); fireworks(b,T,seed=i+3)
        d=ImageDraw.Draw(b); f=font(220); s=str(i); tw=d.textlength(s,font=f)
        d.text(((W-tw)/2,520),s,font=f,fill=(255,210,80),stroke_width=10,stroke_fill=DARK)
        caption(b,tips[i-1],880,t,size=84)
        if i==3: card(b,img("sweetdreams_bolsa.jpg"),W/2,1420,360,t-0.5)
    elif i==4:
        b=cover(img("sweetdreams_ingredientes.jpg"),0.5,0.5,1.0+0.08*ease(t/3)); caption(b,"Con manzanilla, tila y miel",230,t)
    else: b=endcard(t,T,"sweetdreams_pack_hd.jpg","Snacks Sweet Dreams","19,30 €","-10 % con BIENVENIDA10",bg=((110,90,190),(50,35,110)))
    return b
def v4(t,T,i):   # Collar Dog Sport
    if i==0:
        b=cover(img("collar_sport_1.jpg"),0.5,0.5,1.0+0.15*ease(t/3))
        words=["Barro.","Agua.","Tirones."]; d=ImageDraw.Draw(b); y=330
        for k,w_ in enumerate(words):
            if t>k*0.55:
                f=font(130); tw=d.textlength(w_,font=f); d.text(((W-tw)/2,y),w_,font=f,fill=WHITE,stroke_width=12,stroke_fill=DARK)
            y+=170
    elif i==1: b=cover(img("collar_sport_cierre.jpg"),0.5,0.45,1.0+0.12*ease(t/3)); caption(b,"Cierre rápido de acero",260,t)
    elif i==2: b=cover(img("collar_sport_mano.jpg"),0.5,0.5,1.0+0.1*ease(t/3)); caption(b,"¿Sucio? A la lavadora",260,t)
    elif i==3: b=cover(img("collar_sport_varios.jpg"),0.5,0.5,1.0+0.1*ease(t/3)); caption(b,"Aguanta más de 1.000 kg",260,t); chip(b,"Impermeable · tallas S a XXL",1450,54,ORANGE,WHITE,t-0.4)
    else: b=endcard(t,T,"collar_sport_1.jpg","Collar Bestia Dog Sport","42,94 €","Compra 2 y ahorra 10 %",bg=((90,90,100),(30,30,36)))
    return b

VIDEOS={1:(v1,[3.0,2.8,2.8,3.0,3.6],"sin-sonido-01-snacks-aburridos"),
        2:(v2,[3.0,2.6,2.6,2.8,3.6],"sin-sonido-02-paseos-sin-tirones"),
        3:(v3,[3.0,2.4,2.4,2.8,2.6,3.6],"sin-sonido-03-petardos-nochevieja"),
        4:(v4,[2.6,2.4,2.4,2.6,3.6],"sin-sonido-04-collar-indestructible")}

def render(n):
    fn,durs,name=VIDEOS[n]; out=os.path.join(OUTDIR,name+".mp4"); tmp=out+".frames"; os.makedirs(tmp,exist_ok=True)
    total=sum(durs); N=0; T=0.0; prev=None; X=5
    for i,dur in enumerate(durs):
        for k in range(int(dur*FPS)):
            t=k/FPS; T+=1/FPS; b=fn(t,T,i); progress(b,T/total); tag(b)
            if prev is not None and k<X: b=Image.blend(prev,b,(k+1)/(X+1))
            b.save(f"{tmp}/{N:05d}.jpg",quality=90); N+=1
        prev=b
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",f"{tmp}/%05d.jpg","-c:v","libx264","-pix_fmt","yuv420p","-crf","20","-movflags","+faststart",out],check=True)
    subprocess.run(["rm","-rf",tmp]); print("OK",out,round(N/FPS,1),"s",flush=True)

if __name__=="__main__":
    a=sys.argv[1] if len(sys.argv)>1 else "todos"
    if a=="--frame":  # vista previa: --frame video escena t salida.png
        v=int(sys.argv[2]); i=int(sys.argv[3]); t=float(sys.argv[4]); b=VIDEOS[v][0](t,t,i); progress(b,0.5); tag(b); b.save(sys.argv[5]); sys.exit()
    for n in ([1,2,3,4] if a=="todos" else [int(a)]): render(n)

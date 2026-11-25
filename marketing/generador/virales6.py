"""6 vídeos virales con animación, textos grandes y música propia.
Uso: python3 virales6.py [1-6|todos]   |   --frame video escena t salida.png"""
import math, os, sys, subprocess
from functools import lru_cache
from PIL import Image, ImageDraw, ImageEnhance
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from pata import font, W, H, FPS, WHITE, DARK, BROWN, ORANGE, CREAM
from sin_sonido import gradient, caption, chip, card, progress, tag, img, ease, endcard, cover
from personajes import dog_sprite, human_sprite, BG, put
from musica import musica
OUTDIR=os.path.join(HERE,"..","videos")
RED=(230,55,60); GREEN=(60,170,90); YEL=(255,210,60)

@lru_cache(maxsize=4000)
def _dog(expr,talk,tail,tilt,walk,blink,shades):
    return dog_sprite(expr,talk=talk/4,tail=tail*math.pi/8,tilt=tilt,walk=walk*math.pi/4,blink=blink,shades=shades)
def dog(expr="happy",talk=0.0,T=0.0,tilt=0,walk=None,blink=False,shades=False,tailspeed=14):
    return _dog(expr,round(talk*4),int(T*tailspeed*8/math.pi)%16,int(round(tilt/3))*3,(int(walk*4/math.pi)%8) if walk is not None else 0,blink,shades)
def paste_dog(b,sp,cx,bottom,scale):
    w=int(sp.width*scale); s=sp.resize((w,w),Image.LANCZOS); b.paste(s,(int(cx-w/2),int(bottom-w)),s)

def bignum(b,n,y,col=RED,size=200):
    d=ImageDraw.Draw(b); f=font(size); s=str(n); tw=d.textlength(s,font=f)
    d.text(((W-tw)/2,y),s,font=f,fill=col,stroke_width=12,stroke_fill=DARK)

def photo_scene(name,cx,cy,t,dur,z0=1.0,z1=1.12,dark=0.0):
    b=cover(img(name),cx,cy,z0+(z1-z0)*ease(t/dur))
    if dark: b=ImageEnhance.Brightness(b).enhance(1-dark)
    return b

def flash(b,t):
    if t<0.12:
        a=1-t/0.12; w=Image.new("RGB",(W,H),(255,255,255)); b=Image.blend(b,w,a)
    return b

# ---------------- 1. TEST: ¿qué tipo de perro es el tuyo? ----------------
def v1(i,t,T,dur):
    if i==0:
        b=gradient((255,200,90),(235,130,60)); caption(b,"¿Qué tipo de perro es el tuyo?",300,t*1.5,size=100)
        chip(b,"Comenta 1, 2 o 3",760,64,WHITE,BROWN,t-0.6,0.05*math.sin(T*9))
        paste_dog(b,dog("happy",abs(math.sin(T*12))*0.6,T,8*math.sin(T*3)),540,1750,0.75); return b
    opts=[("El glotón","Pide premios a todas horas","lab_bolsa_hd.jpg",0.58,0.45),
          ("El aventurero","Barro, playa y monte","collar_sport_1.jpg",0.5,0.5),
          ("El elegante","Siempre impecable","bijou_dog.png",0.5,0.4)]
    if i in (1,2,3):
        n,sub,ph,cx,cy=opts[i-1]; b=photo_scene(ph,cx,cy,t,dur); b=flash(b,t)
        bignum(b,i,160,YEL,230); caption(b,n,440,t*2,size=100); chip(b,sub,1450,58,WHITE,BROWN,t-0.4); return b
    b=gradient((215,134,80),(150,70,35)); caption(b,"Tenemos algo para cada uno",230,t*1.5,size=80)
    for j,(ph,x,y,lab) in enumerate([("mixpack_hd.jpg",280,700,"1 · Snacks"),("collar_sport_1.jpg",800,700,"2 · Collar"),("bijou_dog.png",540,1150,"3 · Bijou")]):
        card(b,img(ph),x,y,330,t-0.15*j,r=30)
        if t>0.3+0.15*j:
            d=ImageDraw.Draw(b); f=font(46); tw=d.textlength(lab,font=f)
            hh=int(330*img(ph).height/img(ph).width)
            d.text((x-tw/2,y+hh//2+30),lab,font=f,fill=WHITE,stroke_width=6,stroke_fill=DARK)
    chip(b,"-10 % con BIENVENIDA10",1560,56,WHITE,BROWN,t-0.6,0.04*math.sin(T*8))
    d=ImageDraw.Draw(b); f=font(56); s="Link en la bio ↑"; tw=d.textlength(s,font=f); d.text(((W-tw)/2,1690),s,font=f,fill=WHITE,stroke_width=6,stroke_fill=DARK)
    return b
V1=(v1,[2.6,2.4,2.4,2.4,4.2],"viral-01-test-tipo-de-perro",0)

# ---------------- 2. 3 señales de que tu perro te quiere ----------------
def v2(i,t,T,dur):
    if i==0:
        b=gradient((255,180,200),(220,90,130)); caption(b,"3 señales de que tu perro te quiere",300,t*1.5,size=96)
        chip(b,"La 3ª te va a emocionar",820,60,WHITE,(200,50,100),t-0.6,0.05*math.sin(T*9))
        d=ImageDraw.Draw(b)
        for k in range(6):
            y=1800-((t*300+k*200)%900); x=200+k*140+30*math.sin(T*3+k); d.text((x,y),"♥",font=font(90),fill=(255,240,245),stroke_width=4,stroke_fill=(200,50,100))
        paste_dog(b,dog("happy",0,T,6*math.sin(T*3)),540,1650,0.6); return b
    data=[("Te sigue a todas partes","(sí, también al baño)","mujer_perro_hd.jpg",0.4,0.5),
          ("Se tumba pegado a ti","Quiere sentirte cerca","doodle_bolsas_hd.jpg",0.3,0.55),
          ("Te mira a los ojos","Os libera oxitocina a los dos","lab_bolsa_hd.jpg",0.62,0.42)]
    if i in (1,2,3):
        a,sub,ph,cx,cy=data[i-1]; b=photo_scene(ph,cx,cy,t,dur,1.0,1.18); b=flash(b,t)
        bignum(b,i,150,(255,120,160),220); caption(b,a,420,t*2,size=92); chip(b,sub,1450,52,WHITE,(170,40,90),t-0.5); return b
    b=endcard(t,T,"mixpack_hd.jpg","Devuélvele el cariño","Pack Degustación · 23,17 €","-10 % con BIENVENIDA10",bg=((230,110,150),(150,40,80)))
    return b
V2=(v2,[2.6,2.8,2.8,3.2,4.2],"viral-02-senales-te-quiere",2)

# ---------------- 3. Tu perro cuando oye la bolsa de snacks ----------------
def v3(i,t,T,dur):
    if i==0:
        b=BG["room"].copy(); b=ImageEnhance.Brightness(b).enhance(0.75)
        paste_dog(b,dog("happy",0,0,0,blink=True,tailspeed=0),540,1760,0.7)
        d=ImageDraw.Draw(b)
        for k in range(3):
            if (T*2+k*0.6)%2>0.4: d.text((700+k*60,1020-k*70),"z",font=font(70+k*15),fill=WHITE,stroke_width=5,stroke_fill=DARK)
        caption(b,"Tu perro durmiendo profundamente…",260,t*1.5,size=88); return b
    if i==1:
        b=BG["room"].copy(); b=ImageEnhance.Brightness(b).enhance(0.75)
        paste_dog(b,dog("happy",0,0,0,blink=True,tailspeed=0),540,1760,0.7)
        sh=12*math.sin(T*70); card(b,img("mixpack_hd.jpg"),300+sh,700,330,t)
        d=ImageDraw.Draw(b); f=font(110); s="*CRRRUNCH*"; tw=d.textlength(s,font=f)
        d.text(((W-tw)/2+sh,330),s,font=f,fill=YEL,stroke_width=10,stroke_fill=DARK); return b
    if i==2:
        b=BG["room"].copy(); jump=abs(math.sin(min(1,t/0.4)*math.pi))*180
        paste_dog(b,dog("shock",0.8,T,0),540,1760-jump,0.75)
        d=ImageDraw.Draw(b)
        for (x,y,s) in [(200,700,"!!"),(820,650,"?!")]: d.text((x,y),s,font=font(140),fill=RED,stroke_width=10,stroke_fill=DARK)
        caption(b,"¿¡¿HE OÍDO SNACKS?!?",260,t*2,size=96); return b
    if i==3:
        b=BG["room"].copy(); x=1300-1100*ease(t/1.6); walk=T*16
        paste_dog(b,dog("happy",abs(math.sin(T*14)),T,0,walk=walk,tailspeed=30),x,1800-abs(math.sin(T*16))*40,0.62)
        caption(b,"0 a 100 en 0,3 segundos",260,t*2,size=92); return b
    b=endcard(t,T,"mixpack_hd.jpg","El sonido favorito de tu perro","Pack Degustación · 23,17 €","-10 % con BIENVENIDA10",bg=((240,170,90),(190,100,40)))
    return b
V3=(v3,[2.6,2.2,2.2,2.2,4.2],"viral-03-bolsa-de-snacks",4)

# ---------------- 4. 3 errores al elegir collar ----------------
def v4(i,t,T,dur):
    if i==0:
        b=gradient((40,40,50),(10,10,15)); caption(b,"3 errores al elegir el collar de tu perro",300,t*1.5,size=92)
        chip(b,"El 2º lo comete casi todo el mundo",820,52,YEL,DARK,t-0.6,0.05*math.sin(T*9))
        paste_dog(b,dog("sad",0,T,-8,tailspeed=4),540,1700,0.6); return b
    data=[("Demasiado estrecho","En perros grandes, un collar ancho reparte la presión","danger.png",0.5,0.5),
          ("No medir el cuello","Regla de oro: que quepan 2 dedos","maximus.png",0.5,0.5),
          ("Herrajes de mala calidad","Busca hebilla y anilla de acero","collar_sport_cierre.jpg",0.5,0.45)]
    if i in (1,2,3):
        a,sub,ph,cx,cy=data[i-1]
        b=gradient((245,240,232),(215,205,190)); card(b,img(ph),W/2,900,760,t); b=flash(b,t)
        d=ImageDraw.Draw(b); d.text((830,470),"✗",font=font(170),fill=RED,stroke_width=8,stroke_fill=DARK)
        caption(b,a,190,t*2,size=84); caption(b,sub,1340,(t-0.4)*1.6,size=56); return b
    b=endcard(t,T,"collar_sport_1.jpg","Collares que aciertan","Desde 42,94 €","Envío GRATIS desde 55 €",bg=((90,90,100),(30,30,36)))
    return b
V4=(v4,[2.6,3.0,3.0,3.0,4.0],"viral-04-errores-collar",7)

# ---------------- 5. ¿Por qué tu perro tira de la correa? ----------------
def v5(i,t,T,dur):
    if i==0:
        b=gradient((170,200,150),(80,110,70)); card(b,img("harness_bully.png"),W/2,1050,760,t)
        caption(b,"¿Tu perro tira de la correa?",230,t*1.6,size=96); chip(b,"Prueba esto",560,64,WHITE,(60,110,50),t-0.6,0.05*math.sin(T*9)); return b
    tips=[("Para en seco cuando tire","Si tirar no le lleva a ningún sitio, deja de hacerlo"),
          ("Prémiale cuando vaya a tu lado","Un snack en el momento justo vale oro"),
          ("Usa un arnés con asa","Más control sin dañarle el cuello")]
    if i in (1,2,3):
        a,sub=tips[i-1]; b=gradient((235,245,230),(185,210,175)); d=ImageDraw.Draw(b)
        bignum(b,i,150,(60,140,70),220); caption(b,a,420,t*2,size=88)
        ph={1:"collar_sport_mano.jpg",2:"mixpack_hd.jpg",3:"arnes_negro.jpg"}[i]
        card(b,img(ph),W/2,1080,560,t-0.2); caption(b,sub,1430,(t-0.5)*1.6,size=54); return b
    b=endcard(t,T,"arnes_negro.jpg","Arnés GripPro con asa","110 €","Compra 2 y ahorra 10 %",bg=((120,150,110),(60,85,55)))
    return b
V5=(v5,[2.6,3.0,3.0,3.0,4.0],"viral-05-tira-de-la-correa",9)

# ---------------- 6. POV: collar de verdad para tu perro grande ----------------
def v6(i,t,T,dur):
    if i==0:
        b=cover(img("harness_bully.png"),0.5,0.4,1.05); b=ImageEnhance.Color(b).enhance(0.1); b=ImageEnhance.Brightness(b).enhance(0.6)
        caption(b,"POV: tu perro es enorme…",260,t*1.5,size=96)
        caption(b,"y su collar parece de juguete",1380,(t-0.8)*1.5,size=74); return b
    if i==1:
        b=gradient((15,15,20),(0,0,0)); d=ImageDraw.Draw(b); f=font(int(150+30*ease(t/0.5))); s="Y ahora…"; tw=d.textlength(s,font=f)
        d.text(((W-tw)/2,800),s,font=f,fill=YEL,stroke_width=10,stroke_fill=DARK); return b
    cuts=[("maximus.png","Maximus · 101 €"),("danger.png","Danger · 54,53 €"),("maximus_dobermans.png","Hecho a mano en Europa")]
    if i in (2,3,4):
        ph,lab=cuts[i-2]; b=photo_scene(ph,0.5,0.45,t,dur,1.0,1.2); b=flash(b,t)
        chip(b,lab,1500,60,ORANGE,WHITE,t-0.2); return b
    b=endcard(t,T,"maximus.png","Collares de cuero para perros grandes","Desde 54,53 €","Envío GRATIS desde 55 €",bg=((60,45,25),(20,15,8)))
    return b
V6=(v6,[2.8,1.2,1.6,1.6,1.8,4.0],"viral-06-pov-collar-de-verdad",11)

VIDEOS={1:V1,2:V2,3:V3,4:V4,5:V5,6:V6}

def render(n):
    fn,durs,name,key=VIDEOS[n]; out=os.path.join(OUTDIR,name+".mp4"); tmp=out+".frames"; os.makedirs(tmp,exist_ok=True)
    total=sum(durs); N=0; T=0.0; prev=None; X=4
    for i,dur in enumerate(durs):
        for k in range(int(dur*FPS)):
            t=k/FPS; T+=1/FPS; b=fn(i,t,T,dur); progress(b,T/total); tag(b)
            if prev is not None and k<X: b=Image.blend(prev,b,(k+1)/(X+1))
            b.save(f"{tmp}/{N:05d}.jpg",quality=90); N+=1
        prev=b
    wav=out+".wav"; musica(N/FPS,wav,tonalidad=key%12,bpm=104+key*2,semilla=key)
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",f"{tmp}/%05d.jpg","-i",wav,"-filter:a","volume=0.55","-c:v","libx264","-pix_fmt","yuv420p","-crf","20","-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",out],check=True)
    subprocess.run(["rm","-rf",tmp,wav]); print("OK",out,round(N/FPS,1),"s",flush=True)

if __name__=="__main__":
    a=sys.argv[1] if len(sys.argv)>1 else "todos"
    if a=="--frame":
        v=int(sys.argv[2]); i=int(sys.argv[3]); t=float(sys.argv[4]); fn,durs,_,_=VIDEOS[v]
        b=fn(i,t,t,durs[i]); progress(b,0.5); tag(b); b.save(sys.argv[5]); sys.exit()
    for n in ([1,2,3,4,5,6] if a=="todos" else [int(a)]): render(n)

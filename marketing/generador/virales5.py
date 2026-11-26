"""5 vídeos nuevos estilo "Pata + lista", título visible desde el primer fotograma (portada),
cierre con "Tienda en Instagram @mimopata" y música propia.
Uso: python3 virales5.py [1-5|todos]   |   --frame video escena t salida.png"""
import math, os, sys, subprocess
from PIL import Image, ImageDraw
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from pata import font, W, H, FPS, WHITE, DARK, BROWN, ORANGE, CREAM
from sin_sonido import gradient, caption, chip, card, progress, tag, img, ease
from personajes import BG
from virales6 import dog, paste_dog, bignum, flash, RED, GREEN, YEL
from musica import musica
OUTDIR=os.path.join(HERE,"..","videos")

def title(b,txt,y=260,size=100,t=10):  # t grande = texto completo (portada legible)
    return caption(b,txt,y,t,size=size)

def end_ig(t,T,prod,name,price,extra,bg=((215,134,80),(150,70,35))):
    b=gradient(*bg); card(b,img(prod),W/2,720,600,t)
    caption(b,name,1070,10,size=66)
    chip(b,price,1240,62,CREAM,BROWN,t)
    chip(b,extra,1370,54,WHITE,BROWN,t-0.2,0.04*math.sin(T*8))
    if t>0.4:
        d=ImageDraw.Draw(b); f=font(52); s="Tienda en Instagram"; tw=d.textlength(s,font=f)
        d.text(((W-tw)/2,1520),s,font=f,fill=WHITE,stroke_width=6,stroke_fill=DARK)
        f=font(78); s="@mimopata"; tw=d.textlength(s,font=f)
        d.text(((W-tw)/2,1595),s,font=f,fill=YEL,stroke_width=8,stroke_fill=DARK)
    return b

def item_scene(n,head,sub,t,T,expr,bg,col=RED,prop=None,mark=None,tilt=0):
    b=gradient(*bg); b=flash(b,t); bignum(b,n,120,col,200)
    caption(b,head,380,t*2,size=86)
    if prop: card(b,img(prop),W/2,960,520,t-0.15)
    else: paste_dog(b,dog(expr,abs(math.sin(T*12))*0.5,T,tilt),540,1300,0.62)
    if mark:
        d=ImageDraw.Draw(b); d.text((820,620),mark,font=font(170),fill=RED if mark=="✗" else GREEN,stroke_width=8,stroke_fill=DARK)
    if t>0.45: caption(b,sub,1380,(t-0.45)*1.6,size=56)
    if prop: paste_dog(b,dog(expr,0,T,tilt),900,1880,0.3)
    return b

# 1. 3 errores al dar premios
def v1(i,t,T,dur):
    if i==0:
        b=gradient((40,40,50),(10,10,15)); title(b,"3 errores al dar premios a tu perro",280,96)
        chip(b,"El 1º lo hace casi todo el mundo",780,54,YEL,DARK,1,0.05*math.sin(T*9))
        paste_dog(b,dog("shock",abs(math.sin(T*10))*0.4,T,0),540,1720,0.62); return b
    data=[("Darle comida de tu plato","Mucha comida humana le sienta mal","sad",None,"✗"),
          ("Premios demasiado grandes","Un premio debe ser pequeño: es un extra","sad",None,"✗"),
          ("Premiar a destiempo","Dáselo justo en el momento: así aprende","happy",None,"✗")]
    if i in (1,2,3):
        h,s,e,p,m=data[i-1]; return item_scene(i,h,s,t,T,e,((250,235,225),(230,205,185)),RED,p,m)
    if i==4:
        b=gradient((60,170,90),(30,110,60)); title(b,"¿La solución?",300,110,t*2)
        card(b,img("mixpack_hd.jpg"),W/2,1000,520,t-0.2)
        caption(b,"Premios pequeños y 100 % naturales",1380,(t-0.4)*1.6,size=60); return b
    return end_ig(t,T,"mixpack_hd.jpg","Pack Degustación","23,17 €","-10 % con BIENVENIDA10")
V1=(v1,[2.6,2.8,2.8,2.8,2.6,4.0],"nuevo-01-errores-premios",3)

# 2. Quiz
def v2(i,t,T,dur):
    if i==0:
        b=gradient((90,70,200),(40,25,120)); title(b,"¿Cuánto sabes de perros?",260,104)
        chip(b,"3 preguntas · comenta tu nota",760,56,YEL,DARK,1,0.05*math.sin(T*9))
        paste_dog(b,dog("happy",abs(math.sin(T*12))*0.5,T,8*math.sin(T*3)),540,1720,0.62); return b
    qs=[("¿Cuántos dientes tiene un perro adulto?","42","¡10 más que nosotros!"),
        ("¿Por dónde sudan los perros?","Por las almohadillas","Y jadeando se refrescan"),
        ("¿Cuánto mejor huele que tú?","¡Miles de veces más!","Su olfato es su superpoder")]
    if i in (1,2,3):
        q,a,s=qs[i-1]; b=gradient((110,90,220),(55,35,140)); b=flash(b,t)
        bignum(b,i,110,YEL,190); caption(b,q,370,t*2,size=80)
        if t<1.4:
            d=ImageDraw.Draw(b); r=int(120+10*math.sin(T*10)); d.ellipse([540-r,1000-r,540+r,1000+r],fill=(255,255,255))
            f=font(150); tw=d.textlength("?",font=f); d.text((540-tw/2,920),"?",font=f,fill=(90,70,200))
            paste_dog(b,dog("shock",0,T,0),880,1800,0.32)
        else:
            chip(b,a,950,84,YEL,DARK,(t-1.4)*2); caption(b,s,1150,(t-1.6)*2,size=60)
            paste_dog(b,dog("happy",abs(math.sin(T*12))*0.5,T,0),540,1780,0.5)
        return b
    return end_ig(t,T,"mixpack_hd.jpg","¿Cuántas acertaste? 👇".replace(" 👇",""),"Pack Degustación · 23,17 €","-10 % con BIENVENIDA10",bg=((90,70,200),(40,25,120)))
V2=(v2,[2.6,3.2,3.2,3.2,4.0],"nuevo-02-quiz-perros",5)

# 3. Señales de que tu perro se aburre
def v3(i,t,T,dur):
    if i==0:
        b=gradient((120,140,170),(60,70,100)); title(b,"3 señales de que tu perro se aburre",280,96)
        chip(b,"La 3ª te va a sorprender",820,56,YEL,DARK,1,0.05*math.sin(T*9))
        paste_dog(b,dog("sad",0,T,-10,tailspeed=3),540,1720,0.62); return b
    data=[("Te persigue por toda la casa","Busca algo que hacer","sad"),
          ("Ladra o llora sin motivo","Es su forma de pedir atención","sad"),
          ("Rompe cosas","No es maldad: le sobra energía","shock")]
    if i in (1,2,3):
        h,s,e=data[i-1]; return item_scene(i,h,s,t,T,e,((225,232,245),(190,200,225)),(80,110,180),None,None,-8)
    if i==4:
        b=gradient((60,170,90),(30,110,60)); title(b,"Juega con él 10 minutos al día",280,90,t*2)
        card(b,img("mordedor.jpg"),W/2,1000,520,t-0.2)
        paste_dog(b,dog("happy",abs(math.sin(T*12))*0.6,T,8*math.sin(T*4),tailspeed=24),880,1860,0.32)
        caption(b,"Un mordedor resistente le cansa (del bueno)",1380,(t-0.4)*1.6,size=54); return b
    return end_ig(t,T,"mordedor.jpg","Mordedor Bestia Dog Sport","27,41 €","Envío GRATIS desde 55 €",bg=((70,75,90),(25,25,32)))
V3=(v3,[2.6,2.8,2.8,2.8,3.0,4.0],"nuevo-03-perro-aburrido",6)

# 4. Cuando llegas tú vs cuando llega otro
def v4(i,t,T,dur):
    if i==0:
        b=BG["room"].copy(); title(b,"Tu perro cuando llega tu pareja…",260,90)
        paste_dog(b,dog("happy",0,T,0,blink=True,tailspeed=1),540,1760,0.62)
        d=ImageDraw.Draw(b); d.text((680,1100),"meh",font=font(70),fill=WHITE,stroke_width=6,stroke_fill=DARK); return b
    if i==1:
        b=BG["room"].copy(); title(b,"…y cuando llegas TÚ",260,100)
        jump=abs(math.sin(T*9))*160
        paste_dog(b,dog("happy",abs(math.sin(T*14)),T,10*math.sin(T*8),tailspeed=40),540,1760-jump,0.7)
        d=ImageDraw.Draw(b)
        for k in range(7):
            y=1500-((t*400+k*170)%900); x=150+k*130; d.text((x,y),"♥",font=font(80),fill=(240,80,110),stroke_width=4,stroke_fill=WHITE)
        return b
    if i==2:
        b=gradient((255,200,90),(235,130,60)); title(b,"Se merece un premio, ¿no?",300,96,t*2)
        card(b,img("mixpack_hd.jpg"),W/2,1050,540,t-0.2); return b
    return end_ig(t,T,"mixpack_hd.jpg","Pack Degustación","23,17 €","-10 % con BIENVENIDA10")
V4=(v4,[2.8,3.4,2.4,4.0],"nuevo-04-cuando-llegas-tu",8)

# 5. 5 cosas que a muchos perros les molestan
def v5(i,t,T,dur):
    if i==0:
        b=gradient((200,60,70),(110,20,35)); title(b,"5 cosas que a muchos perros les molestan",270,92)
        chip(b,"Y tú las haces cada día",800,58,WHITE,(150,20,35),1,0.05*math.sin(T*9))
        paste_dog(b,dog("sad",0,T,-10,tailspeed=3),540,1720,0.62); return b
    data=[("Los abrazos muy fuertes","Muchos se sienten atrapados"),
          ("Que le toquen la cabeza de golpe","Mejor acaricia el pecho o el lomo"),
          ("Los ruidos fuertes","Petardos, aspiradora, gritos…"),
          ("Los perfumes intensos","Su olfato es muchísimo más sensible"),
          ("Pasar muchas horas solo","Es un animal muy social")]
    if 1<=i<=5:
        h,s=data[i-1]; return item_scene(i,h,s,t,T,"sad" if i%2 else "shock",((255,235,235),(240,200,205)),(200,50,60),None,None,-6)
    return end_ig(t,T,"mixpack_hd.jpg","Y lo que les ENCANTA…","Pack Degustación · 23,17 €","-10 % con BIENVENIDA10",bg=((60,170,90),(30,110,60)))
V5=(v5,[2.6,2.2,2.2,2.2,2.2,2.2,4.0],"nuevo-05-cosas-que-molestan",10)

VIDEOS={1:V1,2:V2,3:V3,4:V4,5:V5}

def render(n):
    fn,durs,name,key=VIDEOS[n]; out=os.path.join(OUTDIR,name+".mp4"); tmp=out+".frames"; os.makedirs(tmp,exist_ok=True)
    total=sum(durs); expected=sum(int(d*FPS) for d in durs); N=0; T=0.0; prev=None; X=4
    if len(os.listdir(tmp))==expected: N=expected; durs=[]
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
        b=fn(i,t,t,durs[i]); progress(b,0.0); tag(b); b.save(sys.argv[5]); sys.exit()
    for n in ([1,2,3,4,5] if a=="todos" else [int(a)]): render(n)

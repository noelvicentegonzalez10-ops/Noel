"""Animación con personajes: Pata (perro) y su dueño. Historia "¿Desde cuándo hablas?".
Uso: python3 personajes.py salida.mp4"""
import math, os, sys, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageChops
HERE=os.path.dirname(os.path.abspath(__file__)); A=os.path.join(HERE,"assets")+"/"
sys.path.insert(0,HERE)
from pata import font, wrap, W, H, FPS, WHITE, DARK, BROWN, ORANGE, CREAM

OUT=(55,35,25)
def ease(k): k=max(0,min(1,k)); return k*k*(3-2*k)
def lerp(a,b,k): return a+(b-a)*k

# ---------- utilidades de dibujo con sombreado ----------
def part(canvas, draw_fn, ctop, cbot, outline=OUT, ow=7, shine=True):
    """Dibuja una pieza: máscara -> degradado vertical + brillo + contorno."""
    m=Image.new("L",canvas.size,0); draw_fn(ImageDraw.Draw(m))
    bbox=m.getbbox()
    if not bbox: return
    x0,y0,x1,y1=bbox; hgt=max(1,y1-y0)
    grad=Image.new("RGB",(1,hgt))
    for y in range(hgt):
        k=y/hgt; grad.putpixel((0,y),tuple(int(ctop[i]*(1-k)+cbot[i]*k) for i in range(3)))
    fill=Image.new("RGBA",canvas.size,(0,0,0,0))
    fill.paste(grad.resize((x1-x0,hgt)),(x0,y0))
    if shine:
        hl=Image.new("L",canvas.size,0); ImageDraw.Draw(hl).ellipse([x0+(x1-x0)*0.18,y0+hgt*0.08,x0+(x1-x0)*0.55,y0+hgt*0.38],fill=90)
        hl=ImageChops.multiply(hl.filter(ImageFilter.GaussianBlur(max(2,(x1-x0)//12))),m)
        fill=Image.composite(Image.new("RGBA",canvas.size,(255,255,255,255)),fill,hl) if False else fill
        white=Image.new("RGBA",canvas.size,(255,255,255,255)); fill.paste(white,(0,0),hl)
    if outline:
        edge=m.filter(ImageFilter.MaxFilter(ow|1))
        canvas.paste(Image.new("RGBA",canvas.size,outline+(255,)),(0,0),edge)
    canvas.paste(fill,(0,0),m)

def shadow(img,cx,cy,w,h,alpha=90):
    s=Image.new("RGBA",(w*2,h*2),(0,0,0,0)); ImageDraw.Draw(s).ellipse([0,0,w*2,h*2],fill=(0,0,0,alpha))
    s=s.filter(ImageFilter.GaussianBlur(10)); img.paste(s,(int(cx-w),int(cy-h)),s)

# ---------- PATA ----------
FUR=((240,184,120),(205,135,75)); FUR_D=((190,120,65),(150,90,45)); CR=((255,240,222),(238,215,190))
def dog_sprite(expr="happy", talk=0.0, blink=False, tail=0.0, tilt=0.0, walk=0.0, eat=0.0, shades=False, look=0.0):
    S=1000; im=Image.new("RGBA",(S,S),(0,0,0,0))
    # cola
    a=math.radians(40+30*math.sin(tail)); tx,ty=690+150*math.cos(a), 610-150*math.sin(a)
    part(im,lambda d:(d.line([640,640,tx,ty],fill=255,width=58),d.ellipse([tx-32,ty-32,tx+32,ty+32],fill=255)),*FUR_D)
    # patas traseras/delanteras con paso
    sw=math.sin(walk)*28
    for i,x in enumerate((300,560)):
        o=sw if i==0 else -sw
        part(im,lambda d,x=x,o=o:d.rounded_rectangle([x+o,790,x+o+110,960],radius=50,fill=255),*FUR_D)
    part(im,lambda d:d.ellipse([230,560,740,930],fill=255),*FUR)
    part(im,lambda d:d.ellipse([360,640,560,910],fill=255),*CR,outline=None)
    for i,x in enumerate((340,500)):
        o=-sw if i==0 else sw
        part(im,lambda d,x=x,o=o:d.rounded_rectangle([x+o,800,x+o+105,975],radius=50,fill=255),*FUR)
        part(im,lambda d,x=x,o=o:d.ellipse([x+o-10,935,x+o+115,995],fill=255),*CR)
    # collar
    part(im,lambda d:d.rounded_rectangle([320,555,620,615],radius=28,fill=255),(225,60,55),(170,30,35),shine=False)
    part(im,lambda d:d.ellipse([445,595,505,655],fill=255),(255,215,80),(215,160,40),shine=False)
    # cabeza en capa aparte (para inclinar)
    hd=Image.new("RGBA",(S,S),(0,0,0,0))
    ef=0.25*math.sin(tail*0.7)
    part(hd,lambda d:d.ellipse([150,150+20*ef,330,500],fill=255),*FUR_D)   # orejas
    part(hd,lambda d:d.ellipse([620,150-20*ef,800,500],fill=255),*FUR_D)
    part(hd,lambda d:d.ellipse([230,90,720,560],fill=255),*FUR)
    part(hd,lambda d:d.ellipse([340,330,610,575],fill=255),*CR,outline=None)
    dd=ImageDraw.Draw(hd)
    # ojos
    for ex in (380,570):
        if shades: continue
        if blink or (expr=="wink" and ex>470):
            dd.arc([ex-42,250,ex+42,320],200,340,fill=OUT,width=11)
        else:
            sz=50 if expr=="shock" else 42
            dd.ellipse([ex-sz,280-sz,ex+sz,280+sz+8],fill=(40,28,22))
            lx=int(10*look)
            dd.ellipse([ex-18+lx,258,ex+6+lx,282],fill=WHITE); dd.ellipse([ex+12+lx,292,ex+22+lx,302],fill=WHITE)
            if expr=="sad": dd.line([ex-50,215+(20 if ex<470 else -20),ex+50,215+(-20 if ex<470 else 20)],fill=(150,90,45),width=14)
    if shades:
        part(hd,lambda d:d.rounded_rectangle([310,225,640,325],radius=40,fill=255),(40,40,48),(10,10,14),shine=True)
    if expr in("happy","wink","cool","shock"):
        for bx in (300,650): dd.ellipse([bx-38,370,bx+38,410],fill=(245,140,130,150))
    # nariz y boca
    part(hd,lambda d:d.ellipse([425,360,525,428],fill=255),(80,55,50),(30,20,18),shine=True,outline=None)
    my=440; op=int(25+85*max(talk,eat))
    if expr=="sad" and talk<0.1:
        dd.arc([410,my+10,540,my+80],200,340,fill=OUT,width=10)
    else:
        dd.chord([405,my-20,545,my+op+30],0,180,fill=(130,35,45),outline=OUT,width=6)
        dd.ellipse([440,my+op-8,510,my+op+28],fill=(245,120,130))
        dd.arc([395,my-42,475,my+18],0,150,fill=OUT,width=9); dd.arc([475,my-42,555,my+18],30,180,fill=OUT,width=9)
    if expr=="sad": dd.ellipse([330,330,360,375],fill=(120,180,240))
    hd=hd.rotate(tilt,center=(475,560),resample=Image.BICUBIC)
    im.alpha_composite(hd)
    return im

# ---------- DUEÑO ----------
SKIN=((250,214,180),(225,175,140)); HAIR=((95,65,45),(60,38,25)); SHIRT=((95,150,215),(55,100,170)); PANT=((70,75,95),(45,48,62))
def human_sprite(expr="neutral", talk=0.0, blink=False, arms=0.0, look=0.0, bounce=0.0):
    Sw,Sh=700,1300; im=Image.new("RGBA",(Sw,Sh),(0,0,0,0)); oy=int(-bounce)
    part(im,lambda d:d.rounded_rectangle([210,820+oy,320,1270],radius=50,fill=255),*PANT)
    part(im,lambda d:d.rounded_rectangle([380,820+oy,490,1270],radius=50,fill=255),*PANT)
    for x in (200,370): part(im,lambda d,x=x:d.rounded_rectangle([x-10,1230,x+140,1295],radius=30,fill=255),(70,60,55),(40,32,28))
    # brazos: arms 0=abajo, 1=arriba (sorpresa)
    for side in (-1,1):
        sx=350+side*150; sy=520+oy
        ang=math.radians(lerp(100,-55,arms))*(1 if side>0 else 1)
        ex=sx+side*170*math.cos(math.radians(lerp(80,40,arms))); ey=sy+lerp(260,-200,arms)
        part(im,lambda d,sx=sx,sy=sy,ex=ex,ey=ey:(d.line([sx,sy,ex,ey],fill=255,width=78),d.ellipse([ex-39,ey-39,ex+39,ey+39],fill=255)),*SHIRT,shine=False)
        part(im,lambda d,ex=ex,ey=ey:d.ellipse([ex-40,ey-40+(-10 if arms>0.5 else 30),ex+40,ey+40+(-10 if arms>0.5 else 30)],fill=255),*SKIN,shine=False)
    part(im,lambda d:d.rounded_rectangle([170,470+oy,530,900+oy],radius=110,fill=255),*SHIRT)
    part(im,lambda d:d.rectangle([310,400+oy,390,500+oy],fill=255),*SKIN,outline=None)
    # cabeza
    part(im,lambda d:d.ellipse([170,90+oy,530,470+oy],fill=255),*SKIN)
    part(im,lambda d:(d.chord([155,60+oy,545,360+oy],180,360,fill=255),d.ellipse([150,150+oy,215,290+oy],fill=255),d.ellipse([485,150+oy,550,290+oy],fill=255),d.ellipse([230,40+oy,420,170+oy],fill=255)),*HAIR)
    d=ImageDraw.Draw(im); lx=int(12*look)
    for ex in (280,420):
        ey=280+oy
        if blink and expr!="shock": d.line([ex-24,ey,ex+24,ey],fill=OUT,width=8); continue
        r=34 if expr=="shock" else 26
        d.ellipse([ex-r,ey-r,ex+r,ey+r+4],fill=WHITE,outline=OUT,width=5)
        d.ellipse([ex-12+lx,ey-12,ex+12+lx,ey+12],fill=(60,40,30)); d.ellipse([ex-5+lx,ey-8,ex+2+lx,ey-1],fill=WHITE)
        by=ey-(62 if expr=="shock" else 46)
        d.line([ex-30,by+(6 if ex<350 else -0),ex+30,by+(0 if ex<350 else 6)],fill=HAIR[1],width=11)
    for bx in (230,470): d.ellipse([bx-30,330+oy,bx+30,360+oy],fill=(245,150,140,130))
    my=380+oy
    if expr=="shock":
        o=int(45+30*talk); d.ellipse([315,my-10,385,my+o],fill=(130,35,45),outline=OUT,width=5)
        d.ellipse([505,150+oy,535,200+oy],fill=(140,200,245))
    elif expr=="happy":
        d.chord([295,my-30,405,my+20+int(35*talk)],0,180,fill=(130,35,45),outline=OUT,width=5)
    else:
        o=int(10+35*talk); d.ellipse([325,my-6,375,my+o],fill=(130,35,45),outline=OUT,width=5)
    return im

# ---------- escenarios (se calculan una vez) ----------
def room():
    img=Image.new("RGB",(W,H)); d=ImageDraw.Draw(img)
    for y in range(0,1300,6):
        k=y/1300; d.rectangle([0,y,W,y+6],fill=(int(250-25*k),int(232-30*k),int(205-35*k)))
    for y in range(1300,H,6):
        k=(y-1300)/620; d.rectangle([0,y,W,y+6],fill=(int(196-40*k),int(140-35*k),int(95-30*k)))
    for x in range(0,W,180): d.line([x+(30 if (x//180)%2 else 0),1300,x-80,H],fill=(160,110,70),width=4)
    d.rectangle([0,1290,W,1315],fill=(235,220,200))
    # ventana
    d.rounded_rectangle([640,300,1000,760],radius=16,fill=(170,215,245),outline=(255,255,255),width=18)
    d.line([820,300,820,760],fill=WHITE,width=12); d.line([640,530,1000,530],fill=WHITE,width=12)
    d.ellipse([700,360,800,420],fill=WHITE); d.ellipse([740,340,840,410],fill=WHITE)
    # cuadro
    d.rounded_rectangle([110,360,420,620],radius=10,fill=(215,134,80),outline=(120,80,50),width=14)
    for i,(dx,dy) in enumerate([(-50,-45),(-15,-65),(25,-65),(60,-45)]): d.ellipse([265+dx-22,520+dy-22,265+dx+22,520+dy+22],fill=CREAM)
    d.ellipse([215,480,315,560],fill=CREAM)
    # planta
    d.rounded_rectangle([880,1130,1010,1300],radius=20,fill=(190,110,70))
    for i in range(7):
        a=math.radians(200+i*22); d.ellipse([945+170*math.cos(a)-40,1120+150*math.sin(a)-60,945+170*math.cos(a)+40,1120+150*math.sin(a)+60],fill=(80,150,90))
    # alfombra
    d.ellipse([140,1500,940,1800],fill=(235,190,150)); d.ellipse([200,1540,880,1760],outline=(215,160,120),width=10)
    return img

def sofa_room():
    img=room(); d=ImageDraw.Draw(img)
    d.rounded_rectangle([20,900,620,1330],radius=60,fill=(110,140,120)); d.rounded_rectangle([0,1060,640,1420],radius=50,fill=(125,160,135))
    d.rounded_rectangle([60,1050,330,1200],radius=40,fill=(140,175,150)); d.rounded_rectangle([320,1050,600,1200],radius=40,fill=(140,175,150))
    return img

def desk():
    img=Image.new("RGB",(W,H)); d=ImageDraw.Draw(img)
    for y in range(0,H,6):
        k=y/H; d.rectangle([0,y,W,y+6],fill=(int(215-60*k),int(228-60*k),int(245-60*k)))
    d.rectangle([0,1300,W,H],fill=(150,105,70)); d.rectangle([0,1290,W,1320],fill=(120,80,50))
    d.ellipse([60,180,260,380],fill=(255,240,190)); d.line([160,0,160,180],fill=(90,90,90),width=6)
    return img

def door():
    img=room(); d=ImageDraw.Draw(img)
    d.rectangle([300,560,780,1300],fill=(140,90,55)); d.rectangle([330,590,750,1300],fill=(165,110,70))
    for y0 in (640,960): d.rounded_rectangle([380,y0,700,y0+260],radius=12,outline=(130,85,50),width=10)
    d.ellipse([690,930,730,970],fill=(240,200,80))
    d.rounded_rectangle([820,860,880,960],radius=14,fill=(230,230,230)); d.ellipse([835,890,865,920],fill=(200,60,60))
    return img

BG={"room":sofa_room(),"desk":desk(),"door":door()}
MIX=Image.open(A+"mixpack_hd.jpg").convert("RGB"); MOVIL=Image.open(A+"tienda_pack_pantalla.png").convert("RGB")

def card(img,src,cx,cy,w,radius=30,border=12):
    h=int(w*src.height/src.width); p=src.resize((w,h),Image.LANCZOS)
    fr=Image.new("RGBA",(w+2*border,h+2*border),(255,255,255,255)); m=Image.new("L",fr.size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,*fr.size],radius=radius+border,fill=255)
    shadow(img,cx,cy+h//2+20,w//2,25,70); img.paste(fr,(int(cx-fr.width/2),int(cy-fr.height/2)),m)
    m2=Image.new("L",(w,h),0); ImageDraw.Draw(m2).rounded_rectangle([0,0,w,h],radius=radius,fill=255); img.paste(p,(int(cx-w/2),int(cy-h/2)),m2)

def put(img,spr,cx,bottom,scale,flip=False):
    if flip: spr=spr.transpose(Image.FLIP_LEFT_RIGHT)
    w,h=int(spr.width*scale),int(spr.height*scale); spr=spr.resize((w,h),Image.LANCZOS)
    shadow(img,cx,bottom-8,int(w*0.33),22); img.paste(spr,(int(cx-w/2),int(bottom-h)),spr)

def bubble(img,txt,y,progress,tail_x,who,color=WHITE,thought=False):
    d=ImageDraw.Draw(img); f=font(56); lines=wrap(d,txt,f,860)
    sl=wrap(d,txt[:max(1,int(len(txt)*min(1,progress*1.5)))],f,860)
    hgt=len(lines)*70+106
    d.rounded_rectangle([70,y,W-70,y+hgt],radius=44,fill=color,outline=DARK,width=6)
    ty=y+hgt-3; d.polygon([(tail_x-40,ty),(tail_x+40,ty),(tail_x+8,ty+75)],fill=color,outline=DARK); d.line([(tail_x-37,ty),(tail_x+37,ty)],fill=color,width=8)
    d.text((110,y+22),who,font=font(38),fill=ORANGE); yy=y+70
    for ln in sl: d.text(((W-d.textlength(ln,font=f))/2,yy),ln,font=f,fill=DARK); yy+=70

def talkv(t,txt,start=0.0): t-=start; return abs(math.sin(t*15))*(0.6+0.4*abs(math.sin(t*3.7))) if 0<t<len(txt)/15+0.2 else 0.0
def blinkv(T,ph=0): return ((int(T*FPS)+ph)%100)<4

def zoomed(img,cx,cy,z):
    if z<=1.001: return img
    w,h=W/z,H/z; x=max(0,min(W-w,cx-w/2)); y=max(0,min(H-h,cy-h/2))
    return img.crop((int(x),int(y),int(x+w),int(y+h))).resize((W,H),Image.LANCZOS)

# ---------- escenas ----------
def s1(t,T,dur):
    img=BG["room"].copy(); txt="Oye, humano… tenemos que hablar."
    put(img,human_sprite("neutral",blink=blinkv(T),look=ease((t-0.8)/0.4)),300,1330,0.62)
    k=ease(t/1.1); x=lerp(1250,760,k); walking=t<1.1
    sp=dog_sprite("happy",talk=talkv(t,txt,1.1),blink=blinkv(T,30),tail=T*12,walk=T*14 if walking else 0,tilt=6*math.sin(T*2) if not walking else 0)
    put(img,sp,x,1720-(abs(math.sin(T*14))*18 if walking else 0),0.52,flip=True)
    if t>1.1: bubble(img,txt,200,(t-1.1)/1.2,780,"PATA")
    return img
def s2(t,T,dur):
    img=BG["room"].copy(); txt="¿¡¿DESDE CUÁNDO HABLAS?!?"
    jump=60*math.sin(min(1,t/0.4)*math.pi)
    put(img,human_sprite("shock",talk=talkv(t,txt,0.3),arms=ease(t/0.3),look=1,bounce=jump),300,1330,0.62)
    put(img,dog_sprite("wink",blink=False,tail=T*14,tilt=-8),760,1720,0.52,flip=True)
    img=zoomed(img,330,900,1.0+0.45*ease(t/0.3))
    if t>0.3: img=zoomed(img,540+8*math.sin(T*50),960+8*math.cos(T*45),1.0)
    bubble(img,txt,180,t/0.9,330,"TÚ",color=(255,245,200))
    d=ImageDraw.Draw(img)
    if t>0.3:
        for (x,y,s,c) in [(880,560,"!!",(255,80,80)),(170,640,"?!",(255,210,60))]:
            d.text((x,y),s,font=font(int(120+10*math.sin(T*12))),fill=c,stroke_width=8,stroke_fill=DARK)
    return img
def s3(t,T,dur):
    img=BG["room"].copy(); txt="Desde que me das siempre las mismas galletas… ¡Necesito variedad: 8 snacks naturales!"
    sad=t<1.6
    sp=dog_sprite("sad" if sad else "happy",talk=talkv(t,txt),blink=blinkv(T,10),tail=T*(3 if sad else 14),tilt=-12 if sad else 8*math.sin(T*3))
    put(img,sp,560,1760,0.78)
    if t>1.6:
        k=ease((t-1.6)/0.5); d=ImageDraw.Draw(img)
        for i,(bx,by,r) in enumerate([(700,1000,20),(760,930,30)]):
            if k>i*0.3: d.ellipse([bx-r,by-r,bx+r,by+r],fill=WHITE,outline=DARK,width=5)
        if k>0.5: card(img,MIX,780,680,int(380*min(1,(k-0.5)*2.2)+1))
    bubble(img,txt,170,t/2.4,520,"PATA")
    return img
def s4(t,T,dur):
    img=BG["desk"].copy(); d=ImageDraw.Draw(img); txt="Está en Mimopata. Tú solo dale al botón."
    x0,y0,sw,sh=120,560,840,525
    d.rounded_rectangle([x0-28,y0-28,x0+sw+28,y0+sh+28],radius=30,fill=(30,30,36))
    img.paste(MOVIL.resize((sw,sh),Image.LANCZOS),(x0,y0))
    d.polygon([(x0-90,y0+sh+28),(x0+sw+90,y0+sh+28),(x0+sw+40,y0+sh+90),(x0-40,y0+sh+90)],fill=(80,80,92))
    bx,by=x0+1254*sw/1440, y0+332*sh/900
    k=ease((t-0.8)/1.3); cx,cy=lerp(x0+sw*0.35,bx,k),lerp(y0+sh*0.85,by,k)
    if t>2.1: r=int(25+70*min(1,(t-2.1)/0.4)); d.ellipse([bx-r,by-r,bx+r,by+r],outline=ORANGE,width=7)
    d.polygon([(cx,cy),(cx,cy+44),(cx+12,cy+33),(cx+22,cy+55),(cx+30,cy+51),(cx+20,cy+30),(cx+36,cy+30)],fill=WHITE,outline=DARK)
    if t>2.4:
        f=font(46); s="¡Añadido al carrito!"; tw=d.textlength(s,font=f)
        d.rounded_rectangle([(W-tw)/2-30,1210,(W+tw)/2+30,1290],radius=40,fill=(60,160,90)); d.text(((W-tw)/2,1224),s,font=f,fill=WHITE)
    paw=1-ease((t-2.0)/0.25) if t>2.0 else ease(t/0.6)
    sp=dog_sprite("happy",talk=talkv(t,txt),blink=blinkv(T,5),tail=T*16,tilt=10*math.sin(T*2),look=0.6)
    put(img,sp,880,1880,0.6)
    bubble(img,txt,160,t/1.4,840,"PATA")
    return img
def s5(t,T,dur):
    img=BG["door"].copy(); d=ImageDraw.Draw(img); txt="¡Ding dong! ¡Ha llegado!"
    if t<1.4:
        for i in range(3):
            r=40+i*35+20*math.sin(T*20); d.arc([850-r,910-r,850+r,910+r],-60,60,fill=(255,200,60),width=8)
        f=font(int(96+8*math.sin(T*18))); s="DING DONG"; tw=d.textlength(s,font=f)
        d.text(((W-tw)/2,420),s,font=f,fill=(255,230,120),stroke_width=9,stroke_fill=DARK)
    k=ease((t-0.4)/0.8); bxc=lerp(-300,540,k)
    shadow(img,bxc,1600,240,30)
    d.rectangle([bxc-230,1330,bxc+230,1600],fill=(196,150,95),outline=(120,85,45),width=7)
    d.rectangle([bxc-28,1330,bxc+28,1600],fill=(228,200,150))
    f=font(50); s="mimopata"; tw=d.textlength(s,font=f); d.rounded_rectangle([bxc-tw/2-20,1470,bxc+tw/2+20,1545],radius=18,fill=WHITE); d.text((bxc-tw/2,1480),s,font=f,fill=BROWN)
    jump=abs(math.sin(T*9))*60 if t>1.0 else 0
    put(img,dog_sprite("happy",talk=talkv(t,txt),tail=T*24,walk=T*16 if t>1.0 else 0),880,1830-jump,0.5,flip=True)
    bubble(img,txt,170,t/1.0,860,"PATA")
    return img
def s6(t,T,dur):
    img=BG["room"].copy(); txt="Ñam… ¡ÑAM! El de ternera es mi favorito."
    card(img,MIX,300,1330,330)
    eat=abs(math.sin(T*11)) if t>0.3 else 0
    put(img,dog_sprite("happy",eat=eat,blink=blinkv(T,7),tail=T*24,tilt=6*math.sin(T*6)),720,1800,0.66,flip=True)
    d=ImageDraw.Draw(img)
    for i in range(7):
        y=1650-((t*260+i*160)%950); x=520+i*75+25*math.sin(t*3+i)
        d.text((x,y),"♥",font=font(78),fill=(240,80,110),stroke_width=4,stroke_fill=WHITE)
    bubble(img,txt,170,t/1.5,700,"PATA")
    return img
def s7(t,T,dur):
    img=BG["room"].copy(); txt="Vale… lo admito: tienes buen gusto."
    put(img,human_sprite("happy",talk=talkv(t,txt),blink=blinkv(T),look=1),300,1330,0.62)
    put(img,dog_sprite("cool",shades=True,tail=T*16,tilt=8*math.sin(T*3)),760,1720,0.52,flip=True)
    img=zoomed(img,540,1100,1.0+0.15*ease(t/dur))
    bubble(img,txt,180,t/1.3,330,"TÚ",color=(255,245,200))
    return img
def s8(t,T,dur):
    img=Image.new("RGB",(W,H)); d=ImageDraw.Draw(img)
    for y in range(0,H,6): k=y/H; d.rectangle([0,y,W,y+6],fill=(int(225-60*k),int(140-60*k),int(85-45*k)))
    card(img,MIX,540,880,int(560*(0.7+0.3*ease(t/0.5))))
    put(img,dog_sprite("wink",talk=talkv(t,"Pack Degustación en Mimopata"),tail=T*16,tilt=8*math.sin(T*3)),860,1400,0.34,flip=True)
    pulse=1+0.04*math.sin(T*8)
    for i,(s,sz,bgc,fg) in enumerate([("Pack Degustación · 23,17 €",56,CREAM,BROWN),("-10 % con BIENVENIDA10",int(62*pulse),WHITE,BROWN)]):
        f=font(sz); tw=d.textlength(s,font=f); y=1420+i*120
        d.rounded_rectangle([(W-tw)/2-36,y-14,(W+tw)/2+36,y+sz+26],radius=46,fill=bgc); d.text(((W-tw)/2,y),s,font=f,fill=fg)
    f=font(52); s="Link en la bio"; tw=d.textlength(s,font=f); d.text(((W-tw)/2,1680),s,font=f,fill=WHITE,stroke_width=5,stroke_fill=DARK)
    bubble(img,"Pack Degustación en Mimopata. ¡Díselo a tu humano!",170,t/1.5,760,"PATA")
    return img

SCENES=[(3.6,s1),(2.4,s2),(4.6,s3),(4.0,s4),(3.2,s5),(3.4,s6),(2.6,s7),(4.4,s8)]

def main(out):
    tmp=out+".frames"; os.makedirs(tmp,exist_ok=True); N=0; T=0.0; prev=None; X=6
    for dur,fn in SCENES:
        for k in range(int(dur*FPS)):
            t=k/FPS; T+=1/FPS; img=fn(t,T,dur)
            d=ImageDraw.Draw(img); f=font(34); tw=d.textlength("@mimopata",font=f); d.text(((W-tw)/2,70),"@mimopata",font=f,fill=WHITE,stroke_width=3,stroke_fill=DARK)
            if prev is not None and k<X: img=Image.blend(prev,img,(k+1)/(X+1))
            img.save(f"{tmp}/{N:05d}.jpg",quality=90); N+=1
        prev=img
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",f"{tmp}/%05d.jpg","-c:v","libx264","-pix_fmt","yuv420p","-crf","20","-movflags","+faststart",out],check=True)
    subprocess.run(["rm","-rf",tmp]); print("OK",out,round(N/FPS,1),"s")

if __name__=="__main__":
    if len(sys.argv)>2 and sys.argv[1]=="--frame":   # vista previa de un fotograma: --frame escena t salida.png
        i=int(sys.argv[2]); t=float(sys.argv[3]); SCENES[i][1](t,t,SCENES[i][0]).save(sys.argv[4]); sys.exit()
    main(sys.argv[1] if len(sys.argv)>1 else "personajes.mp4")

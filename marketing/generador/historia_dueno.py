"""Vídeo-historia: "¿Desde cuándo hablas?" – Pata convence a su dueño de comprar
el Pack Degustación en Mimopata. Uso: python3 historia_dueno.py salida.mp4"""
import math, os, sys, subprocess
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pata import dog, bg, font, wrap, W, H, FPS, WHITE, DARK, BROWN, ORANGE, CREAM, V

SKIN=(240,200,165); HAIR=(70,45,30); SHIRT=(60,110,170); PANTS=(50,55,70)

def human(expr="neutral", talk=0.0, blink=False, S=2):
    w,h=500*S,900*S; im=Image.new("RGBA",(w,h),(0,0,0,0)); d=ImageDraw.Draw(im); s=S
    # legs & body
    d.rounded_rectangle([150*s,560*s,240*s,880*s],radius=30*s,fill=PANTS)
    d.rounded_rectangle([260*s,560*s,350*s,880*s],radius=30*s,fill=PANTS)
    d.rounded_rectangle([120*s,330*s,380*s,620*s],radius=70*s,fill=SHIRT)
    # arms
    if expr=="shock":
        d.line([140*s,380*s,60*s,250*s],fill=SHIRT,width=55*s); d.ellipse([30*s,210*s,95*s,275*s],fill=SKIN)
        d.line([360*s,380*s,440*s,250*s],fill=SHIRT,width=55*s); d.ellipse([405*s,210*s,470*s,275*s],fill=SKIN)
    else:
        d.line([140*s,380*s,100*s,560*s],fill=SHIRT,width=55*s); d.ellipse([70*s,540*s,130*s,600*s],fill=SKIN)
        d.line([360*s,380*s,400*s,560*s],fill=SHIRT,width=55*s); d.ellipse([370*s,540*s,430*s,600*s],fill=SKIN)
    # neck/head
    d.rectangle([220*s,290*s,280*s,350*s],fill=SKIN)
    d.ellipse([130*s,60*s,370*s,320*s],fill=SKIN)
    d.chord([120*s,40*s,380*s,250*s],180,360,fill=HAIR)
    d.ellipse([120*s,120*s,160*s,200*s],fill=HAIR); d.ellipse([340*s,120*s,380*s,200*s],fill=HAIR)
    # eyes
    for ex in (205*s,295*s):
        if blink and expr!="shock": d.line([ex-18*s,185*s,ex+18*s,185*s],fill=DARK,width=6*s)
        elif expr=="shock":
            d.ellipse([ex-24*s,160*s,ex+24*s,212*s],fill=WHITE,outline=DARK,width=4*s); d.ellipse([ex-8*s,178*s,ex+8*s,194*s],fill=DARK)
        else: d.ellipse([ex-13*s,170*s,ex+13*s,200*s],fill=DARK)
    # brows
    if expr=="shock":
        d.line([180*s,130*s,230*s,140*s],fill=HAIR,width=8*s); d.line([270*s,140*s,320*s,130*s],fill=HAIR,width=8*s)
    # mouth
    if expr=="shock":
        o=int((30+25*talk)*s); d.ellipse([225*s,240*s,275*s,240*s+o+20*s],fill=(120,30,40))
        d.ellipse([350*s,120*s,375*s,165*s],fill=(130,190,240))  # sudor
    elif expr=="happy":
        d.chord([200*s,225*s,300*s,275*s+int(25*talk*s)],0,180,fill=(120,30,40))
    else:
        op=int(8*s+30*talk*s); d.ellipse([228*s,245*s,272*s,250*s+op],fill=(120,30,40))
    return im.resize((250,450),Image.LANCZOS)

def bubble_at(img,txt,y,progress,tail_x,who=None,color=WHITE):
    d=ImageDraw.Draw(img); f=font(58); lines=wrap(d,txt,f,860)
    n=max(1,int(len(txt)*min(1,progress*1.5))); sl=wrap(d,txt[:n],f,860)
    top=y; hgt=len(lines)*72+60+(50 if who else 0)
    d.rounded_rectangle([70,top,W-70,top+hgt],radius=46,fill=color,outline=DARK,width=6)
    d.polygon([(tail_x-45,top+hgt-3),(tail_x+45,top+hgt-3),(tail_x,top+hgt+70)],fill=color,outline=DARK)
    d.line([(tail_x-42,top+hgt-3),(tail_x+42,top+hgt-3)],fill=color,width=8)
    yy=top+26
    if who:
        fw=font(40); d.text((110,yy),who,font=fw,fill=ORANGE); yy+=50
    for ln in sl: d.text(((W-d.textlength(ln,font=f))/2,yy),ln,font=f,fill=DARK); yy+=72

def paste(img,sprite,x,y,size=None):
    if size: sprite=sprite.resize(size,Image.LANCZOS)
    img.paste(sprite,(int(x),int(y)),sprite)

def talking(t,txt): return abs(math.sin(t*14)) if t<len(txt)/15+0.2 else 0.0

SCREEN=Image.open(V+"tienda_pack_pantalla.png").convert("RGB")
PACK=Image.open(V+"pack_caja.png").convert("RGB")

def laptop(img,t,click_t):
    d=ImageDraw.Draw(img)
    x0,y0,sw,sh=110,520,860,537
    d.rounded_rectangle([x0-30,y0-30,x0+sw+30,y0+sh+30],radius=30,fill=(35,35,40))
    scr=SCREEN.resize((sw,sh),Image.LANCZOS); img.paste(scr,(x0,y0))
    d.polygon([(x0-90,y0+sh+30),(x0+sw+90,y0+sh+30),(x0+sw+30,y0+sh+90),(x0-30,y0+sh+90)],fill=(70,70,80))
    # cursor moves to "Agregar al carrito" (≈ x 1254, y 332 en la captura de 1440x900)
    tx,ty=x0+1254*sw/1440, y0+332*sh/900
    sx,sy=x0+sw*0.3, y0+sh*0.8
    k=min(1,max(0,t/click_t)); k=k*k*(3-2*k)
    cx,cy=sx+(tx-sx)*k, sy+(ty-sy)*k
    if t>click_t:
        r=int(20+60*min(1,(t-click_t)/0.4)); d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=ORANGE,width=6)
    d.polygon([(cx,cy),(cx,cy+44),(cx+12,cy+33),(cx+22,cy+55),(cx+30,cy+51),(cx+20,cy+30),(cx+36,cy+30)],fill=WHITE,outline=DARK)
    if t>click_t+0.3:
        f=font(46); s="✓ ¡Añadido al carrito!"; s="¡Añadido al carrito!"; tw=d.textlength(s,font=f)
        d.rounded_rectangle([(W-tw)/2-30,y0+sh+120,(W+tw)/2+30,y0+sh+200],radius=40,fill=(60,160,90))
        d.text(((W-tw)/2,y0+sh+134),s,font=f,fill=WHITE)

def box(img,t,open_t,cx=540,cy=1180):
    d=ImageDraw.Draw(img)
    bw,bh=460,300
    # producto saliendo
    if t>open_t:
        k=min(1,(t-open_t)/0.6); k=1-(1-k)**3
        pw=int(380*(0.4+0.6*k)); ph=int(pw*PACK.height/PACK.width)
        p=PACK.resize((pw,ph),Image.LANCZOS)
        m=Image.new("L",(pw,ph),0); ImageDraw.Draw(m).rounded_rectangle([0,0,pw,ph],radius=24,fill=255)
        img.paste(p,(cx-pw//2,int(cy-bh//2-ph*k-10)),m)
        for i in range(8):  # destellos
            a=i*math.pi/4+t*2; r=260+20*math.sin(t*6+i)
            x,y=cx+r*math.cos(a), cy-bh//2-180+r*0.5*math.sin(a)
            d.text((x,y),"✦",font=font(40),fill=(255,230,120))
    d.rectangle([cx-bw//2,cy-bh//2,cx+bw//2,cy+bh//2],fill=(196,150,95),outline=(120,85,45),width=6)
    d.rectangle([cx-30,cy-bh//2,cx+30,cy+bh//2],fill=(225,195,140))
    if t<=open_t:
        d.polygon([(cx-bw//2,cy-bh//2),(cx+bw//2,cy-bh//2),(cx+bw//2-20,cy-bh//2-40),(cx-bw//2+20,cy-bh//2-40)],fill=(210,165,110),outline=(120,85,45))
    else:
        d.polygon([(cx-bw//2,cy-bh//2),(cx-bw//2-120,cy-bh//2-90),(cx-bw//2-60,cy-bh//2-110),(cx,cy-bh//2)],fill=(210,165,110),outline=(120,85,45))
        d.polygon([(cx+bw//2,cy-bh//2),(cx+bw//2+120,cy-bh//2-90),(cx+bw//2+60,cy-bh//2-110),(cx,cy-bh//2)],fill=(210,165,110),outline=(120,85,45))
    f=font(52); s="mimopata"; tw=d.textlength(s,font=f)
    d.rounded_rectangle([cx-tw/2-24,cy+20,cx+tw/2+24,cy+100],radius=20,fill=WHITE)
    d.text((cx-tw/2,cy+30),s,font=f,fill=BROWN)

# (duración, fondo, función de dibujo)
def sc1(img,t,T):  # perro habla por primera vez
    txt="Oye, humano… tenemos que hablar."
    bubble_at(img,txt,170,t/1.6,700,"PATA")
    paste(img,human("neutral",blink=(int(T*FPS)%90)<4),150,1000,(375,675))
    paste(img,dog("happy",talk=talking(t,txt),tail=T*12,bounce=10*abs(math.sin(T*6))),560,1150,(420,467))
def sc2(img,t,T):
    txt="¿¡¿DESDE CUÁNDO HABLAS?!?"
    bubble_at(img,txt,170,t/1.0,330,"TÚ",color=(255,245,200))
    x=150+8*math.sin(T*40)  # tiembla
    paste(img,human("shock",talk=talking(t,txt)),x,1000,(375,675))
    paste(img,dog("wink",tail=T*12),560,1150,(420,467))
def sc3(img,t,T):
    txt="Desde que me das siempre las mismas galletas. Necesito variedad: ¡8 snacks naturales!"
    bubble_at(img,txt,150,t/2.6,700,"PATA")
    paste(img,human("neutral",blink=(int(T*FPS)%90)<4),150,1000,(375,675))
    paste(img,dog("sad" if t<1.2 else "happy",talk=talking(t,txt),tail=T*10),560,1150,(420,467))
def sc4(img,t,T):
    txt="Está en Mimopata. Tú solo dale al botón."
    bubble_at(img,txt,120,t/1.6,820,"PATA")
    laptop(img,t,2.2)
    paste(img,dog("happy",talk=talking(t,txt),tail=T*14),730,1380,(300,333))
def sc5(img,t,T):
    d=ImageDraw.Draw(img)
    txt="¡Ding dong! ¡Ha llegado!"
    bubble_at(img,txt,150,t/1.0,540,"PATA")
    box(img,t,1.6)
    if t<1.6:
        f=font(int(90+10*math.sin(T*20))); s="DING DONG"; tw=d.textlength(s,font=f)
        d.text(((W-tw)/2,560),s,font=f,fill=(255,230,120),stroke_width=8,stroke_fill=DARK)
    paste(img,dog("happy",talk=talking(t,txt),tail=T*20,bounce=25*abs(math.sin(T*9))),80,1430,(330,367))
def sc6(img,t,T):
    d=ImageDraw.Draw(img)
    txt="Ñam… ¡ÑAM! Este de ternera es mi favorito."
    bubble_at(img,txt,150,t/1.8,600,"PATA")
    k=min(1,t/0.4); pw=int(420*k)+1; ph=int(pw*PACK.height/PACK.width)+1
    p=PACK.resize((pw,ph),Image.LANCZOS); m=Image.new("L",(pw,ph),0); ImageDraw.Draw(m).rounded_rectangle([0,0,pw,ph],radius=24,fill=255)
    img.paste(p,(80,640),m)
    eat=abs(math.sin(t*10))
    paste(img,dog("happy",talk=eat,tail=T*22,bounce=8*abs(math.sin(T*9))),520,820,(480,533))
    for i in range(5):  # corazones
        y=1300-((t*220+i*130)%600); x=600+i*80+20*math.sin(t*3+i)
        d.text((x,y),"♥",font=font(70),fill=(230,80,110))
    paste(img,human("happy",talk=0),120,1250,(260,468))
def sc7(img,t,T):
    txt="Vale… lo admito: tienes buen gusto."
    bubble_at(img,txt,170,t/1.4,330,"TÚ",color=(255,245,200))
    paste(img,human("happy",talk=talking(t,txt)),150,1000,(375,675))
    paste(img,dog("cool",shades=True,tail=T*14,bounce=8*abs(math.sin(T*6))),560,1150,(420,467))
def sc8(img,t,T):
    d=ImageDraw.Draw(img)
    txt="Pack Degustación en Mimopata. ¡Díselo a tu humano!"
    bubble_at(img,txt,170,t/1.6,540,"PATA")
    paste(img,dog("wink",talk=talking(t,txt),tail=T*14,bounce=10*abs(math.sin(T*6))),(W-520)//2,700,(520,578))
    pulse=1+0.04*math.sin(T*8)
    for i,(s,sz,bgc,fg) in enumerate([("Pack Degustación · 23,17 €",56,CREAM,BROWN),("-10 % con BIENVENIDA10",int(64*pulse),WHITE,BROWN)]):
        f=font(sz); tw=d.textlength(s,font=f); y=1330+i*120
        d.rounded_rectangle([(W-tw)/2-36,y-14,(W+tw)/2+36,y+sz+26],radius=46,fill=bgc)
        d.text(((W-tw)/2,y),s,font=f,fill=fg)
    f=font(52); s="Link en la bio"; tw=d.textlength(s,font=f)
    d.text(((W-tw)/2,1600),s,font=f,fill=WHITE,stroke_width=5,stroke_fill=DARK)

SCENES=[(2.6,((250,214,165),(235,160,100)),sc1),(2.2,((255,200,120),(230,120,60)),sc2),
        (4.4,((120,140,170),(70,80,110)),sc3),(4.2,((200,220,240),(140,170,210)),sc4),
        (3.6,((250,214,165),(235,160,100)),sc5),(3.6,((240,190,210),(200,120,160)),sc6),
        (2.6,((170,200,150),(110,140,90)),sc7),(4.4,((215,134,80),(160,80,40)),sc8)]

def main(out):
    tmp=out+".frames"; os.makedirs(tmp,exist_ok=True); N=0; T=0.0
    for dur,(c1,c2),fn in SCENES:
        for k in range(int(dur*FPS)):
            t=k/FPS; T+=1/FPS
            img=bg(c1,c2,T); fn(img,t,T)
            d=ImageDraw.Draw(img); f=font(34); tw=d.textlength("@mimopata",font=f)
            d.text(((W-tw)/2,70),"@mimopata",font=f,fill=WHITE,stroke_width=3,stroke_fill=DARK)
            img.save(f"{tmp}/{N:05d}.jpg",quality=90); N+=1
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",f"{tmp}/%05d.jpg","-c:v","libx264","-pix_fmt","yuv420p","-crf","21","-movflags","+faststart",out],check=True)
    subprocess.run(["rm","-rf",tmp]); print("OK",out,round(T,1),"s")

if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else "historia.mp4")

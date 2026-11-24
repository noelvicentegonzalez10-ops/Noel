"""Vídeo medio realista "¿Desde cuándo hablas?" con fotos reales del Pack Degustación.
Uso: python3 historia_realista.py salida.mp4"""
import math, os, sys, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
HERE=os.path.dirname(os.path.abspath(__file__)); A=os.path.join(HERE,"assets")+"/"
sys.path.insert(0,HERE)
from pata import font, wrap, W, H, FPS, WHITE, DARK, BROWN, ORANGE, CREAM

def load(n): return Image.open(A+n).convert("RGB")
LAB=load("lab_bolsa_hd.jpg"); MUJER=load("mujer_perro_hd.jpg"); DOODLE=load("doodle_bolsas_hd.jpg")
MIX=load("mixpack_hd.jpg"); MOVIL=load("tienda_movil.png")

def ease(k): k=max(0,min(1,k)); return k*k*(3-2*k)

def camera(src,cx,cy,zoom,shake=0.0,t=0.0):
    """Recorte tipo cámara: centro (cx,cy) en fracciones de la foto, zoom>=1 sobre el encuadre 'cover'."""
    sw,sh=src.size; base=max(W/sw,H/sh); s=base*zoom
    vw,vh=W/s,H/s
    x=cx*sw-vw/2+shake*math.sin(t*55)*sw*0.01; y=cy*sh-vh/2+shake*math.cos(t*47)*sh*0.01
    x=max(0,min(sw-vw,x)); y=max(0,min(sh-vh,y))
    return src.crop((int(x),int(y),int(x+vw),int(y+vh))).resize((W,H),Image.LANCZOS)

def vignette(img,strength=0.45):
    m=Image.new("L",(W//8,H//8),0); d=ImageDraw.Draw(m)
    d.ellipse([-W//16,-H//20,W//8+W//16,H//8+H//20],fill=255); m=m.filter(ImageFilter.GaussianBlur(18)).resize((W,H))
    dark=ImageEnhance.Brightness(img).enhance(1-strength); img.paste(dark,(0,0),Image.eval(m,lambda v:255-v))

def bubble(img,txt,y,progress,tail_x,who,color=WHITE,tail_down=True):
    d=ImageDraw.Draw(img); f=font(56); lines=wrap(d,txt,f,860)
    n=max(1,int(len(txt)*min(1,progress*1.5))); sl=wrap(d,txt[:n],f,860)
    hgt=len(lines)*70+60+46
    pop=min(1,progress*6); pad=int(10*(1-pop))
    d.rounded_rectangle([70+pad,y+pad,W-70-pad,y+hgt-pad],radius=44,fill=color,outline=DARK,width=6)
    ty=y+hgt-3; d.polygon([(tail_x-40,ty),(tail_x+40,ty),(tail_x+10,ty+75)],fill=color,outline=DARK)
    d.line([(tail_x-37,ty),(tail_x+37,ty)],fill=color,width=8)
    d.text((110,y+22),who,font=font(38),fill=ORANGE); yy=y+70
    for ln in sl: d.text(((W-d.textlength(ln,font=f))/2,yy),ln,font=f,fill=DARK); yy+=70

def sticker(img,txt,x,y,size,col,t,rot=0):
    f=font(size); d0=ImageDraw.Draw(img); tw=int(d0.textlength(txt,font=f))+40
    s=Image.new("RGBA",(tw,size+40),(0,0,0,0)); d=ImageDraw.Draw(s)
    d.text((20,10),txt,font=f,fill=col,stroke_width=8,stroke_fill=DARK)
    sc=1+0.08*math.sin(t*12); s=s.resize((int(s.width*sc),int(s.height*sc))).rotate(rot,expand=True,resample=Image.BICUBIC)
    img.paste(s,(int(x-s.width/2),int(y-s.height/2)),s)

def tag(img):
    d=ImageDraw.Draw(img); f=font(34); tw=d.textlength("@mimopata",font=f)
    d.text(((W-tw)/2,70),"@mimopata",font=f,fill=WHITE,stroke_width=3,stroke_fill=DARK)

# ---- escenas ----
def s1(t,dur):  # labrador "habla"
    talk=0.012*abs(math.sin(t*14)) if t<2.0 else 0
    img=camera(LAB,0.58,0.45,1.0+0.12*ease(t/dur)+talk); vignette(img)
    bubble(img,"Oye, humano… tenemos que hablar.",230,t/1.4,760,"🐶 PATA".replace("🐶 ",""))
    return img
def s2(t,dur):  # zoom dramático a la dueña
    z=1.0+1.1*ease(t/0.35); img=camera(MUJER,0.64,0.30,z,shake=0.6 if t>0.3 else 0,t=t); vignette(img,0.5)
    bubble(img,"¿¡¿DESDE CUÁNDO HABLAS?!?",230,t/0.9,520,"TÚ",color=(255,245,200))
    if t>0.35: sticker(img,"!!",900,700,150,(255,80,80),t,rot=-12); sticker(img,"?!",180,820,130,(255,220,60),t,rot=10)
    return img
def s3(t,dur):  # paneo del perro a las bolsas
    k=ease(t/dur); img=camera(DOODLE,0.22+0.55*k,0.55,1.05); vignette(img)
    bubble(img,"Desde que me das siempre las mismas galletas. Necesito variedad: ¡8 snacks naturales!",190,t/2.4,300 if k<0.5 else 700,"PATA")
    return img
def s4(t,dur):  # compra en el móvil
    bgimg=camera(DOODLE,0.5,0.5,1.0).filter(ImageFilter.GaussianBlur(28)); img=ImageEnhance.Brightness(bgimg).enhance(0.55)
    d=ImageDraw.Draw(img)
    pw,ph=600,1298; px,py=(W-pw)//2,470
    d.rounded_rectangle([px-26,py-26,px+pw+26,py+ph+26],radius=80,fill=(15,15,18))
    scr=MOVIL.resize((pw,int(MOVIL.height*pw/MOVIL.width)),Image.LANCZOS)
    m=Image.new("L",(pw,ph),0); ImageDraw.Draw(m).rounded_rectangle([0,0,pw,ph],radius=60,fill=255)
    img.paste(scr.crop((0,0,pw,ph)),(px,py),m)
    d.rounded_rectangle([px+pw//2-90,py+14,px+pw//2+90,py+48],radius=18,fill=(15,15,18))
    bx,by=px+281*pw/390, py+753*pw/390   # botón "Agregar al carrito"
    k=ease((t-0.6)/1.4); fx,fy=px+pw*0.5+(bx-px-pw*0.5)*k, py+ph+120+(by-(py+ph+120))*k
    if t>2.1:
        r=int(30+90*min(1,(t-2.1)/0.4)); d.ellipse([bx-r,by-r,bx+r,by+r],outline=ORANGE,width=8)
    d.ellipse([fx-38,fy-38,fx+38,fy+38],fill=(255,255,255,200),outline=DARK,width=4)
    if t>2.4:
        f=font(46); s="¡Añadido al carrito!"; tw=d.textlength(s,font=f)
        d.rounded_rectangle([(W-tw)/2-30,py+ph-170,(W+tw)/2+30,py+ph-90],radius=40,fill=(60,160,90)); d.text(((W-tw)/2,py+ph-156),s,font=f,fill=WHITE)
    bubble(img,"Está en Mimopata. Tú solo dale al botón.",150,t/1.4,820,"PATA")
    return img
def s5(t,dur):  # notificación de entrega
    img=camera(MIX,0.5,0.5,1.0+0.08*ease(t/dur)); vignette(img,0.35)
    d=ImageDraw.Draw(img); k=ease(t/0.5); y=int(-260+(400)*k)
    d.rounded_rectangle([60,y,W-60,y+220],radius=40,fill=(250,250,250))
    d.rounded_rectangle([95,y+40,175,y+120],radius=20,fill=ORANGE); d.text((112,y+52),"m",font=font(52),fill=WHITE)
    d.text((200,y+36),"Mimopata · ahora",font=font(34),fill=(110,110,110))
    d.text((200,y+82),"📦 ¡Tu pedido ha llegado!".replace("📦 ",""),font=font(46),fill=DARK)
    d.text((200,y+142),"Pack Degustación Floopp",font=font(36),fill=(90,90,90))
    if t>0.9: sticker(img,"DING DONG",W/2,1500,110,(255,230,120),t,rot=-6)
    return img
def s6(t,dur):  # lo prueba
    chew=0.012*abs(math.sin(t*16)); img=camera(LAB,0.6,0.42,1.25+0.1*ease(t/dur)+chew); vignette(img)
    bubble(img,"Ñam… ¡ÑAM! El de ternera es mi favorito.",230,t/1.5,640,"PATA")
    d=ImageDraw.Draw(img)
    for i in range(6):
        y=1750-((t*260+i*170)%900); x=200+i*140+30*math.sin(t*3+i)
        d.text((x,y),"♥",font=font(80),fill=(240,80,110),stroke_width=4,stroke_fill=WHITE)
    return img
def s7(t,dur):
    img=camera(MUJER,0.5,0.5,1.0+0.1*ease(t/dur)); vignette(img)
    bubble(img,"Vale… lo admito: tienes buen gusto.",230,t/1.3,560,"TÚ",color=(255,245,200))
    return img
def s8(t,dur):
    bgimg=camera(MIX,0.5,0.5,1.0).filter(ImageFilter.GaussianBlur(25)); img=ImageEnhance.Brightness(bgimg).enhance(0.6)
    k=ease(t/0.5); cw=int(760*(0.6+0.4*k)); card=MIX.resize((cw,cw),Image.LANCZOS)
    m=Image.new("L",(cw,cw),0); ImageDraw.Draw(m).rounded_rectangle([0,0,cw,cw],radius=40,fill=255)
    img.paste(card,((W-cw)//2,560+(760-cw)//2),m)
    d=ImageDraw.Draw(img); pulse=1+0.04*math.sin(t*8)
    for i,(s,sz,bgc,fg) in enumerate([("Pack Degustación · 23,17 €",56,CREAM,BROWN),("-10 % con BIENVENIDA10",int(62*pulse),WHITE,BROWN)]):
        f=font(sz); tw=d.textlength(s,font=f); y=1380+i*120
        d.rounded_rectangle([(W-tw)/2-36,y-14,(W+tw)/2+36,y+sz+26],radius=46,fill=bgc); d.text(((W-tw)/2,y),s,font=f,fill=fg)
    f=font(52); s="Link en la bio"; tw=d.textlength(s,font=f); d.text(((W-tw)/2,1640),s,font=f,fill=WHITE,stroke_width=5,stroke_fill=DARK)
    bubble(img,"Pack Degustación en Mimopata. ¡Díselo a tu humano!",170,t/1.5,540,"PATA")
    return img

SCENES=[(2.6,s1),(2.2,s2),(4.4,s3),(4.0,s4),(3.0,s5),(3.4,s6),(2.6,s7),(4.4,s8)]

def main(out):
    tmp=out+".frames"; os.makedirs(tmp,exist_ok=True); N=0; prev=None; X=6
    frames_per=[]
    for dur,fn in SCENES:
        n=int(dur*FPS)
        for k in range(n):
            img=fn(k/FPS,dur); tag(img)
            if prev is not None and k<X: img=Image.blend(prev,img,(k+1)/(X+1))
            img.save(f"{tmp}/{N:05d}.jpg",quality=90); N+=1
        prev=img
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",f"{tmp}/%05d.jpg","-c:v","libx264","-pix_fmt","yuv420p","-crf","20","-movflags","+faststart",out],check=True)
    subprocess.run(["rm","-rf",tmp]); print("OK",out,round(N/FPS,1),"s")

if __name__=="__main__": main(sys.argv[1] if len(sys.argv)>1 else "historia_realista.mp4")

"""Música de fondo sintetizada (sin derechos de autor): ritmo alegre tipo TikTok.
musica(duracion_s, salida.wav, tonalidad=0, bpm=112, semilla=0)"""
import numpy as np, wave

SR=44100
def _env(n,a=0.005,r=0.25):
    t=np.arange(n)/SR; e=np.minimum(1,t/a)*np.exp(-t/r); return e
def _tone(f,n,kind="saw",a=0.005,r=0.3):
    t=np.arange(n)/SR
    if kind=="sine": w=np.sin(2*np.pi*f*t)
    elif kind=="square": w=np.sign(np.sin(2*np.pi*f*t))*0.6
    else: w=2*((f*t)%1)-1
    return w*_env(n,a,r)
def midi(m): return 440*2**((m-69)/12)

def musica(dur,out,tonalidad=0,bpm=112,semilla=0):
    rng=np.random.default_rng(semilla); N=int(dur*SR); mix=np.zeros(N+8*SR)
    beat=60/bpm; step=beat/2
    prog=[[0,4,7],[7,11,14],[9,12,16],[5,9,12]]  # I V vi IV
    root=57+tonalidad
    i=0; t=0.0
    while t<dur:
        bar=int(t/(beat*4))%4; ch=prog[bar]; pos=int(t*SR)
        k=int(round(t/step))
        # bombo y caja
        if k%2==0:
            n=int(0.25*SR); tt=np.arange(n)/SR; kick=np.sin(2*np.pi*(50+90*np.exp(-tt*30))*tt)*np.exp(-tt*9)
            mix[pos:pos+n]+=0.9*kick
        if k%4==2:
            n=int(0.18*SR); sn=rng.standard_normal(n)*np.exp(-np.arange(n)/SR*22); mix[pos:pos+n]+=0.35*sn
        # charles
        n=int(0.05*SR); hh=rng.standard_normal(n)*np.exp(-np.arange(n)/SR*90); mix[pos:pos+n]+=0.12*hh
        # bajo
        if k%2==0:
            n=int(step*SR*1.9); mix[pos:pos+n]+=0.35*_tone(midi(root-12+ch[0]),n,"square",0.004,0.25)
        # arpegio
        m=root+12+ch[k%3]+(12 if (k//3)%2 else 0); n=int(step*SR*1.2)
        mix[pos:pos+n]+=0.18*_tone(midi(m),n,"saw",0.003,0.12)
        # acorde suave
        if k%8==0:
            n=int(beat*4*SR)
            for c in ch: mix[pos:pos+n]+=0.06*_tone(midi(root+c),n,"sine",0.05,1.5)
        t+=step; i+=1
    mix=mix[:N]
    fade=int(0.8*SR); mix[-fade:]*=np.linspace(1,0,fade); mix[:int(0.05*SR)]*=np.linspace(0,1,int(0.05*SR))
    mix=mix/np.max(np.abs(mix))*0.85
    data=(mix*32767).astype(np.int16)
    with wave.open(out,"wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data.tobytes())

if __name__=="__main__":
    import sys; musica(float(sys.argv[1]),sys.argv[2])

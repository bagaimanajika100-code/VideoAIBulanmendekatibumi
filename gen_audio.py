# Membuat sfx.wav (30 detik, efek suara saja) tanpa library tambahan
import math,random,wave,struct
SR=44100;N=SR*30;random.seed(3);buf=[0.0]*N
cl=lambda x:max(0.0,min(1.0,x))
def noise(t0,t1,amp,coef,mod=None):
    y=0.0
    for i in range(int(t0*SR),min(N,int(t1*SR))):
        t=i/SR;y+=coef(t)*((random.random()*2-1)-y)
        buf[i]+=y*amp(t)*(mod(t) if mod else 1)
def tone(t0,t1,f,amp):
    for i in range(int(t0*SR),min(N,int(t1*SR))):
        t=i/SR;buf[i]+=math.sin(2*math.pi*f(t)*t)*amp(t)
# whoosh Bulan mulai mendekat
noise(4,5.8,lambda t:.9*math.sin(math.pi*(t-4)/1.8),lambda t:.02+.1*(t-4))
# dengung gravitasi makin kuat
tone(4,30,lambda t:45,lambda t:(.05+.18*cl((t-4)/17))*(1-cl((t-26)/3)))
tone(4,30,lambda t:62,lambda t:(.03+.1*cl((t-4)/17))*(1-cl((t-26)/3)))
# gelombang laut
noise(9,15.5,lambda t:.9*math.sin(math.pi*(t-9)/6.5),lambda t:.05,lambda t:.5+.5*math.sin(2*math.pi*.4*t))
# gempa
noise(15,21.5,lambda t:.6*cl((t-15)/1.5),lambda t:.02)
for _ in range(14):
    p=random.uniform(15,21);noise(p,p+.15,lambda t:.8,lambda t:.3)
# ledakan di batas Roche
tone(21,23,lambda t:30+90*math.exp(-3*(t-21)),lambda t:.8*math.exp(-2.2*(t-21)))
noise(21,22.2,lambda t:.8*math.exp(-3*(t-21)),lambda t:.15)
# puing berderak
for i in range(int(21.3*SR),int(26*SR)):
    if random.random()<.002*(1-cl((i/SR-21.3)/4.7)):
        for k in range(300):
            if i+k<N:buf[i+k]+=random.uniform(-.4,.4)*math.exp(-k/60)
# dengung cincin yang tenang
tone(26,30,lambda t:440,lambda t:.05*(1-cl((t-27)/3))*(.6+.4*math.sin(6*t)))
tone(26,30,lambda t:660,lambda t:.03*(1-cl((t-27)/3)))
pk=max(abs(x) for x in buf) or 1
w=wave.open("sfx.wav","wb");w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR)
w.writeframes(b"".join(struct.pack("<h",int(max(-1,min(1,x/pk*.85))*32767)) for x in buf));w.close()
print("sfx.wav selesai")

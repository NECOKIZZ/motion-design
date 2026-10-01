# Procedural 120 BPM track for the kickoff.cash film. Phrase = 8 pulses = 4s.
# P0-1 intro (pad, heartbeat), P2-3 groove in, P4-5 turn (bass+claps), P6-7 build + riser,
# stop at 31.5s, DROP at 32s, P8-9 full, P10-12 groove, P13 logo hit at 54s, tail to 60s.
import numpy as np, wave
SR=44100; BPM=120; PULSE=60/BPM; DUR=60.0
N=int(SR*DUR); L=np.zeros(N); R=np.zeros(N)
rng=np.random.default_rng(7)
def t_(d): return np.arange(int(SR*d))/SR
def add(sig,start,gain=1.0,pan=0.0):
    i=int(start*SR); j=min(N,i+len(sig))
    if j<=i: return
    s=sig[:j-i]*gain
    L[i:j]+=s*np.sqrt((1-pan)/2)*1.414/1.414; R[i:j]+=s*np.sqrt((1+pan)/2)
def env(n,a,d,sus=0.0,rel=None):
    e=np.ones(n)
    ai=max(1,int(a*SR)); e[:ai]=np.linspace(0,1,ai)
    return e
def kick(g=1.0):
    t=t_(0.45); f=48+110*np.exp(-t*28); ph=2*np.pi*np.cumsum(f)/SR
    s=np.sin(ph)*np.exp(-t*7.5); s+=0.25*np.sin(ph*2)*np.exp(-t*30)
    c=rng.standard_normal(len(t))*np.exp(-t*250)*0.3
    return np.tanh((s+c)*1.6)*g
def hat(g=0.18,dec=60):
    t=t_(0.12); n=rng.standard_normal(len(t)); n=np.diff(np.concatenate([[0],n]))
    return n*np.exp(-t*dec)*g
def clap(g=0.4):
    t=t_(0.3); n=rng.standard_normal(len(t))
    e=np.exp(-t*22)+0.6*np.exp(-np.maximum(0,t-0.012)*40)*(t>0.012)+0.4*np.exp(-np.maximum(0,t-0.024)*40)*(t>0.024)
    n=np.convolve(n,np.ones(6)/6,'same')-np.convolve(n,np.ones(40)/40,'same')
    return n*e*g
def saw(f,t): return 2*((f*t)%1)-1
def lp(x,a):  # one-pole lowpass, a in (0,1)
    y=np.empty_like(x); acc=0.0
    for i in range(len(x)): acc+=a*(x[i]-acc); y[i]=acc
    return y
def note(m): return 440*2**((m-69)/12)
# chords (minor, dark): Fm - Db - Ab - Eb , 2 bars each? one chord per phrase(4s)
prog=[[53,56,60,65],[49,53,56,61],[56,60,63,68],[51,55,58,63]]
def pad_chord(ch,d,bright):
    t=t_(d); s=np.zeros(len(t))
    for m in ch:
        for det in (-0.12,0.0,0.11):
            s+=saw(note(m)*(1+det/100*3),t)
    s/= (len(ch)*3)
    a=0.02+0.10*bright
    s=lp(lp(s,a),a)
    e=np.minimum(1,t/0.8)*np.minimum(1,(d-t)/0.6)
    return s*e
print('pads'); 
for p in range(15):
    ch=prog[p%4]
    bright={0:0.0,1:0.1,2:0.25,3:0.3,4:0.45,5:0.5,6:0.55,7:0.65,8:1.0,9:1.0,10:0.7,11:0.7,12:0.6,13:0.9,14:0.5}[p]
    g={0:0.35,1:0.45}.get(p,0.38)
    if p==7: pass
    s=pad_chord(ch,4.6 if p<14 else 4.0,bright)
    add(s,p*4,g,-0.2); add(np.roll(s,300),p*4,g,0.2)
# bass: root note pattern from P4, 8ths, sidechain feel
print('bass')
for p in list(range(4,8))+list(range(8,13))+[13]:
    root=prog[p%4][0]-24
    for k in range(8 if p!=13 else 4):
        st=p*4+k*PULSE+PULSE*0.5
        if p==7 and k>=7: continue
        t=t_(PULSE*0.45); f=note(root+(12 if k%4==3 else 0))
        s=np.tanh(2.2*(np.sin(2*np.pi*f*t)+0.3*saw(f,t)))*np.minimum(1,t/0.005)*np.exp(-t*3)
        add(s,st,0.22)
# drums
print('drums')
for b in range(int(DUR/PULSE)):
    tb=b*PULSE; p=int(tb//4); k=b%8
    if 31.5<=tb<32: continue
    if p>=14: continue
    if p in (0,1):
        if k in (0,) : add(kick(0.45),tb,0.6)
        if p==1 and k==6: add(kick(0.35),tb,0.6)
        continue
    if p==7 and k>=4:  # build: kick doubles
        add(kick(0.9),tb,0.8); add(kick(0.6),tb+PULSE/2,0.6); continue
    if p==13 and k>=2: continue  # space for logo lock
    add(kick(1.0),tb,0.85)
    add(hat(0.16),tb+PULSE/2,1.0,0.3)
    if p>=8 and p<=12: add(hat(0.08,90),tb+PULSE/4,1.0,-0.3); add(hat(0.08,90),tb+3*PULSE/4,1.0,-0.3)
    if p>=4 and k%2==1: add(clap(0.42),tb,1.0,0.05)
# riser P6.4 -> 31.5
print('fx')
def riser(d):
    t=t_(d); n=rng.standard_normal(len(t)); out=np.zeros(len(t))
    # sweeping bandpass via two lowpasses with rising cutoff, chunked
    ch=2048; acc1=acc2=0.0
    for i in range(0,len(t),ch):
        a=0.01+0.5*(i/len(t))**2
        for j in range(i,min(len(t),i+ch)):
            acc1+=a*(n[j]-acc1); acc2+=a*0.5*(acc1-acc2); out[j]=acc1-acc2
    return out*(t/d)**1.5
r=riser(5.5); add(r,26.0,0.9)
def impact(g=1.0):
    t=t_(2.5); s=np.sin(2*np.pi*(38+60*np.exp(-t*6))*t)*np.exp(-t*1.6)
    n=rng.standard_normal(len(t)); n=lp(n,0.08)*np.exp(-t*2.5)*1.5
    return np.tanh((s+n)*1.5)*g
add(impact(1.0),32.0,0.9)
add(impact(0.6),1.5,0.55)   # ball lands
add(impact(0.8),54.0,0.85)  # logo lock
add(impact(0.5),16.0,0.6)   # hero turn
def whoosh(d=0.6):
    t=t_(d); n=rng.standard_normal(len(t)); y=lp(n,0.12)-lp(n,0.02)
    e=np.sin(np.pi*t/d)**2
    return y*e*1.6
for tw in (7.75,15.75,23.75,39.75,47.75,51.75):
    add(whoosh(),tw-0.1,0.5)
def tick(): 
    t=t_(0.06); return np.sin(2*np.pi*2400*t)*np.exp(-t*90)*0.5
for tt in (10.0,13.6,15.0):
    add(tick(),tt,0.7); add(tick(),tt+0.06,0.5)
def chime(f0=1046.5):
    t=t_(1.6); s=sum(np.sin(2*np.pi*f0*m*t)*np.exp(-t*(3+m)) / m for m in (1,2.01,3.02,4.2))
    return s*0.35
add(chime(1046.5),33.0,0.5); add(chime(1318.5),33.12,0.4); add(chime(1568),57.0,0.45)
mix=np.stack([L,R],1)
# master: fade out last 1.5s, soft clip, normalise
fade=np.ones(N); fi=int(1.6*SR); fade[-fi:]=np.linspace(1,0,fi)**1.5
mix*=fade[:,None]
mix=np.tanh(mix*1.2); mix/=np.max(np.abs(mix))*1.12
w=wave.open('/home/user/kickoff/proj/assets/music.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((mix*32767).astype('<i2').tobytes()); w.close(); print('done')
